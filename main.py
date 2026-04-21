import requests
import json
import re

def is_japanese(text):
    if not text: return False
    # タイトルに日本語が含まれているか判定
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 成功実績のある「search」APIを使用
    # variant=trending にすることで、最新かつ勢いのある作品をScratch側に選ばせます
    url = "https://api.scratch.mit.edu/search/projects?variant=trending&q=*"
    
    trending_list = []
    try:
        # 1回の実行で多めに（40件）取得して、その中から日本作品をフィルタリングします
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            projects = response.json()
            for p in projects:
                p_id = p.get('id')
                title = p.get('title', '')
                
                # あなたのアイデア通り、IDフィルターで「最近の作品」であることを保証
                # 800,000,000 以上（2024年後半〜2026年）を対象
                if p_id and p_id > 800000000:
                    # かつ、日本語が含まれているものだけを抽出
                    if is_japanese(title):
                        trending_list.append({
                            "title": title,
                            "author": p.get('author', {}).get('username', 'unknown'),
                            "id": p_id,
                            "views": p.get('stats', {}).get('views', 0),
                            "loves": p.get('stats', {}).get('loves', 0),
                            "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p_id}_282x218.png"
                        })
    except Exception as e:
        print(f"エラー発生: {e}")

    # 万が一、日本語作品が1つも捕まらなかった時のための「保険」
    # 前回成功した検索ワード「jp」で再試行します
    if not trending_list:
        try:
            backup_url = "https://api.scratch.mit.edu/search/projects?variant=popular&q=jp"
            res = requests.get(backup_url, headers=headers).json()
            for p in res:
                if p.get('id') > 800000000 and is_japanese(p.get('title', '')):
                    trending_list.append({
                        "title": p['title'], "author": p['author']['username'], "id": p['id'],
                        "views": p['stats']['views'], "loves": p['stats']['loves'],
                        "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p['id']}_282x218.png"
                    })
        except:
            pass

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:24], f, ensure_ascii=False, indent=4)
    print(f"更新完了：{len(trending_list)}件の日本作品を保存しました。")

if __name__ == "__main__":
    get_trending()
