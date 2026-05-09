# 作業フロー

## 案件開始から納品までの流れ

```
Step 1: ヒアリング・情報収集
  → clients/_template/ をコピーして clients/案件名/ を作成
  → brief.md に情報を記入（不足は人間に確認）

Step 2: LP構成の設計（Claude Code）
  → knowledge/構成パターン/ を参照
  → clients/案件名/structure.md に構成を出力

Step 3: コピー文の作成（Claude Code）
  → knowledge/コピー設計/ を参照
  → clients/案件名/copy.md に各セクションのコピーを出力

Step 4: Codexブリーフの生成（Claude Code）
  → ops/codex/briefs/案件名_design.md を作成

Step 5: Codexによるデザイン・コーディング
  → 実行コマンド：
    codex exec --skip-git-repo-check --sandbox workspace-write \
      "$(cat ops/codex/briefs/案件名_design.md)" \
      > ops/codex/runs/案件名_design.log 2>&1

Step 6: 成果物の一次検査（Claude Code）
  → ops/codex/runs/案件名_design.log を確認
  → clients/案件名/review.md を確認
  → 問題があれば人間に報告

Step 7: 人間による最終確認
  → ブラウザでindex.htmlを開いて確認
  → 修正があればStep 4に戻る

Step 8: （必要時）WordPress変換
  → 人間から「WordPressに移植する」と指示されたときのみ実行
  → ops/codex/briefs/案件名_wp.md を作成してCodexに渡す
```

## 並列実行が可能なケース
- 複数案件のコーディングは同時にCodexを起動できる
- ただし同一案件の内部では Step 2 → 3 → 4 → 5 の順序を守る

## Codex起動コマンドのテンプレート
```bash
codex exec --skip-git-repo-check --sandbox workspace-write \
  "$(cat ops/codex/briefs/[ブリーフ名].md)" \
  > ops/codex/runs/[ログ名]_$(date +%Y%m%d_%H%M).log 2>&1 &
```
