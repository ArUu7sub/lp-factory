# LP Factory

Googleフォーム回答から、固定6セクションの24H AI LPを調査・設計・画像生成・実装・独立レビューまで進めるCodex CLI制作基盤です。

## Location

Linux側の正本は `/home/aru/projects/lp-factory` です。Windowsからも確認できるよう、`vault` と同じ階層に次のリンクを置きます。

```text
/mnt/d/workspace/
├── vault/
└── lp-factory -> /home/aru/projects/lp-factory
```

## Automated entrypoint

```bash
/mnt/d/workspace/lp-factory/ops/run-form-job.sh \
  /path/to/checked-out-publication-repo \
  /path/to/checked-out-publication-repo/automation/jobs/current.json
```

The script runs the project-scoped Codex agents, enables live web search, reuses the runner user's ChatGPT login, and validates the complete evidence set. It does not use `OPENAI_API_KEY`.

See [ORCHESTRATION.md](ORCHESTRATION.md) for stages, owners, review loops, and delivery boundaries.

