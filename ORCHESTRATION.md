# ORCHESTRATION.md — エージェント統括定義

このファイルは Claude Code と Codex が共通で読む統括ドキュメント。
作業開始前に必ず読み込み、自分の役割と制約を把握してから動くこと。

---

## システム全体像

```
ユーザー
  ↕ 相談・方針決定・最終確認
Claude Code（指揮者・ライター）
  ↕ ブリーフ（作業指示書）を生成して渡す
ユーザー
  ↕ ブリーフをコピーして渡す
Codex（作業員・デザイナー）
  ↕ 成果物を projects/案件名/ に保存
ユーザー
  ↕ 「完了した」と Claude Code に報告
Claude Code（検査役）
  ↕ レビューブリーフを生成して渡す
Codex（レビュアー）
```

---

## エージェント別の役割

### Claude Code
**役割：指揮者・ライター・検査役**

やること：
- ユーザーへのヒアリング・情報整理
- LP/HP構成の設計（structure.md）
- コピー文の作成（copy.md）
- Codex用ブリーフの生成（projects/案件名/ops/codex/briefs/）
- Codex完了後のレビュー（ファイルを読んで確認）
- WordPress変換が必要な場合の変換ブリーフ生成

やらないこと：
- Codexを自動起動しない（ブリーフを渡すだけ）
- ヒアリング前にコピーを書かない
- WordPressへの変換をデフォルトで行わない

参照ファイル：
- CLAUDE.md（運用ルール詳細）
- self/identity.md, methodology.md, goals.md
- knowledge/index.md → 各ナレッジノード

---

### Codex
**役割：作業員・デザイナー・レビュアー**

やること：
- ブリーフを読んでHTML/CSS/JSを生成
- デザイン実装（カラー・レイアウト・レスポンシブ）
- 成果物をすべて `projects/案件名/` 配下に保存
- レビュー（デザイン4原則・レスポンシブ・画像提案）
- 指示があればWordPress用PHPへの変換

やらないこと：
- ブリーフに書かれていない機能を追加しない
- copy.mdのテキストを勝手に変更しない
- WordPress変換をデフォルトで行わない
- 保存先を projects/案件名/ 以外にしない

参照ファイル：
- AGENTS.md（コーディングルール・レビュー形式）
- projects/案件名/brief.md（案件情報）
- projects/案件名/copy.md（コピー文）
- projects/案件名/structure.md（構成）

---

## ファイルの保存ルール

### Codexが出力するすべてのファイルの保存先
```
projects/案件名/          ← ここ以外に保存しない
├── index.html
├── style.css
├── script.js
├── review.md             ← 1人目レビュー
├── review_2nd.md         ← 2人目レビュー
└── images/
```

### Claude Codeが生成するファイルの保存先
```
projects/案件名/          ← 案件ドキュメント
├── brief.md
├── structure.md
└── copy.md

projects/案件名/ops/codex/briefs/  ← Codex用ブリーフ
├── 案件名_design.md
└── 案件名_review.md
```

---

## 完了報告の形式（Codex）
作業の最終行に必ず出力する：
```
DONE: created=N updated=N skipped=N
files:
- projects/案件名/index.html
- projects/案件名/style.css
notes:
- （判断メモ）
```

---

## 案件フォルダの作り方
新規案件は `ops/project-template/` をコピーして `projects/案件名/` を作成する。
