#!/bin/bash

# ポーカー GTO 分析 Web UI スタートアップスクリプト

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     🎰 ポーカー GTO 分析 Web UI                                   ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ディレクトリ確認
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# venv 確認
if [ ! -d "venv" ]; then
    echo "📦 Python 仮想環境を作成中..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📥 依存パッケージをインストール中..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "✅ 環境準備完了"
echo ""

# IP アドレス確認
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
else
    # Linux
    IP=$(hostname -I | awk '{print $1}')
fi

echo "📱 スマホからのアクセス:"
echo "   http://$IP:5000"
echo ""
echo "🖥️  PC からのアクセス:"
echo "   http://localhost:5000"
echo ""

# Flask 環境設定
export FLASK_APP=app.py

# デバッグモード確認
if [ "$1" = "-d" ] || [ "$1" = "--debug" ]; then
    echo "🔧 デバッグモードで起動..."
    export FLASK_DEBUG=1
    export FLASK_ENV=development
else
    echo "⚙️  本番モードで起動..."
    export FLASK_ENV=production
fi

echo ""
echo "🚀 サーバー起動中..."
echo "   (Ctrl+C で停止)"
echo ""

python app.py
