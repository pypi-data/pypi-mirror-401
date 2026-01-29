### Batch Inference Client

This is a client for the Jane Street dormant models batch inference/activations API. 

The main client is defined in `src/jsinfer/client.py`. It currently supports the following:

- Requesting access to the API
- Creating batch file line items
- Uploading a file to the API
- Submitting a batch of inference/activations requests
- Fetching the results of a batch of inference/activations requests
- Cancelling a batch of inference/activations requests

### Usage

Example usage is provided in `examples/basic.py`.

### PyPi Package

To build and publish the client as a PyPi package, run the following commands:

```bash
uv build
uv publish --token <pypi_token>
```
