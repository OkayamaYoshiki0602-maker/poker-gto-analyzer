#!/usr/bin/env python3
"""
ポーカー GTO 分析エージェント
ハンドID を入力 → 包括的な GTO 分析レポート を生成
"""

import json
from pathlib import Path
from datetime import datetime
import sys
from typing import Dict, List, Any, Optional

# ローカルモジュールのインポート
sys.path.insert(0, str(Path(__file__).parent))
from gto_evaluator import GTOEvaluator
from hand_data_processor import HandDataProcessor


class PokerGTOAgent:
    """GTO 対応ポーカー分析エージェント"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.reports_dir = Path(__file__).parent.parent / 'reports'
        self.hands_data = []
        self.processor = HandDataProcessor()
    
    def analyze_hands(self, hand_ids: list, hand_data_list: Optional[List[Dict[str, Any]]] = None):
        """
        複数のハンドIDから包括的な分析レポートを生成
        
        Args:
            hand_ids: ハンドID のリスト
            hand_data_list: ユーザー提供のハンドデータ（オプション）
        """
        
        print("""
╔════════════════════════════════════════════════════════════════════╗
║         🎰 GTO 対応ポーカー分析エージェント                      ║
╚════════════════════════════════════════════════════════════════════╝

📊 分析を実行中...
""")
        
        # ハンドデータを取得・処理
        if hand_data_list:
            # ユーザー提供データを使用
            processed_hands = self._process_user_data(hand_ids, hand_data_list)
            print("✅ ユーザー提供データを使用")
        else:
            # サンプルデータを使用（API実装待ち）
            processed_hands = self._generate_sample_analysis(hand_ids)
            print("⚠️ サンプルデータを使用（実データ未実装）")
        
        # 分析実行
        report = self._generate_gto_report(processed_hands)
        
        # レポート保存
        self._save_report(report)
        
        print("\n✅ 分析完了！\n")
        return report
    
    def _process_user_data(self, hand_ids: list, hand_data_list: List[Dict[str, Any]]) -> list:
        """ユーザー提供のハンドデータを処理"""
        processed_hands = []
        
        for i, hand_id in enumerate(hand_ids):
            if i < len(hand_data_list):
                # ユーザーデータを使用
                raw_data = hand_data_list[i].copy()
                raw_data['hand_id'] = hand_id
                
                # データを標準化
                processed_data = self.processor.process_hand_data(raw_data)
                
                # GTO分析用に変換
                analysis_data = {
                    'hand_id': hand_id,
                    'position': processed_data['hero']['position'],
                    'hand': processed_data['hero']['hand'],
                    'action': processed_data['hero']['action'],
                    'profit_bb': processed_data['hero']['profit_bb'],
                    'result': processed_data['hero']['result'],
                    'opponent_type': self._get_primary_opponent_type(processed_data['opponents']),
                    'spr': processed_data['spr'],
                    'spr_category': processed_data['spr_category'],
                    'board_texture': processed_data['board_texture'],
                    'board': processed_data['board'],
                    'stack_bb': processed_data['hero']['stack_bb']
                }
                
                processed_hands.append(analysis_data)
            else:
                # データが不足している場合はサンプルデータ
                processed_hands.append(self._create_sample_hand(hand_id))
        
        return processed_hands
    
    def _get_primary_opponent_type(self, opponents: List[Dict[str, Any]]) -> str:
        """主要な対戦相手のタイプを取得"""
        if not opponents:
            return 'UNKNOWN'
        
        # アクティブな対戦相手の中で最初のタイプを返す
        for opponent in opponents:
            if opponent.get('active', True) and opponent.get('type') != 'FOLD':
                return opponent.get('type', 'UNKNOWN')
        
        return opponents[0].get('type', 'UNKNOWN')
    
    def _create_sample_hand(self, hand_id: str) -> Dict[str, Any]:
        """サンプルハンドデータを作成"""
        return {
            'hand_id': hand_id,
            'position': 'BTN',
            'hand': 'AK',
            'action': 'raise',
            'profit_bb': -50,
            'result': 'LOSE',
            'opponent_type': 'TAG',
            'spr': 20,
            'spr_category': 'short',
            'board_texture': {'type': 'DRY', 'description': 'ドライボード'},
            'board': ['As', 'Kh', '7d'],
            'stack_bb': 100
        }
    
    def _generate_sample_analysis(self, hand_ids: list) -> list:
        """サンプル分析データを生成（実装用プレースホルダー）"""
        
        sample_data = []
        for i, hand_id in enumerate(hand_ids):
            if i == 0:
                sample_data.append({
                    'hand_id': hand_id,
                    'position': 'BTN',
                    'hand': 'AK',
                    'action': 'raise',
                    'profit_bb': -50,
                    'result': 'LOSE',
                    'opponent_type': 'TAG',
                    'spr': 20,
                    'spr_category': 'short',
                    'board_texture': {'type': 'DRY', 'description': 'ドライボード'},
                    'board': ['As', 'Kh', '7d'],
                    'stack_bb': 100
                })
            else:
                sample_data.append({
                    'hand_id': hand_id,
                    'position': 'MP',
                    'hand': 'QQ',
                    'action': 'raise',
                    'profit_bb': 75,
                    'result': 'WIN',
                    'opponent_type': 'FISH',
                    'spr': 40,
                    'spr_category': 'medium',
                    'board_texture': {'type': 'WET', 'description': 'ウェットボード'},
                    'board': ['Qh', '9s', '8d'],
                    'stack_bb': 100
                })
        
        return sample_data
    
    def _generate_gto_report(self, hands_data: list) -> str:
        """GTO 分析レポートを生成"""
        
        report = f"""# 🎰 GTO 対応ポーカー分析レポート

