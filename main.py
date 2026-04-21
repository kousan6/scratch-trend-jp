import requests
import json

# 1. 調査対象にする日本の有名なスタジオID（例：日本公式など）
# ここにある作品の中から「今のトレンド」を探します
STUDIO_IDS = [1593530, 2033326] 

def get_trending():
    all_projects = []
    
    for s_id in STUDIO_IDS:
        url = f"https://api.scratch.mit.edu/studios/{s_id}/projects"
        res = requests.get(url).json()
        if isinstance(res, list):
            all_projects.extend(res)

    # データの整理
    trending_list = []
    for p in all_projects[:20]: # 上位20件をチェック
        p_id = p['id']
        # 個別の詳細データを取得
        p_res = requests.get(f"https://api.scratch.mit.edu/projects/{p_id}").json()
        
        trending_list.append({
            "title": p_res['title'],
            "author": p_res['author']['username'],
            "id": p_id,
            "views": p_res['stats']['views'],
            "loves": p_res['stats']['loves'],
            "thumbnail": p_res['images']['282x218']
        })
    
    # 簡易的に「閲覧数」が多い順に並べ替え
    trending_list.sort(key=lambda x: x['views'], reverse=True)

    # 結果を保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_trending()
