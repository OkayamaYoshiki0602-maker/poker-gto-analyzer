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
Rake: 4bb""",

        # Hand 6
        """Hand #PulWv0ae0PqbAuGIoM5d

2026/02/09 09:10 · 6-Max NLH (0.5/1)
BB
okayama
(100bb)
6♠
2♠
-4.33bb
UTG
fGe***
(100bb)
Q♥
3♦
±0bb
HJ
tatataaa
(100bb)
Q♣
J♠
+4.37bb
CO
Rfp***
(100bb)
A♦
5♣
±0bb
BTN
Chappy
(100bb)
Q♠
5♦
±0bb
SB
KJ
(100bb)
9♠
5♠
-0.5bb
Preflop
UTGfGe*** Fold
HJtatataaa Raise 2.5bb
CORfp*** Fold
BTNChappy Fold
SBKJ Fold
BBokayama Call 2.5bb
Flop
K♥
6♦
3♣
BBokayama Check
HJtatataaa Bet 1.83bb
BBokayama Call 1.83bb
Turn
7♠
BBokayama Check
HJtatataaa Check
River
Q♦
BBokayama Fold
Result
tatataaa wins 8.7bb
Rake: 0.46bb""",

        # Hand 7
        """Hand #YRmPovMwgcsNTzrICnJM

2026/02/09 09:08 · 6-Max NLH (0.5/1)
SB
tarosushi
(100bb)
Q♥
6♥
-0.5bb
BB
pmpm920
(100bb)
Q♣
6♦
-1bb
UTG
2vP***
(100bb)
4♠
2♠
±0bb
HJ
okayama
(100bb)
A♥
J♠
-5.75bb
CO
Belami
(100bb)
K♥
7♥
+6.6bb
BTN
MtH***
(100bb)
A♣
7♣
±0bb
Preflop
UTG2vP*** Fold
HJokayama Raise 2.5bb
COBelami Call 2.5bb
BTNMtH*** Fold
SBtarosushi Fold
BBpmpm920 Fold
Flop
Q♦
T♠
5♥
HJokayama Check
COBelami Bet 3.25bb
HJokayama Call 3.25bb
Turn
7♦
HJokayama Check
COBelami Bet 6.5bb
HJokayama Fold
Result
Belami wins 12.35bb
Rake: 0.65bb""",

        # Hand 8
        """Hand #45fF2HtNDuiSmirnLzPh

2026/02/09 09:09 · 6-Max NLH (0.5/1)
CO
YTa***
(100bb)
J♠
T♠
-2.5bb
BTN
okayama
(100bb)
A♦
J♥
+4bb
SB
akaao
(100bb)
A♠
7♣
-0.5bb
BB
WALTER
(100bb)
K♠
5♠
-1bb
UTG
maikii
(100bb)
T♥
T♦
±0bb
HJ
R
(100bb)
3♣
2♥
±0bb
Preflop
UTGmaikii Fold
HJR Fold
COYTa*** Raise 2.5bb
BTNokayama Raise 10bb
SBakaao Fold
BBWALTER Fold
COYTa*** Fold
Result
okayama wins 6.5bb""",

        # Hand 9
        """Hand #lz6diHAxhCaTYjtInttt

2026/02/09 09:06 · 6-Max NLH (0.5/1)
BTN
Cindy
(100bb)
9♦
9♣
-2.5bb
SB
AREI
(100bb)
A♠
Q♥
-0.5bb
BB
0mF***
(100bb)
J♦
6♣
-1bb
UTG
uUs***
(100bb)
8♥
3♣
±0bb
HJ
pmpm920
(100bb)
6♦
2♥
±0bb
CO
okayama
(100bb)
A♦
K♣
+3.67bb
Preflop
UTGuUs*** Fold
HJpmpm920 Fold
COokayama Raise 2.5bb
BTNCindy Call 2.5bb
SBAREI Fold
BB0mF*** Fold
Flop
J♣
T♠
5♦
COokayama Check
BTNCindy Check
Turn
J♠
COokayama Check
BTNCindy Check
River
K♠
COokayama Check
BTNCindy Check
Result
okayama wins 6.17bb
Rake: 0.33bb""",

        # Hand 10
        """Hand #1K0584LNoJIKlPE47n1p

