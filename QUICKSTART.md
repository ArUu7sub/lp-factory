# 操作ガイド（Claude Code単体）

## 全体の流れ

```
ターミナル1本で完結

/lp と入力
  ↓
Claude Code がヒアリング
  ↓
参考デザインサイトを自動検索・分析
  ↓
構成・コピー・コーディングを一気に実行
  ↓
自己レビュー（デザイン4原則・レスポンシブ・画像提案）
  ↓
./ops/deploy.sh でGitHub Pagesに自動公開
  ↓
チームにURLを共有
```

---

## 起動

```bash
cd ~/work/lp-factory
claude
```

---

## 新規案件の開始

```
/lp

または

/lp [案件の概要を一言で]
例：/lp 美容サロンの予約LP
```

Claude Codeがヒアリングを開始する。
以下を順番に確認してくる：
1. サービス・商品の概要
2. ターゲット読者・悩み
3. コンバージョン目標
4. デザインの雰囲気・トーン
5. 参考LP・競合URL（あれば）

---

## Claude Codeが自動でやること

| ステップ | 内容 |
|---------|------|
| 参考デザイン検索 | sankoudesign / rdlp / site-advance から類似LPを取得・分析 |
| 構成設計 | knowledge/ を参照してセクション構成・揃え方を決定 |
| コピー作成 | knowledge/ を参照してコピー文を生成 |
| コーディング | frontend-designプラグイン適用・参考デザインを反映 |
| 自己レビュー | デザイン4原則・レスポンシブ・画像提案 |

---

## デプロイ（チームへの共有）

```bash
cd ~/work/lp-factory
./ops/deploy.sh "案件名: 更新内容"

例：./ops/deploy.sh "ai-start-club: 初回デプロイ"
```

約1分後にこのURLで確認できる：
```
https://ArUu7sub.github.io/lp-factory/案件名/
```

---

## ローカルで確認

```bash
cd ~/work/lp-factory/projects/案件名
npx serve .
# → http://localhost:3000
```

---

## よく使うコマンド

| やること | コマンド |
|---------|---------|
| 新規案件開始 | `/lp` |
| ローカル確認 | `npx serve projects/案件名` |
| GitHub Pages公開 | `./ops/deploy.sh "更新内容"` |
| WordPress変換 | 「WordPressに変換して」と入力 |

---

## Pages URL の構造

```
https://ArUu7sub.github.io/lp-factory/
                               ├── ai-start-club/
                               ├── beauty-salon/
                               └── event-lp/
```
