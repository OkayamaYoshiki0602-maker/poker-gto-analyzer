# 🎰 ポーカー GTO 分析システム - 完成！

## 📋 完成内容

完全な **Web UI ベースのポーカー GTO 分析システム**を構築しました。

```
┌─────────────────────────────────────┐
│   📱 スマホ（Web UI フォーム）      │
│  ハンドID を入力 → 分析を実行      │
└──────────────┬──────────────────────┘
               │
         HTTP POST
               │
┌──────────────▼──────────────────────┐
│  💻 Flask バックエンド（app.py）   │
│  リクエスト処理 & 結果返却          │
└──────────────┬──────────────────────┘
               │
         Python 関数呼び出し
               │
┌──────────────▼──────────────────────┐
│  🧠 GTO 分析エージェント            │
│  poker_gto_agent.py                 │
│  - 分析レポート生成                │
│  - ローカル保存                     │
│  - Git コミット                     │
└──────────────┬──────────────────────┘
               │
         GTOEvaluator.evaluate_action()
               │
┌──────────────▼──────────────────────┐
│  📊 GTO 評価エンジン                │
│  gto_evaluator.py                   │
│  - ハンド単位の GTO 整合性判定      │
│  - 文脈付きアドバイス生成          │
└──────────────┬──────────────────────┘
               │
         GitHub Push（設定時）
               │
┌──────────────▼──────────────────────┐
│  📚 GitHub リポジトリ              │
│  reports/ に自動保存 & 履歴管理    │
└─────────────────────────────────────┘
```

## 🗂️ ファイル構成

```
poker-gto-analyzer/
├── 🚀 start.sh                      # ワンコマンド起動
├── 💻 app.py                        # Flask メインアプリ（GitHub push 付き）
├── 📋 requirements.txt              # Python 依存パッケージ
├── 📋 README.md                     # 使用ガイド（英語版）
├── 📋 QUICK_START_JA.md             # 超シンプル日本語ガイド
├── 📋 COMPLETE_GUIDE.md             # 詳細な完全ガイド
├── 📋 .gitignore                    # Git 追跡設定
│
├── 📂 templates/
│   └── 📄 index.html                # スマホ最適化 Web UI
│       - 美しいグラデーション UI
│       - 分析フォーム & 履歴表示
│       - リアルタイム結果表示
│
├── 📂 core/
│   ├── 📄 poker_gto_agent.py       # GTO 分析エージェント
│   │   - ハンド分析のメイン処理
│   │   - Markdown レポート生成
│   │   - GitHub への自動保存
│   │
│   └── 📄 gto_evaluator.py         # GTO 評価エンジン
│       - ハンド単位の GTO 判定
│       - 文脈付きアドバイス
│       - Preflop ranges 定義
│
├── 📂 reports/                      # 分析結果の自動保存先
│   └── analysis_*.md
│
├── 📂 data/                         # キャッシュデータ（自動生成）
│
├── 📂 .git/                         # Git リポジトリ
│
└── 📄 .env                          # GitHub Token 設定（追跡対象外）
```

## 🎯 主な機能

### 1. 🎯 Web UI（スマホ最適化）

```
✨ デザイン
- グラデーション背景（紫系）
- レスポンシブ対応
- タッチフレンドリー
- ローディングアニメーション

🔧 機能
- ハンドID フォーム（複数行対応）
- メモ入力欄
- 分析ボタン
- 履歴表示モーダル
- リアルタイム結果表示
```

### 2. 🧠 GTO 分析エンジン

```
📊 分析内容
- ハンド別の GTO 整合性判定
- 本質的なアドバイス生成
- 総合 GTO 整合率計算
- リーク検出

💾 出力
- Markdown レポート
- ローカル reports/ に自動保存
- Git コミット
- GitHub push（設定時）
```

### 3. 💾 GitHub 自動保存

```
🔄 フロー
1. 分析完了 → reports/ に MD ファイル保存
2. Git add & commit
3. GitHub に push（Token 設定時）

📚 履歴管理
- 全分析レポートが永続保存
- Web UI から履歴を検索表示
- タイムスタンプ付き
```

## 🚀 使い方

### 超シンプル版（3 ステップ）

```bash
# 1. サーバー起動
./start.sh

# 2. ブラウザで http://localhost:5000 にアクセス
#    （スマホは http://<IP>:5000）

# 3. ハンドID を入力 → 分析
```

