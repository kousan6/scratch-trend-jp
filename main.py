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

    # 作戦：ScratchViewsのHTMLを直接読み込み、jsviewarrayofarrayの中身を強引に抜き出す
    try:
        print("ScratchViewsからデータを抽出中...")
        view_url = "https://scratchviews.com/explore/trending"
        res = requests.get(view_url, headers=headers, timeout=10)
        
        # 正規表現で JavaScriptの配列の中身 [ "id", "title", "user", "uid" ] を探す
        # ["12345", "Title", "User", "6789"] のようなパターンにマッチさせる
        matches = re.findall(r'\["(\d+)",\s*"([^"]+)",\s*"([^"]+)",\s*"(\d+)"\]', res.text)
        
        for m_id, m_title, m_author, m_uid in matches:
            # 2025年〜2026年の作品ID（8億〜13億前後）かつ日本語が含まれる
            # IDが12億を超えているものも出てきているので範囲を広げます
            if int(m_id) > 800000000 and is_japanese(m_title):
                trending_list.append({
                    "title": m_title,
                    "author": m_author,
                    "id": int(m_id),
                    "views": 0, # Viewのデータには数値が含まれていないため0固定
                    "loves": 0,
                    "thumbnail": f"https://uploads.scratch.mit.edu/get_image/project/{m_id}_282x218.png"
                })
        print(f"解析完了: {len(trending_list)}件の日本語作品をViewから抽出しました。")
    except Exception as e:
        print(f"Viewからの抽出に失敗: {e}")

    # 万が一、Viewから取れなかった時のための公式APIバックアップ（従来の成功ルート）
    if not trending_list:
        print("公式APIからバックアップを取得します...")
        # ... (これまでのAPI取得コードをここに短縮して入れる)

    # 重複削除とソート
    unique_list = list({v['id']: v for v in trending_list}.values())
    unique_list.sort(key=lambda x: x['id'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(unique_list[:30], f, ensure_ascii=False, indent=4)
    print(f"最終保存件数: {len(unique_list[:30])}件")

if __name__ == "__main__":
    get_trending()
