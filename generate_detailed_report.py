#!/usr/bin/env python3
"""
詳細な分析レポート生成スクリプト
ポストフロップのアクション分析を含む包括的なレポートを作成
"""

import re
from datetime import datetime
from pathlib import Path
from core.poker_gto_agent import PokerGTOAgent
from core.hand_data_processor import HandDataProcessor
from core.gto_evaluator import GTOEvaluator


class DetailedHandAnalyzer:
    """詳細なハンド分析"""
    
    @staticmethod
    def analyze_postflop_actions(hand_data: dict) -> str:
        """ポストフロップのアクションを分析"""
        
        actions = hand_data.get('actions', {})
        board = hand_data.get('board', [])
        hero_position = hand_data.get('hero_position', 'N/A')
        hero_hand = hand_data.get('hero_hand', 'N/A')
        profit = hand_data.get('hero_profit_bb', 0)
        
        analysis = []
        
        # Flopアクション分析
        if actions.get('flop'):
            analysis.append("\n**フロップでのプレイ:**")
            if board and len(board) >= 3:
                analysis.append(f"- ボード: {' '.join(board[:3])}")
            
            flop_actions = actions['flop']
            for action in flop_actions:
                if hero_position in action or hand_data.get('all_players', {}).get(hero_position, {}).get('name', '') in action:
                    analysis.append(f"- {action}")
            
            # フロップのアドバイス
            if 'Check' in ' '.join(flop_actions):
                analysis.append("  💡 チェックは相手に無料でカードを見せることになります。ベットでポットコントロールを検討。")
        
        # Turnアクション分析
        if actions.get('turn'):
            analysis.append("\n**ターンでのプレイ:**")
            if board and len(board) >= 4:
                analysis.append(f"- ターンカード: {board[3]}")
            
            turn_actions = actions['turn']
            for action in turn_actions:
                if hero_position in action or hand_data.get('all_players', {}).get(hero_position, {}).get('name', '') in action:
                    analysis.append(f"- {action}")
        
        # Riverアクション分析
        if actions.get('river'):
            analysis.append("\n**リバーでのプレイ:**")
            if board and len(board) >= 5:
                analysis.append(f"- リバーカード: {board[4]}")
            
            river_actions = actions['river']
            for action in river_actions:
                if hero_position in action or hand_data.get('all_players', {}).get(hero_position, {}).get('name', '') in action:
                    analysis.append(f"- {action}")
            
            # リバーでの判断アドバイス
            if 'Fold' in ' '.join(river_actions) and profit < 0:
                analysis.append("  💡 リバーでのフォールドは保守的です。ポットオッズを考慮しましたか？")
            elif 'Call' in ' '.join(river_actions) and profit < 0:
                analysis.append("  💡 コールして負けた場合、相手のレンジ推定を見直す必要があるかもしれません。")
        
        return '\n'.join(analysis) if analysis else "（ポストフロップの詳細なし）"
    
    @staticmethod
    def generate_strategic_advice(hand_data: dict, gto_evaluation: dict) -> str:
        """戦略的なアドバイスを生成"""
        
        advice = []
        
        position = hand_data.get('hero_position', '')
        hand = hand_data.get('hero_hand', '')
        profit = hand_data.get('hero_profit_bb', 0)
        result = hand_data.get('result', '')
        
        # ポジション別のアドバイス
        if position in ['CO', 'BTN']:
            advice.append("\n**ポジションアドバンテージ:**")
            advice.append(f"- {position} は有利なポジションです。アグレッシブにプレイできます。")
            if gto_evaluation['gto_alignment'] == 'incorrect':
                advice.append("- しかし、weak hands で無理に攻めるのは避けましょう。")
        
        elif position in ['UTG', 'MP']:
            advice.append("\n**アーリーポジション:**")
            advice.append(f"- {position} は不利なポジションです。タイトなレンジが推奨されます。")
            if gto_evaluation['gto_alignment'] == 'correct':
                advice.append("- 適切なタイトなプレイができています。継続してください。")
        
        elif position in ['SB', 'BB']:
            advice.append("\n**ブラインド:**")
            advice.append(f"- {position} はポストフロップで不利です。")
            if position == 'BB':
                advice.append("- BB ディフェンスは重要ですが、過度にルースになりすぎないように注意。")
            if position == 'SB':
                advice.append("- SB からは強いハンドで積極的に raise し、弱いハンドは fold を検討。")
        
        # 損益に基づくアドバイス
        if profit < -5 and result == 'LOSE':
            advice.append("\n**ポストフロップの改善点:**")
            advice.append("- ベットサイズを見直しましょう（1/3 pot, 1/2 pot, 3/4 pot など）")
            advice.append("- 相手のアクションから何を読み取れますか？")
            advice.append("- フォールドエクイティを考慮していますか？")
        
        # ハンドの強さに基づくアドバイス
        if hand.startswith('A') and hand[1] in ['2', '3', '4', '5']:
            advice.append("\n**Weak Ace の注意点:**")
            advice.append("- A2o-A5o はドミネートされやすいハンドです。")
            advice.append("- ポジションが悪い場合は fold を検討しましょう。")
        
        return '\n'.join(advice) if advice else ""