### 詳細は各ドキュメント参照

- **急いでいる人**: `QUICK_START_JA.md`
- **詳しく知りたい人**: `COMPLETE_GUIDE.md`
- **英語**: `README.md`

## ⚡ クイックコマンド

```bash
# インストール & 起動
cd poker-gto-analyzer
./start.sh

# デバッグモード
./start.sh -d

# 手動起動
python app.py

# GitHub Token を設定
echo "GITHUB_TOKEN=<token>" > .env
echo "GITHUB_REPO=<user>/<repo>" >> .env

# Git ステータス確認
git status

# コミット履歴
git log --oneline
```

## 🔑 API エンドポイント

| メソッド | URL | 機能 |
|---------|-----|------|
| GET | `/` | Web UI トップページ |
| POST | `/api/analyze` | ハンド分析 |
| GET | `/api/history` | 分析履歴一覧 |
| GET | `/api/report/<filename>` | 特定レポート表示 |

## 📊 GTO Ranges（簡略版）

```
BTN（最も有利なポジション）
  raise: AA-77, AK, AQ, KQ, AJ, KJ, QJ (14 ハンド)
  
UTG（最も不利なポジション）
  raise: AA-TT, AK, AQ, AJ, KQ (9 ハンド)
```

詳細は `core/gto_evaluator.py` を参照

## 🎓 学習フロー

```
1. Ten-Four でプレイ
   ↓
2. ハンドID をコピー
   ↓
3. Web UI に入力
   ↓
4. 分析結果を確認
   ↓
5. GTO 的に正解か判定
   ↓
6. 改善策を実装
```

## ✅ チェックリスト

### インストール前

- [ ] Python 3.8+ がインストール済み
- [ ] ターミナルが使える
- [ ] WiFi に接続可能

### 起動前

- [ ] `poker-gto-analyzer/` ディレクトリにいる
- [ ] `start.sh` が実行可能（`chmod +x start.sh`）

### 起動後

- [ ] ブラウザで `http://localhost:5000` にアクセス可能
- [ ] Web UI が表示される
- [ ] フォーム入力 & 分析が動作
- [ ] スマホからもアクセス可能

### オプション（GitHub 連携）

- [ ] GitHub Token を作成
- [ ] `.env` ファイルを設定
- [ ] Git config が正しい

## 🎯 これから

### 短期（1 週間以内）

1. システムを起動してテスト
2. 実ハンドで分析してみる
3. GTO ranges を参考に改善

### 中期（1 ヶ月以内）

1. 100+ ハンドを分析
2. リークパターンを把握
3. 対策を実装

### 長期（3 ヶ月以上）

1. より詳細な ranges を学習
2. ポストフロップ戦略を追加
3. 対戦相手タイプ別の対策

## 🚨 トラブルシューティング

### エラー: `Address already in use :5000`

```bash
# port を変更
python app.py  # port 5001 として起動
```

### スマホから接続できない

```bash
# IP を確認
ifconfig | grep "inet "

# 同じ WiFi に接続しているか確認
```

### GitHub push が失敗

```bash
# Token を確認
cat .env | grep GITHUB_TOKEN

# リモート確認
git remote -v
```

詳細は `QUICK_START_JA.md` の Q&A セクションを参照

## 📚 参考資料

### 公式サイト

- Flask: https://flask.palletsprojects.com/
- Ten-Four: https://tenfour-poker.com/
- GitHub: https://github.com/

### GTO 学習

- Solver: PioSOLVER, Monker
- 本: "Applications of No-Limit Hold'em"
- サイト: https://www.splitsuit.com/

## 🎉 完成！

```
📱 Web UI ✅
💻 Flask バックエンド ✅
🧠 GTO 分析エンジン ✅
💾 GitHub 自動保存 ✅
📚 ドキュメント ✅
🚀 起動スクリプト ✅
```

**すべてが完成しました！さあ、始めましょう！**

---

## 📞 問い合わせ

不明な点があれば：

1. `QUICK_START_JA.md` を確認（日本語）
2. `README.md` を確認（詳細）
3. `COMPLETE_GUIDE.md` を確認（完全ガイド）
4. コード内のコメントを参照

---

**🎰 Happy Poker Learning!**

*「結果より判断」 - GTO プレイヤーの心得*

**Created with ❤️**
