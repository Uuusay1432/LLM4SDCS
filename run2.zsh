#!/bin/zsh

# 引数が指定されていない場合のエラーメッセージ
if [ -z "$1" ]; then
    echo "エラー: 実行回数を指定してください。"
    exit 1
fi

# 引数から実行回数を取得
run_number=$1

# 現在の時間を取得し、ファイル名に使用できる形式にフォーマットする
timestamp=$(date +"%Y%m%d_%H%M%S")

# ログディレクトリを作成（存在しない場合）
mkdir -p log/${run_number}

# src/prompt.py を実行して、ログを log/実行回数/時間.log に出力する
python3 src/prompt2.py > log/${run_number}/${timestamp}.log 2>&1