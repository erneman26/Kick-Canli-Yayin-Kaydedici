import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import datetime
import os
import time
import requests
import sys
import traceback
import ctypes
import json
import webbrowser
from PIL import Image, ImageTk
import io
import math

# ---------- VERSİYON ----------
VERSION = "v1.0"
GITHUB_USERNAME = "erneman26"                    # <-- Senin kullanıcı adın
REPO_NAME = "Kick-Canli-Yayin-Kaydedici"         # <-- Doğru repo adı 
VERSION_CHECK_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/version.json"

# ---------- KONSOL RENKLERİ ----------
class Renkler:
    KIRMIZI = '\033[91m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    MOR = '\033[95m'
    TURKUAZ = '\033[96m'
    BEYAZ = '\033[97m'
    BOLD = '\033[1m'
    SON = '\033[0m'

# ---------- KONSOL AÇILIŞ MESAJI ----------
print(Renkler.BOLD + Renkler.TURKUAZ + "\n" + "="*70)
print(f"                    KICK CANLI YAYIN KAYDEDİCİ {VERSION}")
print("="*70)
print(Renkler.SARI + "╔════════════════════════════════════════════════════════╗")
print("║     ⚠  BU PENCEREYİ KAPATMAYIN!  ⚠                       ║")
print("║                                                          ║")
print("║     Bu siyah pencere (CMD) programın çalışması için      ║")
print("║     gereklidir. Kapatırsanız KAYIT DURUR!               ║")
print("╚════════════════════════════════════════════════════════╝" + Renkler.SON)
print(Renkler.BEYAZ + "-"*70)
print("▶ CMD'yi simge durumuna küçültebilirsiniz")
print("▶ Programı kapatmak için arayüzdeki DURDUR butonunu kullanın")
print("▶ Hata durumunda 'hata_log.txt' dosyasını kontrol edin")
print(Renkler.TURKUAZ + "="*70 + Renkler.SON)
print("")
print(Renkler.YESIL + "Program başlatılıyor... Lütfen bekleyin." + Renkler.SON)
print("")

# Konsol başlığını değiştir
try:
    ctypes.windll.kernel32.SetConsoleTitleW(f"Kick Canlı Yayın Kaydedici {VERSION} - BU PENCEREYİ KAPATMAYIN!")
except:
    pass

# Tema ayarı
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

recording = False
process = None
start_time = None
shutdown_after = False
close_app_after = False
was_recording = False
current_filename = None
internet_offline = False
reconnect_attempts = 0
max_reconnect_attempts = 10

# ---------- TİK ANİMASYONLU CHECKBOX SINIFI ----------
class TickAnimatedCheckbox(ctk.CTkFrame):
    def __init__(self, master, text, variable, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.variable = variable
        self.command = command
        self.animation_progress = 0
        self.is_animating = False
        
        # Ana frame
        self.check_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.check_frame.pack(anchor="w")
        
        # Checkbox kutusu için canvas
        self.canvas = ctk.CTkCanvas(
            self.check_frame, 
            width=25, 
            height=25, 
            bg='#2b2b2b', 
            highlightthickness=1,
            highlightcolor='#3b3b3b'
        )
        self.canvas.pack(side="left", padx=(0, 10))
        
        # Kutu çiz
        self.draw_box()
        
        # Yazı
        self.label = ctk.CTkLabel(
            self.check_frame, 
            text=text,
            font=("Arial", 13)
        )
        self.label.pack(side="left")
        
        # Click event
        self.canvas.bind("<Button-1>", self.toggle_with_animation)
        self.label.bind("<Button-1>", self.toggle_with_animation)
        
        # Başlangıç durumu
        if self.variable.get():
            self.draw_tick(instant=True)
    
    def draw_box(self):
        self.canvas.create_rectangle(
            2, 2, 23, 23, 
            outline='#4b4b4b', 
            fill='#2b2b2b',
            width=2,
            tags="box"
        )
    
    def draw_tick(self, instant=False):
        self.canvas.delete("tick")
        if self.variable.get() or instant:
            # Tik işareti çiz (✓)
            self.canvas.create_line(
                6, 13, 11, 18, 19, 7,
                fill='#4CAF50',
                width=3,
                tags="tick"
            )
    
    def toggle_with_animation(self, event=None):
        self.variable.set(not self.variable.get())
        self.start_animation()
        if self.command:
            self.command()
    
    def start_animation(self):
        self.is_animating = True
        self.animation_progress = 0
        self.animate()
    
    def animate(self):
        if not self.is_animating:
            return
        
        self.animation_progress += 20
        
        if self.variable.get():  # Seçiliyor
            # Tik büyüme animasyonu
            scale = min(1.0, self.animation_progress / 100)
            self.canvas.delete("tick")
            
            # Ölçeklendirilmiş tik çiz
            if scale > 0:
                # Tik koordinatları (merkez = 12.5, 12.5)
                points = [
                    (6, 13), (11, 18), (19, 7)
                ]
                # Merkeze göre ölçekle
                scaled_points = []
                for x, y in points:
                    # Merkeze göre konumlandır
                    cx, cy = 12.5, 12.5
                    nx = cx + (x - cx) * scale
                    ny = cy + (y - cy) * scale
                    scaled_points.extend([nx, ny])
                
                self.canvas.create_line(
                    *scaled_points,
                    fill='#4CAF50',
                    width=max(1, int(3 * scale)),
                    tags="tick",
                    smooth=True,
                    capstyle='round',
                    joinstyle='round'
                )
            
            if self.animation_progress >= 100:
                self.is_animating = False
                self.draw_tick(instant=True)
            else:
                self.after(30, self.animate)
                
        else:  # Seçili değil duruma geçiyor
            # Tik küçülme animasyonu
            scale = max(0, 1.0 - (self.animation_progress / 100))
            self.canvas.delete("tick")
            
            if scale > 0:
                # Ölçeklendirilmiş tik çiz
                points = [
                    (6, 13), (11, 18), (19, 7)
                ]
                scaled_points = []
                for x, y in points:
                    cx, cy = 12.5, 12.5
                    nx = cx + (x - cx) * scale
                    ny = cy + (y - cy) * scale
                    scaled_points.extend([nx, ny])
                
                self.canvas.create_line(
                    *scaled_points,
                    fill='#4CAF50',
                    width=max(1, int(3 * scale)),
                    tags="tick",
                    smooth=True,
                    capstyle='round',
                    joinstyle='round'
                )
            
            if self.animation_progress >= 100:
                self.is_animating = False
                self.canvas.delete("tick")
            else:
                self.after(30, self.animate)
    
    def set(self, value):
        self.variable.set(value)
        if value:
            self.draw_tick(instant=True)
        else:
            self.canvas.delete("tick")

# ---------- OTOMATİK GÜNCELLEME (GITHUB) ----------
def check_for_updates():
    try:
        log("🔄 GitHub'dan güncelleme kontrol ediliyor...", "blue")
        log(f"📁 Kullanıcı: {GITHUB_USERNAME}, Proje: {REPO_NAME}", "cyan")
        
        # GitHub'dan versiyon bilgisini al
        response = requests.get(VERSION_CHECK_URL, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version", VERSION)
            download_url = data.get("download_url", f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/releases/latest")
            release_notes = data.get("release_notes", "Yeni özellikler ve iyileştirmeler")
            
            # Versiyonları karşılaştır
            if latest_version > VERSION:
                # Yeni versiyon var
                log(f"✨ YENİ VERSİYON MEVCUT: {latest_version}", "green")
                log(f"📝 Sürüm notları: {release_notes}", "cyan")
                
                # Detaylı bilgi mesajı
                update_message = (
                    f"╔════════════════════════════════════════╗\n"
                    f"║        🚀 GÜNCELLEME MEVCUT!          ║\n"
                    f"╚════════════════════════════════════════╝\n\n"
                    f"📌 Mevcut versiyon: {VERSION}\n"
                    f"✨ Yeni versiyon: {latest_version}\n\n"
                    f"📋 YENİ ÖZELLİKLER:\n"
                    f"{release_notes}\n\n"
                    f"💡 En yeni özellikleri kullanmak için güncelleyin.\n\n"
                    f"🔗 GitHub: {download_url}"
                )
                
                # Kullanıcıya sor
                result = messagebox.askyesno(
                    "🔄 GÜNCELLEME MEVCUT", 
                    update_message + "\n\nŞimdi indirme sayfasını açmak ister misiniz?",
                    icon="info"
                )
                
                if result:
                    # İndirme sayfasını aç
                    webbrowser.open(download_url)
                    log(f"⬇ GitHub indirme sayfası açıldı: {download_url}", "cyan")
                    messagebox.showinfo(
                        "✅ İşlem Tamam",
                        "İndirme sayfası tarayıcınızda açıldı.\n"
                        "Yeni sürümü indirip kurabilirsiniz.",
                        icon="info"
                    )
                else:
                    log("⏰ Güncelleme daha sonraya ertelendi", "orange")
                    
            else:
                # Versiyon güncel
                log(f"✅ Uygulamanız güncel! (Versiyon: {VERSION})", "green")
                
        else:
            log("⚠ GitHub sunucusuna ulaşılamadı", "orange")
            messagebox.showwarning(
                "⚠ Uyarı",
                f"GitHub sunucusuna ulaşılamadı.\n"
                f"Kontrol: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}\n"
                f"İnternet bağlantınızı kontrol edin veya daha sonra tekrar deneyin.",
                icon="warning"
            )
            
    except requests.exceptions.Timeout:
        log("⏱ Güncelleme kontrolü zaman aşımına uğradı", "orange")
        messagebox.showerror(
            "⏱ Zaman Aşımı",
            "GitHub bağlantısı zaman aşımına uğradı.\n"
            "İnternet hızınızı kontrol edip tekrar deneyin.",
            icon="error"
        )
    except requests.exceptions.ConnectionError:
        log("🌐 İnternet bağlantısı olmadığı için güncelleme kontrol edilemedi", "orange")
        messagebox.showerror(
            "🌐 Bağlantı Hatası",
            "İnternet bağlantınız olmadığı için güncelleme kontrol edilemedi.\n"
            "Bağlantınızı kontrol edip tekrar deneyin.",
            icon="error"
        )
    except Exception as e:
        log(f"❌ Güncelleme kontrolü sırasında hata: {str(e)[:50]}", "red")
        log_error(f"Güncelleme hatası: {traceback.format_exc()}")

# ---------- KAYIT GEÇMİŞİ ----------
HISTORY_FILE = "kayit_gecmisi.json"

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_to_history(channel, filename, duration, size):
    history = load_history()
    history.append({
        "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kanal": channel,
        "dosya": filename,
        "sure": duration,
        "boyut": size
    })
    # Son 100 kaydı tut
    if len(history) > 100:
        history = history[-100:]
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except:
        pass

def show_history():
    history_window = ctk.CTkToplevel(root)
    history_window.title("📋 Kayıt Geçmişi")
    history_window.geometry("600x400")
    
    history = load_history()
    
    if not history:
        ctk.CTkLabel(history_window, text="Henüz kayıt yok").pack(pady=20)
    else:
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for kayit in reversed(history[-50:]):  # Son 50 kaydı göster
            kayit_frame = ctk.CTkFrame(scroll_frame)
            kayit_frame.pack(fill="x", pady=2)
            
            info = f"📺 {kayit['kanal']} | ⏱ {kayit['sure']} | 💾 {kayit['boyut']} | 📅 {kayit['tarih']}"
            ctk.CTkLabel(kayit_frame, text=info, anchor="w").pack(side="left", padx=5)

# ---------- DOSYA BOYUTU HESAPLAMA ----------
def get_file_size(filepath):
    try:
        if os.path.exists(filepath):
            size_bytes = os.path.getsize(filepath)
            if size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        return "0 KB"
    except:
        return "?"

# ---------- BOYUT GÜNCELLEYİCİ ----------
def update_file_size():
    if recording and current_filename and os.path.exists(current_filename):
        size_str = get_file_size(current_filename)
        size_label.configure(text=f"💾 Dosya boyutu: {size_str}")
    else:
        size_label.configure(text="💾 Dosya boyutu: -")
    root.after(2000, update_file_size)

# ---------- HATA LOGLAMA ----------
def log_error(error_msg):
    try:
        with open("hata_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {error_msg}\n")
            f.write("-" * 50 + "\n")
    except:
        pass

# ---------- RENKLİ LOG ----------
def log(msg, renk="beyaz"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    
    log_box.configure(state="normal")
    log_box.insert("end", f"[{now}] {msg}\n", renk)
    log_box.tag_config(renk, foreground=renk)
    log_box.configure(state="disabled")
    log_box.see("end")
    
    renk_kodlari = {
        "green": Renkler.YESIL,
        "red": Renkler.KIRMIZI,
        "orange": Renkler.SARI,
        "cyan": Renkler.TURKUAZ,
        "white": Renkler.BEYAZ,
        "blue": Renkler.MAVI,
        "purple": Renkler.MOR
    }
    
    cmd_renk = renk_kodlari.get(renk, Renkler.BEYAZ)
    print(f"{cmd_renk}[{now}] {msg}{Renkler.SON}")

# ---------- İNTERNET KONTROLÜ ----------
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

# ---------- BİLGİSAYARI KAPAT ----------
def shutdown_computer():
    global shutdown_after, was_recording
    
    log("⚠ Bilgisayar 30 saniye sonra KAPANACAK! Kayıt tamamlandı.", "purple")
    log("⏰ Kapatmayı iptal etmek için DURDUR butonuna basın!", "orange")
    
    for i in range(30, 0, -1):
        if not shutdown_after or not was_recording:
            log("✅ Bilgisayar kapatma iptal edildi!", "green")
            return
        if i % 10 == 0 or i <= 5:
            log(f"⏳ Kapatmaya {i} saniye kaldı...", "orange")
        time.sleep(1)
    
    if shutdown_after and was_recording:
        log("💻 Bilgisayar kapatılıyor... Hoşçakalın!", "purple")
        os.system("shutdown /s /t 5")

# ---------- UYGULAMAYI KAPAT ----------
def close_app():
    global close_app_after, was_recording
    
    log("⚠ Uygulama 10 saniye sonra KAPANACAK! Kayıt tamamlandı.", "purple")
    log("⏰ Kapatmayı iptal etmek için DURDUR butonuna basın!", "orange")
    
    for i in range(10, 0, -1):
        if not close_app_after or not was_recording:
            log("✅ Uygulama kapatma iptal edildi!", "green")
            return
        if i <= 3:
            log(f"⏳ Uygulama {i} saniye sonra kapanacak...", "orange")
        time.sleep(1)
    
    if close_app_after and was_recording:
        log("👋 Uygulama kapatılıyor... Hoşçakalın!", "purple")
        root.quit()
        os._exit(0)

# ---------- KALİTE BUL ----------
def find_best_quality(channel):
    try:
        result = subprocess.run(
            ["streamlink", f"https://kick.com/{channel}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Available streams:" in result.stdout:
            streams = result.stdout.split("Available streams:")[1].strip()
            if "best" in streams:
                return "best"
            elif "1080p" in streams:
                return "1080p"
            elif "720p" in streams:
                return "720p"
            elif "480p" in streams:
                return "480p"
    except:
        pass
    return "best"

# ---------- KLASÖR ----------
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, "end")
        folder_entry.insert(0, folder)
        log(f"📁 Klasör seçildi: {folder}", "green")

# ---------- TEMA DEĞİŞTİR ----------
def change_theme(choice):
    ctk.set_appearance_mode(choice)
    log(f"🎨 Tema değiştirildi: {choice}", "blue")

# ---------- TIMER ----------
def update_timer():
    if recording and start_time:
        elapsed = int(time.time() - start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        timer_label.configure(text=f"⏱ Kayıt süresi: {hrs:02}:{mins:02}:{secs:02}")
    root.after(1000, update_timer)

# ---------- ONLINE KONTROL ----------
def check_live(channel):
    global internet_offline
    
    if not check_internet():
        if not internet_offline:
            log("🌐 İnternet bağlantısı kesildi! Bekleniyor...", "orange")
            internet_offline = True
        return False
    else:
        if internet_offline:
            log("🌐 İnternet bağlantısı geri geldi!", "green")
            internet_offline = False
    
    try:
        # Yöntem 1: API
        url = f"https://kick.com/api/v2/channels/{channel}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if "livestream" in data and data["livestream"] is not None:
                    if data["livestream"].get("is_live") == True:
                        return True
                elif data.get("is_live") == True:
                    return True
        except:
            pass
        
        # Yöntem 2: Sayfa içeriği
        url = f"https://kick.com/{channel}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            html = r.text
            if '"is_live":true' in html or 'isLive":true' in html:
                return True
                
        # Yöntem 3: Streamlink
        try:
            result = subprocess.run(
                ["streamlink", f"https://kick.com/{channel}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if "Available streams:" in result.stdout:
                return True
        except:
            pass
            
        return False
        
    except Exception as e:
        log_error(f"Kontrol hatası: {str(e)}\n{traceback.format_exc()}")
        return False

# ---------- DURUM GÜNCELLE ----------
def set_status(text, color):
    status_label.configure(text=f"● {text}", text_color=color)

# ---------- SEÇENEKLERİ YÖNET ----------
def on_shutdown_toggle():
    global shutdown_after, close_app_after
    if shutdown_var.get():
        close_app_after = False
        close_app_check.set(False)
        shutdown_after = True
        log("💤 Yayın bitince bilgisayar KAPATMA özelliği AKTİF", "purple")
    else:
        shutdown_after = False

def on_close_app_toggle():
    global shutdown_after, close_app_after
    if close_app_var.get():
        shutdown_after = False
        shutdown_check.set(False)
        close_app_after = True
        log("👋 Yayın bitince uygulama KAPATMA özelliği AKTİF", "purple")
    else:
        close_app_after = False

# ---------- KAYIT DÖNGÜSÜ ----------
def record_loop():
    global recording, process, start_time, shutdown_after, close_app_after, was_recording, current_filename, reconnect_attempts

    channel = channel_entry.get().strip().lower()
    quality = quality_menu.get()
    folder = folder_entry.get()
    
    if quality == "auto":
        quality = find_best_quality(channel)
        log(f"⚙ Otomatik kalite seçildi: {quality}", "cyan")
    
    offline_counter = 0
    max_offline_checks = 3
    was_live_before = False
    reconnect_attempts = 0

    log(f"📺 Kanal: {channel}", "cyan")
    log(f"⚙ Kalite: {quality}", "cyan")
    log(f"📁 Klasör: {folder}", "cyan")
    
    if shutdown_after:
        log("💤 Yayın bitince bilgisayar KAPANACAK", "purple")
    elif close_app_after:
        log("👋 Yayın bitince uygulama KAPANACAK", "purple")
    
    log("🔄 Yayın takibi başladı...", "blue")

    while recording:
        try:
            if not check_internet():
                log("🌐 İnternet yok, 30 saniye bekleniyor...", "orange")
                time.sleep(30)
                continue
            
            is_live = check_live(channel)
            
            if not is_live:
                offline_counter += 1
                set_status("OFFLINE", "red")
                
                if offline_counter >= max_offline_checks:
                    if was_live_before:
                        if current_filename and os.path.exists(current_filename):
                            final_size = get_file_size(current_filename)
                            duration = datetime.timedelta(seconds=int(time.time() - start_time)) if start_time else "?"
                            save_to_history(channel, current_filename, str(duration), final_size)
                            log(f"📊 Kaydedilen dosya boyutu: {final_size}", "green")
                        
                        log(f"📴 Yayın sona erdi! {channel} artık offline", "orange")
                        
                        if shutdown_after and was_recording:
                            log("🔌 Bilgisayar kapatma işlemi başlatılıyor...", "purple")
                            threading.Thread(target=shutdown_computer, daemon=True).start()
                        elif close_app_after and was_recording:
                            log("👋 Uygulama kapatma işlemi başlatılıyor...", "purple")
                            threading.Thread(target=close_app, daemon=True).start()
                        
                        was_live_before = False
                        current_filename = None
                        reconnect_attempts = 0
                    
                    log(f"⏳ Yayın offline, {channel} için bekleniyor...", "orange")
                    time.sleep(15)
                else:
                    time.sleep(5)
                continue
            else:
                offline_counter = 0
                
                if not was_live_before:
                    was_live_before = True
                    was_recording = True
                    
                    log(f"🔴 CANLI YAYIN BAŞLADI! Kayıt alınıyor...", "green")
                    
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    
                    channel_folder = os.path.join(folder, channel)
                    if not os.path.exists(channel_folder):
                        os.makedirs(channel_folder)
                        log(f"📂 Kanal klasörü oluşturuldu: {channel}", "cyan")
                    
                    current_filename = os.path.join(channel_folder, f"{channel}_{now}.mp4")
                    start_time = time.time()
                    set_status("ONLINE - KAYIT", "green")
                    
                    log(f"📁 Dosya: {os.path.basename(current_filename)}", "cyan")

                    try:
                        process = subprocess.Popen([
                            "streamlink",
                            f"https://kick.com/{channel}",
                            quality,
                            "-o",
                            current_filename,
                            "--http-no-ssl-verify",
                            "--retry-streams", "5",
                            "--retry-open", "5",
                            "--hls-live-restart",
                            "--retry-max", "10"
                        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        stdout, stderr = process.communicate()
                        
                        if process.returncode != 0:
                            if "404" in stderr or "Not Found" in stderr:
                                log("⚠ Yayın kesildi, yeniden bağlanılıyor...", "orange")
                                reconnect_attempts += 1
                                if reconnect_attempts <= max_reconnect_attempts:
                                    time.sleep(5)
                                    continue
                            else:
                                log(f"❌ Streamlink hatası: {stderr[:200]}", "red")
                                log_error(f"Streamlink hatası: {stderr}")

                    except FileNotFoundError:
                        log("❌ Streamlink bulunamadı! https://streamlink.github.io/ adresinden indirin", "red")
                        messagebox.showerror("Hata", "Streamlink bulunamadı!")
                        break
                    except Exception as e:
                        log(f"❌ Kayıt hatası: {e}", "red")
                        log_error(f"Kayıt hatası: {e}\n{traceback.format_exc()}")

                    log("⏹ Yayın bitti veya kesildi", "orange")
                    
                    if current_filename and os.path.exists(current_filename):
                        final_size = get_file_size(current_filename)
                        log(f"📊 Toplam dosya boyutu: {final_size}", "green")
                    
                    start_time = None
                    timer_label.configure(text="⏱ Kayıt süresi: 00:00:00")
                    time.sleep(5)
                else:
                    set_status("ONLINE - KAYIT", "green")
                    
                    if int(time.time()) % 10 == 0 and current_filename:
                        current_size = get_file_size(current_filename)
                        log(f"📊 Anlık dosya boyutu: {current_size}", "blue")
                    
                    time.sleep(1)
                
        except Exception as e:
            log(f"❌ Döngü hatası: {e}", "red")
            log_error(f"Döngü hatası: {e}\n{traceback.format_exc()}")
            time.sleep(10)

# ---------- START ----------
def start_record():
    global recording, was_recording, current_filename

    if recording:
        log("⚠ Zaten kayıt yapılıyor", "orange")
        return

    if not channel_entry.get():
        log("❌ Lütfen kanal adı girin", "red")
        return

    if not folder_entry.get():
        log("❌ Lütfen kayıt klasörü seçin", "red")
        return

    recording = True
    was_recording = False
    current_filename = None
    log("🎬 Recorder başlatıldı - Yayın bekleniyor...", "cyan")
    set_status("YAYIN BEKLENİYOR", "orange")

    threading.Thread(target=record_loop, daemon=True).start()

# ---------- STOP ----------
def stop_record():
    global recording, process, start_time, shutdown_after, close_app_after, was_recording, current_filename

    recording = False
    was_recording = False
    
    if shutdown_after:
        shutdown_after = False
        shutdown_check.set(False)
        log("🛑 Bilgisayar kapatma iptal edildi!", "green")
    
    if close_app_after:
        close_app_after = False
        close_app_check.set(False)
        log("🛑 Uygulama kapatma iptal edildi!", "green")

    if process:
        try:
            process.terminate()
            process.kill()
            log("⏹ Kayıt durduruldu", "red")
        except:
            pass
        process = None

    if current_filename and os.path.exists(current_filename):
        final_size = get_file_size(current_filename)
        duration = datetime.timedelta(seconds=int(time.time() - start_time)) if start_time else "?"
        save_to_history(channel_entry.get().strip().lower(), current_filename, str(duration), final_size)
        log(f"📊 Kayıt durduruldu - Son dosya boyutu: {final_size}", "green")

    start_time = None
    current_filename = None
    set_status("DURDU", "gray")
    timer_label.configure(text="⏱ Kayıt süresi: 00:00:00")

# ---------- PENCERE KAPANIRKEN ----------
def on_closing():
    if recording:
        if messagebox.askyesno("Uyarı", "Kayıt devam ediyor! Gerçekten çıkmak istiyor musunuz?"):
            stop_record()
            log("👋 Program kapatılıyor...", "blue")
            print(Renkler.MAVI + "\nProgram kapatılıyor. İyi günler!" + Renkler.SON)
            root.destroy()
    else:
        log("👋 Program kapatılıyor...", "blue")
        print(Renkler.MAVI + "\nProgram kapatılıyor. İyi günler!" + Renkler.SON)
        root.destroy()

# ---------- ARAYÜZ ----------
root = ctk.CTk()
root.geometry("800x850")
root.title(f"Kick Canlı Yayın Kaydedici {VERSION} - erneman26")

# ---------- İKON AYARI ----------
def set_app_icon():
    try:
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(application_path, "kick.ico")
        
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(icon_path)
                print("✅ İkon yüklendi")
                return
            except:
                try:
                    icon_image = Image.open(icon_path)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    root.iconphoto(True, icon_photo)
                    root.icon_image = icon_photo
                    print("✅ İkon yüklendi (PIL)")
                    return
                except:
                    pass
        else:
            print(f"❌ İkon bulunamadı: {icon_path}")
    except Exception as e:
        print(f"❌ İkon hatası: {e}")

set_app_icon()
root.protocol("WM_DELETE_WINDOW", on_closing)

# Başlık
title = ctk.CTkLabel(root, text="Kick Canlı Yayın Kaydedici", font=("Arial", 24, "bold"))
title.pack(pady=10)

# Kanal
channel_entry = ctk.CTkEntry(root, placeholder_text="Kanal adı (örnek: pewdiepie)")
channel_entry.pack(pady=5, padx=20, fill="x")

# Kalite
quality_frame = ctk.CTkFrame(root)
quality_frame.pack(pady=5, padx=20, fill="x")

quality_menu = ctk.CTkOptionMenu(quality_frame, values=["auto", "best", "1080p", "720p", "480p", "360p", "audio_only"])
quality_menu.set("auto")
quality_menu.pack(side="left", padx=5)

quality_label = ctk.CTkLabel(quality_frame, text="(auto = otomatik en iyi kalite)")
quality_label.pack(side="left", padx=5)

# Klasör
folder_entry = ctk.CTkEntry(root, placeholder_text="Kayıt klasörü")
folder_entry.pack(pady=5, padx=20, fill="x")

folder_button = ctk.CTkButton(root, text="📁 Klasör seç", command=select_folder)
folder_button.pack(pady=5)

# Seçenekler
options_frame = ctk.CTkFrame(root)
options_frame.pack(pady=10, padx=20, fill="x")

info_label = ctk.CTkLabel(
    options_frame, 
    text="ℹ Sadece bir seçenek işaretlenebilir", 
    font=("Arial", 12, "italic"),
    text_color="gray70"
)
info_label.pack(anchor="w", padx=10, pady=5)

shutdown_var = ctk.BooleanVar(value=False)
close_app_var = ctk.BooleanVar(value=False)

shutdown_check = TickAnimatedCheckbox(
    options_frame, 
    text="💤 Yayın bitince bilgisayarı KAPAT", 
    variable=shutdown_var,
    command=on_shutdown_toggle
)
shutdown_check.pack(anchor="w", padx=10, pady=5)

close_app_check = TickAnimatedCheckbox(
    options_frame, 
    text="👋 Yayın bitince uygulamayı KAPAT", 
    variable=close_app_var,
    command=on_close_app_toggle
)
close_app_check.pack(anchor="w", padx=10, pady=5)

# Tema seçimi
theme_frame = ctk.CTkFrame(root)
theme_frame.pack(pady=5, padx=20, fill="x")

theme_label = ctk.CTkLabel(theme_frame, text="Tema:")
theme_label.pack(side="left", padx=5)

theme_menu = ctk.CTkOptionMenu(theme_frame, values=["dark", "light", "system"], command=change_theme)
theme_menu.set("dark")
theme_menu.pack(side="right", padx=5)

# GitHub bilgisi
github_label = ctk.CTkLabel(
    root, 
    text=f"📁 GitHub: {GITHUB_USERNAME}/{REPO_NAME}", 
    font=("Arial", 11),
    text_color="gray50"
)
github_label.pack(pady=2)

# Butonlar
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

start_button = ctk.CTkButton(button_frame, text="🚀 BAŞLAT", command=start_record, fg_color="green", width=120)
start_button.pack(side="left", padx=10)

stop_button = ctk.CTkButton(button_frame, text="⏹ DURDUR", command=stop_record, fg_color="red", width=120)
stop_button.pack(side="left", padx=10)

history_button = ctk.CTkButton(button_frame, text="📋 Geçmiş", command=show_history, width=120)
history_button.pack(side="left", padx=10)

update_button = ctk.CTkButton(
    button_frame, 
    text="🔄 Güncelleme Kontrol", 
    command=lambda: threading.Thread(target=check_for_updates, daemon=True).start(),
    fg_color="purple",
    width=140
)
update_button.pack(side="left", padx=10)

# Durum
status_label = ctk.CTkLabel(root, text="● HAZIR", text_color="gray", font=("Arial", 16))
status_label.pack(pady=5)

# Timer ve Boyut
info_frame = ctk.CTkFrame(root)
info_frame.pack(pady=5)

timer_label = ctk.CTkLabel(info_frame, text="⏱ Kayıt süresi: 00:00:00", font=("Arial", 14))
timer_label.pack(side="left", padx=10)

size_label = ctk.CTkLabel(info_frame, text="💾 Dosya boyutu: -", font=("Arial", 14))
size_label.pack(side="left", padx=10)

# Log box
log_box = ctk.CTkTextbox(root, height=250)
log_box.pack(padx=20, pady=10, fill="both", expand=True)
log_box.configure(state="disabled")

# Timer ve boyut güncellemelerini başlat
update_timer()
update_file_size()

# Güncelleme kontrolü (arka planda)
threading.Thread(target=check_for_updates, daemon=True).start()

# GUI'ye başlangıç mesajları
log(f"🎥 Kick Canlı Yayın Kaydedici {VERSION} başlatıldı", "green")
log("="*50, "white")
log(f"✅ GitHub: {GITHUB_USERNAME}/{REPO_NAME}", "purple")
log("✅ Tik animasyonlu seçenekler eklendi!", "purple")
log("✅ Otomatik kalite seçimi", "cyan")
log("✅ İnternet kopması toleransı", "cyan")
log("✅ Otomatik yeniden bağlanma", "cyan")
log("✅ Kayıt geçmişi", "cyan")
log("👉 Kanal adını girin ve BAŞLAT'a tıklayın", "cyan")

# CMD'ye son mesaj
print(Renkler.YESIL + "\n" + "-"*70)
print(f"✅ Kick Canlı Yayın Kaydedici {VERSION} başarıyla başlatıldı!")
print(f"📁 GitHub: {GITHUB_USERNAME}/{REPO_NAME}")
print("📝 Hata durumunda 'hata_log.txt' dosyasını kontrol edin")
print("-"*70 + "\n" + Renkler.SON)

root.mainloop()
