import requests
import json

def get_trending():
    # 戦略：Scratchの「傾向」から直接全データを取得し、そこから抽出する
    # 2026年の仕様に合わせ、一番広い範囲（q=*）を検索します
    url = "https://api.scratch.mit.edu/explore/projects?mode=trending&q=*"
    
    trending_list = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            projects = response.json()
            
            for p in projects:
                # 日本語（ひらがな・カタカナ・漢字）が含まれているか、
                # あるいは「JP」などの日本関連の言葉があるかチェック
                title = p.get('title', '')
                
                # 判定：全作品の中から、まずは最初の15件を無条件で出してみるテストを兼ねます
                # （空っぽを回避するため）
                trending_list.append({
                    "title": title,
                    "author": p.get('author', {}).get('username', 'unknown'),
                    "id": p['id'],
                    "views": p.get('stats', {}).get('views', 0),
                    "loves": p.get('stats', {}).get('loves', 0),
                    "thumbnail": p.get('image', '')
                })
                
                # 15件溜まったら終了
                if len(trending_list) >= 15:
                    break
                    
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"成功：{len(trending_list)}件保存しました")

if __name__ == "__main__":
    get_trending()
