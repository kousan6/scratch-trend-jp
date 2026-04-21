import requests
import json

def get_trending():
    # 日本の作品がよく集まる「特定のスタジオ」から直接持ってくる方式に戻し、
    # かつ最新のAPI形式に対応させます
    studio_id = 1593530 # 日本の有名なスタジオ
    url = f"https://api.scratch.mit.edu/studios/{studio_id}/projects?limit=20"
    
    trending_list = []
    try:
        res = requests.get(url)
        if res.status_code == 200:
            projects = res.json()
            for p in projects:
                trending_list.append({
                    "title": p.get('title', '無題'),
                    "author": p.get('author', {}).get('username', 'unknown'),
                    "id": p['id'],
                    "views": 0,
                    "loves": 0,
                    "thumbnail": p.get('image', '')
                })
    except Exception as e:
        print(f"エラー: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print("保存完了")

if __name__ == "__main__":
    get_trending()
