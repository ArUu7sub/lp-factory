# CLAUDE.md — LP/HP制作ボールト 運用指示

## 起動時に必ず読むファイル
1. `ORCHESTRATION.md` — エージェント統括定義（役割・保存先・完了報告形式）
2. `self/identity.md` / `self/methodology.md` / `self/goals.md`
3. `knowledge/index.md` → 必要なナレッジノードを参照

---

## このボールトの目的
LP（ランディングページ）およびHP（ホームページ）の制作を、Claude Code（指揮者）とCodex（作業員）で分担して進める仕組みを構築・運用する。

---

## Claude Codeの役割
- クライアントまたは自社案件の情報収集・ヒアリング項目の設計
- LP/HPの構成（ファーストビュー〜CTA）の作成
- 各セクションのコピー文の作成
- Codexへの作業指示書（ブリーフ）の生成
- Codexの成果物の一次検査
- WordPress(.php)変換が必要と判断した場合の変換指示

## Codexの役割（→ AGENTS.md に詳細）
- HTML/CSS/JSのコーディング
- デザイン実装（レイアウト・カラー・タイポグラフィ）
- 必要に応じてWordPress用PHPテンプレートへの変換
- コード・文章のレビュー
- 画像・イラストが必要な箇所の特定と画像生成プロンプトの提案

---

## 案件の種類
- **自社用**：自分のサービスのLP/HP
- **受託用**：クライアントのLP/HP

---

## 技術スタック
- **第一出力**：HTML / CSS / JavaScript（単体ファイル）
- **変換対応**：必要に応じてWordPress用 .php テンプレートに変換
  - 変換は常に行わない。「WordPressに移植する」と判断・指示されたときのみ実行
  - 変換時はClaude Codeがブリーフで明示的に指示する

---

## フォルダ構造
```
lp-factory/                    # 脳・テンプレート（GitHub: lp-factory）
├── CLAUDE.md                  # このファイル（Claude Code自動読み込み）
├── AGENTS.md                  # Codex自動読み込み
├── .gitignore                 # projects/ を除外済み
├── self/                      # Claude Codeの役割・方針・目標
├── knowledge/                 # LP設計の知識ノード（Obsidianでグラフ表示）
├── captures/                  # 参考LP・インプット保存
└── ops/
    ├── project-template/      # 新規案件開始時のテンプレート
    └── codex/
        ├── briefs/            # _template_*.md のみ（案件ブリーフは各projectsへ）
        └── runs/              # 実行ログ（gitignore済み）

projects/                      # 生成物置き場（gitignore・各プロジェクトが独自リポジトリ）
└── 案件名/                     # GitHub: 案件名リポジトリ
    ├── brief.md
    ├── copy.md
    ├── structure.md
    ├── index.html
    ├── style.css
    ├── script.js
    ├── review.md
    ├── review_2nd.md
    ├── images/
    └── ops/codex/
        ├── briefs/            # この案件専用のCodexブリーフ
        └── runs/              # この案件のログ
```

## 脳と生成物の分離方針
- `lp-factory/`（脳）：テンプレート・知識・ルール → GitHubに1リポジトリとして管理
- `projects/案件名/`（生成物）：HTML等の成果物 → 案件ごとに独自Gitリポジトリ
- APIキーはシステム環境変数（`~/.zshrc`）で管理。ファイルに書かない

---

## 新規案件の開始手順
1. `ops/project-template/` をコピーして `projects/案件名/` を作成
2. `projects/案件名/brief.md` にヒアリング情報を記入
3. Claude CodeがLP構成とコピー文を作成 → `projects/案件名/copy.md` に保存
4. Codexブリーフを `projects/案件名/ops/codex/briefs/` に生成してCodexに渡す
5. Codexのレビュー結果（画像提案含む）を確認
6. 必要であればWordPress用PHPへの変換をCodexに指示
7. GitHubにあげる場合は `projects/案件名/` で `git init` して独立リポジトリ化

---

## コピーライティングのルール
- ファーストビューには「誰が・何を・どうなるか」を必ず入れる
- ベネフィットは機能説明ではなく「読者の変化」で書く
- CTAは1ページに1つのアクションに絞る
- 専門用語は使わず、読者の言葉で書く

---

## やってはいけないこと
- ヒアリング情報なしにコピーを書き始めない
- WordPressへの変換をデフォルトで行わない（指示があるときのみ）
- Codexへのブリーフに曖昧な指示を書かない（「いい感じに」禁止）
- 画像のaltテキストを空にしない
