# 🎰 ポーカー GTO 分析 Web UI

スマホから直接ハンドID を送信し、**リアルタイムで GTO 分析**を実行します。  
分析結果は GitHub リポジトリに自動保存・push されます。

## 🚀 クイックスタート

### 1. インストール

```bash
# リポジトリをクローン
git clone <your-repo-url>
cd poker-gto-analyzer

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. 環境設定（GitHub 自動 push 用、オプション）

```bash
# .env ファイルを作成
cat > .env << 'EOF'
GITHUB_TOKEN=<your-personal-access-token>
GITHUB_REPO=<username>/<repo-name>
EOF
```

**GitHub Token の作成方法:**
- GitHub Settings → Developer settings → Personal access tokens → Generate new token
- `repo` スコープを選択
- Token をコピーして `.env` に貼り付け

### 3. サーバー起動

```bash
# 開発環境
python app.py

# または本番環境
FLASK_ENV=production python app.py
```

### 4. アクセス

**PC から:**
- http://localhost:5000

**スマホから（同じ WiFi）:**
- http://<PC-IP>:5000
  - IP を確認: `ifconfig | grep inet`

## 📱 使い方

1. **ハンドID を入力**
   - Ten-Four の Hand History からコピー
   - 1 行に 1 つの ID

2. **メモを追加（オプション）**
   - BTN vs BB など、セッション情報を記録

3. **🔍 分析する をクリック**
   - GTO 評価
   - 本質的なアドバイス
   - 結果が表示される

4. **📜 履歴 で過去の分析を確認**

## 🎯 分析結果の内容

### 各ハンドについて

- **基本情報**: ポジション、アクション、結果
- **GTO 評価**: GTO 基準との整合性
- **文脈付きアドバイス**:
  - 負けていても GTO 的に正解
  - 判断の見直しが必要な場合
  - ポスト・フロップの改善点

### 総合評価

- GTO 整合率
- 主なリーク
- 推奨アクション

## 💾 データ保存

### ローカル保存

```
reports/
├── analysis_20260207_143021.md
├── analysis_20260207_150145.md
└── ...
```

### GitHub 自動 push

GitHub Token が設定されている場合:
- 自動的に `reports/` にコミット
- GitHub リポジトリにプッシュ
- 履歴が永続的に保存される

## 🔧 構成

```
poker-gto-analyzer/
├── app.py                   # Flask Web UI メインアプリ
├── requirements.txt         # Python 依存パッケージ
├── templates/
│   └── index.html          # スマホ最適化 HTML
├── core/
│   ├── poker_gto_agent.py  # GTO 分析エージェント
│   └── gto_evaluator.py    # GTO 評価エンジン
├── reports/                # 分析結果（自動作成）
├── data/                   # キャッシュデータ（自動作成）
└── .env                    # GitHub 設定（Git 追跡なし）
```

## 🔐 セキュリティ

- `.env` は Git から除外（`.gitignore` で指定済み）
- GitHub Token は local のみで保存
- 本番環境では `FLASK_ENV=production` を設定

## 📝 API リファレンス

### POST `/api/analyze`

ハンドを分析

**リクエスト:**
```json
{
  "hand_ids": ["J674e1buxOGyzZB15uwY", "QZVSZQq4RedGPnlQZ3gs"],
  "notes": "BTN vs BB SRP"
}
```

**レスポンス:**
```json
{
  "success": true,
  "report": "# 分析レポート\n...",
  "hand_count": 2,
  "github_status": "✅ GitHub に保存されました",
  "timestamp": "2026-02-07T14:30:21.123456"
}
```

### GET `/api/history`

分析履歴を取得

**レスポンス:**
```json
{
  "reports": [
    {
      "filename": "analysis_20260207_143021.md",
      "timestamp": 1707305421,
      "preview": "# 🎰 GTO 対応ポーカー分析レポート..."
    }
  ]
}
```

### GET `/api/report/<filename>`

特定の分析レポートを取得

## 🚀 次のステップ

### 1. GitHub リポジトリ作成

```bash
# リポジトリをプッシュ
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. GitHub Pages で公開（オプション）

```bash
# GitHub Actions で自動デプロイ可能
```

### 3. Ten-Four API 統合（将来版）

現在はサンプルデータを使用していますが、将来的に:
- Ten-Four から実ハンドデータを自動取得
- リアルタイムで詳細な GTO 評価

## 📚 GTO 基礎

### 各ポジションの raise レンジ（簡略版）

| ポジション | レンジ例 | ハンド数 |
|--------|---------|--------|
| UTG | AA-TT, AK, AQ, AJ, KQ | 9 |
| MP | AA-TT, 99, AK, AQ, KQ, AJ | 10 |
| CO | AA-88, AK, AQ, KQ, AJ, KJ | 12 |
| BTN | AA-77, AK, AQ, KQ, AJ, KJ, QJ | 14 |
| SB | AA-66, AK, AQ, KQ | 8 |

詳細は `core/gto_evaluator.py` を参照

## 🐛 トラブルシューティング

### スマホからアクセスできない

```bash
# ファイアウォール確認
sudo ufw allow 5000

# IP アドレス確認
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### GitHub push に失敗

```bash
# Token を確認
cat .env | grep GITHUB_TOKEN

# リモート確認
git remote -v
```

### ハンドID が見つからない

1. Ten-Four にログイン済みか確認
2. Hand History ページを開く
3. ハンドをクリック → URL から ID をコピー

## 📞 サポート

問題が発生した場合:
1. ターミナルのエラーメッセージを確認
2. `.env` ファイルが正しく設定されているか確認
3. Flask のデバッグモードで実行: `FLASK_DEBUG=1 python app.py`

## 📄 ライセンス

MIT License

---

**Made with ❤️ for poker players**  
*GTO の基準を学習し、一段階上のプレイヤーになりましょう！*
