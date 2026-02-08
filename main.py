#!/usr/bin/env python3
"""
メイン エントリーポイント
ハンドID を受け取り、GTO 分析を実行
"""

import sys
from pathlib import Path

# core モジュールのインポート
sys.path.insert(0, str(Path(__file__).parent / 'core'))
from poker_gto_agent import PokerGTOAgent


def main():
    """メイン処理"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         🎰 ポーカー GTO 分析システム                             ║
║         ハンドID → 包括的な分析レポート                           ║
╚════════════════════════════════════════════════════════════════════╝

【使用方法】

python3 main.py <hand_id_1> <hand_id_2> ... <hand_id_N>

【例】

python3 main.py J674e1buxOGyzZB15uwY QZVSZQq4RedGPnlQZ3gs KTFeCBYS3lIPNYyTJkRk

════════════════════════════════════════════════════════════════════
""")
    
    # コマンドライン引数でハンドID を受け取る
    hand_ids = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not hand_ids:
        print("❌ ハンドIDが指定されていません\n")
        print("使用方法:")
        print("  python3 main.py <hand_id_1> <hand_id_2> ...\n")
        sys.exit(1)
    
    # GTO 分析を実行
    agent = PokerGTOAgent()
    report = agent.analyze_hands(hand_ids)
    
    # レポート表示
    print("\n" + "="*70)
    print(report)
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
