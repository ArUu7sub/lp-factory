#!/usr/bin/env bash
set -euo pipefail

node_version="v24.21.0"
playwright_version="1.63.0"
runtime_root="${LP_BROWSER_RUNTIME_ROOT:-${HOME}/.cache/lp-factory-browser}"
node_root="$runtime_root/node-$node_version-linux-x64"
package_root="$runtime_root/package"
browsers_root="$runtime_root/browsers"
node_bin="$node_root/bin/node"
npm_bin="$node_root/bin/npm"

mkdir -p "$runtime_root" "$package_root" "$browsers_root"

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

export PATH="$node_root/bin:$PATH"
export PLAYWRIGHT_BROWSERS_PATH="$browsers_root"

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
}));
NODE
