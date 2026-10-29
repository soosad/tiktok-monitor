import subprocess
import os

def check_tiktok_updates():
    channels_file = "channels.txt"
    archive_file = "archive.txt"
    
    if not os.path.exists(channels_file):
        print(f"❌ 找不到 {channels_file} 檔案！")
        return

    # 1. 讀取名單，並自動把純帳號轉成完整的 TikTok 網址
    with open(channels_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    formatted_urls = []
    for line in lines:
        if line.startswith("http"):
            formatted_urls.append(line)
        else:
            # 如果只有帳號名稱，自動補上 TikTok 完整網址
            formatted_urls.append(f"https://www.tiktok.com/@{line}")

    # 2. 建立一個暫時的完整網址名單供 yt-dlp 讀取
    temp_batch_file = "temp_channels.txt"
    with open(temp_batch_file, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted_urls))

    print(f"📋 成功載入並轉換 {len(formatted_urls)} 位主播網址，開始檢查...")

    # 3. yt-dlp 執行指令（改讀 temp_batch_file）
    command = [
        "yt-dlp",
        "--batch-file", temp_batch_file,
        "--download-archive", archive_file,
        "--playlist-end", "2",
        "--skip-download", # 只檢查不下載影片，省時省流量
        "-o", "./downloads/%(uploader)s/%(id)s.%(ext)s"
    ]

    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
        
    # 4. 清理暫存檔
    if os.path.exists(temp_batch_file):
        os.remove(temp_batch_file)

if __name__ == "__main__":
    check_tiktok_updates()
