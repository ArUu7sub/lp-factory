# Codexブリーフ：WordPress用PHP変換

## 案件名
[案件名をここに記入]

## 前提
このブリーフは「WordPressへの移植」が明示的に指示された場合のみ使用する。

## 事前に読むファイル
1. `AGENTS.md` — ルールと出力形式を把握せよ
2. `clients/[案件名]/index.html` — 変換元のHTML
3. `clients/[案件名]/brief.md` — WPテーマ名・Elementor使用有無を確認

## 作業内容

### 変換ルール
- `clients/[案件名]/index.html` を WordPress用 `.php` テンプレートに変換する
- 出力先：`clients/[案件名]/wp-template.php`
- WordPress関数を使う：
  - `get_header()` / `get_footer()`
  - `the_title()` / `the_content()`
  - `get_template_directory_uri()` （画像パス用）
  - `wp_nav_menu()` （ナビゲーション用）
- CSSは `clients/[案件名]/style.css` をそのまま使う（変更不要）
- brief.mdに「Elementor使用：はい」の場合はElementorウィジェット構造のコメントを追加する

### 出力先
```
clients/[案件名]/
└── wp-template.php
```

## 完了報告
最終行に以下を出力せよ：
```
DONE: created=N updated=N skipped=N
files:
- clients/[案件名]/wp-template.php
notes:
- （変換時の判断メモ・注意点）
```
