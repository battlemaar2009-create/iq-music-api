import json
import os
import time
from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ملف الكاش لتسريع الاستجابة
DB_FILE = "music_cache.json"

def load_cache():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")

cache = load_cache()

@app.route('/stream', methods=['GET'])
def stream():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query is missing"}), 400

    # خيارات جلب البيانات من يوتيوب (محسنة لتجاوز الحظر)
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        # إضافة User-Agent لتبدو العملية كمتصفح حقيقي
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        print(f"🔍 Searching for: {query}")
        
        with YoutubeDL(ydl_opts) as ydl:
            # البحث عن الأغنية
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                
                # بناء النتيجة
                result = {
                    "url": video.get('url'),
                    "title": video.get('title'),
                    "id": video.get('id'),
                    "timestamp": time.time() # لحساب وقت انتهاء صلاحية الرابط لاحقاً
                }
                
                # حفظ في الكاش
                cache[query] = result
                save_cache(cache)
                
                print(f"✅ Success: {video.get('title')[:30]}...")
                return jsonify(result)
            else:
                return jsonify({"error": "No results found on YouTube"}), 404

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error occurred: {error_msg}")
        # إذا كان الخطأ متعلق بالحظر (Sign in to confirm...)
        if "confirm you are not a bot" in error_msg:
            return jsonify({"error": "YouTube Bot Detection. Try changing IP or use Cookies."}), 403
        return jsonify({"error": error_msg}), 500

@app.route('/')
def index():
    return "IQ MUSIC API is Running!"

if __name__ == '__main__':
    # تأكد من قتل العمليات القديمة قبل التشغيل عبر pkill python في Termux
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
