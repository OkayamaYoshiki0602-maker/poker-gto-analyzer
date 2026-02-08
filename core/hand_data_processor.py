#!/usr/bin/env python3
"""
ハンドデータ処理モジュール
ユーザー提供のハンドデータを標準化し、GTO分析用に変換
"""

import json
import re
from typing import Dict, List, Optional, Any


class HandDataProcessor:
    """ハンドデータの処理と標準化"""
    
    # SPR分類
    SPR_CATEGORIES = {
        'short': (0, 30),
        'medium': (30, 50),
        'deep': (50, 100),
        'super_deep': (100, float('inf'))
    }
    
    # 対戦相手タイプ
    OPPONENT_TYPES = ['TAG', 'LAG', 'FISH', 'NIT', 'MANIAC', 'UNKNOWN']
    
    # ポジション順序
    POSITIONS = ['UTG', 'UTG+1', 'MP', 'MP+1', 'HJ', 'CO', 'BTN', 'SB', 'BB']
    
    @staticmethod
    def process_hand_data(hand_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        ユーザー入力のハンドデータを標準化
        
        Args:
            hand_input: ユーザー提供のハンドデータ
            
        Returns:
            標準化されたハンドデータ
        """
        
        # 必須フィールドの確認
        required_fields = ['hand_id', 'hero_position', 'hero_hand', 'hero_action']
        for field in required_fields:
            if field not in hand_input:
                raise ValueError(f"必須フィールド '{field}' が不足しています")
        
        # 標準化されたデータ構造
        processed_data = {
            'hand_id': hand_input['hand_id'],
            'hero': {
                'position': HandDataProcessor._normalize_position(hand_input['hero_position']),
                'hand': HandDataProcessor._normalize_hand(hand_input['hero_hand']),
                'action': HandDataProcessor._normalize_action(hand_input['hero_action']),
                'profit_bb': float(hand_input.get('hero_profit_bb', 0)),
                'result': hand_input.get('result', 'UNKNOWN').upper(),
                'stack_bb': float(hand_input.get('stack_size_bb', 100))
            },
            'opponents': HandDataProcessor._process_opponents(hand_input.get('opponent_types', {})),
            'board': HandDataProcessor._normalize_board(hand_input.get('board', [])),
            'spr': HandDataProcessor._calculate_spr(hand_input),
            'spr_category': HandDataProcessor._categorize_spr(hand_input),
            'board_texture': HandDataProcessor._analyze_board_texture(hand_input.get('board', [])),
            'actions': hand_input.get('actions', {}),
            'metadata': {
                'date': hand_input.get('date', ''),
                'game_type': hand_input.get('game_type', '6-Max NLH'),
                'pot_size_bb': float(hand_input.get('pot_size_bb', 0)),
                'rake_bb': float(hand_input.get('rake_bb', 0))
            }
        }
        
        return processed_data
    
    @staticmethod
    def _normalize_position(position: str) -> str:
        """ポジションを標準化"""
        position = position.upper().strip()
        
        # エイリアス処理
        aliases = {
            'UNDER_THE_GUN': 'UTG',
            'HIJACK': 'HJ',
            'CUTOFF': 'CO',
            'BUTTON': 'BTN',
            'SMALL_BLIND': 'SB',
            'BIG_BLIND': 'BB',
            'MIDDLE_POSITION': 'MP'
        }
        
        return aliases.get(position, position)
    
    @staticmethod
    def _normalize_hand(hand: str) -> str:
        """ハンドを標準化（例: "QQ", "AKs", "72o"）"""
        hand = hand.upper().strip()
        
        # スーツ記号を標準化
        hand = hand.replace('♠', 's').replace('♥', 'h').replace('♦', 'd').replace('♣', 'c')
        
        # ペアの場合
        if len(hand) == 2 and hand[0] == hand[1]:
            return hand
        
        # スーテッド/オフスーツの場合
        if len(hand) >= 3:
            if 's' in hand.lower() or 'h' in hand.lower() or 'd' in hand.lower() or 'c' in hand.lower():
                # スーテッド
                cards = re.findall(r'[AKQJT2-9]', hand)
                if len(cards) >= 2:
                    return f"{cards[0]}{cards[1]}s"
            else:
                # オフスーツ
                cards = re.findall(r'[AKQJT2-9]', hand)
                if len(cards) >= 2:
                    return f"{cards[0]}{cards[1]}o"
        
        return hand
    
    @staticmethod
    def _normalize_action(action: str) -> str:
        """アクションを標準化"""
        action = action.lower().strip()
        
        action_map = {
            'raise': 'raise',
            'bet': 'bet',
            'call': 'call',
            'fold': 'fold',
            'check': 'check',
            'all-in': 'all_in',
            'allin': 'all_in'
        }
        
        return action_map.get(action, action)
    
    @staticmethod
    def _process_opponents(opponent_types: Dict[str, str]) -> List[Dict[str, Any]]:
        """対戦相手情報を処理"""
        opponents = []
        
        for position, opp_type in opponent_types.items():
            opponents.append({
                'position': HandDataProcessor._normalize_position(position),
                'type': opp_type.upper() if opp_type.upper() in HandDataProcessor.OPPONENT_TYPES else 'UNKNOWN',
                'active': True
            })
        
        return opponents
    
    @staticmethod
    def _normalize_board(board: List[str]) -> List[str]:
        """ボードを標準化"""
        if isinstance(board, str):
            # "Js6h3dKs7d" のような文字列を分割
            cards = []
            i = 0
            while i < len(board):
                if i + 1 < len(board):
                    card = board[i:i+2]
                    cards.append(card)
                    i += 2
                else:
                    i += 1
            return cards
        
        return [card.replace('♠', 's').replace('♥', 'h').replace('♦', 'd').replace('♣', 'c') 
                for card in board]
    
    @staticmethod
    def _calculate_spr(hand_input: Dict[str, Any]) -> float:
        """SPR（Stack-to-Pot Ratio）を計算"""
        stack_bb = float(hand_input.get('stack_size_bb', 100))
        pot_bb = float(hand_input.get('pot_size_bb', 5))  # デフォルト5bb
        
        if 'spr' in hand_input:
            return float(hand_input['spr'])
        
        return stack_bb / pot_bb if pot_bb > 0 else stack_bb / 5
    
    @staticmethod
    def _categorize_spr(hand_input: Dict[str, Any]) -> str:
        """SPRをカテゴリ分類"""
        spr = HandDataProcessor._calculate_spr(hand_input)
        
        for category, (min_spr, max_spr) in HandDataProcessor.SPR_CATEGORIES.items():
            if min_spr <= spr < max_spr:
                return category
        
        return 'unknown'
    
    @staticmethod
    def _analyze_board_texture(board: List[str]) -> Dict[str, Any]:
        """ボードテクスチャを分析"""
        if not board:
            return {'type': 'preflop', 'description': 'プリフロップ'}
        
        # スーツ分析
        suits = {}
        ranks = {}
        
        for card in board:
            if len(card) >= 2:
                rank = card[0]
                suit = card[1] if len(card) > 1 else ''
                
                ranks[rank] = ranks.get(rank, 0) + 1
                suits[suit] = suits.get(suit, 0) + 1
        
        # フラッシュドロー判定
        max_suit_count = max(suits.values()) if suits else 0
        flush_draw = max_suit_count >= 3
        
        # ストレートドロー判定（簡易版）
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                      '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        
        board_ranks = sorted([rank_values.get(rank, 0) for rank in ranks.keys()])
        straight_draw = False
        
        if len(board_ranks) >= 3:
            # 連続性チェック（簡易版）
            gaps = [board_ranks[i+1] - board_ranks[i] for i in range(len(board_ranks)-1)]
            straight_draw = any(gap <= 2 for gap in gaps)
        
        # テクスチャ分類
        if flush_draw and straight_draw:
            texture_type = 'WET'
            description = 'ウェットボード（フラッシュ・ストレートドロー）'
        elif flush_draw:
            texture_type = 'SEMI_WET'
            description = 'セミウェットボード（フラッシュドロー）'
        elif straight_draw:
            texture_type = 'SEMI_WET'
            description = 'セミウェットボード（ストレートドロー）'
        else:
            texture_type = 'DRY'
            description = 'ドライボード（ドロー少ない）'
        
        return {
            'type': texture_type,
            'description': description,
            'flush_draw': flush_draw,
            'straight_draw': straight_draw,
            'suits': suits,
            'ranks': ranks
        }
    
    @staticmethod
    def create_sample_data(hand_id: str) -> Dict[str, Any]:
        """サンプルデータを作成（テスト用）"""
        return {
            'hand_id': hand_id,
            'hero_position': 'UTG',
            'hero_hand': 'QQ',
            'hero_action': 'raise',
            'hero_profit_bb': 4.37,
            'result': 'WIN',
            'stack_size_bb': 100,
            'opponent_types': {'BB': 'TAG'},
            'board': ['Js', '6h', '3d', 'Ks', '7d'],
            'spr': 25,
            'pot_size_bb': 8.7,
            'rake_bb': 0.46
        }


def main():
    """テスト実行"""
    processor = HandDataProcessor()
    
    # サンプルデータでテスト
    sample_input = processor.create_sample_data('LTsCqZnvNbskQfoenRQB')
    processed = processor.process_hand_data(sample_input)
    
    print("📊 処理結果:")
    print(json.dumps(processed, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()