# Codexブリーフ：AIスタートクラブ デザインレビュー（2人目）

## 役割
このブリーフを受け取ったCodexは「レビュアー」として動く。
コーディングは行わない。既存のHTMLとCSSを読んで評価・改善提案のみを行う。

## 事前に読むファイル
1. `AGENTS.md` — レビュー形式・4原則の定義を把握せよ
2. `clients/ai-start-club/index.html` — レビュー対象HTML
3. `clients/ai-start-club/style.css` — レビュー対象CSS
4. `clients/ai-start-club/copy.md` — 文章の正としてコピーと照合せよ

## 作業内容

### 1. レスポンシブ確認
style.cssのメディアクエリを読み、以下を確認せよ：
- 375px・768px・1280pxそれぞれで問題になりそうな箇所
- グリッド列数の切り替えが適切か
- フォントサイズ・余白がSPで窮屈になっていないか
- ボタン幅がSPで十分タップできるサイズか（最低44px高さ）
- 問題があればstyle.cssを直接修正してよい

### 2. デザイン4原則の確認
HTMLとCSSを読んで、AGENTS.mdのデザイン4原則レビュー項目を埋めよ。
問題があれば具体的なセレクタ名・改善案まで記載し、必要であればstyle.cssを修正せよ。

### 3. 文章確認
copy.mdと照合し、テキストの抜け・変更がないか確認せよ。

## 出力先
`clients/ai-start-club/review_2nd.md` に出力する（既存のreview.mdは上書きしない）

## 完了報告
```
DONE: created=N updated=N skipped=N
files:
- clients/ai-start-club/review_2nd.md
notes:
- （総合評価の一言サマリー）
```
