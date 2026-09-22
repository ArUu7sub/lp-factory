#!/usr/bin/env bash
set -euo pipefail

node_version="v24.21.0"
playwright_version="1.63.0"
runtime_root="${LP_BROWSER_RUNTIME_ROOT:-${HOME}/.cache/lp-factory-browser}"
node_root="$runtime_root/node-$node_version-linux-x64"
package_root="$runtime_root/package"
browsers_root="$runtime_root/browsers"
fonts_root="$runtime_root/fonts"
node_bin="$node_root/bin/node"
npm_bin="$node_root/bin/npm"
font_file="$fonts_root/NotoSansJP-Variable.ttf"
font_license="$fonts_root/OFL.txt"
font_sha256="c2f3b4d463500a2ddcd3849cded1fceeb9fd6d1c32e6cbecd568453ba50fc68f"
font_license_sha256="1c05c68c34f9708415aada51f17e1b0092d2cea709bf4a94cd38114f9e73d7d9"

mkdir -p "$runtime_root" "$package_root" "$browsers_root" "$fonts_root"

retry() {
  local attempt=1
  local max_attempts=4
  until "$@"; do
    if (( attempt >= max_attempts )); then
      return 1
    fi
    sleep $((attempt * 3))
    attempt=$((attempt + 1))
  done
}

if [[ ! -x "$node_bin" ]]; then
  archive="$runtime_root/node-$node_version-linux-x64.tar.xz"
  retry curl -fL --retry 3 --retry-all-errors \
    "https://nodejs.org/dist/$node_version/node-$node_version-linux-x64.tar.xz" \
    -o "$archive"
  tar -xJf "$archive" -C "$runtime_root"
  rm -f "$archive"
fi

download_verified() {
  local url="$1"
  local destination="$2"
  local expected_sha256="$3"
  local temporary="$destination.tmp"

  if [[ -f "$destination" ]] && [[ "$(sha256sum "$destination" | cut -d' ' -f1)" == "$expected_sha256" ]]; then
    return 0
  fi

  rm -f "$temporary"
  retry curl -fL --retry 3 --retry-all-errors "$url" -o "$temporary"
  echo "$expected_sha256  $temporary" | sha256sum --check --status
  mv "$temporary" "$destination"
}

download_verified \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf" \
  "$font_file" \
  "$font_sha256"
download_verified \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/OFL.txt" \
  "$font_license" \
  "$font_license_sha256"

export PATH="$node_root/bin:$PATH"
export PLAYWRIGHT_BROWSERS_PATH="$browsers_root"
export LP_JAPANESE_FONT_PATH="$font_file"
export LP_JAPANESE_FONT_LICENSE_PATH="$font_license"

installed_version=""
if [[ -f "$package_root/node_modules/playwright/package.json" ]]; then
  installed_version="$($node_bin -p "require('$package_root/node_modules/playwright/package.json').version")"
fi

if [[ "$installed_version" != "$playwright_version" ]]; then
  printf '{"private":true}\n' > "$package_root/package.json"
  retry "$npm_bin" install \
    --prefix "$package_root" \
    --no-audit \
    --no-fund \
    --save-exact \
    "playwright@$playwright_version"
fi

export NODE_PATH="$package_root/node_modules"

if ! "$node_bin" - <<'NODE'
const {chromium} = require('playwright');
const fs = require('node:fs');
process.exit(fs.existsSync(chromium.executablePath()) ? 0 : 1);
NODE
then
  retry "$package_root/node_modules/.bin/playwright" install chromium
fi

"$node_bin" - <<'NODE'
const {chromium} = require('playwright');
const fs = require('node:fs');
const executable = chromium.executablePath();
if (!fs.existsSync(executable)) {
  throw new Error(`Chromium executable is missing: ${executable}`);
}
console.log(JSON.stringify({
  node: process.version,
  playwright: require('playwright/package.json').version,
  chromium: executable,
  japaneseFont: process.env.LP_JAPANESE_FONT_PATH || null,
}));
NODE
