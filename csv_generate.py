import os
import time
import shutil
import requests
import re
import csv

from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from video_links import VIDEO_LINKS
# === AYARLAR ===
#VIDEO_LINKS = [
#    "https://drive.google.com/file/d/1eUiQwGdoh_vHDjhQsZPfnuHMldSEDwgR/view"
#]
PROFILE_DIR = "./chrome-profile"
FLAG_FILE = "use_profile.flag"
OUTPUT_DIR = "downloads"
OUTPUT_CSV = "media_links.csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

USE_SAVED_PROFILE = os.path.exists(FLAG_FILE)

# === ARAÇ FONKSİYONLARI ===

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def extract_title(driver):
    try:
        title = driver.title.replace(" - Google Drive", "").strip()
        return sanitize_filename(title)
    except:
        return "untitled"

def temizle_url(url, silinecek_parametreler):
    parsed_url = urlparse(url)
    query_params = parse_qsl(parsed_url.query)
    filtrelenmis_params = [(k, v) for k, v in query_params if k not in silinecek_parametreler]
    yeni_sorgu = urlencode(filtrelenmis_params)
    return urlunparse(parsed_url._replace(query=yeni_sorgu))

from tqdm import tqdm
def download_video(video_url, headers, cookies, filename):
    if os.path.exists(filename):
        print(f"✅ Zaten var, atlanıyor: {filename}")
        return

    print(f"⬇️ İndiriliyor: {filename}")
    session = requests.Session()
    silinecekler = ["range", "ump"]
    video_url = temizle_url(video_url, silinecekler)

    for name, value in cookies.items():
        session.cookies.set(name, value)

    headers = dict(headers)
    headers.pop('Content-Length', None)
    headers.pop('Host', None)
    headers['Referer'] = 'https://drive.google.com/'
    
    with session.get(video_url, headers=headers, stream=True) as r:
        print(f"📥 HTTP Status: {r.status_code}")
        print(f"📦 Content-Length: {r.headers.get('Content-Length')}")
        print(f"📂 Content-Type: {r.headers.get('Content-Type')}")
        content_type = r.headers.get('Content-Type')
        if "video" in content_type or "audio" in content_type:
            total = int(r.headers.get('Content-Length', 0))
            downloaded = 0
            progress = tqdm(total=total, unit='B', unit_scale=True, desc=f"⬇️ {os.path.basename(filename)}")
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total) * 100 if total else 0
                        progress.update(len(chunk))
            progress.close()
            print("✅ İndirme tamamlandı.")
            return "OK"
        else:
            print(f"❌ İndirme tamamlanamadı: {filename} geçerli bir medya değil! Content-Type: {content_type}")
            return "TryAgain"



# === SELENIUM ===
import os
import shutil
import stat

def safe_rmtree(path):
    def onerror(func, path, exc_info):
        try:
            if not os.access(path, os.W_OK):
                # Dosya varsa ve yazılabilir değilse izin ver, sonra tekrar sil
                if os.path.exists(path):
                    os.chmod(path, stat.S_IWUSR)
                    func(path)
        except Exception as e:
            print(f"Dosya silme hatası atlandı: {path} -> {e}")
    if os.path.exists(path):
        shutil.rmtree(path, onerror=onerror)


def setup_driver():
    USE_SAVED_PROFILE = os.path.exists(FLAG_FILE)
    if not USE_SAVED_PROFILE and os.path.exists(PROFILE_DIR):
        print("🧹 Eski kullanıcı profili siliniyor...")
        if os.path.exists(PROFILE_DIR):
            safe_rmtree(PROFILE_DIR)

    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument(f"--user-data-dir={os.path.abspath(PROFILE_DIR)}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=300,600")

    seleniumwire_options = {'disable_encoding': True}
    driver = uc.Chrome(options=options, seleniumwire_options=seleniumwire_options)
    driver.requests.clear()
    return driver

def wait_for_login(driver, timeout=120):
    print("🔐 Elle giriş yapmanız bekleniyor...")
    WebDriverWait(driver, timeout).until(
        lambda d: (
            "accounts.google.com" not in d.current_url.lower()
            and "signin" not in d.current_url
            and "drive.google.com" in d.current_url
        )
    )
    print("✅ Giriş başarılı, profil kaydediliyor.")
    open(FLAG_FILE, "w").close()

