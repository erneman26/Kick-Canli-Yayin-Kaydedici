# 🎥 Kick Canlı Yayın Kaydedici

**v1.3** | Windows | Python

Kick platformundaki canlı yayınları otomatik olarak kaydeden, kullanıcı dostu ve modern arayüzlü bir program.

![Version](https://img.shields.io/badge/version-v1.3-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📥 KURULUM

### 1. Streamlink'i İndir
Programın çalışması için **Streamlink** gereklidir.  
👉 [https://streamlink.github.io/](https://streamlink.github.io/)

### 2. Kick Kaydedici'yi İndir
Sağ taraftaki **Releases** sayfasından son sürümü indir.

### 3. RAR'dan Çıkar
İndirdiğin RAR dosyasını WinRAR veya 7-Zip ile aç. İçinden çıkanlar:
- `KickCanliYayinKaydedici.exe` - Programın kendisi
- `kayit_gecmisi.json` - Kayıt geçmişi (otomatik oluşur)

### 4. Çalıştır
`KickCanliYayinKaydedici.exe` dosyasını çalıştır.

---

## ⚠ ÖNEMLİ UYARILAR

### 🖥️ CMD Penceresi
Program çalışırken arkada bir komut ekranı açık kalır. **Bu pencereyi kapatmayın!**  
İsterseniz simge durumuna küçültebilirsiniz.

### 🛡️ Windows Uyarısı
İlk çalıştırmada Windows SmartScreen uyarısı alabilirsiniz. Bu normaldir, **"Diğer bilgiler" → "Yine de çalıştır"** seçeneğini kullanabilirsiniz.

---

## 🚀 KULLANIM

| Adım | Açıklama |
|------|----------|
| 1 | Kanal adını girin (örnek: `j0mada`) |
| 2 | Kayıtların kaydedileceği klasörü seçin |
| 3 | **BAŞLAT** butonuna tıklayın |
| 4 | Program yayını bekler, başlayınca otomatik kaydeder |

> 💡 **İpucu:** Aynı buton kayıt sırasında **DURDUR** olur. Tek buton ile başlatıp durdurabilirsiniz.

---

## ✨ ÖZELLİKLER

### 🎬 KAYIT ÖZELLİKLERİ
- ✅ **Tek buton sistemi** - BAŞLAT / DURDUR aynı butonda
- ✅ **Otomatik kayıt** - Yayın başlayınca başlar, bitince durur
- ✅ **Anlık bilgi** - Kayıt süresi ve dosya boyutu gösterimi
- ✅ **Otomatik kalite seçimi** - Mevcut en iyi kaliteyi bulur
- ✅ **İnternet kopması toleransı** - Bağlantı gelince devam eder
- ✅ **Yayın bitince bilgisayarı kapatma**
- ✅ **Yayın bitince uygulamayı kapatma**

### ⭐ PROFİLLER
- ✅ **Kanal kaydetme** - Sık kullandığın kanalları profillere ekle
- ✅ **Klasör desteği** - Her kanal için farklı kayıt klasörü
- ✅ **Canlı yayın göstergesi** - 🟢 CANLI / 🔴 YAYINDA DEĞİL
- ✅ **Tek tıkla seçme** - Profile tıkla, kanal ve klasör otomatik doldurulsun
- ✅ **Seçili profil vurgusu** - Aktif profil yeşil çerçeve ile belirgin

### 📅 PLANLAYICI
- ✅ **Zamanlı kayıt** - Belirlediğin saatte otomatik kayıt başlat
- ✅ **Çoklu gün seçimi** - Hangi günlerde çalışacağını seç
- ✅ **Plan silme** - İptal etmek istediğin planları kaldır

### 🌍 DİL DESTEĞİ
- ✅ **11 dil** - Türkçe, English, Deutsch, Français, Español, Italiano, Português, Русский, 日本語, 한국어, 中文
- ✅ **Otomatik algılama** - Sistem dilini algılar, o dilde başlar

### 🎨 ARAYÜZ
- ✅ **Modern tasarım** - Yuvarlak köşeler, kart görünümü
- ✅ **Animasyonlu butonlar** - Fare üzerine gelince renk değiştirir
- ✅ **Hover efektleri** - Tüm butonlarda görsel geri bildirim
- ✅ **Karanlık / Açık tema** - Sistem temasını takip eder
- ✅ **Renkli durum çubuğu** - Kayıt durumuna göre renk değiştirir

### 📜 DİĞER
- ✅ **Kayıt geçmişi** - Daha önce kaydettiğin yayınları listeler
- ✅ **Otomatik güncelleme kontrolü** - Yeni sürüm var mı kontrol eder
- ✅ **Detaylı log sistemi** - Tüm işlemleri kaydeder

---

## 📁 DOSYA YAPISI
KickCanliYayinKaydedici.exe
profiller.json
kayit_gecmisi.json
planlar.json

---

## ❓ SIK SORULAN SORULAR

### Program neden "Streamlink bulunamadı" hatası veriyor?
Streamlink bilgisayarınızda kurulu değil. [Buradan](https://streamlink.github.io/) indirip kurun.

### CMD penceresini kapatırsam ne olur?
Kayıt durur ve program kapanır. Bu pencereyi **simge durumuna küçültmeniz** önerilir.

### 1080p seçmeme rağmen neden daha düşük kalitede kaydediyor?
Yayıncı 1080p yayın yapmıyor olabilir. Program otomatik olarak mevcut en yüksek kaliteyi bulur ve onu kullanır.

### Profillerdeki 🟢 ve 🔴 ne anlama geliyor?
- 🟢 **CANLI** - Kanal şu anda yayında
- 🔴 **YAYINDA DEĞİL** - Kanal yayında değil

### Kayıtlar nereye kaydediliyor?
Program, seçtiğiniz ana klasör içinde **kanal_adı** adında bir alt klasör oluşturur. Dosya adı formatı: `kanal_2024-01-01_12-30-00.mp4`

---

## 🔧 GELİŞTİRİCİLER İÇİN

### Gereksinimler
```bash
pip install customtkinter pillow requests schedule streamlink
