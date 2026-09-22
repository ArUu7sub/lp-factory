# LP Factory

Googleフォーム回答から、固定6セクションの24H AI LPを調査・設計・画像生成・実装・独立レビューまで進めるCodex CLI制作基盤です。

## Location

正本はWSLのLinuxファイルシステム上にある次のディレクトリです。

```text
/home/aru/projects/lp-factory
```

## Automated entrypoint

```bash
/home/aru/projects/lp-factory/ops/run-form-job.sh \
  /path/to/checked-out-publication-repo \
  /path/to/checked-out-publication-repo/automation/jobs/current.json
```

The script runs the project-scoped Codex agents, enables live web search, reuses the runner user's ChatGPT login, and validates the complete evidence set. It does not use `OPENAI_API_KEY`.

On its first run for each self-hosted runner user, the entrypoint installs pinned Node.js, Playwright, Chromium, and the official Noto Sans JP variable font under `~/.cache/lp-factory-browser`. Each download is checksum verified. It verifies Chromium and Japanese glyph loading before starting production. Codex creates deterministic HTML/CSS design and implementation source without launching a browser inside its sandbox; the trusted runner bundles the licensed Japanese font into the generated LP, captures five PNG files, and a second Codex pass performs rendered creative, implementation, and delivery reviews.

See [ORCHESTRATION.md](ORCHESTRATION.md) for stages, owners, review loops, and delivery boundaries.
