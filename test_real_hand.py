#!/usr/bin/env python3
"""
実ハンドデータのテスト
LTsCqZnvNbskQfoenRQB の実データを使用してテスト
"""

import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent / 'core'))

from poker_gto_agent import PokerGTOAgent


def test_real_hand():
    """実ハンドデータでテスト"""
    
    # 実ハンドデータ（LTsCqZnvNbskQfoenRQB）
    # Hand #LTsCqZnvNbskQfoenRQB
    # 2026/02/08 22:09 · 6-Max NLH (0.5/1)
    # UTG okayama: QQ (100bb) → WIN +4.37bb
    # BB hayassi: 53h (100bb) → LOSE -4.33bb
    # Board: Js 6h 3d Ks 7d
    hand_data = [
        {
            "hand_id": "LTsCqZnvNbskQfoenRQB",
            "date": "2026/02/08 22:09",
            "game_type": "6-Max NLH (0.5/1)",
            "hero_position": "UTG",
            "hero_hand": "QQ",
            "hero_action": "raise",
            "hero_profit_bb": 4.37,
            "result": "WIN",
            "stack_size_bb": 100,
            "opponent_types": {"BB": "TAG"},
            "board": ["Js", "6h", "3d", "Ks", "7d"],
            "spr": 25,
            "pot_size_bb": 8.7,
            "rake_bb": 0.46,
            "actions": {
                "preflop": "UTG raise 2.5bb, BB call",
                "flop": "BB check, UTG bet 1.83bb, BB call",
                "turn": "BB check, UTG check",
                "river": "BB check, UTG check"
            }
        }
    ]
    
    # 分析実行
    agent = PokerGTOAgent()
    hand_ids = ["LTsCqZnvNbskQfoenRQB"]
    
    print("🎰 実ハンドデータでテスト実行")
    print(f"ハンドID: {hand_ids[0]}")
    print(f"実データ: UTG QQ raise → WIN +4.37bb")
    print("-" * 50)
    
    report = agent.analyze_hands(hand_ids, hand_data)
    
    print("\n📊 分析結果:")
    print(report)


def test_sample_data():
    """サンプルデータでテスト"""
    
    agent = PokerGTOAgent()
    hand_ids = ["LTsCqZnvNbskQfoenRQB"]
    
    print("🎰 サンプルデータでテスト実行")
    print(f"ハンドID: {hand_ids[0]}")
    print(f"サンプルデータ: BTN AK raise → LOSE -50bb")
    print("-" * 50)
    
    report = agent.analyze_hands(hand_ids)
    
    print("\n📊 分析結果:")
    print(report)


if __name__ == '__main__':
    print("=" * 60)
    print("🧪 ハンドデータ処理テスト")
    print("=" * 60)
    
    print("\n1️⃣ 実ハンドデータテスト:")
    test_real_hand()
    
    print("\n" + "=" * 60)
    
    print("\n2️⃣ サンプルデータテスト:")
    test_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ テスト完了")