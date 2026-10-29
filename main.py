import os
import yt_dlp

# 歷史記錄檔案名稱
HISTORY_FILE = "history_ids.txt"

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

def get_channel_videos(channel_url):
    """使用 yt-dlp 取得頻道/用戶的最新影片 ID 列表（不直接下載）"""
    ydl_opts = {
        'extract_flat': True,  # 僅提取清單資訊，不下載影片
        'quiet': True,
    }
    video_ids = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            if 'entries' in result:
                for entry in result['entries']:
                    if entry and 'id' in entry:
                        video_ids.append(str(entry['id']))
            elif 'id' in result:
                video_ids.append(str(result['id']))
    except Exception as e:
        print(f"[-] 抓取頻道 {channel_url} 失敗: {e}")
    return video_ids

def download_video(video_id):
    """下載指定的影片"""
    # 範例以 YouTube 為例：組合完整網址
    # 如果你是其他平台（例如 TikTok），請將網址格式改為對應的格式，例如：
    # url = f"https://www.tiktok.com/@username/video/{video_id}"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        # 'outtmpl': '%(title)s.%(ext)s', # 你可以在這裡自訂下載後的檔名格式
    }
    
    print(f"[*] 開始下載新影片: {video_id}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"[-] 下載影片 {video_id} 失敗: {e}")
        return False

def main():
    # 1. 在這裡填入你想監控的頻道或用戶網址列表
    target_channels = [
        "https://www.youtube.com/@ExampleChannel",  # 請替換成你要抓取的目標網址
    ]

    # 2. 載入歷史記錄
    history_ids = load_history_ids()
    print(f"[*] 目前歷史記錄中有 {len(history_ids)} 筆已下載的影片。")

    # 3. 逐一檢查目標頻道
    for channel_url in target_channels:
        print(f"[*] 正在檢查頻道: {channel_url}")
        latest_ids = get_channel_videos(channel_url)
        
        for vid in latest_ids:
            if vid not in history_ids:
                print(f"[+] 發現新影片！ID: {vid}")
                success = download_video(vid)
                
                # 如果下載成功，立即加入歷史記錄並寫入檔案
                if success:
                    history_ids.add(vid)
                    save_history_id(vid)
            else:
                print(f"[-] 已存在歷史記錄中，略過: {vid}")

if __name__ == "__main__":
    main()
