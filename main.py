import requests
import json
import re

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 日本の作品が集まるスタジオID
    studio_id = 34105373
    url = f"https://api.scratch.mit.edu/studios/{studio_id}/projects?limit=40"
    
    trending_list = []
    try:
        response = requests.get(url, headers=headers)
        print(f"ステータスコード: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # データの形式（リスト型か辞書型か）を問わず、中身をループで回す
            projects = data if isinstance(data, list) else data.get('results', data.get('projects', []))
            
            for p in projects:
                # どんな名前でデータが入っていても対応できるようにする
                p_id = p.get('id') or p.get('project_id')
                title = p.get('title') or p.get('project_title') or '無題'
                
                if p_id:
                    trending_list.append({
                        "title": title,
                        "author": "Scratcher", 
                        "id": p_id,
                        "views": 0,
                        "loves": 0,
                        "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png"
                    })
        
    except Exception as e:
        print(f"エラー発生: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"解析成功：{len(trending_list)}件の作品を無理やり見つけました！")

if __name__ == "__main__":
    get_trending()
