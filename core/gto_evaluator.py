#!/usr/bin/env python3
"""
GTO 評価エンジン
ハンドの決定を GTO 基準と比較し、評価・アドバイスを生成
"""

class GTOEvaluator:
    """GTO 戦略ベースの評価エンジン"""
    
    # GTO 基準データ（簡略版）
    GTO_PREFLOP_RANGES = {
        'UTG': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', 'AK', 'AQ', 'AJ', 'KQ'],
            'fold': ['72o', '73o', '82o', '83o', '92o', '93o', '82s'],
        },
        'MP': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AK', 'AQ', 'KQ', 'AJ'],
            'fold': ['72o', '73o', '82o'],
        },
        'CO': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AK', 'AQ', 'KQ', 'AJ', 'KJ'],
            'fold': ['72o'],
        },
        'BTN': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AK', 'AQ', 'KQ', 'AJ', 'KJ', 'QJ'],
            'fold': [],
        },
        'SB': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', 'AK', 'AQ', 'KQ'],
            'fold': ['72o', '73o'],
        },
        'BB': {
            'raise': [],  # BB は基本的に守備的
            'call': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AK', 'AQ'],
        },
    }
    
    @staticmethod
    def evaluate_action(position: str, hand: str, action: str, result: dict) -> dict:
        """
        プレイヤーのアクションを GTO 基準と比較
        
        Args:
            position: ポジション (UTG, MP, CO, BTN, SB, BB)
            hand: ハンド（例: 'AK', '77', '92o'）
            action: アクション (raise, call, fold)
            result: 結果 (WIN, LOSE, FOLD)
        
        Returns:
            評価情報
        """
        
        ranges = GTOEvaluator.GTO_PREFLOP_RANGES.get(position, {})
        
        # GTO 基準と比較
        is_in_raise_range = hand in ranges.get('raise', [])
        is_in_fold_range = hand in ranges.get('fold', [])
        
        # 評価ロジック
        if action == 'raise':
            if is_in_raise_range:
                evaluation = 'GTO通り ✅'
                explanation = f'{position} からの {hand} raise は GTO 基準に合致しています'
                gto_alignment = 'correct'
            else:
                evaluation = '非GTO ⚠️'
                explanation = f'{position} からの {hand} raise は GTO 基準から外れています'
                gto_alignment = 'incorrect'
        
        elif action == 'fold':
            if is_in_fold_range:
                evaluation = 'GTO通り ✅'
                explanation = f'{position} からの {hand} fold は GTO 基準に合致しています'
                gto_alignment = 'correct'
            else:
                evaluation = '議論の余地あり'
                explanation = f'{position} からの {hand} fold は GTO より広いレンジの一部かもしれません'
                gto_alignment = 'acceptable'
        
        else:
            evaluation = '評価対象外'
            explanation = ''
            gto_alignment = 'unknown'
        
        # 結果の文脈
        result_text = result.get('profit_bb', 0)
        win_lose = result.get('result', 'UNKNOWN')
        
        # 本質的なアドバイス
        advice = GTOEvaluator._generate_advice(
            gto_alignment, win_lose, result_text, position, hand
        )
        
        return {
            'evaluation': evaluation,
            'gto_alignment': gto_alignment,
            'explanation': explanation,
            'advice': advice,
            'win_lose': win_lose,
            'profit': result_text,
        }
    
    @staticmethod
    def _generate_advice(alignment: str, result: str, profit: float, position: str, hand: str) -> str:
        """本質的なアドバイスを生成"""
        
        advice_text = []
        
        # GTO 整合性に基づくアドバイス
        if alignment == 'correct':
            advice_text.append("✅ **判断は正しいです**")
            
            if result == 'LOSE':
                advice_text.append(
                    f"負けていますが、{hand} を {position} から raise するのは GTO 戦略の標準的な判断です。"
                )
                advice_text.append(
                    "短期的な結果に左右されず、長期的には正しい判断を繰り返すことが重要です。"
                )
            elif result == 'WIN':
                advice_text.append("また、勝ったのは判断が正しかったからです。")
                advice_text.append("このスタイルを継続してください。")
        
        elif alignment == 'incorrect':
            advice_text.append("⚠️  **判断を見直してください**")
            advice_text.append(
                f"{hand} は {position} からの raise レンジに含まれていません。"
            )
            advice_text.append(
                "より強いハンドで raise し、弱いハンドは fold するようにしてください。"
            )
        
        # 利益ベースのアドバイス
        if profit < -20:
            advice_text.append(f"\n💰 大きな損失 ({profit:.1f}bb) が発生しています。")
            advice_text.append(
                "ポスト・フロップの play が甘い可能性があります。"
            )
        
        return "\n".join(advice_text)
    
    @staticmethod
    def get_gto_frequency(position: str, hand: str) -> dict:
        """位置とハンドのGTO周波数を取得"""
        
        ranges = GTOEvaluator.GTO_PREFLOP_RANGES.get(position, {})
        raise_hands = len(ranges.get('raise', []))
        total_hands = 1326  # ポーカーの総ハンド数
        
        if hand in ranges.get('raise', []):
            frequency = raise_hands / total_hands * 100
            return {
                'frequency': f'{frequency:.1f}%',
                'action': 'raise',
                'description': 'GTO 基準では raise することが推奨されます'
            }
        else:
            return {
                'frequency': f'{(100-frequency):.1f}%',
                'action': 'fold',
                'description': 'GTO 基準では fold することが推奨されます'
            }
