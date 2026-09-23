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

Every run writes a local, read-only diagnostic bundle to `/tmp/lp-factory-diagnostics/<job-id>/`. It contains the GitHub run ID, exit code, stage state, review JSON, render evidence when available, and Codex final messages. The normalized form payload is intentionally excluded.

## Visual production contract

- Heroは「左にHTMLテキスト＋右全面にimagegen画像」または「中央にHTMLテキスト＋全面背景画像」の2型から選びます。
- Heroの絵はimagegenで生成し、人物・端末・風景などをCSSで描きません。
- 390px表示で安全に切り抜けない場合はスマホ専用Heroを生成します。
- 最終CTAにはHeroと別のimagegen背景を使います。
- その他の4セクションも画像の要否を判断し、理由と使用ファイルを`design/assets-manifest.json`へ記録します。
- 画像内にコピーを入れず、見出し・本文・ボタン・CTAはHTMLテキストとして実装します。

この契約は制作エージェント、独立レビュー、Preview前バリデーションの3箇所で確認されます。

See [ORCHESTRATION.md](ORCHESTRATION.md) for stages, owners, review loops, and delivery boundaries.
