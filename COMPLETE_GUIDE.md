# 📂 ポーカー GTO 分析システム - 完全ガイド

## 🎯 システム概要

このシステムは、**Ten-Four ポーカーアプリ**のハンドデータを GTO 基準で分析し、改善提案を提供する Web UI です。

```
ユーザー（スマホ）
    ↓
Web UI（フォーム）
    ↓
Flask バックエンド
    ↓
GTO 分析エージェント
    ↓
GitHub リポジトリ（履歴保存）
```

## 📁 ファイル構成

### メインシステム: `poker-gto-analyzer/`

```
poker-gto-analyzer/
├── 🚀 start.sh                      # サーバー起動スクリプト
├── 📋 app.py                        # Flask メインアプリ（GitHub push 付き）
├── 📋 requirements.txt              # Python 依存パッケージ
├── 📋 README.md                     # 使用ガイド
├── 📋 .gitignore                    # Git 追跡設定
│
├── 📂 templates/
│   └── 📄 index.html                # スマホ最適化 Web UI
│
├── 📂 core/
│   ├── 📄 poker_gto_agent.py       # GTO 分析エージェント（メイン分析ロジック）
│   └── 📄 gto_evaluator.py         # GTO 評価エンジン（ハンド単位の評価）
│
├── 📂 reports/                      # 分析結果の保存先（自動生成）
│   ├── 📄 analysis_20260207_143021.md
│   ├── 📄 analysis_20260207_150145.md
│   └── ...
│
├── 📂 data/                         # キャッシュデータ（自動生成）
│
└── 📄 .env                          # GitHub Token 設定（git 追跡対象外）
```

### レガシーファイル（旧システム、必要に応じて参照）

**参照用のみ - 削除してもOK:**
- `../auto_collect_hands.py` - Playwright ハンド自動収集（トークン取得問題で未完）
- `../auto_collect_hands_advanced.py` - 高度な自動収集版
- `../safari_webkit_auto.py` - Safari ログイン自動化試行版
- 他の shell スクリプト

## 🚀 使い方（ステップバイステップ）

### Step 1: 環境セットアップ

```bash
cd poker-gto-analyzer

# 初回のみ
chmod +x start.sh

# または仮想環境を手動で作成
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: サーバー起動

```bash
# 簡単起動
./start.sh

# または Python で直接実行
python app.py
```

出力例:
```
╔══════════════════════════════════════════════╗
║     🎰 ポーカー GTO 分析 Web UI              ║
╠══════════════════════════════════════════════╣
║  http://localhost:5000                      ║
║  スマホからアクセス: http://192.168.1.100:5000
╚══════════════════════════════════════════════╝
```

### Step 3: スマホからアクセス

1. 同じ WiFi に接続
2. ブラウザで `http://<PC-IP>:5000` にアクセス
3. ハンドID を入力 → 分析

## 📊 分析フロー

### ユーザー操作

```
[Web UI フォーム]
    ↓
[ハンドID を入力]
例: J674e1buxOGyzZB15uwY
    ↓
[🔍 分析する をクリック]
```

### バックエンド処理

```
1. app.py が POST リクエストを受け取る
2. poker_gto_agent.py を呼び出し
3. gto_evaluator.py で各ハンドを評価
4. Markdown レポート を生成
5. reports/ にローカル保存
6. Git コミット
7. GitHub に push（設定されている場合）
8. JSON レスポンスを Web UI に返す
```

### 出力

```markdown
# 🎰 GTO 対応ポーカー分析レポート

**分析日時:** 2026-02-07 14:30:21

## 📊 分析結果サマリー

### ハンド 1: AK

**基本情報:**
- ハンドID: J674e1buxOGyzZB15uwY
- ポジション: BTN
- アクション: raise
- 結果: LOSE (-50.0bb)
- 対戦相手: TAG

**GTO 評価:**
- GTO通り ✅
- BTN からの AK raise は GTO 基準に合致しています

**文脈付きアドバイス:**
✅ **判断は正しいです**
負けていますが、AK を BTN から raise するのは GTO 戦略の標準的な判断です。
短期的な結果に左右されず、長期的には正しい判断を繰り返すことが重要です。

---

## 🎯 総合評価

- **GTO 整合率:** 1/1 (100%)
- **主なリーク:** 位置別戦略の改善が必要
- **推奨アクション:** 弱いハンドの fold 率を上げる
```

## 🔑 GitHub 自動 push 設定

### オプション：GitHub Token を設定（自動 push に必要）

```bash
# .env ファイルを作成
cat > .env << 'EOF'
GITHUB_TOKEN=<your-personal-access-token>
GITHUB_REPO=<username>/<repo-name>
EOF
```

**Token の作成:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token"
3. `repo` スコープを選択
4. Token をコピーして `.env` に貼り付け

### 設定なしの場合

- レポートは **ローカル `reports/` に保存**
- Git コミットは実行される
- push は実行されない

## 📱 フロントエンド機能

### 1. 分析フォーム

- **ハンドID**: 複数行入力可能
- **メモ**: セッション情報を記録
- **リアルタイム送信**: JSON API 経由

