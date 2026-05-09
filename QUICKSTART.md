# ターミナル2画面 操作ガイド

## 画面の配置

```
┌─────────────────────────┬─────────────────────────┐
│   左：Claude Code       │   右：Codex             │
│   (指揮者・ライター)    │   (作業員・デザイナー)  │
├─────────────────────────┼─────────────────────────┤
│ 相談・構成・コピー作成  │ コーディング・レビュー  │
│ ブリーフ生成            │ ブリーフを受け取って実行│
└─────────────────────────┴─────────────────────────┘
```

---

## 初回のみ：GitHubリポジトリを作成してPages設定

```bash
cd ~/work/lp-factory

git init
git add .
git commit -m "initial commit"
gh repo create lp-factory --public --push --source=.
```

GitHubのリポジトリページで：
**Settings → Pages → Source：「GitHub Actions」を選択 → Save**

以降は新規案件を追加するたびに deploy.sh を叩くだけで自動公開される。

---

## 起動コマンド

### 左ターミナル（Claude Code）
```bash
cd ~/work/lp-factory
claude
```

### 右ターミナル（Codex）
```bash
cd ~/work/lp-factory
# 各STEPのコマンドをここで実行する
```

---

## STEP別 操作手順

### STEP 1：新規案件を始める
```
左（Claude Code）に入力：
  /lp

  → ヒアリングが始まる。質問に答えていく。
  → 完了すると以下が生成される：
     projects/案件名/brief.md
     projects/案件名/structure.md
     projects/案件名/copy.md
     projects/案件名/ops/codex/briefs/案件名_design.md
  → 右ターミナルへの実行コマンドが表示される
```

---

### STEP 2：Codexにコーディングさせる
```
右（Codex）に入力（左に表示されたコマンドをそのまま実行）：
  codex "$(cat projects/案件名/ops/codex/briefs/案件名_design.md)"

  → DONE: ... が表示されたら完了
  → 生成される：
     projects/案件名/index.html
     projects/案件名/style.css
     projects/案件名/script.js
     projects/案件名/review.md
```

---

### STEP 3：Claude Code にレビューブリーフを作らせる
```
左（Claude Code）に入力：
  Codexのコーディングが完了しました。レビューブリーフを作成してください。

  → 生成される：
     projects/案件名/ops/codex/briefs/案件名_review.md
  → 右ターミナルへの実行コマンドが表示される
```

---

### STEP 4：Codexにレビューさせる
```
右（Codex）に入力：
  codex "$(cat projects/案件名/ops/codex/briefs/案件名_review.md)"

  → 生成される：projects/案件名/review_2nd.md
  → デザイン4原則・レスポンシブ・画像提案が出力される
```

---

### STEP 5：GitHub Pagesに自動デプロイ
```
左または右どちらでも：
  cd ~/work/lp-factory
  ./ops/deploy.sh "案件名: 更新内容"

  例：./ops/deploy.sh "ai-start-club: コーディング完了"

  → projects/ の変更を git add → commit → push
  → GitHub Actions が自動で Pages にデプロイ（約1分）
  → チームに共有するURLが表示される：
     https://ユーザー名.github.io/lp-factory/案件名/
```

---

### STEP 6：（必要時）WordPressに変換する
```
左（Claude Code）に入力：
  WordPressに変換するブリーフを作成してください

右（Codex）に入力：
  codex "$(cat projects/案件名/ops/codex/briefs/案件名_wp.md)"

  → projects/案件名/wp-template.php が生成される
```

---

## よく使うコマンド早見表

| やること | どっち | 入力 |
|---------|--------|------|
| 新規案件開始 | 左 | `/lp` |
| コーディング実行 | 右 | `codex "$(cat projects/案件名/ops/codex/briefs/案件名_design.md)"` |
| レビュー実行 | 右 | `codex "$(cat projects/案件名/ops/codex/briefs/案件名_review.md)"` |
| ブラウザ確認 | どちらでも | `open projects/案件名/index.html` |
| GitHub Pagesに公開 | どちらでも | `./ops/deploy.sh "更新メモ"` |

---

## Pages URL の構造
```
https://ユーザー名.github.io/lp-factory/
                                  ├── ai-start-club/   ← 案件1
                                  ├── beauty-salon/    ← 案件2
                                  └── event-lp/        ← 案件3
```
新規案件を追加して deploy.sh を叩くだけで自動追加される。
