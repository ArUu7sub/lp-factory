#!/bin/bash
# 使い方：./ops/deploy.sh "コミットメッセージ"
# 例：  ./ops/deploy.sh "ai-start-club: FVに画像を追加"
#
# projects/ 配下の変更を検知してpush。
# GitHub Actionsが自動でPagesにデプロイする。

MSG=${1:-"update projects"}

cd ~/work/lp-factory

# 変更ファイルを確認
CHANGED=$(git status --short projects/ 2>/dev/null)
if [ -z "$CHANGED" ]; then
  echo "⚠️  projects/ に変更がありません"
  exit 0
fi

echo "変更ファイル："
echo "$CHANGED"
echo ""

git add projects/
git commit -m "$MSG"
git push origin main

echo ""
echo "✅ Push完了 → GitHub Actionsが自動デプロイ中（約1分）"
echo ""

# リポジトリ名からPagesのURLを生成
REMOTE=$(git remote get-url origin 2>/dev/null)
if [[ $REMOTE == git@github.com:* ]]; then
  REPO_PATH=${REMOTE#git@github.com:}
  REPO_PATH=${REPO_PATH%.git}
elif [[ $REMOTE == https://github.com/* ]]; then
  REPO_PATH=${REMOTE#https://github.com/}
  REPO_PATH=${REPO_PATH%.git}
fi

if [ -n "$REPO_PATH" ]; then
  USER=$(echo $REPO_PATH | cut -d'/' -f1)
  REPO=$(echo $REPO_PATH | cut -d'/' -f2)
  echo "🌐 Pages URL（案件ごと）："
  for dir in projects/*/; do
    PROJECT=$(basename "$dir")
    echo "   https://${USER}.github.io/${REPO}/${PROJECT}/"
  done
fi