2026/02/09 10:23 · 6-Max NLH (0.5/1)
UTG
maty
(100bb)
J♠
J♦
+37.5bb
HJ
saba
(100bb)
7♦
6♠
±0bb
CO
78k***
(100bb)
9♣
4♦
±0bb
BTN
seki
(100bb)
Q♠
7♥
±0bb
SB
OGW
(100bb)
J♥
9♠
-0.5bb
BB
okayama
(100bb)
A♣
K♠
-41bb
Preflop
UTGmaty Raise 2bb
HJsaba Fold
CO78k*** Fold
BTNseki Fold
SBOGW Fold
BBokayama Raise 8bb
UTGmaty Call 8bb
Flop
J♣
5♦
3♦
BBokayama Bet 8.25bb
UTGmaty Call 8.25bb
Turn
5♠
BBokayama Bet 24.75bb
UTGmaty Call 24.75bb
River
9♦
BBokayama Check
UTGmaty Bet 59bb
BBokayama Fold
Result
maty wins 78.5bb
Rake: 4bb""",

        # Hand 11
        """Hand #aMla8UsUzbFrH4pCS2UX

2026/02/09 12:44 · 6-Max NLH (0.5/1)
CO
Vanilla
(100bb)
T♠
9♦
±0bb
BTN
CUU***
(100bb)
J♠
4♦
±0bb
SB
39Niki
(100bb)
K♣
T♦
+4.5bb
BB
okayama
(100bb)
J♦
3♦
-5bb
UTG
Levi
(100bb)
7♥
2♣
±0bb
HJ
qdQ***
(100bb)
4♠
3♥
±0bb
Preflop
UTGLevi Fold
HJqdQ*** Fold
COVanilla Fold
BTNCUU*** Fold
SB39Niki Raise 3bb
BBokayama Call 3bb
Flop
K♦
2♥
2♦
SB39Niki Bet 2bb
BBokayama Call 2bb
Turn
9♥
SB39Niki Bet 10bb
BBokayama Fold
Result
39Niki wins 9.5bb
Rake: 0.5bb""",

        # Hand 12
        """Hand #7eAHAowiFG7HugAzLvb7

2026/02/09 12:44 · 6-Max NLH (0.5/1)
BB
momokuro
(100bb)
T♣
3♠
-1bb
UTG
39Niki
(100bb)
A♥
Q♦
-31.55bb
HJ
Chunichi
(100bb)
Q♠
7♥
±0bb
CO
okayama
(100bb)
A♦
K♣
+29.82bb
BTN
Daichi
(100bb)
6♠
3♣
±0bb
SB
Himadajin
(100bb)
K♠
7♠
-0.5bb
Preflop
UTG39Niki Raise 2bb
HJChunichi Fold
COokayama Raise 7bb
BTNDaichi Fold
SBHimadajin Fold
BBmomokuro Fold
UTG39Niki Call 7bb
Flop
K♥
Q♣
J♠
UTG39Niki Check
COokayama Bet 5.17bb
UTG39Niki Call 5.17bb
Turn
4♠
UTG39Niki Check
COokayama Check
River
4♦
UTG39Niki Check
COokayama Bet 19.38bb
UTG39Niki Call 19.38bb
Result
okayama wins 61.37bb
Rake: 3.23bb""",

        # Hand 13
        """Hand #qN8mgWMS8CVFQqyogWin

2026/02/09 16:53 · 6-Max NLH (0.5/1)
CO
Nahte138
(100bb)
7♣
4♦
±0bb
BTN
okayama
(100bb)
K♥
T♥
-25.09bb
SB
XhZ***
(100bb)
A♠
8♠
-0.5bb
BB
akane
(100bb)
9♦
3♣
-1bb
UTG
kuwazari
(100bb)
9♥
2♣
±0bb
HJ
X
(100bb)
A♦
A♣
+24.01bb
Preflop
UTGkuwazari Fold
HJX Raise 2bb
CONahte138 Fold
BTNokayama Raise 7bb
SBXhZ*** Fold
BBakane Fold
HJX Call 7bb
Flop
K♦
J♣
9♠
HJX Check
BTNokayama Bet 5.17bb
HJX Call 5.17bb
Turn
3♥
HJX Check
BTNokayama Bet 12.92bb
HJX Call 12.92bb
River
J♥
HJX Check
BTNokayama Check
Result
X wins 49.1bb
Rake: 2.58bb""",

        # Hand 14
        """Hand #zEceAOqarkokWmNpdlSN

2026/02/09 23:02 · 6-Max NLH (0.5/1)
UTG
Enos
(100bb)
K♣
9♠
±0bb
HJ
BONEFISH
(100bb)
A♣
6♥
±0bb
CO
1mK***
(100bb)
A♠
5♠
-2.5bb
BTN
hirokawa
(100bb)
J♣
T♣
-18.51bb
SB
Pei
(100bb)
J♦
3♦
-0.5bb
BB
okayama
(100bb)
5♦
4♦
+19.51bb
Preflop
UTGEnos Fold
HJBONEFISH Fold
CO1mK*** Raise 2.5bb
BTNhirokawa Call 2.5bb
SBPei Fold
BBokayama Call 2.5bb
Flop
9♥
9♣
4♣
BBokayama Check
CO1mK*** Check
BTNhirokawa Bet 2.67bb
BBokayama Call 2.67bb
CO1mK*** Fold
Turn
4♠
BBokayama Check
BTNhirokawa Check
River
7♣
BBokayama Bet 13.34bb
BTNhirokawa Call 13.34bb
Result
okayama wins 38.02bb
Rake: 2bb""",

        # Hand 15
        """Hand #btzGlwsMVwy76EIbaJRg

