name: Scratch Trend Update

on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    # ここに最新の環境設定を追加します
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
    steps:
      - name: リポジトリを読み込む
        uses: actions/checkout@v4 # v3からv4に更新

      - name: Pythonの準備
        uses: actions/setup-python@v5 # v4からv5に更新
        with:
          python-version: '3.x'

      - name: 必要なライブラリをインストール
        run: pip install requests

      - name: プログラムを実行
        run: python main.py

      - name: 更新したデータを保存する
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data.json
          git commit -m "トレンドデータを更新" || exit 0
          git push
