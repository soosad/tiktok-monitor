import os
import yt_dlp

# 歷史記錄檔案名稱
HISTORY_FILE = "history_ids.txt"
ACCOUNTS_FILE = "accounts.txt"
VIDEOS_FILE = "all_videos.txt"

def load_history_ids():
    """載入歷史影片 ID 集合"""
    history = set()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                vid = line.strip()
                if vid:
                    history.add(vid)
    return history

def save_history_id(vid):
    """將新的影片 ID 寫入歷史記錄檔案"""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(vid + "\n")

def load_txt_lines(file_path):
    """讀取文字檔中的清單（略過空白與註解）"""
    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                item = line.strip()
                if item and not item.startswith("#"):
                    lines.append(item)
    return lines

def get_target_videos(target_url):
    """使用 yt-dlp 取得 TikTok 用戶頁面或單支影片的資訊"""
    ydl_opts = {
        'extract_flat': True,  # 僅提取清單資訊，不直接下載
        'quiet': True,
    }
    video_items = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(target_url, download=False)
            if 'entries' in result:
                for entry in result['entries']:
                    if entry:
                        # 取得影片網址或 ID
                        v_url = entry.get('url') or f"https://www.tiktok.com/@{entry.get('uploader')}/video/{entry.get('id')}"
                        v_id = str(entry.get('id'))
                        video_items.append({'id': v_id, 'url': v_url})
            elif 'id' in result:
                v_id = str(result['id'])
                video_items.append({'id': v_id, 'url': target_url})
    except Exception as e:
        print(f"[-] 抓取目標 {target_url} 失敗: {e}")
    return video_items

def download_video(video_url):
    """下載指定的 TikTok 影片"""
    ydl_opts = {
        # 'outtmpl': '%(title)s.%(ext)s', # 可自訂下載後的檔名格式
    }
    
    print(f"[*] 開始下載影片: {video_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return True
    except Exception as e:
        print(f"[-] 下載影片失敗 {video_url}: {e}")
        return False

def main():
    # 1. 載入歷史記錄
    history_ids = load_history_ids()
    print(f"[*] 目前歷史記錄中有 {len(history_ids)} 筆已下載的影片。")

    # 2. 讀取 accounts.txt 中的帳號清單與 all_videos.txt 中的指定影片
    accounts = load_txt_lines(ACCOUNTS_FILE)
    specific_videos = load_txt_lines(VIDEOS_FILE)
    
    targets = accounts + specific_videos
    print(f"[*] 總共載入了 {len(accounts)} 個監控帳號與 {len(specific_videos)} 個指定影片連結。")

    # 3. 逐一檢查目標
    for target in targets:
        print(f"[*] 正在檢查目標: {target}")
        videos = get_target_videos(target)
        
        for item in videos:
            vid = item['id']
            v_url = item['url']
            
            if vid not in history_ids:
                print(f"[+] 發現新影片！ID: {vid}")
                success = download_video(v_url)
                
                # 如果下載成功，立即加入歷史記錄並寫入檔案
                if success:
                    history_ids.add(vid)
                    save_history_id(vid)
            else:
                print(f"[-] 已存在歷史記錄中，略過: {vid}")

if __name__ == "__main__":
    main()
