import yt_dlp
import os
import time
import random

def check_tiktok_updates():
    channels_file = "channels.txt"
    output_report = "video_ids_report.txt"
    
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
    print(f"📋 成功載入 {total} 位主播名單，開始提取影片 ID...\n")

    # 2. 設定 yt-dlp 參數（使用 extract_flat 輕量化抓取）
    ydl_opts = {
        'extract_flat': True,      # 僅抓取列表與基本 ID，不解析完整網頁，速度快且不易被擋
        'playlist_end': 5,         # 每個主播抓取最新的 5 支影片 ID
        'quiet': True,
        'no_warnings': True,
    }

    all_results = []

    # 3. 逐一檢查並收集 ID
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for idx, url in enumerate(urls, 1):
            print(f"[{idx}/{total}] 正在檢查: {url}")
            try:
                result = ydl.extract_info(url, download=False)
                if result and 'entries' in result:
                    print(f"  └─ 成功！找到影片清單")
                    for entry in result['entries']:
                        video_id = entry.get('id')
                        video_title = entry.get('title', '無標題')
                        if video_id:
                            log_line = f"主播網址: {url} | 影片 ID: {video_id} | 標題: {video_title}"
                            all_results.append(log_line)
                            print(f"     • ID: {video_id}")
                else:
                    print(f"  └─ 該帳號無公開影片或無法解析")
            except Exception as e:
                print(f"  └─ ⚠️ 擷取失敗（被限制或帳號異常），跳過...")
            
            # 隨機暫停 3 到 6 秒，保護連線
            time.sleep(random.uniform(3.0, 6.0))

    # 4. 將統整結果寫入檔案，方便你之後下載檢視
    with open(output_report, "w", encoding="utf-8") as f:
        f.write("\n".join(all_results))

    print(f"\n🎉 檢查完畢！共成功收集到 {len(all_results)} 筆影片 ID，已儲存至 {output_report}")

if __name__ == "__main__":
    check_tiktok_updates()
