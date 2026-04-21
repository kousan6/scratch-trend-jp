import requests
import json
import re

def is_japanese(text):
    if not text: return False
    # 日本語が含まれているか判定
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 検索ワードのバリエーションを増やし、より多くの日本作品を捕まえます
    queries = ["jp", "ja", "日本語", "ゲーム"]
    
    trending_list = []
    
    for q in queries:
        # popular（人気）だけでなく trending（傾向）も混ぜて取得
        for variant in ["popular", "trending"]:
            url = f"https://api.scratch.mit.edu/search/projects?variant={variant}&q={q}"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    projects = response.json()
                    for p in projects:
                        p_id = p.get('id')
                        title = p.get('title', '')
                        
                        # 【ここがポイント】
                        # 1. IDが8億以上（2024年後半〜現在）ならOKとする（少し条件を緩めました）
                        # 2. かつ、タイトルに日本語が含まれているものだけを厳選
                        if p_id and p_id > 800000000 and is_japanese(title):
                            if not any(item['id'] == p_id for item in trending_list):
                                trending_list.append({
                                    "title": title,
                                    "author": p.get('author', {}).get('username', 'unknown'),
                                    "id": p_id,
                                    "views": p.get('stats', {}).get('views', 0),
                                    "loves": p.get('stats', {}).get('loves', 0),
                                    "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png"
                                })
            except:
                continue

    # 閲覧数（views）が多い順に並べ替えて「トレンド感」を出します
    trending_list.sort(key=lambda x: x['views'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:24], f, ensure_ascii=False, indent=4)
    print(f"最新の日本作品を{len(trending_list[:24])}件抽出しました。")

if __name__ == "__main__":
    get_trending()