def click_play_button(driver):
    try:
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            print("➡️ iframe'e geçildi.")
        except:
            print("ℹ️ iframe bulunamadı, geçilmeyecek.")

        actions = ActionChains(driver)
        actions.send_keys('k').perform()
        actions.send_keys('m').perform()
        print("🎬 'k' ve 'm' tuşlarına basıldı (oynat/duraklat).")
        return True
    except Exception as e:
        print(f"⛔ Oynatma işlemi başarısız: {e}")
        return False

def wait_for_media_requests(driver, timeout=50):
    print("⏳ Medya akışları aranıyor (video ve ses)...")
    start_time = time.time()
    video_url, audio_url = None, None
    headers, cookies = None, None

    while time.time() - start_time < timeout:
        for request in driver.requests:
            if not request.response or "videoplayback" not in request.url:
                continue
            if "itag=136" in request.url and not video_url:
                video_url = request.url
            elif "itag=140" in request.url and not audio_url:
                audio_url = request.url

            if video_url and audio_url:
                cookies_list = driver.get_cookies()
                cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
                headers = dict(request.headers)
                return video_url, audio_url, headers, cookies
        time.sleep(1)

    print("❌ Tüm medya akışları bulunamadı.")
    return video_url, audio_url, headers, cookies

import subprocess

def birlestir_ses_goruntu(video_path, audio_path, output_path):
    print("🎞️ FFmpeg ile birleştirme işlemi başlatılıyor...")
    try:
        cmd = [
            "ffmpeg",
            "-y",  # Üzerine yaz
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_path
        ]
        #subprocess.run(cmd, check=True)
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            print("✅ Birleştirme tamamlandı.")
            try:
                os.remove(audio_path)
                os.remove(video_path)
                print("🧹 Geçici dosyalar silindi.")
            except Exception as e:
                print(f"⚠️ Dosya silme hatası: {e}")
        else:
            print("❌ Birleştirme işlemi başarısız oldu.")
    except Exception as ee:
            print(f"❌ Birleştirme işlemi başarısız oldu: {ee}")


# === ANA FONKSİYONUN GÜNCELLENMİŞ HALİ ===
def restart_driver(driver=None):
    if driver:
        try:
            driver.quit()
        except:
            pass
    os.system("taskkill /f /im chromedriver.exe")
    os.system("taskkill /f /im chrome.exe")
    time.sleep(2)
    return setup_driver()


def append_to_csv(data):
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["original_url", "media_type", "videoplayback_url", "output_filename"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

from selenium.webdriver.support.ui import WebDriverWait

def wait_for_page_load(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_video_ready(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@aria-label="Resmi önizle"]')
        )
    )
def wait_for_video_started(driver, timeout=60):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@aria-label="Video oynatıcı"]')
        )
    )

def main():
    driver = setup_driver()

    if not USE_SAVED_PROFILE:
        driver.get("https://drive.google.com/drive/my-drive")
        wait_for_login(driver)
    rows = []
    for idx, url in enumerate(VIDEO_LINKS, 1):
        print(f"\n[{idx}/{len(VIDEO_LINKS)}] İşleniyor: {url}")
        if (idx - 1) % 15 == 0:
            print("🧹 Cookie'ler siliniyor...")
            driver.delete_all_cookies()
        driver = restart_driver(driver)
        time.sleep(1)
        driver.get(url)
        wait_for_page_load(driver)
        wait_for_video_ready(driver)
        time.sleep(2)
        click_play_button(driver)
        #wait_for_video_started(driver)
        time.sleep(5)
        video_url, audio_url, headers, cookies = wait_for_media_requests(driver)
        title = extract_title(driver)
        if video_url:
            append_to_csv({
                "original_url": url,
                "media_type": "video",
                "videoplayback_url": video_url,
                "output_filename": f"{title}.mp4"
            })
        else:
            append_to_csv({
                "original_url": url,
                "media_type": "None",
                "videoplayback_url": "None",
                "output_filename": f"{title}.mp4"
            })
            """rows.append({
                "original_url": url,
                "media_type": "video",
                "videoplayback_url": video_url,
                "output_filename": f"{title}.mp4"
            })"""
        if audio_url:
            append_to_csv({
                "original_url": url,
                "media_type": "audio",
                "videoplayback_url": audio_url,
                "output_filename": f"{title}.m4a"
            })
        else:
            append_to_csv({
                "original_url": url,
                "media_type": "None",
                "videoplayback_url": "None",
                "output_filename": f"{title}.m4a"
            })
            """rows.append({
                "original_url": url,
                "media_type": "audio",
                "videoplayback_url": audio_url,
                "output_filename": f"{title}.m4a"
            })"""
            

    driver.quit()
    
    print("\n🏁 Tüm işlemler tamamlandı.")


if __name__ == "__main__":
    main()