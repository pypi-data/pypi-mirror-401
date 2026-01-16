# Publishing `agentic-student-assistant` to PyPI

This guide validates how to publish your package to PyPI using `uv`.

## Prerequisites

1.  **PyPI Account**: Create an account at [pypi.org](https://pypi.org/).
2.  **API Token**:
    *   Go to **Account Settings** -> **API Tokens** on PyPI.
    *   Create a new token (scope it to "Entire account" for the first upload, or specific project if it exists).
    *   **Copy the token** (it starts with `pypi-`).

## Publishing Steps

### 1. Build the Package

Run the following command to build the source distribution (`.tar.gz`) and wheel (`.whl`):

```bash
uv build
```

This will create a `dist/` directory containing your package artifacts.

### 2. Publish to PyPI

Run the publish command. You will be prompted for your token.

```bash
uv publish
```

*Note: `uv` looks for the token in the `UV_PUBLISH_TOKEN` environment variable or prompts you.*

To avoid pasting the token every time, you can set it in your terminal session or `.env` (be careful not to commit it!):

**PowerShell:**
```powershell
$env:UV_PUBLISH_TOKEN = "pypi-AgEI..."
uv publish
```

### 3. Verify

Visit [https://pypi.org/project/agentic-student-assistant/](https://pypi.org/project/agentic-student-assistant/ (once uploaded) to see your package.

## Troubleshooting

- **Name Conflicts**: If `agentic-student-assistant` is already taken on PyPI, you will get an error. You must change the `name` in `pyproject.toml` to something unique (e.g., `hsrak-agentic-assistant`).
- **Version Conflicts**: You cannot overwrite an existing version. Increment `version = "0.1.0"` in `pyproject.toml` for every new release.
