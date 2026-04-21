import requests
import json

def get_trending():
    # 日本の作品が大量に集まっている、現在アクティブなスタジオIDのリストです。
    # 2026年でも稼働している可能性が高い日本の大型コミュニティスタジオを選定しています。
    STUDIO_IDS = [
        34105373,  # 日本の作品が集まる大規模スタジオ
        1593530,   # 日本Scratchコミュニティ
        2033326    # 日本語の作品集
    ]
    
    trending_list = []
    
    for s_id in STUDIO_IDS:
        try:
            # スタジオ内の作品を取得するAPI（ここは比較的制限が緩いです）
            url = f"https://api.scratch.mit.edu/studios/{s_id}/projects?limit=40"
            response = requests.get(url)
            
            if response.status_code == 200:
                projects = response.json()
                for p in projects:
                    # まだリストに入れていない作品だけを追加
                    if not any(item['id'] == p['id'] for item in trending_list):
                        trending_list.append({
                            "title": p.get('title', '無題'),
                            "author": p.get('author', {}).get('username', 'unknown'),
                            "id": p['id'],
                            "views": 0, # スタジオ経由では詳細は取れないため、一旦0にします
                            "loves": 0,
                            "thumbnail": p.get('image', '')
                        })
        except Exception as e:
            print(f"スタジオ {s_id} の取得に失敗: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"成功：合計{len(trending_list)}件の作品情報を取得しました。")

if __name__ == "__main__":
    get_trending()
