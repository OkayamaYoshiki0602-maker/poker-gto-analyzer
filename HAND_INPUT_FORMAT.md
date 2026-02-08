# 📝 ハンド入力フォーマット

## 🎯 シンプル版（推奨）

```json
{
  "hand_id": "LTsCqZnvNbskQfoenRQB",
  "hero_position": "UTG",
  "hero_hand": "QQ",
  "hero_action": "raise",
  "hero_profit_bb": 4.37,
  "result": "WIN",
  "stack_size_bb": 100,
  "opponent_types": {
    "BB": "TAG"
  },
  "board": ["Js", "6h", "3d", "Ks", "7d"],
  "actions": {
    "preflop": "UTG raise 2.5bb, BB call",
    "flop": "BB check, UTG bet 1.83bb, BB call",
    "turn": "BB check, UTG check",
    "river": "BB check, UTG check"
  }
}
```

## 🔧 詳細版

```json
{
  "hand_id": "LTsCqZnvNbskQfoenRQB",
  "date": "2026/02/08 22:09",
  "game_type": "6-Max NLH (0.5/1)",
  "hero": {
    "position": "UTG",
    "hand": ["Qh", "Qc"],
    "stack_bb": 100,
    "profit_bb": 4.37,
    "result": "WIN"
  },
  "opponents": [
    {"position": "HJ", "hand": ["7s", "2o"], "stack_bb": 100, "profit_bb": 0, "type": "FOLD"},
    {"position": "CO", "hand": ["8d", "7c"], "stack_bb": 100, "profit_bb": 0, "type": "FOLD"},
    {"position": "BTN", "hand": ["4d", "3c"], "stack_bb": 100, "profit_bb": 0, "type": "FOLD"},
    {"position": "SB", "hand": ["Qd", "5c"], "stack_bb": 100, "profit_bb": -0.5, "type": "FOLD"},
    {"position": "BB", "hand": ["5h", "3h"], "stack_bb": 100, "profit_bb": -4.33, "type": "TAG"}
  ],
  "board": {
    "flop": ["Js", "6h", "3d"],
    "turn": ["Ks"],
    "river": ["7d"]
  },
  "action_sequence": {
    "preflop": [
      {"player": "UTG", "action": "raise", "amount_bb": 2.5},
      {"player": "HJ", "action": "fold"},
      {"player": "CO", "action": "fold"},
      {"player": "BTN", "action": "fold"},
      {"player": "SB", "action": "fold"},
      {"player": "BB", "action": "call", "amount_bb": 2.5}
    ],
    "flop": [
      {"player": "BB", "action": "check"},
      {"player": "UTG", "action": "bet", "amount_bb": 1.83},
      {"player": "BB", "action": "call", "amount_bb": 1.83}
    ],
    "turn": [
      {"player": "BB", "action": "check"},
      {"player": "UTG", "action": "check"}
    ],
    "river": [
      {"player": "BB", "action": "check"},
      {"player": "UTG", "action": "check"}
    ]
  },
  "pot_size_bb": 8.7,
  "rake_bb": 0.46,
  "spr": 25
}
```

## 🚀 超シンプル版（最小限）

```json
{
  "hand_id": "LTsCqZnvNbskQfoenRQB",
  "position": "UTG",
  "hand": "QQ",
  "action": "raise",
  "profit_bb": 4.37,
  "result": "WIN",
  "opponent_type": "TAG",
  "board": "Js6h3dKs7d",
  "spr": 25
}
```

## 📊 分類情報

### SPR 分類
- **SPR < 30**: ショートスタック
- **SPR 30-50**: ミディアムスタック  
- **SPR 50-100**: ディープスタック
- **SPR 100+**: 超ディープスタック

### 対戦相手タイプ
- **TAG**: タイト・アグレッシブ
- **LAG**: ルース・アグレッシブ
- **FISH**: フィッシュ（弱いプレイヤー）
- **NIT**: ニット（超タイト）
- **MANIAC**: マニアック（超アグレッシブ）

### ボードテクスチャ
- **DRY**: ドライボード（連続性が低い）
- **WET**: ウェットボード（ドロー多数）
- **RAINBOW**: レインボー（スーツがバラバラ）
- **MONOTONE**: モノトーン（同じスーツ3枚以上）

## 🎯 使用例

### Web UI での入力
```
ハンドID: LTsCqZnvNbskQfoenRQB

ハンドデータ（JSON）:
{
  "position": "UTG",
  "hand": "QQ",
  "action": "raise",
  "profit_bb": 4.37,
  "result": "WIN",
  "opponent_type": "TAG",
  "spr": 25
}
```

### Cursor Agents での依頼
```
以下のハンドを分析してください：

Hand ID: LTsCqZnvNbskQfoenRQB
Position: UTG
Hand: QQ  
Action: raise
Profit: +4.37bb
Result: WIN
Opponent: TAG
SPR: 25
Board: Js6h3dKs7d

GTO 的な評価とアドバイスをお願いします。
```

## 💡 推奨フォーマット

**最も使いやすいのは「シンプル版」です**：

```json
{
  "hand_id": "LTsCqZnvNbskQfoenRQB",
  "hero_position": "UTG",
  "hero_hand": "QQ",
  "hero_action": "raise",
  "hero_profit_bb": 4.37,
  "result": "WIN",
  "opponent_types": {"BB": "TAG"},
  "spr": 25,
  "board": ["Js", "6h", "3d", "Ks", "7d"]
}
```

このフォーマットで入力していただければ、すぐに実装に取り掛かれます！