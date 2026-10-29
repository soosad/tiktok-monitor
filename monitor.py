import subprocess
import os

def check_tiktok_updates():
    channels_file = "channels.txt"
    archive_file = "archive.txt"
    
    if not os.path.exists(channels_file):
        print(f"❌ 找不到 {channels_file} 檔案！")
        return

    # 讀取名單並轉換成 yt-dlp 支援的格式
    with open(channels_file, "r", encoding="utf-8") as f:
        usernames = [line.strip() for line in f if line.strip()]

    print(f"📋 成功載入 {len(usernames)} 位主播名單，開始檢查...")

    # yt-dlp 執行指令
    command = [
        "yt-dlp",
        "--batch-file", channels_file,
        "--download-archive", archive_file,
        "--playlist-end", "2",
        "--skip-download", # 只檢查不下載影片，省時省流量
        "-o", "./downloads/%(uploader)s/%(id)s.%(ext)s"
    ]

    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    check_tiktok_updates()
