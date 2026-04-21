import requests
import json

def get_trending():
    # ブラウザのふりをする設定
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    # 2026年でも比較的安定している「検索API」を使用します。
    # 日本語の作品を直接見つけるため、検索ワードに「日本」や「JP」を指定します。
    url = "https://api.scratch.mit.edu/search/projects?variant=trending&q=jp"
    
    trending_list = []
    try:
        response = requests.get(url, headers=headers)
        print(f"ステータスコード: {response.status_code}")
        
        if response.status_code == 200:
            projects = response.json()
            # 取得できたデータがリスト型であることを確認してループ
            if isinstance(projects, list):
                for p in projects:
                    p_id = p.get('id')
                    if p_id:
                        trending_list.append({
                            "title": p.get('title', '無題'),
                            "author": p.get('author', {}).get('username', 'unknown'),
                            "id": p_id,
                            "views": p.get('stats', {}).get('views', 0),
                            "loves": p.get('stats', {}).get('loves', 0),
                            "thumbnail": p.get('images', {}).get('282x218', f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png")
                        })
        
    except Exception as e:
        print(f"エラー発生: {e}")

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"結果：{len(trending_list)}件の日本関連作品を取得しました。")

if __name__ == "__main__":
    get_trending()
