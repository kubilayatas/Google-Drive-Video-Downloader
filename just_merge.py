import os
import subprocess

def birlestir_ses_goruntu(video_path, audio_path, output_path):
    print(f"🎞️ FFmpeg ile birleştirme başlatılıyor:\n{video_path}\n{audio_path}")
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
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            print("✅ Birleştirme tamamlandı:", output_path)
            try:
                os.remove(audio_path)
                os.remove(video_path)
                print("🧹 Geçici dosyalar silindi.")
            except Exception as e:
                print(f"⚠️ Dosya silme hatası: {e}")
        else:
            print("❌ Birleştirme işlemi başarısız oldu.")
    except Exception as ee:
        print(f"❌ Birleştirme sırasında hata: {ee}")

def ayni_isimli_dosyalari_birlestir(klasor):
    mp4_dosyalar = [f for f in os.listdir(klasor) if f.endswith(".mp4")]
    for mp4 in mp4_dosyalar:
        temel_ad = os.path.splitext(mp4)[0]
        m4a = temel_ad + ".m4a"
        video_path = os.path.join(klasor, mp4)
        audio_path = os.path.join(klasor, m4a)
        output_path = os.path.join(klasor, temel_ad + "_merged.mp4")

        if os.path.exists(audio_path):
            birlestir_ses_goruntu(video_path, audio_path, output_path)
        else:
            print(f"⚠️ Ses dosyası bulunamadı: {m4a}")

if __name__ == "__main__":
    klasor = "./downloads"  # Geçerli klasör
    ayni_isimli_dosyalari_birlestir(klasor)