2026/02/09 22:59 · 6-Max NLH (0.5/1)
CO
8ae***
(100bb)
A♦
7♠
±0bb
BTN
Y90***
(100bb)
8♠
8♦
+10.51bb
SB
snorlax
(100bb)
7♥
3♦
-0.5bb
BB
Casai
(100bb)
Q♦
6♥
-1bb
UTG
okayama
(100bb)
5♥
5♦
-10.09bb
HJ
nana
(100bb)
7♣
3♣
±0bb
Preflop
UTGokayama Raise 2.5bb
HJnana Fold
CO8ae*** Fold
BTNY90*** Call 2.5bb
SBsnorlax Fold
BBCasai Fold
Flop
T♥
6♣
4♣
UTGokayama Bet 2.17bb
BTNY90*** Call 2.17bb
Turn
3♠
UTGokayama Bet 5.42bb
BTNY90*** Call 5.42bb
River
4♥
UTGokayama Check
BTNY90*** Check
Result
Y90*** wins 20.6bb
Rake: 1.08bb""",

        # Hand 16
        """Hand #vCs5qRH6AFH3MHf3RwGA

2026/02/09 22:58 · 6-Max NLH (0.5/1)
HJ
aJj***
(100bb)
A♠
3♠
-2bb
CO
kCk***
(100bb)
K♥
K♦
+34.5bb
BTN
yoshimy
(100bb)
T♥
2♣
±0bb
SB
1mK***
(100bb)
J♠
T♦
-0.5bb
BB
okayama
(100bb)
A♣
9♣
-30bb
UTG
gjG***
(100bb)
7♥
7♦
-2bb
Preflop
UTGgjG*** Raise 2bb
HJaJj*** Call 2bb
COkCk*** Raise 10bb
BTNyoshimy Fold
SB1mK*** Fold
BBokayama Raise 30bb
UTGgjG*** Fold
HJaJj*** Fold
COkCk*** Raise 100bb
BBokayama Fold
Result
kCk*** wins 64.5bb""",

        # Hand 17
        """Hand #UnB9iyDFN3baAMxatkUK

2026/02/09 22:57 · 6-Max NLH (0.5/1)
SB
WtU
(100bb)
K♠
6♥
-0.5bb
BB
Toman
(100bb)
3♥
3♣
+28.91bb
UTG
AgMadagas
(100bb)
8♠
2♦
±0bb
HJ
Ke
(100bb)
T♣
2♥
±0bb
CO
okayama
(100bb)
Q♥
9♥
-31.6bb
BTN
hirocho
(100bb)
J♠
4♦
±0bb
Preflop
UTGAgMadagas Fold
HJKe Fold
COokayama Raise 2.3bb
BTNhirocho Fold
SBWtU Fold
BBToman Call 2.3bb
Flop
J♥
5♣
2♣
BBToman Check
COokayama Bet 1.7bb
BBToman Call 1.7bb
Turn
4♥
BBToman Check
COokayama Bet 2.83bb
BBToman Raise 8.49bb
COokayama Call 8.49bb
River
7♠
BBToman Check
COokayama Bet 19.11bb
BBToman Call 19.11bb
Result
Toman wins 60.51bb
Rake: 3.19bb""",

        # Hand 18
        """Hand #8PwhBm7mvyaOOSiyBXRw

2026/02/09 22:54 · 6-Max NLH (0.5/1)
SB
okayama
(100bb)
8♦
8♣
-8.75bb
BB
kuwatake
(100bb)
Q♠
6♣
-1bb
UTG
Tomstory2
(100bb)
J♣
9♥
±0bb
HJ
xxxpoker
(100bb)
A♣
6♥
±0bb
CO
yoshimy
(100bb)
Q♥
2♦
±0bb
BTN
mfF***
(100bb)
J♦
9♠
+8.82bb
Preflop
UTGTomstory2 Fold
HJxxxpoker Fold
COyoshimy Fold
BTNmfF*** Raise 2.5bb
SBokayama Raise 8.75bb
BBkuwatake Fold
BTNmfF*** Call 8.75bb
Flop
J♠
3♠
3♥
SBokayama Check
BTNmfF*** Bet 6.17bb
SBokayama Fold
Result
mfF*** wins 17.57bb
Rake: 0.93bb""",

        # Hand 19
        """Hand #QKDf0Xt6wQkZgalXtQoC

