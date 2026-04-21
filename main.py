import requests
import json
import re

def is_japanese(text):
    if not text: return False
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    trending_list = []
    
    # 成功実績のある「search」APIを使い、
    # offset（ページ送り）を変えながら4回（160件分）スキャンします
    for i in range(4):
        offset = i * 40
        url = f"https://api.scratch.mit.edu/search/projects?variant=trending&q=*&limit=40&offset={offset}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                projects = response.json()
                for p in projects:
                    p_id = p.get('id')
                    title = p.get('title', '')
                    
                    # ID 8億以上（最近の作品）かつ 日本語が含まれる
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

    # 保存（最大24件）
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:24], f, ensure_ascii=False, indent=4)
    print(f"完了：最新の日本作品を{len(trending_list[:24])}件見つけました。")

if __name__ == "__main__":
    get_trending()
