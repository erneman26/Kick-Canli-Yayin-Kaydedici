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
VERSION = "v1.2"
GITHUB_USERNAME = "erneman26"
REPO_NAME = "Kick-Canli-Yayin-Kaydedici"
VERSION_CHECK_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/version.json"

# ---------- DİL DOSYASI ----------
LANGUAGES = {
    "Türkçe": {
        "channel_placeholder": "Kanal adı",
        "quality_auto": "otomatik",
        "quality_best": "en iyi",
        "folder_placeholder": "Kayıt klasörü",
        "folder_select": "Seç",
        "shutdown_title": "KAPATMA SEÇENEKLERİ (sadece biri seçilebilir)",
        "shutdown_option": "Yayın bitince bilgisayarı kapat",
        "close_app_option": "Yayın bitince uygulamayı kapat",
        "other_title": "DİĞER AYARLAR",
        "theme_label": "Tema:",
        "theme_dark": "Koyu",
        "theme_light": "Açık",
        "theme_system": "Sistem",
        "button_start": "BAŞLAT",
        "button_stop": "DURDUR",
        "button_history": "Yayın Geçmişi",
        "button_update": "Güncelle",
        "status_ready": "HAZIR",
        "status_waiting": "YAYIN BEKLENİYOR",
        "status_online": "KAYIT",
        "status_offline": "ÇEVRİMDIŞI",
        "status_stopped": "DURDU",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Program başlatıldı",
        "log_button": "Tek buton sistemi aktif",
        "log_quality": "Otomatik kalite seçimi",
        "log_internet": "İnternet kopması toleransı",
        "log_instruction": "Kanal adını girin ve BAŞLAT'a tıklayın",
        "error_channel": "Lütfen kanal adı girin",
        "error_folder": "Lütfen kayıt klasörü seçin",
        "shutdown_active": "Yayın bitince bilgisayar KAPATMA özelliği AKTİF",
        "close_app_active": "Yayın bitince uygulama KAPATMA özelliği AKTİF",
        "shutdown_cancel": "Bilgisayar kapatma iptal edildi",
        "close_app_cancel": "Uygulama kapatma iptal edildi",
        "shutdown_warning": "Bilgisayar 30 saniye sonra KAPANACAK! Kayıt tamamlandı.",
        "close_app_warning": "Uygulama 10 saniye sonra KAPANACAK! Kayıt tamamlandı.",
        "shutdown_countdown": "Kapatmaya {} saniye kaldı...",
        "close_app_countdown": "Uygulama {} saniye sonra kapanacak...",
        "cancel_shutdown": "Kapatmayı iptal etmek için DURDUR butonuna basın!",
        "internet_lost": "İnternet bağlantısı kesildi! Bekleniyor...",
        "internet_back": "İnternet bağlantısı geri geldi!",
        "no_internet": "İnternet yok, 30 saniye bekleniyor...",
        "stream_ended": "Yayın sona erdi! {} artık çevrimdışı",
        "stream_started": "CANLI YAYIN BAŞLADI! Kayıt alınıyor...",
        "folder_created": "Kanal klasörü oluşturuldu: {}",
        "file_info": "Dosya: {}",
        "file_size": "Kaydedilen dosya boyutu: {}",
        "total_size": "Toplam dosya boyutu: {}",
        "current_size": "Anlık dosya boyutu: {}",
        "recording_stopped": "Kayıt durduruldu",
        "final_size": "Kayıt durduruldu - Son dosya boyutu: {}",
        "update_check": "Güncelleme kontrol ediliyor...",
        "update_available": "YENİ VERSİYON MEVCUT: {}",
        "update_current": "Uygulamanız güncel!",
        "update_error": "Güncelleme sunucusuna ulaşılamadı",
        "update_timeout": "Güncelleme kontrolü zaman aşımına uğradı",
        "update_connection_error": "İnternet bağlantısı olmadığı için güncelleme kontrol edilemedi",
        "update_download": "İndirme sayfası açıldı",
        "update_later": "Güncelleme daha sonraya ertelendi",
        "update_question": "Şimdi indirme sayfasını açmak ister misiniz?",
        "update_title": "GÜNCELLEME MEVCUT",
        "update_downloaded": "İndirme sayfası tarayıcınızda açıldı.",
        "update_complete": "İşlem Tamam",
        "error_streamlink": "Streamlink bulunamadı! https://streamlink.github.io/ adresinden indirin",
        "error_streamlink_title": "Hata",
        "error_generic": "Streamlink hatası: {}",
        "exit_warning": "Kayıt devam ediyor! Gerçekten çıkmak istiyor musunuz?",
        "exit_title": "Uyarı",
        "exit_message": "Program kapatılıyor...",
    }
}

