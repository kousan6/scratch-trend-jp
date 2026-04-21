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
    
    # 2026年現在の最新トレンドを網羅するため、
    # 検索の「並び替え順」を「最新(recent)」にして大量に取得します
    # q="*" は全作品を対象にする魔法のワードです
    url = "https://api.scratch.mit.edu/explore/projects?mode=recent&q=*"
    
    try:
        # 1ページあたり40件、最大10ページ分（400件）くらいをスキャン
        for offset in range(0, 400, 40):
            paged_url = f"{url}&offset={offset}&limit=40"
            response = requests.get(paged_url, headers=headers)
            
            if response.status_code == 200:
                projects = response.json()
                for p in projects:
                    title = p.get('title', '')
                    p_id = p.get('id')
                    
                    # 日本語が含まれているかチェック
                    if is_japanese(title):
                        # 重複を避けてリストに追加
                        if not any(item['id'] == p_id for item in trending_list):
                            trending_list.append({
                                "title": title,
                                "author": p.get('author', {}).get('username', 'unknown'),
                                "id": p_id,
                                "views": p.get('stats', {}).get('views', 0),
                                "loves": p.get('stats', {}).get('loves', 0),
                                "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png"
                            })
            else:
                break # エラーが出たら中断
                
    except Exception as e:
        print(f"エラー発生: {e}")

    # 抽出した「最新の日本作品」を、注目度（loves + viewsの比率など）で並べ替える
    # ここではシンプルに閲覧数順にします
    trending_list.sort(key=lambda x: x['views'], reverse=True)

    # 最終的に20〜30件程度を保存
    final_data = trending_list[:30]
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"スキャン完了：最新の日本作品を{len(final_data)}件見つけました。")

if __name__ == "__main__":
    get_trending()
