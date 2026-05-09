# Codexブリーフ：AIスタートクラブ LP コーディング

## 事前に読むファイル
1. `AGENTS.md` — ルールと出力形式を把握せよ
2. `clients/ai-start-club/brief.md` — デザイン方針・カラー
3. `clients/ai-start-club/copy.md` — コピー文（そのまま使うこと・変更禁止）
4. `clients/ai-start-club/structure.md` — セクション構成

## カラー指定
- メイン：#F59E0B（アンバーオレンジ）
- サブ背景：#FFFBF0（クリーム）
- アクセント：#166534（深緑）
- テキスト：#1C1C1C（ダークブラウン寄り）
- ボタンホバー：#D97706
- 白：#FFFFFF

## フォント
- Google Fonts：Noto Sans JP（400, 700）
- 見出しfont-weight: 700、本文: 400

## 作業内容

### 1. HTML/CSS/JSを作成せよ
出力先：
- `clients/ai-start-club/index.html`
- `clients/ai-start-club/style.css`
- `clients/ai-start-club/script.js`

### 2. セクション構成（structure.mdの順番通りに実装）
1. ヘッダー（ロゴ + ナビ + CTAボタン）
2. ファーストビュー（height: 100vh、グラデーション背景）
3. 問題提起（悩みカード3〜4枚）
4. できること・ベネフィット（4カラムグリッド）
5. 学べる内容（カード形式、アイコン付き）
6. 地方×AIビジョン（背景色を変えて強調）
7. 会員の声（3枚カード）
8. 料金・申込（価格プレースホルダー、CTAボタン）
9. FAQ（アコーディオン形式）
10. 最終CTA
11. フッター

### 3. デザイン実装の条件
- ファーストビュー：#F59E0B → #FFFBF0 のグラデーション背景
- セクションごとに背景色を交互に変える（#FFFFFF / #FFFBF0）
- 悩みカード：左に❌アイコン、転換後は✅アイコン
- ベネフィットカード：上部にアイコン（emoji可）、タイトル、説明文
- 学べる内容：グリッドカード形式（PC: 3列、SP: 1列）
- 会員の声：引用符スタイルのカード
- FAQアコーディオン：クリックで開閉（JavaScriptで実装）
- CTAボタン：背景#F59E0B、ホバー時#D97706、角丸16px、paddingたっぷり
- セクション間padding: 80px上下
- モバイルファースト・レスポンシブ（375px / 768px / 1280px）

### 4. 画像プレースホルダー
- FVの背景：グラデーションのみでOK（画像不要）
- ロゴ：`<div class="logo">AIスタートクラブ</div>` でテキストロゴ
- 会員の声のアバター：SVGの丸いプレースホルダーを生成して `images/avatar1.svg` 等に保存

### 5. レビューの実施
コーディング完了後、`clients/ai-start-club/review.md` にAGENTS.mdのレビュー形式で出力せよ。
画像・イラスト提案の表を必ず含めること。

## やってはいけないこと
- copy.mdのテキストを勝手に変更しない
- 料金の数字を勝手に入れない（¥〇〇〇〇のままにする）
- ダーク系・冷たいデザインにしない
- WordPressへの変換は行わない
- jQueryを使わない

## 完了報告
最終行に以下を出力せよ：
```
DONE: created=N updated=N skipped=N
files:
- clients/ai-start-club/index.html
- clients/ai-start-club/style.css
- clients/ai-start-club/script.js
- clients/ai-start-club/review.md
notes:
- （判断メモ）
```
