# 自己レビュー：AIスタートクラブ LP（第2版）

レビュー日：2026-05-09

---

## コードレビュー
- [x] HTMLバリデーション問題なし（lang属性・charset・viewport完備）
- [x] altテキスト全て記述済み（SVGにはaria-hidden="true"で対応）
- [x] レスポンシブ確認（375px / 768px / 1024px / 1280px）
- [x] CTAボタンのリンク先：`#price`（料金セクション）に統一済み
- [x] WAI-ARIA属性: aria-labelledby・aria-label・aria-expanded を適切に付与
- [x] details/summary 要素でFAQを実装（JavaScriptなしでも動作）

---

## レスポンシブレビュー

### 375px（スマートフォン）
- [x] タップ領域44px以上（btn・mobile-link・faq__questionにmin-height: 44px）
- [x] 1カラムレイアウト（全グリッドを1列化）
- [x] ヒーローのビジュアルエリアを非表示にして本文優先
- [x] ハンバーガーメニュー表示・モバイルナビ実装済み
- [x] 余白：padding-inline 24px で確保

### 768px（タブレット）
- [x] 問題提起・ベネフィット・会員の声：2列グリッド
- [x] 学べる内容：2列グリッド
- [x] デスクトップナビを非表示・ハンバーガー対応

### 1280px（デスクトップ）
- [x] 最大幅 1140px で中央揃え
- [x] 問題提起：4列グリッド
- [x] ベネフィット：2列グリッド
- [x] 会員の声・学べる内容：3列グリッド
- [x] ヒーロー：2カラム（コンテンツ+フローティングカード）

---

## 文章レビュー
- [x] FVに「誰が・何を・どうなるか」が入っている
  - 誰が：「あなた」
  - 何を：AIを味方に学ぶ
  - どうなるか：「可能性は広がる」＋山梨発地方から全国へ
- [x] 専門用語なし（「Intersection Observer」などはコメント内のみ）
- [x] CTAが1アクションに絞られている（入会する → #price）
- [x] ベネフィットが機能ではなく「読者の変化」で書かれている
  - 例：「AIが使える」→「転職市場での価値が上がります」

---

## デザイン4原則レビュー

### 近接
**評価**：良好（4/4）
- 見出し↔本文：margin-bottom 16px（設計通り）
- セクション間：padding 80px 0（設計通り）
- カード内アイコン↔テキスト：margin-bottom 14〜16px
- 関連要素のグルーピングが明確（ベネフィット：アイコン→タイトル→説明→タグ）

**改善提案**：特になし

### 整列
**評価**：良好（4/4）
- structure.mdの揃え指定を忠実に実装
- FV・問題提起・ビジョン・FAQ・最終CTA：中央揃え
- ベネフィットカード・コンテンツカード本文：左揃え（読みやすさ優先）
- ヒーローは2カラム時左揃え・モバイル時中央揃えに切り替え
- 1140px コンテナで一貫した水平軸

**改善提案**：特になし

### 反復
**評価**：良好（4/4）
- CSSカスタムプロパティで色・フォント・角丸・影を全セクション統一
- 全カード：border-radius 16px・shadow-card で統一
- ボタン：border-radius 50px・プライマリカラーで統一
- セクション eyebrow：同一フォント（Zen Maru Gothic）・同一スタイル
- ホバー演出：translateY(-4px) + shadow-hover で全カード共通

**改善提案**：特になし

### 対比
**評価**：良好（3.5/4）
- 見出し（Noto Serif JP、clamp 1.6〜2.8rem）vs 本文（Noto Sans JP、0.85〜1rem）
- CTA（#F59E0B、shadow付き）vs 周辺要素（クリーム/白背景）
- ヒーローラベル（深緑）vs ページ基調（アンバー/クリーム）
- ビジョンセクション：深緑背景で白文字→最大のコントラストポイント

**改善提案**：価格数字（¥3,980）のコントラストをさらに強調するため、将来的に価格テキストをプライマリカラーに変えると訴求力が上がる

**総合スコア：3.9/4**

---

## 参考デザインの反映

- **参考にしたLP**：
  - sankoudesign.com — 教育・コミュニティ系事例（暖色＋丸みゴシック＋カードUI）
  - lp-web.com — スクール系事例（オレンジ×白×信頼感）

- **反映した特徴**：
  - **配色**：アンバーオレンジ×クリーム×深緑（温かみ+自然+信頼の3色構成）
  - **フォント**：Noto Serif JP（見出し）+ Zen Maru Gothic（丸みゴシック）+ Noto Sans JP（本文）
  - **FVレイアウト**：山のSVGシルエット背景＋フローティングカードで立体感
  - **セクション構成**：クリーム↔白の交互切り替えで視覚的リズム
  - **UIパターン**：全カードリフトホバー・FAQアコーディオン・スクロールリビール

---

## 画像・イラスト提案

| セクション | 提案内容 | 透過判断 | 画像生成プロンプト（英語） |
|-----------|---------|---------|------------------------|
| FV ビジュアルエリア | スマホ/PCでAIを学ぶ人物イラスト、暖かいトーン | **要（透過）** | `A cheerful young Japanese person studying AI on a laptop in a cozy rural setting, warm amber and cream tones, flat illustration style, transparent background, no text` |
| ビジョンセクション | 山梨の山並みと人々のコミュニティイメージ | **不要** | `Yamanashi mountain landscape with warm sunset, community gathering silhouettes, Japanese countryside feel, watercolor illustration style` |
| 会員アバター（田中さん） | 30代男性会社員のやわらかいアイコン | **要（透過）** | `Simple cute avatar illustration of a 30s Japanese male office worker, warm color palette, round friendly face, flat style, transparent background` |
| 会員アバター（鈴木さん） | 40代女性主婦のやわらかいアイコン | **要（透過）** | `Simple cute avatar illustration of a 40s Japanese housewife, warm color palette, round friendly face, flat style, transparent background` |
| 会員アバター（山田さん） | 20代若者のやわらかいアイコン | **要（透過）** | `Simple cute avatar illustration of a 20s young Japanese person, warm color palette, round friendly face, flat style, transparent background` |
| コンテンツカードアイコン | ChatGPT・画像生成・副業・SNS・効率化・地方の6種 | **要（透過）** | `Flat icon set for AI education topics: chatbot, image generation art, side income coins, social media phone, efficiency clock gear, rural community houses, warm amber color scheme, transparent background, white outline` |

---

## 総合評価

**完成度**：★★★★☆（4/5）

**強み**：
- frontend-designプラグイン指針に従いAI汎用デザイン（紫グラデ×白）を完全回避
- 温かみ×地方コミュニティのトーンが配色・フォント・コピーで一貫
- レスポンシブ完備（375/768/1024/1280px）
- FVのフローティングカードで動きと現実感を演出
- FAQをdetails/summaryで実装しJS依存ゼロ
- CSSカスタムプロパティでデザイントークンを統一管理

**改善余地**：
- 価格「¥〇〇〇〇」がプレースホルダー → 実際の金額に要変更
- 画像・イラストを実装することで視覚的完成度が大幅向上（上記プロンプト参照）
- OGP（og:image・og:title等）メタタグを追加するとSNSシェア対応になる
