# 📥 Google Drive Video Downloader

Google Drive üzerinde yalnızca izleme izni olan, ancak indirme izni olmayan videoları otomatik olarak indirip `.mp4` formatında birleştiren bir Python otomasyon aracıdır.

Bu proje, Google Drive videolarının oynatılması sırasında ağdan gelen video ve ses parçalarını (chunk) tespit eder, indirir ve `ffmpeg` yardımıyla birleştirerek kullanılabilir bir video dosyası oluşturur.

---

## 🚀 Özellikler

- `selenium` + `selenium-wire` ile video ve ses veri akışını yakalar
- Google Drive içindeki iframe'e geçiş yaparak otomatik oynatmayı başlatır
- Video ve sesin her bir parçasını (range chunk) toplar
- Eksik dosyaları atlayıp sadece indirilmeyenleri indirir
- `ffmpeg` ile video ve sesi birleştirerek `.mp4` çıktısı üretir
- Toplu link işleme ve durum takibi için CSV destekler

---

## 🧰 Gereksinimler

- **Python 3.8+**
- **Google Chrome (yüklenmiş olmalı)**
- **ffmpeg** (sistem PATH'ine eklenmiş olmalı)
- **pip paketleri**:
  - `selenium`
  - `selenium-wire`
  - `undetected-chromedriver`
  - `pandas`

---

## 📦 Kurulum

### 1. Projeyi klonla

```bash
git clone https://github.com/kullaniciadi/drive-video-downloader.git
cd drive-video-downloader```

### 2. Gereksinimleri yükle
```bash
pip install -r requirements.txt```
Eğer requirements.txt yoksa manuel olarak şunları yükleyin:

```bash
pip install selenium selenium-wire undetected-chromedriver pandas```
### 3. ffmpeg'i indir ve PATH'e ekle
https://ffmpeg.org/download.html

ffmpeg.exe’yi indir, örneğin C:\ffmpeg\bin klasörüne çıkar

Ortam değişkenlerine (PATH) bu klasörü ekle

## ⚙️ Kullanım
### 1. video_links.py Dosyasını Oluştur
Google Drive video bağlantılarını içeren linkleri içeren bir py dosyası oluştur
sonrasında csv_generate.py scriptini çalıştır ve tüm indirilebilir bağlatıları bir csv dosyasına kaydet

```bash
python csv_generate.py```
Bu adım:

Videoları sırayla açar

Oynatmayı tetikler

Ağdan alınan ses ve video parçalarını listeler

Bilgileri media_links.csv dosyasına yazar

2. Videoları İndir ve Birleştir
```bash
python download_videos.py```
Bu adım:

media_links.csv dosyasını okur

Her bir bağlantıya ait parçaları indirir

Parçaları ffmpeg ile birleştirir

output/ klasörüne .mp4 olarak kaydeder

## 📁 Dosya Yapısı
```bash
drive-video-downloader/
│
├── csv_generate.py         # Linkleri işler, parçaları analiz eder
├── download_videos.py      # İndirme ve birleştirme işlemleri
├── videos.csv              # İşlenmiş bağlantı bilgileri (otomatik oluşur)
├── chunks/                 # Geçici video/ses parçaları
├── output/                 # Nihai .mp4 dosyaları
└── README.md               # Bu dosya
```
## 🛠️ Sorun Giderme
❌ Chrome açılmıyor veya bağlantı sağlanamıyor
Bilgisayarında açık olan tüm Chrome/Chromedriver işlemlerini kapat

Aşağıdaki komutla undetected-chromedriver’ı güncelle:

```bash
pip install -U undetected-chromedriver```
❌ FFmpeg bulunamadı hatası
Komut satırında ffmpeg yazdığında çalışıyor olmalı

Windows için: C:\ffmpeg\bin klasörünü sistem PATH'ine eklemeyi unutma

## 🤝 Katkıda Bulun
Katkı yapmak için:

Bu repoyu forklayın 🍴

Yeni bir branch oluşturun: feature/yenilik

Geliştirmelerinizi yapıp commitleyin

Pull Request gönderin

## 📝 Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Dilediğiniz gibi kullanabilir, geliştirebilir ve paylaşabilirsiniz.

## 📫 İletişim
Herhangi bir hata veya öneri için GitHub Issues kısmından ulaşabilirsiniz.