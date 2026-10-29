import yt_dlp
import os

def check_tiktok_updates():
    channels_file = "channels.txt"
    archive_file = "archive.txt"
    
    if not os.path.exists(channels_file):
        print(f"❌ 找不到 {channels_file} 檔案！")
        return

    # 1. 讀取名單並轉換成完整的 TikTok 網址
    with open(channels_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    urls = []
    for line in lines:
        if line.startswith("http"):
            urls.append(line)
        else:
            urls.append(f"https://www.tiktok.com/@{line}")

    total = len(urls)
    print(f"📋 成功載入 {total} 位主播名單，開始逐一檢查...\n")

    # 2. 設定 yt-dlp 參數
    ydl_opts = {
        'download_archive': archive_file,  # 自動記錄與比對歷史紀錄
        'playlist_end': 2,                 # 只檢查最新 2 支影片
        'skip_download': True,             # 只檢查不下載影片，省時省流量
        'quiet': True,                     # 隱藏過多冗長警告
        'no_warnings': True,
    }

    # 3. 逐一迴圈檢查，並即時印出進度
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for idx, url in enumerate(urls, 1):
            print(f"[{idx}/{total}] 正在檢查: {url}")
            try:
                ydl.extract_info(url, download=False)
            except Exception as e:
                print(f"⚠️ 檢查 {url} 時發生錯誤，跳過繼續...")

    print("\n🎉 所有名單檢查完畢！")

if __name__ == "__main__":
    check_tiktok_updates()
