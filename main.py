import requests
import json

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 戦略：
    # 1. 検索ワードを「jp 2026」や「jp 2025」にして、最近の作品を強制的に狙う
    # 2. IDが「930,000,000」以上のもの（2025年末〜2026年以降の作品）に限定する
    queries = ["jp 2026", "jp 2025", "日本語 2026"]
    
    trending_list = []
    
    for q in queries:
        url = f"https://api.scratch.mit.edu/search/projects?variant=popular&q={q}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                projects = response.json()
                for p in projects:
                    p_id = p.get('id')
                    # IDの足切りラインを大幅にアップ（最近の作品のみ許可）
                    if p_id and p_id > 900000000:
                        if not any(item['id'] == p_id for item in trending_list):
                            trending_list.append({
                                "title": p.get('title', '無題'),
                                "author": p.get('author', {}).get('username', 'unknown'),
                                "id": p_id,
                                "views": p.get('stats', {}).get('views', 0),
                                "loves": p.get('stats', {}).get('loves', 0),
                                "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png"
                            })
        except Exception as e:
            print(f"エラー: {e}")

    # IDが新しい順に並べ替え
    trending_list.sort(key=lambda x: x['id'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:20], f, ensure_ascii=False, indent=4)
    print(f"2026年基準で{len(trending_list[:20])}件の最新作を抽出しました。")

if __name__ == "__main__":
    get_trending()