def generate_detailed_report(parsed_hands: list) -> str:
    """詳細な分析レポートを生成"""
    
    analyzer = DetailedHandAnalyzer()
    
    report = f"""# 🎰 詳細なGTO分析レポート

**生成日時:** {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**プレイヤー:** okayama
**分析対象:** {len(parsed_hands)} ハンド

---

## 📊 全体サマリー

"""
    
    # 統計情報を計算
    total_profit = sum(hand.get('hero_profit_bb', 0) for hand in parsed_hands)
    wins = sum(1 for hand in parsed_hands if hand.get('result') == 'WIN')
    losses = sum(1 for hand in parsed_hands if hand.get('result') == 'LOSE')
    
    report += f"""
| 指標 | 値 |
|------|-----|
| 総損益 | {total_profit:+.2f}bb |
| 勝利ハンド | {wins}/{len(parsed_hands)} ({wins/len(parsed_hands)*100:.0f}%) |
| 敗北ハンド | {losses}/{len(parsed_hands)} ({losses/len(parsed_hands)*100:.0f}%) |
| 平均損益/ハンド | {total_profit/len(parsed_hands):+.2f}bb |

---

"""
    
    # 各ハンドの詳細分析
    gto_correct_count = 0
    
    for i, hand in enumerate(parsed_hands, 1):
        position = hand.get('hero_position', 'N/A')
        hand_name = hand.get('hero_hand', 'N/A')
        action = hand.get('hero_action', 'N/A')
        profit = hand.get('hero_profit_bb', 0)
        result = hand.get('result', 'N/A')
        hand_id = hand.get('hand_id', 'N/A')
        date = hand.get('date', 'N/A')
        board = hand.get('board', [])
        
        # GTO 評価
        evaluation = GTOEvaluator.evaluate_action(
            position, hand_name, action, hand
        )
        
        if evaluation['gto_alignment'] == 'correct':
            gto_correct_count += 1
        
        # ボードテクスチャ情報
        board_texture = hand.get('board_texture', {})
        
        report += f"""
## ハンド {i}: {hand_name} @ {position}

**基本情報:**
- **ハンドID:** `{hand_id}`
- **日時:** {date}
- **ポジション:** {position}
- **ハンド:** {hand_name}
- **スタック:** {hand.get('stack_size_bb', 100)}bb
- **結果:** {result} ({profit:+.1f}bb)

**プリフロップ:**
- **アクション:** {action.upper()}
"""
        
        # プリフロップのアクションシーケンス
        if hand.get('actions', {}).get('preflop'):
            report += f"- **アクションシーケンス:**\n"
            for pf_action in hand['actions']['preflop']:
                report += f"  - {pf_action}\n"
        
        # ボード情報
        if board:
            report += f"\n**ボード:**\n"
            report += f"- {' '.join(board)}\n"
            if board_texture:
                report += f"- **テクスチャ:** {board_texture.get('description', 'N/A')}\n"
        
        # GTO評価
        report += f"""
**GTO評価:**
- **評価:** {evaluation['evaluation']}
- **説明:** {evaluation['explanation']}

**アドバイス:**
{evaluation['advice']}
"""
        
        # ポストフロップ分析
        postflop_analysis = analyzer.analyze_postflop_actions(hand)
        if postflop_analysis:
            report += f"\n{postflop_analysis}\n"
        
        # 戦略的アドバイス
        strategic_advice = analyzer.generate_strategic_advice(hand, evaluation)
        if strategic_advice:
            report += f"\n{strategic_advice}\n"
        
        report += "\n---\n"
    
    # 総合評価
    gto_rate = gto_correct_count / len(parsed_hands) * 100
    
    report += f"""
## 🎯 総合評価

### GTO整合性
- **GTO整合率:** {gto_correct_count}/{len(parsed_hands)} ({gto_rate:.0f}%)

### 主なリーク
"""
    
    # リークの特定
    leaks = []
    
    # 弱いハンドでのraiseを確認
    weak_hand_raises = []
    for hand in parsed_hands:
        if hand.get('hero_action') == 'raise':
            hand_name = hand.get('hero_hand', '')
            position = hand.get('hero_position', '')
            evaluation = GTOEvaluator.evaluate_action(position, hand_name, 'raise', hand)
            if evaluation['gto_alignment'] == 'incorrect':
                weak_hand_raises.append(f"{hand_name} @ {position}")
    
    if weak_hand_raises:
        leaks.append(f"弱いハンドでの raise: {', '.join(weak_hand_raises)}")
    
    # 負けハンドの分析
    losing_hands = [hand for hand in parsed_hands if hand.get('result') == 'LOSE']
    if losing_hands:
        avg_loss = sum(hand.get('hero_profit_bb', 0) for hand in losing_hands) / len(losing_hands)
        leaks.append(f"平均敗北額: {avg_loss:.2f}bb/ハンド")
    
    if leaks:
        for leak in leaks:
            report += f"- {leak}\n"
    else:
        report += "- 主要なリークは検出されませんでした。\n"
    
    report += """
### 推奨アクション

1. **プリフロップレンジの見直し**
   - 各ポジションの標準的な GTO レンジを学習
   - 特に early position と SB でタイトにプレイ

2. **ポストフロップのベットサイジング**
   - バリューベット: 2/3 - 3/4 pot
   - ブラフ: 1/3 - 1/2 pot
   - ポットコントロール: 1/3 pot

3. **対戦相手の分析**
   - 各プレイヤーの VPIP/PFR を記録
   - アグレッション頻度をメモ
   - exploitative play を検討

4. **メンタルゲーム**
   - 短期的な結果に惑わされない
   - 正しいプロセスに集中
   - バッドビートは学習機会と捉える

---

## 📚 参考資料

### GTO レンジチャート

**CO オープンレンジ（推奨）:**
```
AA-77, AKs-AJs, AKo-ATo, KQs-KJs, KQo-KJo, QJs, JTs
```

**BTN オープンレンジ（推奨）:**
```
AA-55, AKs-A9s, AKo-ATo, KQs-KTs, KQo-KJo, QJs-QTs, QJo, JTs
```

**SB オープンレンジ（推奨）:**
```
AA-55, AKs-ATs, AKo-AJo, KQs-KJs, KQo
```

**BB ディフェンスレンジ（vs 2.5bb open）:**
```
広範囲: 22+, A2s+, A2o+, K5s+, K9o+, Q8s+, QTo+, J8s+, JTo, T8s+, 98s, 87s, 76s, 65s, 54s, 43s
```

### 推奨学習リソース

1. **GTO ソルバー**
   - PioSOLVER
   - GTO+
   - Simple Postflop

2. **書籍**
   - "The Grinder's Manual" by Peter Clarke
   - "Modern Poker Theory" by Michael Acevedo
   - "Applications of No-Limit Hold'em" by Matthew Janda

3. **トレーニングサイト**
   - Upswing Poker
   - Run It Once
   - PokerCoaching.com

---

*Generated by Poker GTO Agent v2.0*
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report


def main():
    """メイン実行関数"""
    
    from analyze_hands import TenFourHandParser, hands_raw
    
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
    
    # 詳細レポートを生成
    if parsed_hands:
        print(f"\n{'='*70}")
        print(f"📊 詳細なGTO分析レポートを生成中...")
        print(f"{'='*70}\n")
        
        report = generate_detailed_report(parsed_hands)
        
        # レポートを保存
        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f'detailed_analysis_{timestamp}.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ 詳細レポートを保存: {report_file}")
        print(f"\n{'='*70}")
        print(f"📄 詳細分析レポート")
        print(f"{'='*70}\n")
        print(report)
    else:
        print("\n✗ パース可能なハンドがありませんでした")


if __name__ == '__main__':
    main()
