# Generate Homebrew Formula for gmfind

Generate the `gmfind.rb` Homebrew formula using `poet` (homebrew-pypi-poet) to resolve dependencies correctly.

## Prerequisites

Install poet via uv:

```bash
uv pip install homebrew-pypi-poet
```

## Generate Formula

Run poet to generate the base formula with resolved dependencies:

```bash
uv run poet --formula gmfind
```

This outputs a complete formula with all resource stanzas. However, playwright only provides wheels (no sdist), so the playwright resource will be empty and needs manual fixing.

## Manual Fixes Required

After generating, update the formula with:

1. **desc** - Set proper description
2. **homepage** - Set to `https://github.com/automoto/gmfind`
3. **license** - Add `license "MIT"`
4. **depends_on** - Change `python3` to `python@3.12`
5. **playwright resource** - Replace empty url/sha256 with macOS universal wheel:
   ```ruby
   resource "playwright" do
     url "https://files.pythonhosted.org/packages/<path>/playwright-X.X.X-py3-none-macosx_11_0_universal2.whl"
     sha256 "<sha256>"
   end
   ```
   Get the latest wheel URL from: https://pypi.org/pypi/playwright/json

6. **install** - Simplify to just `virtualenv_install_with_resources`
7. **post_install** - Add to run browser setup:
   ```ruby
   def post_install
     system bin/"gmfind-setup"
   end
   ```
8. **caveats** - Add user instructions:
   ```ruby
   def caveats
     <<~EOS
       Playwright browsers have been installed automatically via gmfind-setup.
       To manually reinstall browsers, run:
         gmfind-setup
     EOS
   end
   ```
9. **test** - Update to:
   ```ruby
   test do
     system bin/"gmfind", "--help"
   end
   ```

## Get Playwright Wheel URL

```bash
curl -s "https://pypi.org/pypi/playwright/json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for url_info in data['urls']:
    if 'macosx_11_0_universal2' in url_info['filename']:
        print(f\"url: {url_info['url']}\")
        print(f\"sha256: {url_info['digests']['sha256']}\")
        break
"
```

## Output Location

Copy the final formula to your homebrew tap:

```bash
cp gmfind.rb ~/code/homebrew-gmfind/Formula/gmfind.rb
```
