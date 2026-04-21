import requests
import json
import re

def is_japanese(text):
    # 日本語（ひらがな・カタカナ・漢字）が含まれているかチェックする関数
    if not text: return False
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def get_trending():
    # 戦略：Scratch全体の「人気」作品から日本語が含まれるものだけを抽出する
    url = "https://api.scratch.mit.edu/explore/projects?mode=trending&q=*"
    
    trending_list = []
    try:
        res = requests.get(url)
        if res.status_code == 200:
            projects = res.json()
            
            for p in projects:
                title = p.get('title', '')
                author = p.get('author', {}).get('username', '')
                
                # タイトルに日本語が含まれているものだけを「日本トレンド」とする
                if is_japanese(title):
                    trending_list.append({
                        "title": title,
                        "author": author,
                        "id": p['id'],
                        "views": p.get('stats', {}).get('views', 0),
                        "loves": p.get('stats', {}).get('loves', 0),
                        "thumbnail": p.get('image', '')
                    })
    except Exception as e:
        print(f"エラー: {e}")

    # もし日本語作品が見つからなかった時のための予備（有名な日本のスタジオ）
    if not trending_list:
        backup_url = "https://api.scratch.mit.edu/studios/1593530/projects"
        res = requests.get(backup_url).json()
        for p in res[:10]:
            trending_list.append({
                "title": p['title'],
                "author": p['author']['username'],
                "id": p['id'],
                "views": 0, "loves": 0, # スタジオ一覧からは取得できないため0
                "thumbnail": p['image']
            })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list, f, ensure_ascii=False, indent=4)
    print(f"成功：{len(trending_list)}件の日本作品を保存しました。")

if __name__ == "__main__":
    get_trending()
