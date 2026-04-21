import requests
import json
import re

def is_japanese(text):
    if not text: return False
    # ひらがな、カタカナ、漢字、または全角記号が含まれているか
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3000-\u303F]', text))

def get_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    trending_list = []

    try:
        # ターゲット：ScratchViewsのトレンドページ
        view_url = "https://scratchviews.com/explore/trending"
        res = requests.get(view_url, headers=headers, timeout=15)
        
        # ソースコード内の jsviewarrayofarray = [[...]] の中身を抽出
        # 今回はクォーテーションの有無やスペースに影響されないよう、より柔軟なパターンにします
        # パターン: ["ID", "TITLE", "AUTHOR", "UID"]
        raw_projects = re.findall(r'\[\s*"(\d+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"(\d+)"\s*\]', res.text)
        
        print(f"Viewのソースから {len(raw_projects)} 件の候補を発見しました。")

        for m_id, m_title, m_author, m_uid in raw_projects:
            # 1. 日本語が含まれているか（あなたのこだわりポイント）
            # 2. 念のためIDが最近のものか（2024年以降目安の8億以上）
            if is_japanese(m_title) and int(m_id) > 800000000:
                trending_list.append({
                    "title": m_title,
                    "author": m_author,
                    "id": int(m_id),
                    "views": 0, 
                    "loves": 0,
                    "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{m_id}_282x218.png"
                })
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    # 万が一Viewから日本語作品が1つも見つからなかった時のため、
    # 以前成功した「jp」検索の結果を最低限1つ混ぜる処理（全滅防止）
    if not trending_list:
        print("Viewから日本語作品が見つからなかったため、APIで補完します。")
        try:
            backup_res = requests.get("https://api.scratch.mit.edu/search/projects?variant=popular&q=jp", headers=headers).json()
            for p in backup_res:
                if is_japanese(p['title']):
                    trending_list.append({
                        "title": p['title'], "author": p['author']['username'], "id": p['id'],
                        "views": p['stats']['views'], "loves": p['stats']['loves'],
                        "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{p['id']}_282x218.png"
                    })
        except:
            pass

    # IDの大きい順（最新順）に並べ替え
    trending_list.sort(key=lambda x: x['id'], reverse=True)

    # 最終結果を保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(trending_list[:30], f, ensure_ascii=False, indent=4)
    
    print(f"完了！ {len(trending_list[:30])} 件の『今』の日本作品を抽出しました。")

if __name__ == "__main__":
    get_trending()
