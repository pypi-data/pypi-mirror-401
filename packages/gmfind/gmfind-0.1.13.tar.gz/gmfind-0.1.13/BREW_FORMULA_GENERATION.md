# Generate Homebrew Formula for gmfind

To generate the `gmfind.rb` Homebrew formula using native `brew` commands and `jq`, follow these steps.

## One-Command Generation

You can run this block of commands in your terminal. It automatically fetches the latest source distribution URL from PyPI and uses `brew create` with the `--python` flag to generate the formula file in your current directory.

```bash
# 1. Get the latest source tarball URL from PyPI using jq
PACKAGE_URL=$(curl -s https://pypi.org/pypi/gmfind/json | jq -r '.urls[] | select(.packagetype == "sdist") | .url' | head -n 1)

# 2. Use brew create with the python flag
# We use a custom EDITOR command to intercept the file content and write it to gmfind.rb
# instead of opening an interactive editor.
env EDITOR="sed -n 'w gmfind.rb'" brew create --python "$PACKAGE_URL" --set-name gmfind --force
```

## Verify Output

After running the above, check if the file was created:

```bash
ls -l gmfind.rb
```

## Troubleshooting

If you encounter `Error: No available tap homebrew/core`, run:

```bash
brew tap homebrew/core
```