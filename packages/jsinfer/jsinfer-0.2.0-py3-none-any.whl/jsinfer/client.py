from typing import Optional
from dataclasses import dataclass, asdict
import os
import json
import aiohttp
import asyncio
import time
import aiofiles
import zipfile
import numpy as np
import tempfile
from collections import defaultdict


@dataclass
class Message:
    """Represents a message in a conversation."""

    role: str
    content: str


@dataclass
class ActivationsRequest:
    """Request for activations from specific model layers."""

    custom_id: str
    messages: list[Message]
    module_names: list[str]


@dataclass
class ChatCompletionRequest:
    """Request for chat completion."""

    custom_id: str
    messages: list[Message]


@dataclass
class ActivationsResponse:
    """Response containing activations arrays for a single request."""

    custom_id: str
    activations: dict[str, np.ndarray]  # module_name -> array


@dataclass
class ChatCompletionResponse:
    """Response containing chat completion messages."""

    custom_id: str
    messages: list[Message]


class BatchInferenceClient:
    """Async client for submitting batch jobs and fetching results from Andromeda."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client with an optional API key."""
        self.api_key = api_key
        self.url = "https://dormant-puzzle.janestreet.com"
        self._models = {
            "dormant-model-1": "Model-Organisms-1/model-a",
            "dormant-model-2": "Model-Organisms-1/model-b",
            "dormant-model-3": "Model-Organisms-1/model-h",
        }
        self.supported_endpoints = {"/v1/activations", "/v1/chat/completions"}

    def set_api_key(self, api_key: str):
        """Update the API key after initialization."""
        self.api_key = api_key

    async def request_access(self, email: str, andromeda_api_key: str):
        """Request access for a user via Andromeda's partner API."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/api/partners/jane-street/users",
                headers={"Authorization": f"Bearer {andromeda_api_key}"},
                json={"email": email},
            ) as response:
                response.raise_for_status()
                return await response.json()

    @property
    def models(self):
        """Expose available model IDs mapped to full Hugging Face model paths."""
        return self._models

    def line_entry_activations(
        self, custom_id: str, messages: list[dict], module_names: list[str]
    ):
        """Create a batch line entry for activations.

        Args:
            custom_id: Identifier that will be echoed back in the results.
            messages: Message payload to send to the model.
            module_names: Activation module names to request.

        Returns:
            A dictionary formatted for the batch input NDJSON file.
        """
        if len(messages) == 0:
            raise ValueError("Messages list cannot be empty")
        if len(module_names) == 0:
            raise ValueError("Module names list cannot be empty")
        payload = {
            "custom_id": custom_id,
            "method": "POST",
            "endpoint": "/v1/activations",
            "body": {
                "input": messages,
                "module_names": module_names,
            },
        }

        return payload

    def line_entry_chat_completions(self, custom_id: str, messages: list[dict]):
        """Create a batch line entry for chat completions.

        Args:
            custom_id: Identifier that will be echoed back in the results.
            messages: Chat history to send to the model.

        Returns:
            A dictionary formatted for the batch input NDJSON file.
        """
        if len(messages) == 0:
            raise ValueError("Messages list cannot be empty")
        payload = {
            "custom_id": custom_id,
            "method": "POST",
            "endpoint": "/v1/chat/completions",
            "body": {
                "messages": messages,
            },
        }

        return payload

    async def upload_file(self, file_path: str, expires_after: int = 3600):
        """Upload an NDJSON batch file and return the file ID.

        Args:
            file_path: Path to the NDJSON payload.
            expires_after: Seconds after which the uploaded file expires.

        Returns:
            The file ID returned by the service.
        """
        form = aiohttp.FormData()
        form.add_field(
            "file",
            open(file_path, "rb"),
            filename=os.path.basename(file_path),
            content_type="application/x-ndjson",
        )
        form.add_field("purpose", "batch")
        form.add_field("expires_after[anchor]", "created_at")
        form.add_field("expires_after[seconds]", str(expires_after))

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/api/v1/files",
                data=form,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                },
            ) as response:
                response.raise_for_status()
                try:
                    response_json = await response.json()
                    file_id = response_json["fileId"]
                    return file_id
                except Exception as e:
                    raise Exception(
                        f"No file ID returned. Likely failed to upload file: {response.status} {response.text()}"
                    )

    async def _batch_submit_file(
        self, file_id: str, model: str, endpoint: str, completion_window: str = "24h"
    ):
        """Submit an uploaded file to the batch API for a given endpoint.

        Args:
            file_id: File ID returned by `upload_file`.
            model: Supported model ID (for example, `dormant-model-1`).
            endpoint: Target inference endpoint.
            completion_window: Desired SLA for processing.

        Returns:
            The created batch ID.
        """
        if model not in self.models:
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.models}"
            )
        if endpoint not in self.supported_endpoints:
            raise ValueError(
                f"Endpoint {endpoint} not supported. Supported endpoints: {self.supported_endpoints}"
            )
        payload = {
            "completion_window": completion_window,
            "endpoint": endpoint,
            "model": self._models[model],
            "input_file_id": file_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/api/v1/batches",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            ) as response:
                print(await response.text())
                try:
                    response.raise_for_status()
                    response_json = await response.json()
                    batch_id = response_json["batchId"]
                    return batch_id
                except Exception as e:
                    raise Exception(
                        f"No batch ID returned. Likely failed to submit batch: {response.status} {await response.text()}"
                    )

    async def submit_activations(self, file_id: str, model: str):
        """Submit a batch file to the activations endpoint."""
        return await self._batch_submit_file(file_id, model, "/v1/activations")

    async def submit_chat_completions(self, file_id: str, model: str):
        """Submit a batch file to the chat completions endpoint."""
        return await self._batch_submit_file(file_id, model, "/v1/chat/completions")

    async def get_batch(self, batch_id: str):
        """Retrieve batch metadata by batch ID.

        Args:
            batch_id: Batch identifier returned on submission.

        Returns:
            Parsed JSON payload describing the batch.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.url}/api/v1/batches/{batch_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            ) as response:
                response.raise_for_status()
                try:
                    return await response.json()
                except Exception:
                    raise Exception(
                        f"No batch returned. Likely failed to get batch: {response.status} {response.text()}"
                    )

    async def cancel_batch(self, batch_id: str):
        """Cancel a running batch.

        Args:
            batch_id: Batch identifier returned on submission.

        Returns:
            Parsed JSON payload describing the cancelled batch.
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.url}/api/v1/batches/{batch_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            ) as response:
                response.raise_for_status()
                try:
                    return await response.json()
                except Exception:
                    raise Exception(
                        f"No batch returned. Likely failed to cancel batch: {response.status} {response.text()}"
                    )

    async def poll_batch(self, batch_id: str, timeout: int = 60 * 60 * 24):
        """Poll a batch until completion or timeout, returning the results URL.

        Args:
            batch_id: Batch identifier returned on submission.
            timeout: Maximum number of seconds to wait for completion.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            batch = await self.get_batch(batch_id)
            try:
                if batch["batch"]["status"] == "completed":
                    return batch["resultsUrl"]
                elif batch["batch"]["status"] in {
                    "failed",
                    "cancelled",
                    "expired",
                    "error",
                }:
                    raise Exception(
                        f"Batch {batch_id} failed with status {batch['batch']['status']}. Errors: {batch['batch']['errors']}"
                    )
            except Exception:
                raise Exception(
                    f"No batch returned. Likely failed to get batch: {batch['status']}. Errors: {batch['errors']}"
                )
            await asyncio.sleep(1)
        raise Exception(f"Batch {batch_id} timed out after {timeout} seconds")

    async def _download_results(self, batch_id: str, download_path: str):
        """Download batch results archive to the given path.

        Args:
            batch_id: Batch identifier returned on submission.
            download_path: Directory where the ZIP file should be written.
        """
        if not os.path.exists(download_path):
            raise ValueError(f"Download path {download_path} does not exist")

        results_url = await self.poll_batch(batch_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(results_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get batch results: {response.status}")
                async with aiofiles.open(
                    f"{download_path}/batch_{batch_id}.zip", "wb"
                ) as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        await f.write(chunk)
        print(f"Batch results saved to `{download_path}/batch_{batch_id}.zip`")

    def _unzip_batch_results(self, batch_id: str, download_path: str):
        """Unzip the batch results archive into the download directory.

        Args:
            batch_id: Batch identifier returned on submission.
            download_path: Directory where results were downloaded.
        """
        with zipfile.ZipFile(f"{download_path}/batch_{batch_id}.zip", "r") as zip_ref:
            zip_ref.extractall(f"{download_path}/batch_{batch_id}")
        print(f"Batch results unzipped to `{download_path}/batch_{batch_id}`")

        for file in zip_ref.namelist():
            if file.endswith(".zip"):
                with zipfile.ZipFile(
                    f"{download_path}/batch_{batch_id}/{file}", "r"
                ) as zip_ref:
                    zip_ref.extractall(f"{download_path}/batch_{batch_id}")
        print(f"Batch results unzipped to `{download_path}/batch_{batch_id}`")

    def _aggregate_json_files(self, batch_id: str, download_path: str):
        """Aggregate JSON result files from the batch output directory.

        Args:
            batch_id: Batch identifier returned on submission.
            download_path: Directory containing the unzipped result files.

        Returns:
            Mapping of `custom_id` to the corresponding result payload.
        """
        batch_results_dict = {}
        for file in os.listdir(f"{download_path}/batch_{batch_id}"):
            if file.endswith(".json"):
                with open(f"{download_path}/batch_{batch_id}/{file}", "r") as f:
                    data = json.load(f)
                    file_custom_id = data["custom_id"]
                    batch_results_dict[file_custom_id] = data
        return batch_results_dict

    async def fetch_results(
        self,
        batch_id: str,
        download_path: Optional[str] = None,
        is_activations: bool = True,
    ):
        """Download, unpack, and parse batch results.

        Args:
            batch_id: Batch identifier returned on submission.
            download_path: Directory where results should be stored. If None, uses a temporary directory.
            is_activations: Whether the batch requested activations instead of tokens.

        Returns:
            Aggregated results as tensors (activations) or raw JSON dict.
        """
        if download_path is None:
            download_path = tempfile.mkdtemp()
            print(f"Using temporary directory for results: {download_path}")

        await self._download_results(batch_id, download_path)
        self._unzip_batch_results(batch_id, download_path)
        aggregate_results = self._aggregate_json_files(batch_id, download_path)

        if is_activations:
            # Convert activation lists to numpy arrays for return
            array_dict = {}
            for entry in aggregate_results.keys():
                if "activations" in aggregate_results[entry]:
                    array_dict[entry] = {}
                    for module in aggregate_results[entry]["activations"]:
                        array_dict[entry][module] = np.array(
                            aggregate_results[entry]["activations"][module]
                        )
            return array_dict

        async with aiofiles.open(
            f"{download_path}/batch_{batch_id}/aggregate_results.json", "w"
        ) as f:
            await f.write(json.dumps(aggregate_results))
        print(
            f"Aggregate results saved to `{download_path}/batch_{batch_id}/aggregate_results.json`"
        )
        return aggregate_results

    async def activations(
        self, requests: list[ActivationsRequest], model: str = "dormant-model-3"
    ) -> dict[str, ActivationsResponse]:
        """Submit activation requests and fetch results using a temporary directory.

        Args:
            requests: List of ActivationsRequest objects.
            model: Model ID to use (default: "dormant-model-3").

        Returns:
            Dictionary mapping custom_id to ActivationsResponse objects.
        """
        # Create temporary JSONL file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as tmp_file:
            for request in requests:
                entry = {
                    "custom_id": request.custom_id,
                    "method": "POST",
                    "endpoint": "/v1/activations",
                    "body": {
                        "input": [asdict(msg) for msg in request.messages],
                        "module_names": request.module_names,
                    },
                }
                tmp_file.write(json.dumps(entry) + "\n")
            tmp_path = tmp_file.name

        try:
            # Upload file
            file_id = await self.upload_file(tmp_path)
            print(f"Successfully uploaded file. File ID: {file_id}")

            # Submit batch
            batch_id = await self.submit_activations(file_id, model)
            print(f"Successfully submitted batch. Batch ID: {batch_id}")

            # Fetch results (uses tmpdir automatically)
            raw_results = await self.fetch_results(batch_id, is_activations=True)

            # Convert to response dataclasses
            return {
                custom_id: ActivationsResponse(
                    custom_id=custom_id, activations=activations
                )
                for custom_id, activations in raw_results.items()
            }
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)

    async def chat_completions(
        self, requests: list[ChatCompletionRequest], model: str = "dormant-model-3"
    ) -> dict[str, ChatCompletionResponse]:
        """Submit chat completion requests and fetch results using a temporary directory.

        Args:
            requests: List of ChatCompletionRequest objects.
            model: Model ID to use (default: "dormant-model-3").

        Returns:
            Dictionary mapping custom_id to ChatCompletionResponse objects.
        """
        # Create temporary JSONL file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as tmp_file:
            for request in requests:
                entry = {
                    "custom_id": request.custom_id,
                    "model": self._models[model],
                    "endpoint": "/v1/chat/completions",
                    "method": "POST",
                    "body": {
                        "messages": [asdict(msg) for msg in request.messages],
                    },
                }
                tmp_file.write(json.dumps(entry) + "\n")
            tmp_path = tmp_file.name

        try:
            # Upload file
            file_id = await self.upload_file(tmp_path)
            print(f"Successfully uploaded file. File ID: {file_id}")

            # Submit batch
            batch_id = await self.submit_chat_completions(file_id, model)
            print(f"Successfully submitted batch. Batch ID: {batch_id}")

            # Fetch results (uses tmpdir automatically)
            raw_results = await self.fetch_results(batch_id, is_activations=False)

            # Convert to response dataclasses
            return {
                custom_id: ChatCompletionResponse(
                    custom_id=custom_id,
                    messages=[Message(**msg) for msg in result["messages"]],
                )
                for custom_id, result in raw_results.items()
            }
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
