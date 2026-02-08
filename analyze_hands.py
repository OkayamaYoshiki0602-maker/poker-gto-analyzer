#!/usr/bin/env python3
"""
ハンド履歴パーサーと分析スクリプト
Ten-Fourフォーマットのハンド履歴をパースしてGTO分析を実行
"""

import re
from datetime import datetime
from pathlib import Path
from core.poker_gto_agent import PokerGTOAgent
from core.hand_data_processor import HandDataProcessor


class TenFourHandParser:
    """Ten-Fourハンド履歴パーサー"""
    
    @staticmethod
    def parse_card(card_str: str) -> str:
        """カード表記を標準化"""
        card_map = {
            '♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'
        }
        
        for symbol, letter in card_map.items():
            card_str = card_str.replace(symbol, letter)
        
        return card_str
    
    @staticmethod
    def parse_hand_notation(card1: str, card2: str) -> str:
        """2枚のカードからハンド表記を生成"""
        card1 = TenFourHandParser.parse_card(card1)
        card2 = TenFourHandParser.parse_card(card2)
        
        rank1 = card1[0]
        suit1 = card1[1] if len(card1) > 1 else ''
        rank2 = card2[0]
        suit2 = card2[1] if len(card2) > 1 else ''
        
        # ランク値マップ
        rank_values = {
            'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
            '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
        }
        
        # ペアの場合
        if rank1 == rank2:
            return f"{rank1}{rank2}"
        
        # 高いランクを先に
        if rank_values.get(rank1, 0) < rank_values.get(rank2, 0):
            rank1, rank2 = rank2, rank1
            suit1, suit2 = suit2, suit1
        
        # スーテッド/オフスーツ
        if suit1 and suit2:
            if suit1 == suit2:
                return f"{rank1}{rank2}s"
            else:
                return f"{rank1}{rank2}o"
        
        return f"{rank1}{rank2}"
    
    @staticmethod
    def parse_hand_history(hand_text: str, hero_name: str = "okayama") -> dict:
        """
        Ten-Fourフォーマットのハンド履歴をパース
        
        Args:
            hand_text: ハンド履歴テキスト
            hero_name: プレイヤー名（デフォルト: "okayama"）
        
        Returns:
            パースされたハンドデータ
        """
        
        # Hand IDを抽出
        hand_id_match = re.search(r'Hand #(\w+)', hand_text)
        hand_id = hand_id_match.group(1) if hand_id_match else 'unknown'
        
        # 日時を抽出
        date_match = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2})', hand_text)
        date = date_match.group(1) if date_match else ''
        
        # ゲームタイプを抽出
        game_type_match = re.search(r'6-Max NLH \(([\d.]+)/([\d.]+)\)', hand_text)
        game_type = game_type_match.group(0) if game_type_match else '6-Max NLH'
        
        # プレイヤー情報を抽出
        players = {}
        player_pattern = re.compile(
            r'(UTG|HJ|CO|BTN|SB|BB)\n(\w+)\n\((\d+)bb\)\n([AKQJT2-9][♠♥♦♣])\n([AKQJT2-9][♠♥♦♣])\n([+-][\d.]+bb|±0bb)'
        )
        
        for match in player_pattern.finditer(hand_text):
            position = match.group(1)
            name = match.group(2)
            stack = match.group(3)
            card1 = match.group(4)
            card2 = match.group(5)
            profit = match.group(6)
            
            # 利益をパース
            profit_value = 0
            if profit.startswith('+'):
                profit_value = float(profit[1:-2])
            elif profit.startswith('-'):
                profit_value = -float(profit[1:-2])
            
            # ハンド表記を生成
            hand_notation = TenFourHandParser.parse_hand_notation(card1, card2)
            
            players[position] = {
                'name': name,
                'stack_bb': int(stack),
                'card1': TenFourHandParser.parse_card(card1),
                'card2': TenFourHandParser.parse_card(card2),
                'hand': hand_notation,
                'profit_bb': profit_value
            }
        
        # Heroの情報を取得
        hero_position = None
        hero_data = None
        for position, player in players.items():
            if player['name'] == hero_name:
                hero_position = position
                hero_data = player
                break
        
        if not hero_data:
            raise ValueError(f"プレイヤー '{hero_name}' が見つかりません")
        
        # ボードを抽出
        board = []
        flop_match = re.search(r'Flop\n([AKQJT2-9][♠♥♦♣])\n([AKQJT2-9][♠♥♦♣])\n([AKQJT2-9][♠♥♦♣])', hand_text)
        if flop_match:
            board.extend([
                TenFourHandParser.parse_card(flop_match.group(1)),
                TenFourHandParser.parse_card(flop_match.group(2)),
                TenFourHandParser.parse_card(flop_match.group(3))
            ])
        
        turn_match = re.search(r'Turn\n([AKQJT2-9][♠♥♦♣])', hand_text)
        if turn_match:
            board.append(TenFourHandParser.parse_card(turn_match.group(1)))
        
        river_match = re.search(r'River\n([AKQJT2-9][♠♥♦♣])', hand_text)
        if river_match:
            board.append(TenFourHandParser.parse_card(river_match.group(1)))
        
        # アクションを抽出
        actions = TenFourHandParser._extract_actions(hand_text, hero_name, hero_position)
        
        # Heroのプリフロップアクションを判定
        hero_action = 'fold'
        if f'{hero_position}{hero_name} Raise' in hand_text:
            hero_action = 'raise'
        elif f'{hero_position}{hero_name} Call' in hand_text:
            hero_action = 'call'
        elif f'{hero_position}{hero_name} Fold' in hand_text:
            hero_action = 'fold'
        
        # 結果を判定
        result = 'LOSE'
        if hero_data['profit_bb'] > 0:
            result = 'WIN'
        elif hero_data['profit_bb'] == 0:
            result = 'FOLD'
        
        # 対戦相手タイプ（デフォルト：UNKNOWN）
        opponent_types = {}
        for position, player in players.items():
            if player['name'] != hero_name:
                opponent_types[position] = 'UNKNOWN'
        
        return {
            'hand_id': hand_id,
            'date': date,
            'game_type': game_type,
            'hero_position': hero_position,
            'hero_hand': hero_data['hand'],
            'hero_action': hero_action,
            'hero_profit_bb': hero_data['profit_bb'],
            'result': result,
            'stack_size_bb': hero_data['stack_bb'],
            'opponent_types': opponent_types,
            'board': board,
            'actions': actions,
            'all_players': players
        }
    
    @staticmethod
    def _extract_actions(hand_text: str, hero_name: str, hero_position: str) -> dict:
        """アクションシーケンスを抽出"""
        actions = {
            'preflop': [],
            'flop': [],
            'turn': [],
            'river': []
        }
        
        # Preflopセクションを抽出
        preflop_section = re.search(r'Preflop\n(.*?)(?:Flop|Result)', hand_text, re.DOTALL)
        if preflop_section:
            preflop_text = preflop_section.group(1)
            # アクションを抽出
            action_lines = preflop_text.strip().split('\n')
            for line in action_lines:
                if line.strip():
                    actions['preflop'].append(line.strip())
        
        # Flopセクションを抽出
        flop_section = re.search(r'Flop\n[AKQJT2-9][♠♥♦♣]\n[AKQJT2-9][♠♥♦♣]\n[AKQJT2-9][♠♥♦♣]\n(.*?)(?:Turn|Result)', hand_text, re.DOTALL)
        if flop_section:
            flop_text = flop_section.group(1)
            action_lines = flop_text.strip().split('\n')
            for line in action_lines:
                if line.strip():
                    actions['flop'].append(line.strip())
        
        # Turnセクションを抽出
        turn_section = re.search(r'Turn\n[AKQJT2-9][♠♥♦♣]\n(.*?)(?:River|Result)', hand_text, re.DOTALL)
        if turn_section:
            turn_text = turn_section.group(1)
            action_lines = turn_text.strip().split('\n')
            for line in action_lines:
                if line.strip():
                    actions['turn'].append(line.strip())
        
        # Riverセクションを抽出
        river_section = re.search(r'River\n[AKQJT2-9][♠♥♦♣]\n(.*?)Result', hand_text, re.DOTALL)
        if river_section:
            river_text = river_section.group(1)
            action_lines = river_text.strip().split('\n')
            for line in action_lines:
                if line.strip():
                    actions['river'].append(line.strip())
        
        return actions