### 2. 分析結果表示

```
✅ 分析完了 (3 ハンド)

# 🎰 GTO 対応ポーカー分析レポート
...（詳細レポート）...
```

### 3. 履歴機能

- 📜 「履歴」ボタンで過去の分析一覧を表示
- クリックで詳細内容を表示

## 🔧 API リファレンス

### POST `/api/analyze`

**例:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "hand_ids": ["J674e1buxOGyzZB15uwY", "QZVSZQq4RedGPnlQZ3gs"],
    "notes": "BTN vs BB SRP"
  }'
```

**レスポンス:**
```json
{
  "success": true,
  "report": "# 🎰 GTO 対応ポーカー分析レポート\n...",
  "hand_count": 2,
  "github_status": "✅ GitHub に保存されました",
  "timestamp": "2026-02-07T14:30:21.123456"
}
```

### GET `/api/history`

最近の分析一覧を取得

```bash
curl http://localhost:5000/api/history
```

### GET `/api/report/<filename>`

特定のレポートを取得

```bash
curl http://localhost:5000/api/report/analysis_20260207_143021.md
```

## 🧠 GTO 基礎

### 簡略版 Preflop Ranges（raise）

| ポジション | ハンド数 | 例 |
|--------|---------|-----|
| UTG | 9 | AA-TT, AK, AQ, AJ, KQ |
| MP | 10 | AA-99, AK, AQ, KQ, AJ |
| CO | 12 | AA-88, AK, AQ, KQ, AJ, KJ |
| BTN | 14 | AA-77, AK, AQ, KQ, AJ, KJ, QJ |
| SB | 8 | AA-66, AK, AQ, KQ |

詳細は `core/gto_evaluator.py` 内の `GTO_PREFLOP_RANGES` を参照

## ⚙️ カスタマイズ

### GTO Ranges を更新

`core/gto_evaluator.py` の `GTO_PREFLOP_RANGES` を編集：

```python
'BTN': {
    'raise': ['AA', 'KK', 'QQ', ...],  # ← ここを編集
    'fold': [],
}
```

### 分析レポートのテンプレートを変更

`core/poker_gto_agent.py` の `_generate_gto_report()` メソッドを編集

### Web UI のデザインを変更

`templates/index.html` の CSS を編集

## 🐛 デバッグ

### デバッグモードで起動

```bash
./start.sh -d
# または
FLASK_DEBUG=1 python app.py
```

### ログを確認

```bash
# ターミナルに詳細ログが出力されます
# IP アドレスや port 番号の問題を確認できます
```

### スマホからアクセスできない場合

```bash
# IP アドレスを確認
ifconfig | grep "inet " | grep -v 127.0.0.1

# ファイアウォール許可（macOS）
sudo lsof -i :5000

# または Linux
sudo ufw allow 5000
```

## 📚 参考資料

### Ten-Four

- https://tenfour-poker.com/
- Hand History にハンドが保存される

### GTO 学習

- Preflop ranges: ハンドの強さとポジションで判断
- Postflop play: フロップ以降は相手の傾向で判断
- 短期的な結果より判断の正確性を重視

### Python/Flask

- Flask: https://flask.palletsprojects.com/
- Python: https://www.python.org/

## 🎓 次のステップ

### 1. 実データで試す

1. Ten-Four でプレイ
2. ハンドID を Web UI に入力
3. 分析結果から学習

### 2. GitHub リポジトリを公開

```bash
# リモート設定
git remote add origin https://github.com/<user>/<repo>
git push -u origin main
```

### 3. GTO Ranges を洗練させる

- より詳細な ranges を追加
- ポストフロップ戦略を実装
- 対戦相手タイプ別の対策を追加

### 4. Ten-Four API 統合（将来版）

- 現在: サンプルデータ + 手入力
- 将来: API から自動取得 + リアルタイム分析

## 📞 よくある質問

### Q. ハンドID はどこから取得？

A. Ten-Four の Hand History ページでハンドをクリック → URL から ID をコピー

### Q. スマホから見たら文字が小さい

A. ブラウザで拡大（ピンチ）可能

### Q. 分析結果を CSV でエクスポートしたい

A. 将来版で対応予定

### Q. ローカルのみで使いたい（GitHub 連携なし）

A. `.env` を設定せず使用可能 → `reports/` にローカル保存

## ✅ チェックリスト

起動前に確認：

- [ ] Python 3.8 以上がインストールされている
- [ ] `poker-gto-analyzer` ディレクトリに移動
- [ ] `start.sh` が実行可能（`chmod +x start.sh`）
- [ ] スマホが同じ WiFi に接続

起動後に確認：

- [ ] ブラウザで `http://localhost:5000` にアクセス可能
- [ ] Web UI が表示される
- [ ] フォームに入力可能
- [ ] 「分析する」ボタンが動作

---

**🎰 これで完全版のシステムが完成しました！**

**スマホから送信 → Python で分析 → GitHub に自動保存**

何か質問があれば、`README.md` または各コードのコメントを参照してください。
