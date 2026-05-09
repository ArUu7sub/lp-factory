# Codexブリーフ：デザイン・コーディング

## 案件名
[案件名をここに記入]

## 保存先（最優先で確認）
**すべてのファイルは以下のパスに保存する。他の場所には保存しない。**
```
~/work/lp-factory/projects/[案件名]/
```

## 事前に読むファイル
1. `ORCHESTRATION.md` — 統括定義（役割・保存先ルールを確認）
2. `AGENTS.md` — コーディングルールと出力形式を把握せよ
3. `projects/[案件名]/brief.md` — 案件情報・デザイン方針
4. `projects/[案件名]/copy.md` — 使用するコピー文（そのまま使うこと）
5. `projects/[案件名]/structure.md` — LP構成

## 作業内容

### 1. HTML/CSSのコーディング
- `projects/[案件名]/index.html` を作成せよ
- `projects/[案件名]/style.css` を作成せよ
- `projects/[案件名]/script.js` を作成せよ（必要な場合のみ）
- copy.mdのテキストをそのまま使うこと（変更禁止）
- structure.mdのセクション順に実装すること

### 2. デザイン実装の条件
- brief.mdに指定カラーがある場合はそれに従う
- ない場合はトーンに合わせてカラーを選定し、notes:に理由を書く
- フォントはGoogle Fonts（日本語：Noto Sans JP）を使う
- ファーストビューは height: 100vh で実装する
- ボタンにはホバーアニメーションを入れる
- レスポンシブ対応（375px / 768px / 1280px）

### 3. 画像プレースホルダー
- 画像が入る箇所は `<img src="images/placeholder.jpg" alt="説明">` で仮置きする
- `projects/[案件名]/images/` フォルダを作成し、placeholder用のSVGダミーを生成してもよい

## レビューの実施
コーディング完了後、`projects/[案件名]/review.md` にAGENTS.mdのレビュー形式で出力せよ。
画像・イラスト提案の表（透過判断含む）も必ず含めること。

## 出力先（再確認）
```
projects/[案件名]/     ← ここ以外に保存しない
├── index.html
├── style.css
├── script.js（必要な場合）
├── images/
└── review.md
```

## やってはいけないこと
- copy.mdのテキストを勝手に変更しない
- WordPressへの変換を行わない（このブリーフでは不要）
- jQueryを使わない
- インラインstyleを多用しない
- `projects/[案件名]/` 以外の場所にファイルを保存しない

## 完了報告
最終行に以下を出力せよ：
```
DONE: created=N updated=N skipped=N
files:
- projects/[案件名]/index.html
- projects/[案件名]/style.css
- projects/[案件名]/review.md
notes:
- （カラー選定理由・判断メモ）
```
