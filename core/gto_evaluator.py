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
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'KQs', 'KQo'],
            'fold': ['72o', '73o', '82o', '83o', '92o', '93o', '82s', 'J2o', 'J3o', 'Q2o', 'Q3o', 'K2o', 'K3o', 'K4o', 'K5o', 'K6o', 'A2o', 'A3o', 'A4o', 'A5o', 'A6o', 'A7o'],
        },
        'MP': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'KQs', 'KQo', 'ATs'],
            'fold': ['72o', '73o', '82o', '83o', 'J2o', 'Q2o', 'K2o', 'K3o', 'K4o', 'K5o', 'K6o', 'A2o', 'A3o', 'A4o'],
        },
        'CO': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'ATs', 'ATo', 'KQs', 'KQo', 'KJs', 'KJo', 'QJs'],
            'fold': ['72o', '73o', '82o', 'J2o', 'Q2o', 'K2o', 'K3o', 'K4o', 'K5o', 'K6o', 'A2o', 'A3o'],
        },
        'BTN': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'ATs', 'ATo', 'A9s', 'KQs', 'KQo', 'KJs', 'KJo', 'KTs', 'QJs', 'QJo', 'QTs', 'JTs'],
            'fold': ['72o', '82o', '92o'],
        },
        'SB': {
            'raise': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'ATs', 'KQs', 'KQo', 'KJs'],
            'fold': ['72o', '73o', '82o', '83o', 'J2o', 'Q2o', 'K2o', 'K3o', 'K4o', 'K5o', 'K6o', 'A2o', 'A3o'],
        },
        'BB': {
            'raise': [],  # BB は基本的に守備的
            'call': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22', 'AKs', 'AKo', 'AQs', 'AQo', 'AJs', 'AJo', 'ATs', 'ATo', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'KQs', 'KQo', 'KJs', 'KJo', 'KTs', 'K9s', 'QJs', 'QJo', 'QTs', 'JTs', 'J9s', 'T9s', '98s', '87s', '76s', '65s', '54s', '43s'],
            'fold': ['72o', '73o', '82o', '83o', '84o', '92o', '93o', '94o', 'T2o', 'T3o', 'J2o', 'J3o', 'Q2o', 'Q3o', 'K2o', 'K3o', 'A2o'],
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
        
        # BBのcallレンジを確認
        is_in_call_range = hand in ranges.get('call', [])
        
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
        
        elif action == 'call':
            if is_in_call_range or is_in_raise_range:
                evaluation = 'GTO通り ✅'
                explanation = f'{position} からの {hand} call は GTO 基準に合致しています'
                gto_alignment = 'correct'
            elif is_in_fold_range:
                evaluation = '非GTO ⚠️'
                explanation = f'{position} からの {hand} は fold すべきでした'
                gto_alignment = 'incorrect'
            else:
                evaluation = '許容範囲内'
                explanation = f'{position} からの {hand} call は状況によっては適切です'
                gto_alignment = 'acceptable'
        
        elif action == 'fold':
            if is_in_fold_range:
                evaluation = 'GTO通り ✅'
                explanation = f'{position} からの {hand} fold は GTO 基準に合致しています'
                gto_alignment = 'correct'
            elif is_in_raise_range or is_in_call_range:
                evaluation = '非GTO ⚠️'
                explanation = f'{position} からの {hand} fold はタイトすぎます。raise または call を検討すべきでした'
                gto_alignment = 'incorrect'
            else:
                evaluation = '許容範囲内'
                explanation = f'{position} からの {hand} fold は保守的ですが状況によっては適切です'
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
                    f"負けていますが、{hand} を {position} でプレイするのは GTO 戦略の標準的な判断です。"
                )
                advice_text.append(
                    "短期的な結果に左右されず、長期的には正しい判断を繰り返すことが重要です。"
                )
            elif result == 'WIN':
                advice_text.append("勝ったのは判断が正しかったからです。")
                advice_text.append("このスタイルを継続してください。")
            else:
                advice_text.append("適切な判断でした。")
        
        elif alignment == 'acceptable':
            advice_text.append("📊 **許容範囲内の判断です**")
            advice_text.append(
                f"{hand} を {position} でプレイするのは状況によっては適切ですが、より標準的な GTO 戦略との差異があります。"
            )
            advice_text.append(
                "相手のプレイスタイルや過去のアクションを考慮した exploitative play の可能性があります。"
            )
        
        elif alignment == 'incorrect':
            advice_text.append("⚠️  **判断を見直してください**")
            advice_text.append(
                f"{hand} は {position} からの標準的な GTO レンジに含まれていません。"
            )
            advice_text.append(
                "より強いハンドでプレイし、弱いハンドは fold するようにしてください。"
            )
            
            if result == 'WIN':
                advice_text.append(
                    f"\n今回は勝ちましたが、長期的には -{profit:.1f}bb よりも大きな損失につながる可能性があります。"
                )
        
        # 利益ベースのアドバイス
        if profit < -20:
            advice_text.append(f"\n💰 **大きな損失 ({profit:.1f}bb) が発生しています**")
            advice_text.append(
                "ポスト・フロップのプレイを見直す必要があります："
            )
            advice_text.append("- ベットサイズは適切でしたか？")
            advice_text.append("- ブラフキャッチの判断は正しかったですか？")
            advice_text.append("- 相手のレンジを正確に読めていましたか？")
        elif profit > 20:
            advice_text.append(f"\n💰 **大きな勝利 (+{profit:.1f}bb) おめでとうございます！**")
            if alignment == 'correct':
                advice_text.append("適切な判断と実行の結果です。")
            else:
                advice_text.append("今回は勝ちましたが、より GTO に沿ったプレイを心がけることで安定した利益が期待できます。")
        
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
