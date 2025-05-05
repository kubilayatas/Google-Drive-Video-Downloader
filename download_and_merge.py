import csv
import os
import requests
import subprocess
from urllib.parse import urlparse, parse_qs

CSV_FILE = "media_links.csv"
TEMP_DIR = "temp"
OUTPUT_DIR = "output"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_file(url, out_path):
    if os.path.exists(out_path):
        print(f"✅ Zaten var: {out_path}")
        return
    print(f"⬇️  İndiriliyor: {out_path}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"📁 Kaydedildi: {out_path}")

def merge_files(video_path, audio_path, output_path):
    if os.path.exists(output_path):
        print(f"🎬 Birleşmiş dosya zaten var: {output_path}")
        return
    print(f"🛠️  Birleştiriliyor: {output_path}")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c", "copy",
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Oluşturuldu: {output_path}")

def main():
    media_map = {}
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            base_name = os.path.splitext(row["output_filename"])[0]
            media_map.setdefault(base_name, {})[row["media_type"]] = row["videoplayback_url"]

    for base_name, parts in media_map.items():
        video_path = os.path.join(TEMP_DIR, f"{base_name}_video.mp4")
        audio_path = os.path.join(TEMP_DIR, f"{base_name}_audio.m4a")
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

        if "video" in parts:
            download_file(parts["video"], video_path)
        if "audio" in parts:
            download_file(parts["audio"], audio_path)

        if os.path.exists(video_path) and os.path.exists(audio_path):
            merge_files(video_path, audio_path, output_path)
            os.remove(video_path)
            os.remove(audio_path)

if __name__ == "__main__":
    main()