**生成日時:** {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

---

## 📊 分析結果サマリー

分析対象: {len(hands_data)} ハンド

"""
        
        # 各ハンドの分析
        gto_correct_count = 0
        
        for i, hand in enumerate(hands_data, 1):
            position = hand.get('position', 'N/A')
            hand_name = hand.get('hand', 'N/A')
            action = hand.get('action', 'N/A')
            profit = hand.get('profit_bb', 0)
            result = hand.get('result', 'N/A')
            
            # GTO 評価
            evaluation = GTOEvaluator.evaluate_action(
                position, hand_name, action, hand
            )
            
            if evaluation['gto_alignment'] == 'correct':
                gto_correct_count += 1
            
            # レポート追加
            report += f"""
### ハンド {i}: {hand_name}

**基本情報:**
- ハンドID: {hand.get('hand_id', 'N/A')}
- ポジション: {position}
- アクション: {action}
- 結果: {result} ({profit:+.1f}bb)
- 対戦相手: {hand.get('opponent_type', 'N/A')}

**GTO 評価:**
- {evaluation['evaluation']}
- **{evaluation['explanation']}**

**文脈付きアドバイス:**
{evaluation['advice']}

---

"""
        
        # サマリー
        report += f"""
## 🎯 総合評価

- **GTO 整合率:** {gto_correct_count}/{len(hands_data)} ({gto_correct_count/len(hands_data)*100:.0f}%)
- **主なリーク:** 位置別戦略の改善が必要
- **推奨アクション:** 弱いハンドの fold 率を上げる

## 💡 本質的な改善提案

1. **短期的な結果に左右されない**
   - ポーカーは確率のゲーム
   - 負けていても判断が正しければ継続

2. **GTO 基準を学習**
   - 各ポジションの推奨レンジを暗記
   - 逸脱時は理由を明確に

3. **定期的な復習**
   - 毎週 50 ハンドを分析
   - 月 1 回の包括レビュー

---

*Generated by Poker GTO Agent v1.0*
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report
    
    def _save_report(self, report: str):
        """レポートをファイルに保存"""
        
        self.reports_dir.mkdir(exist_ok=True)
        
        report_file = self.reports_dir / 'GTO_ANALYSIS_REPORT.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ レポートを保存: {report_file}")
        print(f"\n📖 レポートを表示:")
        print(f"  open {report_file}\n")


def main():
    """メインエントリーポイント"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='GTO 対応ポーカー分析')
    parser.add_argument('hand_ids', nargs='*', help='分析するハンドID')
    
    args = parser.parse_args()
    
    agent = PokerGTOAgent()
    report = agent.analyze_hands(args.hand_ids)
    
    print(report)


if __name__ == '__main__':
    main()
