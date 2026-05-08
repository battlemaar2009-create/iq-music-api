import requests
import json

# كلمات البحث (يمكنك تغييرها لأي أسماء تريدها)
queries = ["اغاني عراقية 2026", "اغاني عربية جديدة", "تريند تيك توك"]

def fetch_music(query):
    # نستخدم سيرفرات بديلة لضمان عدم الفشل
    servers = [
        "https://pipedapi.kavin.rocks",
        "https://api.piped.dev",
        "https://pipedapi.drgns.space"
    ]
    
    for server in servers:
        url = f"{server}/search?q={query}&filter=music_songs"
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                items = r.json().get('items', [])
                if items:
                    return items
        except:
            continue
    return []

# تجميع النتائج
music_database = []
for q in queries:
    print(f"جاري البحث عن: {q}...")
    results = fetch_music(q)
    for item in results:
        # التأكد من وجود البيانات الأساسية
        if item.get('title') and item.get('url'):
            music_database.append({
                "title": item.get('title'),
                "image": item.get('thumbnail'),
                "id": item.get('url', '').split('=')[-1]
            })

# حماية: إذا كانت القائمة فارغة لا تحذف البيانات القديمة (اختياري)
if len(music_database) > 0:
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(music_database, f, ensure_ascii=False, indent=4)
    print(f"✅ تم بنجاح! تم جمع {len(music_database)} أغنية.")
else:
    print("⚠️ فشل جلب البيانات، السيرفرات قد تكون مضغوطة حالياً.")
