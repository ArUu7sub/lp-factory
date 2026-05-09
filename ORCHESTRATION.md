# ORCHESTRATION.md — エージェント統括定義

このファイルは Claude Code が作業開始前に読む統括ドキュメント。
役割・保存先・完了報告形式を把握してから動くこと。

---

## システム全体像

```
ユーザー
  ↕ 相談・方針決定・最終確認
Claude Code（指揮者・ライター・デザイナー・エンジニア）
  └─ ヒアリング
  └─ 参考デザイン検索・分析
  └─ LP構成・コピー文作成
  └─ HTML/CSS/JSのコーディング
  └─ 自己レビュー（デザイン4原則・レスポンシブ・画像提案）
  └─ GitHub Pagesへのデプロイ
ユーザー
  ↕ ブラウザで最終確認・フィードバック
```

---

## Claude Codeの役割
**すべての工程を一人で担当する。**

| 工程 | やること |
|------|---------|
| ヒアリング | サービス・ターゲット・CVなどを確認 |
| 参考デザイン検索 | 3つの参考サイトからトーンに合ったLPを取得・分析 |
| 構成設計 | knowledge/構成パターン/ を参照 |
| コピー作成 | knowledge/コピー設計/ を参照 |
| コーディング | frontend-designプラグインを適用してHTML/CSS/JS生成 |
| 自己レビュー | デザイン4原則・レスポンシブ・画像提案 |
| デプロイ | ./ops/deploy.sh で GitHub Pages に自動公開 |

---

## 参考デザインサイト
コーディング前に必ず以下のサイトから案件のトーン・業種に合ったLPを検索する：
1. https://sankoudesign.com/category/lp/
2. https://rdlp.jp/lp-archive/
3. https://site-advance.info/

---

## ファイルの保存ルール

```
projects/案件名/          ← すべての成果物はここに保存
├── brief.md              ← ヒアリング情報
├── structure.md          ← LP構成（各要素の揃え方明記）
├── copy.md               ← コピー文
├── index.html            ← LP本体
├── style.css             ← スタイル
├── script.js             ← JavaScript
├── review.md             ← 自己レビュー
└── images/               ← 画像・SVG
```

---

## デプロイ
```bash
cd ~/work/lp-factory
./ops/deploy.sh "案件名: 更新内容"
```
URL：https://ArUu7sub.github.io/lp-factory/案件名/

---

## デザイン方針

### frontend-designプラグイン
- 汎用フォント（Inter・Roboto・Arial）禁止
- 紫グラデーション×白背景などの定番AI aesthetic禁止
- コンテキストに合った独自のカラーパレットを選定
- 参考デザインの特徴を活かした個性的な実装

### デザイン4原則
- **近接**：関連要素を近くに。見出し↔本文 margin 8〜16px、セクション間 padding 64〜80px
- **整列**：structure.mdの揃え指定をそのままCSS実装
- **反復**：CSSカスタムプロパティで色・フォント・角丸・影を統一
- **対比**：見出しサイズ差・CTAの色差・font-weight差を明確に
