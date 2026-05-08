import requests
import json

# الكلمات التي سيبحث عنها البايثون تلقائياً
queries = ["اغاني عراقية 2026", "اغاني عربية تريند", "اغاني ريمكس"]

def get_songs(query):
    # نستخدم سيرفر وسيط (Piped) لجلب البيانات دون حظر
    url = f"https://pipedapi.kavin.rocks/search?q={query}&filter=music_songs"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('items', [])
    except:
        return []

all_songs = []
for q in queries:
    songs = get_songs(q)
    for s in songs:
        all_songs.append({
            "name": s.get('title'),
            "img": s.get('thumbnail'),
            "id": s.get('url').split('=')[-1] # نأخذ معرف الفيديو فقط
        })

# حفظ النتائج في ملف JSON
with open('database.json', 'w', encoding='utf-8') as f:
    json.dump(all_songs, f, ensure_ascii=False, indent=4)

print("تم تحديث القائمة!")