# ---------- DİL DEĞİŞKENİ ----------
current_lang = "Türkçe"

def _(key):
    """Çeviri fonksiyonu"""
    return LANGUAGES[current_lang].get(key, LANGUAGES["Türkçe"].get(key, key))

def change_language(choice):
    global current_lang
    current_lang = choice
    update_ui_texts()

def update_ui_texts():
    """Tüm UI metinlerini güncelle"""
    channel_entry.configure(placeholder_text=_("channel_placeholder"))
    quality_menu.configure(values=[_("quality_auto"), "best", "1080p", "720p", "480p", "360p", "audio_only"])
    quality_menu.set(_("quality_auto"))
    quality_label.configure(text=f"({_('quality_auto')})")
    folder_entry.configure(placeholder_text=_("folder_placeholder"))
    folder_button.configure(text=_("folder_select"))
    shutdown_title.configure(text=_("shutdown_title"))
    shutdown_check.label.configure(text=_("shutdown_option"))
    close_app_check.label.configure(text=_("close_app_option"))
    other_title.configure(text=_("other_title"))
    theme_label.configure(text=_("theme_label"))
    theme_menu.configure(values=[_("theme_dark"), _("theme_light"), _("theme_system")])
    current_theme = theme_menu.get()
    if current_theme in ["Koyu", "Dark", "Dunkel", "Sombre", "Oscuro", "Scuro", "Escuro", "Тёмная", "ダーク", "다크", "深色"]:
        theme_menu.set(_("theme_dark"))
    elif current_theme in ["Açık", "Light", "Hell", "Clair", "Claro", "Chiaro", "Светлая", "ライト", "라이트", "浅色"]:
        theme_menu.set(_("theme_light"))
    else:
        theme_menu.set(_("theme_system"))
    
    if recording:
        toggle_button.configure(text=_("button_stop"))
    else:
        toggle_button.configure(text=_("button_start"))
    history_button.configure(text=_("button_history"))
    update_button.configure(text=_("button_update"))
    status_label.configure(text=f"● {_('status_ready')}")

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
    ctypes.windll.kernel32.SetConsoleTitleW(f"Kick Canlı Yayın Kaydedici {VERSION}")
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
        
        # Ana frame - arkaplanı transparan
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
            font=("Arial", 13),
            fg_color="transparent"
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

