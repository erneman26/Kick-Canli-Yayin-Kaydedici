# 🎬 Kick Canlı Yayın Kaydedici

<div align="center">

![Version](https://img.shields.io/badge/version-v1.4-green)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-purple)

**Kick.com canlı yayınlarını otomatik olarak kaydeden, modern arayüzlü bir masaüstü uygulaması.**

</div>

---

## 📸 Ekran Görüntüleri

> Kayıt, Planlayıcı, Profiller ve Loglar sekmeleri

---

## ✨ Özellikler

- 🔴 **Otomatik kayıt** — Yayın başlayınca otomatik kayıt, bitince durur
- 📅 **Planlayıcı** — Haftalık program ile istediğin saatte otomatik kayıt
- ⭐ **Profiller** — Sık takip ettiğin kanalları kaydet, tek tıkla seç
- 📜 **Kayıt geçmişi** — Tüm kayıtlarını tarih, süre ve boyutuyla listeler
- 🌍 **11 dil desteği** — Türkçe, English, Deutsch, Français, Español, Italiano, Português, Русский, 日本語, 한국어, 中文
- ⚙ **Kalite seçimi** — otomatik, best, 1080p, 720p, 480p
- 💻 **Yayın bitince kapat** — Bilgisayarı veya uygulamayı otomatik kapat
- 🔔 **Bildirim desteği** — Kayıt başlayınca/bitince sistem bildirimi (plyer)
- 🖥 **System tray** — Pencereyi kapatınca arka planda çalışmaya devam eder (pystray)
- 📊 **Gerçek zamanlı bilgi** — Kayıt süresi ve dosya boyutu anlık güncellenir

---

## 🚀 Kurulum

### Yöntem 1 — EXE (Önerilen)

1. [Releases](../../releases) sayfasından son sürümü indir
2. `KickRecorder_v1.4.rar` dosyasını aç
3. `KickRecorder.exe` dosyasını çalıştır

> ⚠ **streamlink** kurulu olması gerekiyor:
> ```bash
> pip install streamlink
> ```

## 📁 Dosya Yapısı

```
├── kickrecorder.exe   # Ana uygulama
├── languages.json     # 11 dil dosyası
```

---

## 🛠 Kullanım

1. **Kanal Adı** alanına Kick kullanıcı adını gir (örn: `xqc`)
2. **Kalite** seç (otomatik önerilir)
3. **Kayıt Klasörü** seç
4. **▶ BAŞLAT** butonuna bas
5. Uygulama yayını bekler, başlayınca otomatik kayıt alır

### Planlayıcı
- Kanal adı, saat (HH:MM) ve günleri seç
- **➕ Ekle** ile planı kaydet
- Belirlenen saatte uygulama otomatik kayda başlar

### Profiller
- Sık kullandığın kanalları kaydet
- Listedeki kanala **çift tıkla** → direkt kayıt başlar
- 🟢 yeşil = şu an canlı, 🔴 kırmızı = çevrimdışı

---

## ❓ Sık Sorulan Sorular

**Antivirüs uyarısı veriyor?**
> PyInstaller ile paketlenen uygulamalarda yaygın bir durum. False positive — güvenli.

**streamlink nedir?**
> Canlı yayınları kaydetmek için kullanılan açık kaynaklı bir araç. `pip install streamlink` ile kurulur.

**Kayıt nereye kaydediliyor?**
> Seçtiğin klasörün altında `kanal_adı/kanal_adı_TARIH-SAAT.mp4` formatında.

**Yayın canlı değilken ne oluyor?**
> Uygulama yayını bekler. Her 10 saniyede bir kontrol eder, yayın başlayınca otomatik kaydeder.

---

## 📝 Lisans

MIT License — dilediğin gibi kullanabilirsin.

---

<div align="center">
Geliştirici: <b>erneman26</b> &nbsp;•&nbsp; 
<a href="https://github.com/erneman26">GitHub</a>
</div>