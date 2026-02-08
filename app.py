"""
ポーカー GTO 分析 Web UI
スマホ最適化フォーム + GitHub 自動 push
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess
import os
import re

sys.path.insert(0, str(Path(__file__).parent / 'core'))
from poker_gto_agent import PokerGTOAgent

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

agent = PokerGTOAgent()

# GitHub configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_REPO = os.getenv('GITHUB_REPO', '')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    ハンドID を受け取り、分析を実行して結果を返す
    """
    try:
        data = request.get_json()
        hand_ids = data.get('hand_ids', [])
        hand_data_list = data.get('hand_data', [])  # 新機能：ハンドデータ
        notes = data.get('notes', '')
        
        if not hand_ids:
            return jsonify({'error': 'ハンドID が必要です'}), 400
        
        # 分析実行
        if hand_data_list:
            # ユーザー提供データを使用
            report = agent.analyze_hands(hand_ids, hand_data_list)
            analysis_type = "実データ分析"
        else:
            # サンプルデータを使用
            report = agent.analyze_hands(hand_ids)
            analysis_type = "サンプルデータ分析"
        
        # リポジトリに保存
        github_status = save_to_repository(hand_ids, report, notes)
        
        return jsonify({
            'success': True,
            'report': report,
            'hand_count': len(hand_ids),
            'analysis_type': analysis_type,
            'github_status': github_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def history():
    """
    分析履歴を取得
    """
    try:
        reports_dir = Path(__file__).parent / 'reports'
        
        if not reports_dir.exists():
            return jsonify({'reports': []})
        
        reports = []
        for report_file in sorted(reports_dir.glob('*.md'), reverse=True)[:20]:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    preview = content[:200].replace('\n', ' ')
                    stat = report_file.stat()
                    reports.append({
                        'filename': report_file.name,
                        'timestamp': stat.st_mtime,
                        'preview': preview
                    })
            except Exception as e:
                print(f"Error reading {report_file}: {e}")
                continue
        
        return jsonify({'reports': reports})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/<filename>', methods=['GET'])
def get_report(filename):
    """
    特定のレポートを取得
    """
    try:
        # セキュリティ: ファイル名を検証
        if '..' in filename or '/' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        report_file = Path(__file__).parent / 'reports' / filename
        
        if not report_file.exists():
            return jsonify({'error': 'Report not found'}), 404
        
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def save_to_repository(hand_ids, report, notes):
    """
    レポートをリポジトリに保存
    - ローカル reports/ に保存
    - Git コミット
    - GitHub に push
    """
    try:
        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        # タイムスタンプ付きファイル名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f'analysis_{timestamp}.md'
        
        # メタデータ付きレポート
        full_report = f"""# 🎰 ポーカー GTO 分析レポート

**分析日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**ハンド数**: {len(hand_ids)}  
**メモ**: {notes if notes else '(なし)'}  

---

## 分析結果

{report}

---

**ハンドID一覧**:
```
{chr(10).join(hand_ids)}
```
"""
        
        # ファイルに保存
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        repo_path = Path(__file__).parent
        
        # Git コミット
        try:
            subprocess.run(
                ['git', 'add', 'reports/'],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            commit_message = f'Add analysis report: {len(hand_ids)} hands ({timestamp})'
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            # GitHub に push
            if GITHUB_TOKEN and GITHUB_REPO:
                push_to_github(repo_path, commit_message)
                status = "✅ GitHub に保存されました"
            else:
                status = "✅ ローカルに保存されました (GitHub 連携は未設定)"
        except subprocess.CalledProcessError as e:
            status = f"⚠️ Git 操作に失敗: {e.stderr}"
        
        return status
    except Exception as e:
        return f"⚠️ 保存に失敗: {str(e)}"


def push_to_github(repo_path, commit_message):
    """
    GitHub に push
    """
    try:
        # リモート URL を確認
        result = subprocess.run(
            ['git', 'remote', '-v'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if 'origin' not in result.stdout:
            print("⚠️ Git リモートが設定されていません")
            return
        
        # SSH キーまたは Personal Access Token を使用して push
        subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, 'GIT_ASKPASS': 'echo', 'GIT_PASSWORD': GITHUB_TOKEN}
        )
        
        print(f"✅ GitHub に push 完了: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ GitHub push に失敗: {e.stderr}")
    except Exception as e:
        print(f"⚠️ GitHub 連携エラー: {str(e)}")


if __name__ == '__main__':
    # 開発環境では debug=True, 本番では False
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    print(f"""
╔══════════════════════════════════════════════╗
║     🎰 ポーカー GTO 分析 Web UI              ║
╠══════════════════════════════════════════════╣
║  http://localhost:5000                      ║
║  スマホからアクセス: http://<IP>:5000      ║
╚══════════════════════════════════════════════╝
    """)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