# ---------- OTOMATİK GÜNCELLEME ----------
def check_for_updates():
    try:
        log(f"🔄 {_('update_check')}", "blue")
        
        response = requests.get(VERSION_CHECK_URL, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version", VERSION)
            download_url = data.get("download_url", f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/releases/latest")
            release_notes = data.get("release_notes", "Yeni özellikler ve iyileştirmeler")
            
            if latest_version > VERSION:
                log(f"✨ {_('update_available').format(latest_version)}", "green")
                
                update_message = (
                    f"╔════════════════════════════════════════╗\n"
                    f"║        🚀 {_('update_title')}          ║\n"
                    f"╚════════════════════════════════════════╝\n\n"
                    f"📌 Mevcut versiyon: {VERSION}\n"
                    f"✨ Yeni versiyon: {latest_version}\n\n"
                    f"📋 YENİ ÖZELLİKLER:\n"
                    f"{release_notes}\n\n"
                    f"💡 {_('update_question')}"
                )
                
                result = messagebox.askyesno(
                    f"🔄 {_('update_title')}", 
                    update_message,
                    icon="info"
                )
                
                if result:
                    webbrowser.open(download_url)
                    log(f"⬇ {_('update_download')}", "cyan")
                    messagebox.showinfo(
                        f"✅ {_('update_complete')}",
                        _("update_downloaded"),
                        icon="info"
                    )
                else:
                    log(f"⏰ {_('update_later')}", "orange")
                    
            else:
                log(f"✅ {_('update_current')}", "green")
                
        else:
            log(f"⚠ {_('update_error')}", "orange")
            messagebox.showwarning(
                f"⚠ {_('update_error')}",
                _("update_error"),
                icon="warning"
            )
            
    except requests.exceptions.Timeout:
        log(f"⏱ {_('update_timeout')}", "orange")
    except requests.exceptions.ConnectionError:
        log(f"🌐 {_('update_connection_error')}", "orange")
    except Exception as e:
        log(f"❌ {_('update_error')}", "red")
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
    if len(history) > 100:
        history = history[-100:]
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except:
        pass

def show_history():
    history_window = ctk.CTkToplevel(root)
    history_window.title(f"📋 {_('button_history')}")
    history_window.geometry("600x400")
    
    history = load_history()
    
    if not history:
        ctk.CTkLabel(history_window, text="Henüz kayıt yok").pack(pady=20)
    else:
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for kayit in reversed(history[-50:]):
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
        size_label.configure(text=f"{_('filesize')} {size_str}")
    else:
        size_label.configure(text=f"{_('filesize')} -")
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
    
    log(f"⚠ {_('shutdown_warning')}", "purple")
    log(f"⏰ {_('cancel_shutdown')}", "orange")
    
    for i in range(30, 0, -1):
        if not shutdown_after or not was_recording:
            log(f"✅ {_('shutdown_cancel')}", "green")
            return
        if i % 10 == 0 or i <= 5:
            log(f"⏳ {_('shutdown_countdown').format(i)}", "orange")
        time.sleep(1)
    
    if shutdown_after and was_recording:
        log(f"💻 {_('shutdown_warning')}", "purple")
        os.system("shutdown /s /t 5")

# ---------- UYGULAMAYI KAPAT ----------
def close_app():
    global close_app_after, was_recording
    
    log(f"⚠ {_('close_app_warning')}", "purple")
    log(f"⏰ {_('cancel_shutdown')}", "orange")
    
    for i in range(10, 0, -1):
        if not close_app_after or not was_recording:
            log(f"✅ {_('close_app_cancel')}", "green")
            return
        if i <= 3:
            log(f"⏳ {_('close_app_countdown').format(i)}", "orange")
        time.sleep(1)
    
    if close_app_after and was_recording:
        log(f"👋 {_('close_app_warning')}", "purple")
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
        log(f"📁 {_('folder_select')}: {folder}", "green")

# ---------- TEMA DEĞİŞTİR ----------
def change_theme(choice):
    theme_map = {
        _("theme_dark"): "dark",
        _("theme_light"): "light",
        _("theme_system"): "system"
    }
    ctk.set_appearance_mode(theme_map.get(choice, "dark"))
    log(f"🎨 {_('theme_label')} {choice}", "blue")

# ---------- TIMER ----------
def update_timer():
    if recording and start_time:
        elapsed = int(time.time() - start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        timer_label.configure(text=f"{_('timer')} {hrs:02}:{mins:02}:{secs:02}")
    root.after(1000, update_timer)

# ---------- ONLINE KONTROL ----------
def check_live(channel):
    global internet_offline
    
    if not check_internet():
        if not internet_offline:
            log(f"🌐 {_('internet_lost')}", "orange")
            internet_offline = True
        return False
    else:
        if internet_offline:
            log(f"🌐 {_('internet_back')}", "green")
            internet_offline = False
    
    try:
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
        
        url = f"https://kick.com/{channel}"
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            html = r.text
            if '"is_live":true' in html or 'isLive":true' in html:
                return True
                
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
        log(f"💤 {_('shutdown_active')}", "purple")
    else:
        shutdown_after = False

def on_close_app_toggle():
    global shutdown_after, close_app_after
    if close_app_var.get():
        shutdown_after = False
        shutdown_check.set(False)
        close_app_after = True
        log(f"👋 {_('close_app_active')}", "purple")
    else:
        close_app_after = False

# ---------- KAYIT DÖNGÜSÜ ----------
def record_loop():
    global recording, process, start_time, shutdown_after, close_app_after, was_recording, current_filename, reconnect_attempts

    channel = channel_entry.get().strip().lower()
    quality = quality_menu.get()
    folder = folder_entry.get()
    
    if quality == _("quality_auto") or quality == "auto":
        quality = find_best_quality(channel)
        log(f"⚙ {_('quality_auto')}: {quality}", "cyan")
    
    offline_counter = 0
    max_offline_checks = 3
    was_live_before = False
    reconnect_attempts = 0

    log(f"📺 {_('channel_placeholder')}: {channel}", "cyan")
    log(f"⚙ {_('quality_auto')}: {quality}", "cyan")
    log(f"📁 {_('folder_placeholder')}: {folder}", "cyan")
    
    if shutdown_after:
        log(f"💤 {_('shutdown_active')}", "purple")
    elif close_app_after:
        log(f"👋 {_('close_app_active')}", "purple")
    
    log(f"🔄 {_('log_instruction')}", "blue")

    while recording:
        try:
            if not check_internet():
                log(f"🌐 {_('no_internet')}", "orange")
                time.sleep(30)
                continue
            
            is_live = check_live(channel)
            
            if not is_live:
                offline_counter += 1
                set_status(_("status_offline"), "red")
                
                if offline_counter >= max_offline_checks:
                    if was_live_before:
                        if current_filename and os.path.exists(current_filename):
                            final_size = get_file_size(current_filename)
                            duration = datetime.timedelta(seconds=int(time.time() - start_time)) if start_time else "?"
                            save_to_history(channel, current_filename, str(duration), final_size)
                            log(f"📊 {_('file_size').format(final_size)}", "green")
                        
                        log(f"📴 {_('stream_ended').format(channel)}", "orange")
                        
                        if shutdown_after and was_recording:
                            log(f"🔌 {_('shutdown_warning')}", "purple")
                            threading.Thread(target=shutdown_computer, daemon=True).start()
                        elif close_app_after and was_recording:
                            log(f"👋 {_('close_app_warning')}", "purple")
                            threading.Thread(target=close_app, daemon=True).start()
                        
                        was_live_before = False
                        current_filename = None
                        reconnect_attempts = 0
                    
                    log(f"⏳ {_('stream_ended').format(channel)}", "orange")
                    time.sleep(15)
                else:
                    time.sleep(5)
                continue
            else:
                offline_counter = 0
                
                if not was_live_before:
                    was_live_before = True
                    was_recording = True
                    
                    log(f"🔴 {_('stream_started')}", "green")
                    
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    
                    channel_folder = os.path.join(folder, channel)
                    if not os.path.exists(channel_folder):
                        os.makedirs(channel_folder)
                        log(f"📂 {_('folder_created').format(channel)}", "cyan")
                    
                    current_filename = os.path.join(channel_folder, f"{channel}_{now}.mp4")
                    start_time = time.time()
                    set_status(_("status_online"), "green")
                    
                    log(f"📁 {_('file_info').format(os.path.basename(current_filename))}", "cyan")

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
                                log(f"⚠ {_('stream_ended').format(channel)}", "orange")
                                reconnect_attempts += 1
                                if reconnect_attempts <= max_reconnect_attempts:
                                    time.sleep(5)
                                    continue
                            else:
                                log(f"❌ {_('error_generic').format(stderr[:200])}", "red")
                                log_error(f"Streamlink hatası: {stderr}")

                    except FileNotFoundError:
                        log(f"❌ {_('error_streamlink')}", "red")
                        messagebox.showerror(_("error_streamlink_title"), _("error_streamlink"))
                        break
                    except Exception as e:
                        log(f"❌ {_('error_generic').format(e)}", "red")
                        log_error(f"Kayıt hatası: {e}\n{traceback.format_exc()}")

                    log(f"⏹ {_('recording_stopped')}", "orange")
                    
                    if current_filename and os.path.exists(current_filename):
                        final_size = get_file_size(current_filename)
                        log(f"📊 {_('total_size').format(final_size)}", "green")
                    
                    start_time = None
                    timer_label.configure(text=f"{_('timer')} 00:00:00")
                    time.sleep(5)
                else:
                    set_status(_("status_online"), "green")
                    
                    if int(time.time()) % 10 == 0 and current_filename:
                        current_size = get_file_size(current_filename)
                        log(f"📊 {_('current_size').format(current_size)}", "blue")
                    
                    time.sleep(1)
                
        except Exception as e:
            log(f"❌ {_('error_generic').format(e)}", "red")
            log_error(f"Döngü hatası: {e}\n{traceback.format_exc()}")
            time.sleep(10)

# ---------- TEK BUTON İŞLEVİ (BAŞLAT/DURDUR) ----------
def toggle_record():
    if recording:
        stop_record()
        toggle_button.configure(text=_("button_start"), fg_color="green", state="normal")
    else:
        if not channel_entry.get():
            log(f"❌ {_('error_channel')}", "red")
            toggle_button.configure(text=_("button_start"), fg_color="green", state="normal")
            return

        if not folder_entry.get():
            log(f"❌ {_('error_folder')}", "red")
            toggle_button.configure(text=_("button_start"), fg_color="green", state="normal")
            return
            
        start_record()
        toggle_button.configure(text=_("button_stop"), fg_color="red", state="normal")

# ---------- START ----------
def start_record():
    global recording, was_recording, current_filename

    recording = True
    was_recording = False
    current_filename = None
    log(f"🎬 {_('log_start')}", "cyan")
    set_status(_("status_waiting"), "orange")

    threading.Thread(target=record_loop, daemon=True).start()

# ---------- STOP ----------
def stop_record():
    global recording, process, start_time, shutdown_after, close_app_after, was_recording, current_filename

    recording = False
    was_recording = False
    
    if shutdown_after:
        shutdown_after = False
        shutdown_check.set(False)
        log(f"🛑 {_('shutdown_cancel')}", "green")
    
    if close_app_after:
        close_app_after = False
        close_app_check.set(False)
        log(f"🛑 {_('close_app_cancel')}", "green")

    if process:
        try:
            process.terminate()
            process.kill()
            log(f"⏹ {_('recording_stopped')}", "red")
        except:
            pass
        process = None

    if current_filename and os.path.exists(current_filename):
        final_size = get_file_size(current_filename)
        duration = datetime.timedelta(seconds=int(time.time() - start_time)) if start_time else "?"
        save_to_history(channel_entry.get().strip().lower(), current_filename, str(duration), final_size)
        log(f"📊 {_('final_size').format(final_size)}", "green")

    start_time = None
    current_filename = None
    set_status(_("status_stopped"), "gray")
    timer_label.configure(text=f"{_('timer')} 00:00:00")

# ---------- PENCERE KAPANIRKEN ----------
def on_closing():
    if recording:
        if messagebox.askyesno(_("exit_title"), _("exit_warning")):
            stop_record()
            log(f"👋 {_('exit_message')}", "blue")
            print(Renkler.MAVI + f"\n{_('exit_message')}" + Renkler.SON)
            root.destroy()
    else:
        log(f"👋 {_('exit_message')}", "blue")
        print(Renkler.MAVI + f"\n{_('exit_message')}" + Renkler.SON)
        root.destroy()

# ---------- ARAYÜZ ----------
root = ctk.CTk()
root.geometry("800x800")
root.title(f"Kick Canlı Yayın Kaydedici {VERSION}")

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
title_frame = ctk.CTkFrame(root, fg_color="transparent")
title_frame.pack(pady=10)

title = ctk.CTkLabel(title_frame, text="Kick Canlı Yayın Kaydedici", font=("Arial", 24, "bold"))
title.pack()

# Dil seçimi
lang_frame = ctk.CTkFrame(root, fg_color="transparent")
lang_frame.pack(pady=5)

lang_label = ctk.CTkLabel(lang_frame, text="🌐", font=("Arial", 14))
lang_label.pack(side="left", padx=5)

lang_menu = ctk.CTkOptionMenu(
    lang_frame, 
    values=list(LANGUAGES.keys()),
    command=change_language,
    width=150
)
lang_menu.set("Türkçe")
lang_menu.pack(side="left", padx=5)

# Kanal
channel_entry = ctk.CTkEntry(root, placeholder_text=_("channel_placeholder"))
channel_entry.pack(pady=5, padx=20, fill="x")

# Kalite
quality_frame = ctk.CTkFrame(root, fg_color="transparent")
quality_frame.pack(pady=5, padx=20, fill="x")

quality_menu = ctk.CTkOptionMenu(quality_frame, values=[_("quality_auto"), "best", "1080p", "720p", "480p", "360p", "audio_only"])
quality_menu.set(_("quality_auto"))
quality_menu.pack(side="left", padx=5)

quality_label = ctk.CTkLabel(quality_frame, text=f"({_('quality_auto')})", font=("Arial", 11), text_color="gray60")
quality_label.pack(side="left", padx=5)

# Klasör
folder_frame = ctk.CTkFrame(root, fg_color="transparent")
folder_frame.pack(pady=5, padx=20, fill="x")

folder_entry = ctk.CTkEntry(folder_frame, placeholder_text=_("folder_placeholder"))
folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

folder_button = ctk.CTkButton(folder_frame, text=_("folder_select"), command=select_folder, width=60)
folder_button.pack(side="right")

# ---------- KAPATMA SEÇENEKLERİ ----------
shutdown_frame = ctk.CTkFrame(root, fg_color="transparent")
shutdown_frame.pack(pady=10, padx=20, fill="x")

shutdown_title = ctk.CTkLabel(
    shutdown_frame, 
    text=_("shutdown_title"), 
    font=("Arial", 13, "bold"),
    text_color="orange"
)
shutdown_title.pack(anchor="w", padx=5, pady=5)

shutdown_var = ctk.BooleanVar(value=False)
close_app_var = ctk.BooleanVar(value=False)

shutdown_check = TickAnimatedCheckbox(
    shutdown_frame, 
    text=_("shutdown_option"), 
    variable=shutdown_var,
    command=on_shutdown_toggle
)
shutdown_check.pack(anchor="w", padx=15, pady=2)

close_app_check = TickAnimatedCheckbox(
    shutdown_frame, 
    text=_("close_app_option"), 
    variable=close_app_var,
    command=on_close_app_toggle
)
close_app_check.pack(anchor="w", padx=15, pady=2)

# ---------- DİĞER AYARLAR ----------
other_frame = ctk.CTkFrame(root, fg_color="transparent")
other_frame.pack(pady=10, padx=20, fill="x")

other_title = ctk.CTkLabel(
    other_frame, 
    text=_("other_title"), 
    font=("Arial", 13, "bold"),
    text_color="gray70"
)
other_title.pack(anchor="w", padx=5, pady=5)

# Tema seçimi
theme_inner = ctk.CTkFrame(other_frame, fg_color="transparent")
theme_inner.pack(anchor="w", padx=15, pady=2)

theme_label = ctk.CTkLabel(theme_inner, text=_("theme_label"), font=("Arial", 13))
theme_label.pack(side="left", padx=5)

theme_menu = ctk.CTkOptionMenu(
    theme_inner, 
    values=[_("theme_dark"), _("theme_light"), _("theme_system")], 
    command=change_theme, 
    width=100
)
theme_menu.set(_("theme_dark"))
theme_menu.pack(side="left", padx=5)

# ---------- ANA BUTON (BAŞLAT/DURDUR) ----------
toggle_button = ctk.CTkButton(
    root, 
    text=_("button_start"), 
    command=toggle_record, 
    fg_color="green", 
    width=400,
    height=60,
    font=("Arial", 20, "bold")
)
toggle_button.pack(pady=20)

# ---------- ALT BUTONLAR ----------
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=10)

history_button = ctk.CTkButton(
    button_frame, 
    text=_("button_history"), 
    command=show_history, 
    width=120,
    height=40
)
history_button.pack(side="left", padx=5)

update_button = ctk.CTkButton(
    button_frame, 
    text=_("button_update"), 
    command=lambda: threading.Thread(target=check_for_updates, daemon=True).start(),
    fg_color="purple",
    width=100,
    height=40
)
update_button.pack(side="left", padx=5)

# Durum
status_label = ctk.CTkLabel(root, text=f"● {_('status_ready')}", text_color="gray", font=("Arial", 14))
status_label.pack(pady=5)

# Timer ve Boyut
info_frame = ctk.CTkFrame(root, fg_color="transparent")
info_frame.pack(pady=5)

timer_label = ctk.CTkLabel(info_frame, text=f"{_('timer')} 00:00:00", font=("Arial", 13))
timer_label.pack(side="left", padx=10)

size_label = ctk.CTkLabel(info_frame, text=f"{_('filesize')} -", font=("Arial", 13))
size_label.pack(side="left", padx=10)

# Log box
log_box = ctk.CTkTextbox(root, height=150)
log_box.pack(padx=20, pady=10, fill="both", expand=True)
log_box.configure(state="disabled")

# Timer ve boyut güncellemelerini başlat
update_timer()
update_file_size()

# Güncelleme kontrolü (arka planda)
threading.Thread(target=check_for_updates, daemon=True).start()

# GUI'ye başlangıç mesajları
log(f"🎥 Kick Canlı Yayın Kaydedici {VERSION} {_('log_start')}", "green")
log("="*50, "white")
log(f"✅ {_('log_button')}", "purple")
log(f"✅ {_('log_quality')}", "cyan")
log(f"✅ {_('log_internet')}", "cyan")
log(f"👉 {_('log_instruction')}", "cyan")

# CMD'ye son mesaj
print(Renkler.YESIL + "\n" + "-"*70)
print(f"✅ Kick Canlı Yayın Kaydedici {VERSION} başlatıldı")
print("-"*70 + "\n" + Renkler.SON)

root.mainloop()
