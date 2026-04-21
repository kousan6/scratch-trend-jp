import requests
import json
import re

def is_japanese(text):
    if not text: return False
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def get_trending():
    # 戦略：最新の作品（recent）から日本語のものを探し、
    # その中から「星（loves）」がついているものを抽出します
    url = "https://api.scratch.mit.edu/explore/projects?mode=recent&q=*"
    
    trending_list = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            projects = response.json()
            for p in projects:
                title = p.get('title', '')
                # 「日本語が含まれている」かつ「最新」の作品をチェック
                if is_japanese(title):
                    trending_list.append({
                        "title": title,
                        "author": p.get('author', {}).get('username', 'unknown'),
                        "id": p['id'],
                        "views": p.get('stats', {}).get('views', 0),
                        "loves": p.get('stats', {}).get('loves', 0),
                        "thumbnail": p.get('image', '')
                    })
    except Exception as e:
        print(f"エラー: {e}")

    # もし最新に日本語が少なければ、日本の活発なスタジオからも補填します
    if len(trending_list) < 5:
        studio_url = "https://api.scratch.mit.edu/studios/34105373/projects?limit=20"
        try:
            res = requests.get(studio_url).json()
            for p in res:
                if not any(item['id'] == p['id'] for item in trending_list):
                    trending_list.append({
                        "title": p['title'],
                        "author": p['author']['username'],
                        "id": p['id'],
                        "views": 0, "loves": 0,
                        "thumbnail": p['image']
                    })
        except: pass

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:20], f, ensure_ascii=False, indent=4)
    print(f"最新の日本作品を{len(trending_list)}件更新しました。")

if __name__ == "__main__":
    get_trending()
