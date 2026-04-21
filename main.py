import requests
import json

# 日本のトレンドを探すための対象スタジオID
STUDIO_IDS = [1593530, 2033326] 

def get_trending():
    all_projects = []
    
    for s_id in STUDIO_IDS:
        try:
            url = f"https://api.scratch.mit.edu/studios/{s_id}/projects"
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    all_projects.extend(data)
        except Exception as e:
            print(f"エラー: {e}")

    trending_list = []
    # データを取得（負荷を抑えるため上位15件）
    for p in all_projects[:15]:
        try:
            p_id = p['id']
            p_res = requests.get(f"https://api.scratch.mit.edu/projects/{p_id}").json()
            
            trending_list.append({
                "title": p_res.get('title', '無題'),
                "author": p_res.get('author', {}).get('username', 'unknown'),
                "id": p_id,
                "views": p_res.get('stats', {}).get('views', 0),
                "loves": p_res.get('stats', {}).get('loves', 0),
                "thumbnail": p_res.get('images', {}).get('282x218', '')
            })
        except:
            continue
    
    # 閲覧数順に並べ替え
    trending_list.sort(key=lambda x: x['views'], reverse=True)

    # data.json という名前で保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print("成功：data.jsonを更新しました。")

if __name__ == "__main__":
    get_trending()