# ユーザー提供のハンド履歴
hands_raw = [
        # Hand 1
        """Hand #1XeRyAzhRXOExk2HxMU1

2026/02/09 00:50 · 6-Max NLH (0.5/1)
SB
hj0***
(100bb)
Q♦
4♦
-0.5bb
BB
okayama
(100bb)
8♥
8♦
-3.13bb
UTG
Ukey
(100bb)
K♦
7♠
±0bb
HJ
kugatti
(100bb)
A♠
9♥
+3.29bb
CO
Kurama
(100bb)
A♣
T♦
±0bb
BTN
S
(100bb)
9♣
2♠
±0bb
Preflop
UTGUkey Fold
HJkugatti Raise 2bb
COKurama Fold
BTNS Fold
SBhj0*** Fold
BBokayama Call 2bb
Flop
A♥
5♦
3♥
BBokayama Check
HJkugatti Check
Turn
T♥
BBokayama Check
HJkugatti Bet 1.13bb
BBokayama Call 1.13bb
River
5♣
BBokayama Check
HJkugatti Bet 5.07bb
BBokayama Fold
Result
kugatti wins 6.42bb
Rake: 0.34bb""",

        # Hand 2
        """Hand #0BzxT499i2HnGZ4VgZzP

2026/02/09 00:49 · 6-Max NLH (0.5/1)
HJ
Wadada
(100bb)
8♠
8♥
-2bb
CO
coffee
(100bb)
6♠
3♣
±0bb
BTN
okayama
(100bb)
A♣
J♣
-7bb
SB
sushiro
(100bb)
A♥
A♦
+10bb
BB
etf***
(100bb)
5♠
4♥
-1bb
UTG
FvW***
(100bb)
T♣
6♦
±0bb
Preflop
UTGFvW*** Fold
HJWadada Raise 2bb
COcoffee Fold
BTNokayama Raise 7bb
SBsushiro Raise 21bb
BBetf*** Fold
HJWadada Fold
BTNokayama Fold
Result
sushiro wins 17bb""",

        # Hand 3
        """Hand #3B2U3NZb9stPvbSzJSaD

2026/02/08 22:06 · 6-Max NLH (0.5/1)
SB
LqX***
(100bb)
6♠
5♥
-0.5bb
BB
RiGi
(100bb)
Q♦
9♣
+5.2bb
UTG
godan
(100bb)
J♦
T♠
±0bb
HJ
Jg2***
(100bb)
J♥
8♥
±0bb
CO
okayama
(100bb)
A♣
2♦
-5.25bb
BTN
S
(100bb)
Q♥
4♠
±0bb
Preflop
UTGgodan Fold
HJJg2*** Fold
COokayama Raise 2.5bb
BTNS Fold
SBLqX*** Fold
BBRiGi Call 2.5bb
Flop
9♥
8♠
2♣
BBRiGi Check
COokayama Check
Turn
K♦
BBRiGi Check
COokayama Bet 2.75bb
BBRiGi Call 2.75bb
River
4♣
BBRiGi Check
COokayama Check
Result
RiGi wins 10.45bb
Rake: 0.55bb""",

        # Hand 4
        """Hand #h4DAgxUWCjXBEcNG6AXq

2026/02/08 22:05 · 6-Max NLH (0.5/1)
HJ
mh
(100bb)
9♠
7♥
±0bb
CO
tatanmiya
(100bb)
K♣
8♠
±0bb
BTN
tPP***
(100bb)
9♦
7♠
±0bb
SB
okayama
(100bb)
K♦
6♣
-3.75bb
BB
kelipord
(100bb)
A♣
3♦
+3.37bb
UTG
karimero
(100bb)
7♦
4♥
±0bb
Preflop
UTGkarimero Fold
HJmh Fold
COtatanmiya Fold
BTNtPP*** Fold
SBokayama Raise 2.5bb
BBkelipord Call 2.5bb
Flop
Q♠
Q♦
8♥
SBokayama Check
BBkelipord Check
Turn
6♠
SBokayama Check
BBkelipord Check
River
A♠
SBokayama Check
BBkelipord Bet 1.25bb
SBokayama Call 1.25bb
Result
kelipord wins 7.12bb
Rake: 0.38bb""",

        # Hand 5
        """Hand #i4BttriqnrNsV6PymfdY

2026/02/08 22:04 · 6-Max NLH (0.5/1)
BTN
Rn2***
(100bb)
T♠
T♣
-44.41bb
SB
WAI
(100bb)
9♣
3♦
-0.5bb
BB
okayama
(100bb)
4♣
3♠
+40.91bb
UTG
TOTO
(100bb)
T♦
8♠
±0bb
HJ
Y0l***
(100bb)
Q♥
J♦
±0bb
CO
Ububu
(100bb)
4♥
3♥
±0bb
Preflop
UTGTOTO Fold
HJY0l*** Fold
COUbubu Fold
BTNRn2*** Raise 2.3bb
SBWAI Fold
BBokayama Call 2.3bb
Flop
6♣
5♥
2♥
BBokayama Check
BTNRn2*** Bet 3.83bb
BBokayama Call 3.83bb
Turn
Q♠
BBokayama Check
BTNRn2*** Bet 6.38bb
BBokayama Call 6.38bb
River
9♦
BBokayama Bet 31.9bb
BTNRn2*** Call 31.9bb
Result
okayama wins 85.32bb
Rake: 4bb"""
]


def main():
    """メイン実行関数"""
    
    # パーサーを初期化
    parser = TenFourHandParser()
    
    # 各ハンドをパース
    parsed_hands = []
    for i, hand_text in enumerate(hands_raw, 1):
        try:
            parsed_hand = parser.parse_hand_history(hand_text)
            parsed_hands.append(parsed_hand)
            print(f"✓ ハンド {i} をパースしました: {parsed_hand['hand_id']}")
        except Exception as e:
            print(f"✗ ハンド {i} のパースに失敗: {e}")
    
    # GTO分析を実行
    if parsed_hands:
        print(f"\n{'='*70}")
        print(f"📊 {len(parsed_hands)} ハンドのGTO分析を開始...")
        print(f"{'='*70}\n")
        
        agent = PokerGTOAgent()
        hand_ids = [hand['hand_id'] for hand in parsed_hands]
        
        # レポートを生成
        report = agent.analyze_hands(hand_ids, parsed_hands)
        
        print("\n" + "="*70)
        print("📄 分析レポート")
        print("="*70 + "\n")
        print(report)
    else:
        print("\n✗ パース可能なハンドがありませんでした")


if __name__ == '__main__':
    main()
