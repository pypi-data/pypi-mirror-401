# This is a PyPi package

## Publishing

1. Bump the version in `pyproject.toml`
2. Run the publish command:

```bash
uv lock -U && uv export --frozen --no-editable --no-dev -o requirements.txt > /tmp/uv.txt && \
      rm -rf dist/* && uv build && uv publish --token $PYPI_TOKEN
```