2026/02/09 22:53 · 6-Max NLH (0.5/1)
BB
XmA***
(100bb)
A♥
J♥
+98.5bb
UTG
Koy0JRN
(100bb)
9♥
4♥
±0bb
HJ
Yossiah
(100bb)
K♠
9♠
±0bb
CO
Rj7***
(100bb)
7♥
3♦
±0bb
BTN
Azumaya
(100bb)
K♥
Q♠
-2.5bb
SB
okayama
(100bb)
A♠
K♦
-100bb
Preflop
UTGKoy0JRN Fold
HJYossiah Fold
CORj7*** Fold
BTNAzumaya Raise 2.5bb
SBokayama Raise 7.5bb
BBXmA*** Raise 22.5bb
BTNAzumaya Fold
SBokayama Call 22.5bb
Flop
A♣
5♥
2♥
SBokayama Bet 15.83bb
BBXmA*** Raise 39.58bb
SBokayama Raise 77.5bb
BBXmA*** Call 77.5bb
Turn
4♣
-
River
J♣
-
Result
XmA*** wins 198.5bb
Rake: 4bb
All-in EV
XmA***: -7.06bb
okayama: +5.56bb""",

        # Hand 20
        """Hand #0LnVywBiaFl65ah9OTvf

2026/02/09 22:52 · 6-Max NLH (0.5/1)
SB
take
(100bb)
K♦
7♠
-0.5bb
BB
5HL***
(100bb)
J♥
6♠
-1bb
UTG
SK
(100bb)
A♠
7♣
±0bb
HJ
watergod
(100bb)
T♠
T♥
+40.75bb
CO
Pei
(100bb)
9♥
5♥
±0bb
BTN
okayama
(100bb)
3♠
3♥
-43.25bb
Preflop
UTGSK Fold
HJwatergod Raise 2.3bb
COPei Fold
BTNokayama Raise 8.05bb
SBtake Fold
BB5HL*** Fold
HJwatergod Call 8.05bb
Flop
A♥
J♣
T♦
HJwatergod Check
BTNokayama Bet 8.8bb
HJwatergod Call 8.8bb
Turn
J♦
HJwatergod Check
BTNokayama Bet 26.4bb
HJwatergod Call 26.4bb
River
8♦
HJwatergod Bet 56.75bb
BTNokayama Fold
Result
watergod wins 84bb
Rake: 4bb""",

        # Hand 21
        """Hand #hd8Yfot6t7S9ZMLsQRD4

2026/02/09 22:50 · 6-Max NLH (0.5/1)
BB
39Niki
(100bb)
7♦
4♣
-1bb
UTG
okayama
(100bb)
A♠
A♣
+105.55bb
HJ
itigo
(100bb)
A♥
Q♥
-8.05bb
CO
RYUCA
(100bb)
T♥
9♦
±0bb
BTN
Bell
(100bb)
Q♦
Q♣
-100bb
SB
GGLemon
(100bb)
K♠
2♣
-0.5bb
Preflop
UTGokayama Raise 2.3bb
HJitigo Raise 8.05bb
CORYUCA Fold
BTNBell Raise 24.15bb
SBGGLemon Fold
BB39Niki Fold
UTGokayama Raise 60.38bb
HJitigo Fold
BTNBell Raise 100bb
UTGokayama Call 100bb
Flop
K♦
7♠
3♦
-
Turn
T♠
-
River
4♥
-
Result
okayama wins 205.55bb
Rake: 4bb
All-in EV
okayama: +67.66bb
Bell: -62.11bb""",

        # Hand 22
        """Hand #hCm8SItGDptlGuGgh6kU

2026/02/09 22:49 · 6-Max NLH (0.5/1)
BTN
4iF***
(100bb)
6♠
3♦
±0bb
SB
okayama
(100bb)
A♦
J♦
-13.75bb
BB
JK
(100bb)
A♥
T♦
-1bb
UTG
Sirube596
(100bb)
Q♥
7♦
±0bb
HJ
kaguraVT
(100bb)
5♥
5♦
+13.32bb
CO
appusuta
(100bb)
Q♣
4♠
±0bb
Preflop
UTGSirube596 Fold
HJkaguraVT Raise 2.3bb
COappusuta Fold
BTN4iF*** Fold
SBokayama Raise 8.05bb
BBJK Fold
HJkaguraVT Call 8.05bb
Flop
9♥
7♥
5♣
SBokayama Bet 5.7bb
HJkaguraVT Raise 17.1bb
SBokayama Fold
Result
kaguraVT wins 27.07bb
Rake: 1.43bb"""
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
