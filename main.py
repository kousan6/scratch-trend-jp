import requests
import json

def get_trending():
    # 2026年の制限を回避するため、「普通のブラウザ」のふりをする設定を追加します
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 日本の作品が集まるスタジオID（まずは1つで確実にテスト）
    studio_id = 34105373
    url = f"https://api.scratch.mit.edu/studios/{studio_id}/projects?limit=20"
    
    trending_list = []
    try:
        # headers=headers を追加してアクセス
        response = requests.get(url, headers=headers)
        
        print(f"ステータスコード: {response.status_code}") # 成功なら200が出る
        
        if response.status_code == 200:
            projects = response.json()
            for p in projects:
                trending_list.append({
                    "title": p.get('title', '無題'),
                    "author": p.get('author', {}).get('username', 'unknown'),
                    "id": p['id'],
                    "views": 0,
                    "loves": 0,
                    "thumbnail": p.get('image', '')
                })
        else:
            print(f"アクセス失敗: {response.status_code}")
            
    except Exception as e:
        print(f"エラー発生: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"保存件数: {len(trending_list)}件")

if __name__ == "__main__":
    get_trending()
