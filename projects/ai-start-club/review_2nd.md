## コードレビュー
- [x] HTMLバリデーション問題なし
- [x] altテキスト全て記述済み
- [x] レスポンシブ確認（375px / 768px / 1280px）
- [x] CTAボタンのリンク先確認

補足：
- `img` は会員の声のアバター3点にあり、すべて `alt` / `width` / `height` が記述済み。
- CTAリンクはすべて `#price` に統一されており、1アクションに絞られている。
- FAQボタンは `button` と `aria-expanded` / `hidden` の組み合わせで実装されており、構造上の問題は見当たらない。

## レスポンシブレビュー
- [x] 375px（スマホ）：1カラム・文字サイズ・ボタン幅・余白を確認
- [x] 768px（タブレット）：2カラム切り替え・ナビ表示を確認
- [x] 1280px（PC）：最大幅・グリッド列数・余白バランスを確認
- [x] 問題があった箇所と修正内容を記載

### 375px
- `lp-container` / `lp-hero__inner` は `100% - 40px` のため左右20px相当の余白が確保されている。
- `.lp-button--large` は初期状態で `width: 100%`、`.lp-button` は `min-height: 52px` のため、タップ領域44px以上を満たしている。
- `.lp-hero__title` は `clamp(2.2rem, 10vw, 4.8rem)` でSPでも大きめ。ファーストビューの印象は強いが、長い日本語見出しでも折り返し前提の設計で許容範囲。
- 各グリッドは初期状態が1カラムで、カード幅の窮屈さは出にくい。

### 768px
- `@media (min-width: 640px)` で問題提起・ベネフィット・会員の声・学べる内容が2カラムへ切り替わる。
- `@media (min-width: 768px)` でヘッダーナビとヘッダーCTAが表示される。リンク数が4つで、`gap: 22px` のため768px付近ではやや密だが、現状の文言長では収まる想定。
- `.lp-button--large` が `width: auto` になるため、CTAの横幅が自然になる。

### 1280px
- `@media (min-width: 1024px)` でベネフィットは4カラム、学べる内容・会員の声は3カラムに切り替わる。
- 最大幅は `.lp-container` が1120px、ヘッダーが1180pxで管理されており、余白バランスは良好。
- ベネフィット4カラムは本文量に差があるが、カードの視覚的な密度は大きく崩れていない。

### 修正有無
- style.cssの直接修正は不要と判断。致命的なレスポンシブ崩れ、タップ領域不足、グリッド列数の不整合は見当たらない。

## 文章レビュー
- [x] ファーストビューに「誰が・何を・どうなるか」が入っている
- [x] 専門用語がない
- [x] CTAが1アクションに絞られている

copy.mdとの照合結果：
- ファーストビュー、問題提起、できること、学べる内容、地方×AIビジョン、会員の声、料金、FAQ、最終CTAの主要コピーは一致。
- HTML側には補助ラベルとして `.lp-hero__label`「山梨発・地方から全国へ」、`.lp-vision__label`「地方×AIビジョン」、`.lp-price__label`「月額プラン」が追加されている。コピーの意味を変える追加ではないため問題なし。
- 文言の抜け・意図しない変更は見当たらない。

## デザイン4原則レビュー

### 近接（Proximity）
- [x] 関連する要素（見出し＋本文、画像＋キャプション）が近くに配置されている
- [x] 無関係な要素の間に十分な余白がある
- 評価：OK
- 改善提案：`.lp-section` の上下余白80px、`.lp-section__head` の下余白34pxにより、セクション単位のまとまりは明確。カード内も `padding: 24px` と本文上 `margin: 12px` で関連要素が近い。現状修正不要。

### 整列（Alignment）
- [x] テキストの揃え方にルールがある（左揃え or 中央揃えが混在していない）
- [x] カードや要素の端が揃っている
- 評価：OK
- 改善提案：セクション見出しは中央、カード本文は左、価格・最終CTAは中央という役割別の揃え方が一貫している。`.lp-container` とグリッドでカード端も揃っている。現状修正不要。

### 反復（Repetition）
- [x] 見出しのフォント・サイズ・色が全セクションで統一されている
- [x] ボタンのスタイルが全体で統一されている
- [x] カードのデザイン（角丸・影・余白）が統一されている
- 評価：OK
- 改善提案：`.lp-section__title`、`.lp-button`、カード系セレクタで反復ルールが作られている。角丸8px、白背景、境界線、影の扱いも統一されている。現状修正不要。

### 対比（Contrast）
- [x] タイトルと本文の文字サイズに明確な差がある
- [x] CTAボタンが背景から視覚的に目立っている
- [x] 重要な情報が色・サイズ・太さで強調されている
- 評価：OK
- 改善提案：ヒーロー見出し、セクション見出し、価格表示でサイズ差が明確。CTAはオレンジ背景と白文字で視認性が高い。アクセントの緑も価格強調・ラベル・名前に使われ、重要情報が区別されている。現状修正不要。

### 総合評価
- 4原則の充足度：4/4 すべて満たしている
- 優先改善事項：なし

## 画像・イラスト提案
以下の箇所に画像またはイラストを追加することを提案する：

| セクション | 提案内容 | 透過判断 | 画像生成プロンプト（英語） |
|-----------|---------|---------|------------------------|
| ファーストビュー | 地方からAI活用へ踏み出す世界観を強め、抽象グラフィックだけでなくサービスの印象を直感化する | 不要：ファーストビュー背景として全面に敷く想定のため | A hopeful wide landscape photo of a small Japanese regional city with mountains in the background, subtle AI network light patterns, warm morning sunlight, professional and approachable mood, wide landscape photo, 16:9 aspect ratio |
| できること | ベネフィットの理解を補助する人物イラストをカード横やセクション内に置ける | 必要：白背景やカード付近に重ねて使う想定のため | Friendly Japanese adult learning AI skills on a laptop, career growth and side business icons around them, clean modern illustration, transparent background, PNG format |
| 地方×AIビジョン | 山梨・地方性を視覚的に補強し、ビジョンセクションの説得力を上げる | 不要：濃い緑のセクション背景または全面背景として使う想定のため | Scenic Yamanashi-inspired landscape with Mount Fuji silhouette, local town, digital AI connection lines, optimistic civic technology mood, wide landscape photo, 16:9 aspect ratio |

