"""
Kick Canlı Yayın Kaydedici  —  v1.4
Geliştirici : erneman26
UI          : PyQt6 + kick_widgets.py
"""

import subprocess, threading, datetime, os, time
import requests, sys, ctypes, json, webbrowser, re
import schedule, logging
from logging.handlers import RotatingFileHandler

# ── PyQt6 ────────────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QScrollArea, QFrame,
    QFileDialog, QMessageBox, QSystemTrayIcon, QMenu,
    QRadioButton, QButtonGroup, QTextEdit, QSizePolicy,
    QGraphicsOpacityEffect,
    QStackedWidget, QGridLayout,
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QPropertyAnimation,
    QEasingCurve, QPoint,
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QPainter,
    QAction,
)

# ── Kendi widget kütüphanemiz ─────────────────────────────────────────────────
from kick_widgets import HoverButton, PulseIndicator, FadeStack, AnimatedCheckBox

# ── Opsiyonel bağımlılıklar ───────────────────────────────────────────────────
try:
    from plyer import notification as _plyer_notif
    PLYER_OK = True
except ImportError:
    PLYER_OK = False

try:
    import pystray
    from PIL import Image as PilImage
    TRAY_OK = True
except ImportError:
    TRAY_OK = False

# ─── LOGGING ──────────────────────────────────────────────────────────────────
def _setup_logging() -> logging.Logger:
    logger = logging.getLogger("KickRecorder")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s  %(message)s", datefmt="%H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    fh = RotatingFileHandler("hata_log.txt", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.WARNING)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger

log = _setup_logging()

# ─── SABITLER ─────────────────────────────────────────────────────────────────
VERSION       = "v1.5"
PROFILES_FILE = "profiller.json"
HISTORY_FILE  = "kayit_gecmisi.json"
LANG_FILE     = "languages.json"
DATA_FILE     = "user_data.json"
LANG_SEL_FILE = "language.json"

# ─── KONSOL RENKLERİ ──────────────────────────────────────────────────────────
class R:
    KIRMIZI = '\033[91m'; YESIL = '\033[92m'; SARI = '\033[93m'
    MAVI    = '\033[94m'; MOR   = '\033[95m'; TURKUAZ = '\033[96m'
    BEYAZ   = '\033[97m'; BOLD  = '\033[1m';  DIM = '\033[2m'; SON = '\033[0m'

def _print_banner():
    if sys.platform == "win32":
        try: ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
        except: pass

    W = R.BEYAZ; C = R.TURKUAZ; G = R.YESIL
    Y = R.SARI;  M = R.MOR;     B = R.BOLD; S = R.SON

    W60 = "═" * 60

    print()
    # ── Logo ──────────────────────────────────────────────────────────────────
    print(f"{B}{C}  ╔{W60}╗{S}")
    print(f"{B}{C}  ║{'':^60}║{S}")
    print(f"{B}{C}  ║{'':^4}{G}██╗  ██╗██╗ ██████╗██╗  ██╗{C}{'':^4}║{S}")
    print(f"{B}{C}  ║{'':^4}{G}██║ ██╔╝██║██╔════╝██║ ██╔╝{C}{'':^4}║{S}")
    print(f"{B}{C}  ║{'':^4}{Y}█████╔╝ ██║██║     █████╔╝ {C}{'':^4}║{S}")
    print(f"{B}{C}  ║{'':^4}{Y}██╔═██╗ ██║██║     ██╔═██╗ {C}{'':^4}║{S}")
    print(f"{B}{C}  ║{'':^4}{M}██║  ██╗██║╚██████╗██║  ██╗{C}{'':^4}║{S}")
    print(f"{B}{C}  ║{'':^4}{M}╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝{C}{'':^3}║{S}")
    print(f"{B}{C}  ║{'':^60}║{S}")
    title = f"🎬  CANLI YAYIN KAYDEDİCİ  {VERSION}  by erneman26"
    print(f"{B}{C}  ║{title:^60}║{S}")
    print(f"{B}{C}  ║{'':^60}║{S}")
    print(f"{B}{C}  ╠{W60}╣{S}")
    # ── Uyarı ─────────────────────────────────────────────────────────────────
    print(f"{B}{Y}  ║{'':^60}║{S}")
    warn = "⚠   BU PENCEREYI KAPATMAYIN!   ⚠"
    print(f"{B}{Y}  ║{warn:^60}║{S}")
    print(f"{B}{Y}  ║{'':^60}║{S}")
    info1 = "Kapatırsanız aktif KAYIT DURUR!"
    info2 = "Simge durumuna küçültebilirsiniz  ✔"
    info3 = f"Hata detayları  →  hata_log.txt"
    print(f"{B}{W}  ║  • {info1:<56}║{S}")
    print(f"{B}{W}  ║  • {info2:<56}║{S}")
    print(f"{B}{W}  ║  • {info3:<56}║{S}")
    print(f"{B}{Y}  ║{'':^60}║{S}")
    print(f"{B}{C}  ╚{W60}╝{S}")
    print()
    print(f"{B}{G}  ✔  Program başlatılıyor...{S}")
    print()

_print_banner()

try:
    ctypes.windll.kernel32.SetConsoleTitleW(f"🎬 Kick Canlı Yayın Kaydedici {VERSION}")
except: pass

# ─── DİL ──────────────────────────────────────────────────────────────────────
def detect_system_language() -> str:
    try:
        if sys.platform == "win32":
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return {1055:"Türkçe",1033:"English",1031:"Deutsch",1036:"Français",
                    1034:"Español",1040:"Italiano",1046:"Português",1049:"Русский",
                    1041:"日本語",1042:"한국어",2052:"中文"}.get(lang_id,"Türkçe")
    except: pass
    return "Türkçe"

def _load_languages() -> dict:
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data:
                return data
        except Exception as e:
            log.warning(f"languages.json okunamadı: {e}")
    # Minimal fallback
    return {"Türkçe": {
        "app_title":"Kick Canlı Yayın Kaydedici","tab_record":"🎬 KAYIT",
        "tab_scheduler":"📅 PLANLAYICI","tab_profiles":"⭐ PROFİLLER",
        "tab_settings":"⚙ AYARLAR","tab_logs":"📋 LOGLAR",
        "channel_placeholder":"Kanal adı","quality_auto":"otomatik",
        "folder_placeholder":"Kayıt klasörü","folder_select":"📁 Seç",
        "shutdown_option":"Yayın bitince bilgisayarı kapat",
        "close_app_option":"Yayın bitince uygulamayı kapat",
        "button_start":"▶ BAŞLAT","button_stop":"⏹ DURDUR",
        "button_history":"📜 Geçmiş","button_update":"🔄 Güncelle",
        "status_ready":"HAZIR","status_waiting":"YAYIN BEKLENİYOR",
        "status_online":"🔴 KAYIT YAPILIYOR","status_offline":"⚫ ÇEVRİMDIŞI",
        "status_stopped":"⏸ DURDU","timer":"⏱","filesize":"💾",
        "log_start":"Program başlatıldı","scheduler_empty":"Plan yok",
        "profile_added":"✅ Profil eklendi: {}","profile_deleted":"❌ Profil silindi: {}",
        "profile_exists":"⚠ {} zaten profillerde","error_channel":"Lütfen kanal adı girin",
        "error_folder":"Lütfen kayıt klasörü seçin","error_time":"Geçersiz saat! Örnek: 14:30",
        "error_days":"En az bir gün seçin!","error_no_selection":"Bir plan seçin!",
        "shutdown_active":"Bilgisayar kapatma AKTİF","close_app_active":"Uygulama kapatma AKTİF",
        "lang_detected":"🌍 Sistem dili: {}","log_scheduler":"Planlayıcı başlatıldı",
        "log_instruction":"Kanal adını girin ve BAŞLAT'a tıklayın",
        "profiles_title":"Kayıtlı Kanallar","profile_channel":"Kanal Adı:",
        "profile_folder":"Klasör:","profile_save":"💾 Kaydet","profile_delete":"🗑 Sil",
        "theme_label":"Tema","theme_dark":"Koyu","theme_light":"Açık","theme_system":"Sistem",
        "language_label":"Dil","scheduler_channel":"Kanal","scheduler_time":"Saat",
        "scheduler_days":"Günler","scheduler_quality":"Kalite",
        "scheduler_add":"➕ Ekle","scheduler_delete":"❌ Sil",
        "scheduler_stop":"⏹ Kaydı Durdur","scheduler_list":"Planlanan Kayıtlar",
        "active_profile":"✅ SEÇİLİ","next_trigger":"Sonraki: {}",
        "notif_started":"Kayıt başladı","notif_stopped":"Kayıt tamamlandı",
        "dep_missing_title":"Eksik Bağımlılık",
        "dep_missing_msg":"Aşağıdaki araçlar bulunamadı:\n{}\n\npip install streamlink",
    }}

LANGUAGES    = _load_languages()
current_lang = detect_system_language()
try:
    with open(LANG_SEL_FILE,"r",encoding="utf-8") as _f:
        _s = json.load(_f)
        if _s.get("language") in LANGUAGES: current_lang = _s["language"]
except: pass
if current_lang not in LANGUAGES: current_lang = "Türkçe"

def _(key:str) -> str:
    return LANGUAGES[current_lang].get(key) or LANGUAGES.get("Türkçe",{}).get(key,key)

# ─── BİLDİRİM ─────────────────────────────────────────────────────────────────
def send_notification(title:str, message:str):
    if not PLYER_OK: return
    try: _plyer_notif.notify(title=title,message=message,app_name=f"Kick Recorder {VERSION}",timeout=6)
    except Exception as e: log.debug(f"Bildirim hatası: {e}")

# ─── BAĞIMLILIK KONTROLÜ ──────────────────────────────────────────────────────
def check_dependencies() -> list[str]:
    missing = []
    try:
        r = subprocess.run(["streamlink","--version"],capture_output=True,text=True,timeout=5)
        if r.returncode != 0: missing.append("streamlink")
    except (FileNotFoundError,subprocess.TimeoutExpired):
        missing.append("streamlink")
    return missing

# ─── RECORD MANAGER ───────────────────────────────────────────────────────────
class RecordManager:
    _BACKOFF_BASE = 10
    _BACKOFF_MAX  = 300

    def __init__(self, on_log, on_status, on_size, on_timer_reset, on_history_saved=None):
        self._on_log, self._on_status = on_log, on_status
        self._on_size, self._on_timer_reset = on_size, on_timer_reset
        self._on_history_saved = on_history_saved  # geçmiş kaydedilince çağrılır
        self.recording = False
        self.process: subprocess.Popen | None = None
        self.start_time: float | None = None
        self.current_filename: str | None = None
        self.was_recording = False
        self._stop_event = threading.Event()

    def check_live(self, channel:str) -> bool:
        try:
            r = requests.get(f"https://kick.com/api/v2/channels/{channel}",
                headers={"User-Agent":"Mozilla/5.0","Accept":"application/json","Referer":"https://kick.com/"},
                timeout=8)
            if r.status_code == 200:
                data = r.json()
                ls = data.get("livestream")
                if ls and ls.get("is_live"): return True
                if data.get("is_live"): return True
            r2 = requests.get(f"https://kick.com/{channel}",headers={"User-Agent":"Mozilla/5.0"},timeout=8)
            if r2.status_code==200 and ('"is_live":true' in r2.text or 'isLive":true' in r2.text): return True
            res = subprocess.run(["streamlink",f"https://kick.com/{channel}"],capture_output=True,text=True,timeout=10)
            return "Available streams:" in res.stdout
        except requests.RequestException as e:
            log.debug(f"Ağ hatası ({channel}): {e}"); return False
        except Exception as e:
            log.warning(f"Canlılık hatası ({channel}): {e}"); return False

    def find_best_quality(self, channel:str, preferred:str="best") -> str:
        try:
            res = subprocess.run(["streamlink",f"https://kick.com/{channel}"],capture_output=True,text=True,timeout=15)
            streams = []
            if "Available streams:" in res.stdout:
                section = res.stdout.split("Available streams:")[1].strip()
                for line in section.split("\n"):
                    q = line.strip().split(" ")[0].strip()
                    if q and q not in ("worst","best"): streams.append(q)
                if "best" in section or "(best)" in section: streams.insert(0,"best")
            order = ["best","1080p60","1080p","720p60","720p","480p","360p","160p"]
            sorted_s = [q for q in order if q in streams]
            auto = {"otomatik","auto","自動","자동","авто"}
            if preferred not in auto and preferred != "best":
                return preferred if preferred in streams else (sorted_s[0] if sorted_s else "best")
            return sorted_s[0] if sorted_s else "best"
        except: return "best"

    def start(self, channel:str, folder:str, quality:str, shutdown_cb=None, close_app_cb=None):
        self.recording = True
        self.was_recording = False
        self._stop_event.clear()
        threading.Thread(target=self._loop,
            args=(channel,folder,quality,shutdown_cb,close_app_cb),daemon=True).start()

    def stop(self):
        self.recording = False
        self._stop_event.set()
        proc, self.process = self.process, None
        if proc:
            try:
                proc.terminate()
                try: proc.wait(timeout=3)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
            except Exception as e: log.warning(f"Process durdurulamadı: {e}")
        self.start_time = None
        self._on_timer_reset()

    def _loop(self, channel, folder, quality, shutdown_cb, close_app_cb):
        actual = self.find_best_quality(channel, quality)
        if actual != quality:
            self._on_log(f"⚠ '{quality}' yok, '{actual}' kullanılıyor","orange")
        was_live = False; fail = 0; rec_start = None
        while self.recording:
            try:
                is_live = self.check_live(channel); fail = 0
            except Exception as e:
                fail += 1
                wait = min(self._BACKOFF_BASE*(2**(fail-1)),self._BACKOFF_MAX)
                self._on_log(f"⚠ Ağ hatası, {wait}s sonra tekrar...","orange")
                self._on_status(_("status_waiting"),"#FF9800")
                self._stop_event.wait(wait); continue

            if not is_live:
                self._on_status("⚫ ÇEVRİMDIŞI","#888888")
                if was_live:
                    was_live = False
                    self._on_log(f"📴 Yayın bitti: {channel}","orange")
                    if rec_start and self.current_filename:
                        elapsed = int(time.time()-rec_start)
                        size_mb = os.path.getsize(self.current_filename)/1_048_576 if os.path.exists(self.current_filename) else 0.0
                        self._save_history(channel,elapsed,size_mb,self.current_filename)
                        if self._on_history_saved:
                            self._on_history_saved()
                    send_notification(_("notif_stopped"),channel)
                    if self.was_recording:
                        if shutdown_cb: threading.Thread(target=shutdown_cb,daemon=True).start()
                        elif close_app_cb: threading.Thread(target=close_app_cb,daemon=True).start()
                    rec_start = None
                self._stop_event.wait(10); continue

            if not was_live:
                was_live = True; self.was_recording = True; rec_start = time.time()
                self._on_log(f"🔴 CANLI! Kayıt başlıyor: {channel}","green")
                send_notification(_("notif_started"),channel)
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                ch_folder = os.path.join(folder,channel)
                os.makedirs(ch_folder,exist_ok=True)
                self.current_filename = os.path.join(ch_folder,f"{channel}_{now}.mp4")
                self.start_time = time.time()
                self._on_status(_("status_online"),"#4CAF50")
                self._on_log(f"📁 {os.path.basename(self.current_filename)}","cyan")
                self.process = subprocess.Popen(
                    ["streamlink",f"https://kick.com/{channel}",actual,"-o",self.current_filename,"--quiet"],
                    stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                self.process.wait()
                if self.current_filename and os.path.exists(self.current_filename):
                    size = os.path.getsize(self.current_filename)/1_048_576
                    self._on_log(f"📊 Kayıt tamamlandı: {size:.2f} MB","green")
                    self._on_size(size)
                self.start_time = None
                self._stop_event.wait(5)
            else:
                self._on_status(_("status_online"),"#4CAF50")
                self._stop_event.wait(1)

    @staticmethod
    def _save_history(channel,duration_secs,size_mb,filepath):
        try:
            history = []
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE,"r",encoding="utf-8") as f: history = json.load(f)
            h,m,s = duration_secs//3600,(duration_secs%3600)//60,duration_secs%60
            history.append({"kanal":channel,"tarih":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "sure":f"{h:02}:{m:02}:{s:02}","boyut":f"{size_mb:.2f} MB","dosya":filepath})
            history = history[-200:]
            with open(HISTORY_FILE,"w",encoding="utf-8") as f: json.dump(history,f,indent=2,ensure_ascii=False)
        except Exception as e: log.warning(f"Geçmiş kaydedilemedi: {e}")

# ─── SCHEDULER MANAGER ────────────────────────────────────────────────────────
class SchedulerManager:
    _DAY_MAP = {"Pazartesi":"monday","Salı":"tuesday","Çarşamba":"wednesday",
                "Perşembe":"thursday","Cuma":"friday","Cumartesi":"saturday","Pazar":"sunday"}

    def __init__(self, trigger_cb, on_log):
        self.tasks:list = []
        self._trigger_cb = trigger_cb
        self._on_log = on_log
        self._running = False

    def start_thread(self):
        if self._running: return
        self._running = True
        self.rebuild()
        threading.Thread(target=self._run,daemon=True).start()

    def _run(self):
        while True: schedule.run_pending(); time.sleep(30)

    def rebuild(self):
        schedule.clear()
        for task in self.tasks:
            ch,ts,days = task[0],task[1],task[2]
            folder  = task[3] if len(task)>3 else ""
            quality = task[4] if len(task)>4 else "best"
            for day in days:
                eng = self._DAY_MAP.get(day)
                if eng:
                    getattr(schedule.every(),eng).at(ts).do(self._trigger_cb,ch,folder,quality)

    def next_run_str(self, idx:int) -> str:
        jobs = schedule.get_jobs()
        if idx < len(jobs):
            nr = jobs[idx].next_run
            if nr:
                delta = nr - datetime.datetime.now()
                total = int(delta.total_seconds())
                if total >= 0:
                    return f"{total//3600}s {(total%3600)//60}d"
        return ""

    def add(self,channel,time_str,days,folder="",quality="best"):
        self.tasks.append([channel,time_str,days,folder,quality]); self.rebuild()

    def remove(self,index:int):
        if 0 <= index < len(self.tasks): self.tasks.pop(index); self.rebuild()

# ─── PROFILE MANAGER ──────────────────────────────────────────────────────────
class ProfileManager:
    _CACHE_TTL = 60

    def __init__(self, on_render):
        self.profiles:list = []
        self._cache:dict   = {}
        self._on_render    = on_render
        self.active_channel:str|None = None

    def add(self,channel:str,folder:str) -> bool:
        if any(p["channel"]==channel for p in self.profiles): return False
        self.profiles.append({"channel":channel,"folder":folder}); self.save(); return True

    def remove_last(self) -> dict|None:
        if not self.profiles: return None
        removed = self.profiles.pop()
        if self.active_channel == removed["channel"]: self.active_channel = None
        self.save(); return removed

    def save(self):
        try:
            with open(PROFILES_FILE,"w",encoding="utf-8") as f:
                json.dump(self.profiles,f,indent=2,ensure_ascii=False)
        except Exception as e: log.warning(f"Profiller kaydedilemedi: {e}")

    def load(self):
        try:
            if os.path.exists(PROFILES_FILE):
                with open(PROFILES_FILE,"r",encoding="utf-8") as f:
                    self.profiles = json.load(f)
        except Exception as e: log.warning(f"Profiller yüklenemedi: {e}")

    def check_live_cached(self,channel:str,rec_mgr:"RecordManager") -> bool:
        now = time.time()
        if channel in self._cache:
            result,ts = self._cache[channel]
            if now-ts < self._CACHE_TTL: return result
        result = rec_mgr.check_live(channel)
        self._cache[channel] = (result,now); return result

    def refresh_async(self,rec_mgr:"RecordManager"):
        def _work():
            for p in self.profiles: self.check_live_cached(p["channel"],rec_mgr)
            self._on_render()
        threading.Thread(target=_work,daemon=True).start()

# ─── STYLESHEET ───────────────────────────────────────────────────────────────
APP_STYLE = """
QMainWindow, QWidget#central {
    background: #1a1a2e;
}
QWidget {
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}
/* Kart */
QFrame#card {
    background: #16213e;
    border-radius: 14px;
    border: 1px solid #0f3460;
}
/* Başlık çubuğu */
QFrame#titlebar {
    background: #0d0d1a;
    border-radius: 12px;
    border: 1px solid #1a1a3e;
}
/* Tab bar */
QTabBar::tab {
    background: #16213e;
    color: #888;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    margin: 2px 3px;
    font-weight: 500;
}
QTabBar::tab:selected {
    background: #4CAF50;
    color: white;
}
QTabBar::tab:hover:!selected {
    background: #1a2a4a;
    color: #aaa;
}
QTabWidget::pane {
    background: #1a1a2e;
    border: none;
}
/* Input */
QLineEdit {
    background: #0d0d1a;
    border: 1.5px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e0e0e0;
    font-size: 13px;
}
QLineEdit:focus {
    border-color: #4CAF50;
}
QLineEdit::placeholder {
    color: #555;
}
/* ComboBox */
QComboBox {
    background: #0d0d1a;
    border: 1.5px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e0e0e0;
    font-size: 13px;
}
QComboBox:focus { border-color: #4CAF50; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #888;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    selection-background-color: #4CAF50;
    color: #e0e0e0;
}
/* ScrollArea ve içindeki tüm widget'lar — beyaz arka planı engelle */
QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: transparent; }
QAbstractScrollArea { background: transparent; }
QAbstractScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical {
    background: #0d0d1a; width: 6px; border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #2a2a4a; border-radius: 3px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #4CAF50; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
/* TextEdit (loglar) */
QTextEdit {
    background: #0d0d1a;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    color: #c0c0c0;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    padding: 8px;
}
/* RadioButton */
QRadioButton { color: #888; spacing: 6px; }
QRadioButton::indicator {
    width: 16px; height: 16px;
    border-radius: 8px; border: 2px solid #555; background: transparent;
}
QRadioButton::indicator:checked {
    background: #4CAF50; border-color: #4CAF50;
}
/* Label */
QLabel#section-label {
    color: #4CAF50;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    margin: 0px;
    padding: 0px;
    border: none;
}
QLabel#status-label { font-size: 13px; }
QLabel#title-label  { font-size: 20px; font-weight: 700; color: #4CAF50; }
QLabel#info-bar-label { font-size: 14px; color: #aaa; }
"""

# ─── ANA PENCERE ──────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    # Thread'den UI'ya sinyal
    _sig_log    = pyqtSignal(str, str)
    _sig_status = pyqtSignal(str, str)
    _sig_size   = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{_('app_title')} {VERSION}")
        self.resize(1020, 980)
        self.setMinimumSize(900, 820)

        # ── Pencere & taskbar ikonu ───────────────────────────────────────────
        ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kick.ico")
        if not os.path.exists(ico_path):
            # PyInstaller ile paketlendiyse
            ico_path = os.path.join(getattr(sys, "_MEIPASS", ""), "kick.ico")
        if os.path.exists(ico_path):
            app_icon = QIcon(ico_path)
            self.setWindowIcon(app_icon)
            QApplication.instance().setWindowIcon(app_icon)

        # Sinyaller UI thread'ine yönlendir
        self._sig_log.connect(self._do_log)
        self._sig_status.connect(self._do_status)
        self._sig_size.connect(self._on_recording_size)

        # Yöneticiler
        self.rec_mgr = RecordManager(
            on_log           = lambda m,c: self._sig_log.emit(m,c),
            on_status        = lambda t,c: self._sig_status.emit(t,c),
            on_size          = lambda mb: self._sig_size.emit(mb),
            on_timer_reset   = lambda: self.timer_label.setText("⏱ 00:00:00"),
            on_history_saved = lambda: QTimer.singleShot(300, self._refresh_history_panel),
        )
        self.profile_mgr = ProfileManager(
            on_render = lambda: QTimer.singleShot(0, self._render_profiles)
        )
        self.sched_mgr = SchedulerManager(
            trigger_cb = self._trigger_scheduled_record,
            on_log     = lambda m,c: self._sig_log.emit(m,c),
        )

        self.shutdown_after  = False
        self.close_app_after = False
        self._tray_icon: QSystemTrayIcon | None = None

        # UI kur
        self._build_ui()

        # Veri yükle
        self.profile_mgr.load()
        self._load_user_data()
        self.sched_mgr.start_thread()

        # Bağımlılık kontrolü
        missing = check_dependencies()
        if missing:
            msg = _("dep_missing_msg").format("\n".join(f"  • {m}" for m in missing))
            QTimer.singleShot(600, lambda: QMessageBox.warning(
                self, _("dep_missing_title"), msg))
            self._do_log(f"⚠ Eksik araç: {', '.join(missing)}", "red")

        # Başlangıç logları
        self._do_log(_("lang_detected").format(current_lang), "cyan")
        self._do_log(f"🎥 {_('app_title')} {VERSION} — {_('log_start')}", "green")
        self._do_log(f"👉 {_('log_instruction')}", "cyan")

        # Timer, güncelleme, profil yenileme
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick_timer)
        self._timer.start(1000)

        self._size_timer = QTimer(self)
        self._size_timer.timeout.connect(self._tick_size)
        self._size_timer.start(2000)

        QTimer.singleShot(1000, lambda: threading.Thread(
            target=self._check_updates, daemon=True).start())
        self._schedule_profile_refresh()

        if TRAY_OK:
            self._init_tray()

    # ── UI KURULUMU ───────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(12)

        root.addWidget(self._make_title_bar())
        root.addWidget(self._make_tabs(), stretch=1)

    def _make_title_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("titlebar")
        bar.setFixedHeight(62)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(20, 0, 20, 0)

        title = QLabel(f"🎬 {_('app_title')} {VERSION}")
        title.setObjectName("title-label")
        lay.addWidget(title)
        lay.addStretch()

        # Pulse göstergesi
        self.pulse = PulseIndicator(color="#f44336", size=36)
        self.pulse.hide()
        lay.addWidget(self.pulse)

        self.status_label = QLabel(f"● {_('status_ready')}")
        self.status_label.setObjectName("status-label")
        self.status_label.setStyleSheet("color: #888; margin-left: 8px;")
        lay.addWidget(self.status_label)
        return bar

    def _make_tabs(self) -> QWidget:
        from PyQt6.QtWidgets import QTabWidget
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_record_tab(),    _("tab_record"))
        self.tabs.addTab(self._make_scheduler_tab(), _("tab_scheduler"))
        self.tabs.addTab(self._make_profiles_tab(),  _("tab_profiles"))
        self.tabs.addTab(self._make_settings_tab(),  _("tab_settings"))
        self.tabs.addTab(self._make_logs_tab(),      _("tab_logs"))
        self.tabs.currentChanged.connect(self._on_tab_changed)
        return self.tabs

    def _on_tab_changed(self, index: int) -> None:
        """
        Sekme değişince içerik yukarıdan aşağıya kayarak gelir.
        Eş zamanlı olarak fade-in de uygulanır — kayma + belirme birlikte.
        """
        widget = self.tabs.widget(index)
        if widget is None:
            return

        # ── Mevcut geometriyi al ──────────────────────────────────────────────
        final_rect = widget.geometry()

        # Başlangıç konumu: widget'ın üstünden %40 kadar yukarıda
        offset     = int(final_rect.height() * 0.40)
        start_rect = final_rect.translated(0, -offset)  # y ekseni: yukarı

        # ── Kayma animasyonu (geometry) ───────────────────────────────────────
        slide = QPropertyAnimation(widget, b"geometry")
        slide.setDuration(320)
        slide.setStartValue(start_rect)
        slide.setEndValue(final_rect)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        # ── Fade-in animasyonu (opacity) ──────────────────────────────────────
        fx = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(fx)
        fade = QPropertyAnimation(fx, b"opacity")
        fade.setDuration(320)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.Type.OutCubic)

        # ── İkisini birlikte başlat ───────────────────────────────────────────
        # widget'a bağlı tut — GC tarafından silinmesin
        widget._tab_slide = slide
        widget._tab_fade  = fade
        widget._tab_fx    = fx
        slide.start()
        fade.start()

    # ── KAYIT SEKMESİ ─────────────────────────────────────────────────────────
    def _make_record_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(20, 20, 20, 20)

        card = QFrame(); card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 20, 28, 20)
        lay.setSpacing(0)

        def slbl(text, top=14):
            lay.addSpacing(top)
            l = QLabel(text)
            l.setObjectName("section-label")
            l.setFixedHeight(16)
            l.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(l)
            lay.addSpacing(3)

        # Kanal
        slbl("📺  " + _("channel_placeholder").upper(), top=0)
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText(_("channel_placeholder"))
        self.channel_input.setFixedHeight(44)
        lay.addWidget(self.channel_input)

        # Kalite
        slbl("⚙  KALİTE")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([_("quality_auto"), "best", "1080p", "720p", "480p"])
        self.quality_combo.setFixedHeight(40)
        lay.addWidget(self.quality_combo)

        # Klasör
        slbl("📁  " + _("folder_placeholder").upper())
        fr = QWidget()
        fr.setFixedHeight(40)
        fl = QHBoxLayout(fr); fl.setContentsMargins(0,0,0,0); fl.setSpacing(8)
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText(_("folder_placeholder"))
        fl.addWidget(self.folder_input)
        btn_folder = HoverButton(_("folder_select"), base="#2196F3", hover="#1565C0", radius=8)
        btn_folder.setFixedSize(90, 40)
        btn_folder.clicked.connect(self._select_folder)
        fl.addWidget(btn_folder)
        lay.addWidget(fr)

        lay.addSpacing(6)

        # Checkbox'lar
        self.cb_shutdown  = AnimatedCheckBox(_("shutdown_option"))
        self.cb_close_app = AnimatedCheckBox(_("close_app_option"))
        self.cb_shutdown.toggled.connect(self._on_shutdown_toggle)
        self.cb_close_app.toggled.connect(self._on_close_app_toggle)
        lay.addWidget(self.cb_shutdown)
        lay.addWidget(self.cb_close_app)

        lay.addSpacing(10)

        # Ana buton
        self.toggle_btn = HoverButton(_("button_start"), base="#4CAF50", hover="#2e7d32", radius=12)
        self.toggle_btn.setFixedHeight(58)
        font = self.toggle_btn.font(); font.setPointSize(14); font.setBold(True)
        self.toggle_btn.setFont(font)
        self.toggle_btn.clicked.connect(self._toggle_record)
        lay.addWidget(self.toggle_btn)

        # Bilgi çubuğu
        info_bar = QFrame(); info_bar.setObjectName("card")
        info_bar.setFixedHeight(44)
        info_bar.setStyleSheet("QFrame#card { background: #0d0d1a; border-radius: 10px; }")
        ibl = QHBoxLayout(info_bar); ibl.setContentsMargins(16, 0, 16, 0)
        self.timer_label = QLabel("⏱ 00:00:00"); self.timer_label.setObjectName("info-bar-label")
        self.size_label  = QLabel("💾 -");        self.size_label.setObjectName("info-bar-label")
        ibl.addWidget(self.timer_label); ibl.addStretch(); ibl.addWidget(self.size_label)
        lay.addWidget(info_bar)

        # Alt buton — sadece güncelle kalıyor
        brow = QWidget(); brl = QHBoxLayout(brow); brl.setContentsMargins(0,0,0,0); brl.setSpacing(8)
        btn_upd = HoverButton(_("button_update"), base="#FF9800", hover="#e65100", radius=8)
        btn_upd.setFixedSize(130, 40)
        btn_upd.clicked.connect(lambda: threading.Thread(target=self._check_updates,daemon=True).start())
        brl.addWidget(btn_upd); brl.addStretch()
        lay.addWidget(brow)

        outer.addWidget(card)

        # ── Geçmiş Paneli — gömülü, kayıt sekmesinin altında ─────────────────
        hist_header = QWidget()
        hhl = QHBoxLayout(hist_header); hhl.setContentsMargins(4, 0, 4, 0)
        hist_lbl = QLabel("📜  KAYIT GEÇMİŞİ")
        hist_lbl.setObjectName("section-label")
        hist_lbl.setFixedHeight(16)
        hhl.addWidget(hist_lbl); hhl.addStretch()
        outer.addWidget(hist_header)

        self.hist_panel = QScrollArea()
        self.hist_panel.setWidgetResizable(True)
        self.hist_panel.setFixedHeight(160)
        self.hist_panel.setStyleSheet(
            "background:#0d0d1a; border-radius:10px; border:1px solid #1a1a3e;")
        self.hist_inner = QWidget()
        self.hist_inner.setStyleSheet("background: transparent;")
        self.hist_layout = QVBoxLayout(self.hist_inner)
        self.hist_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hist_layout.setSpacing(3)
        self.hist_layout.setContentsMargins(8, 8, 8, 8)
        self.hist_panel.setWidget(self.hist_inner)
        outer.addWidget(self.hist_panel)

        self._refresh_history_panel()
        return tab

    # ── PLANLAYICI SEKMESİ ────────────────────────────────────────────────────
    def _make_scheduler_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(20, 20, 20, 20); outer.setSpacing(10)

        card = QFrame(); card.setObjectName("card")
        lay = QVBoxLayout(card); lay.setContentsMargins(24, 16, 24, 16); lay.setSpacing(0)

        def slbl(text, top=10):
            lay.addSpacing(top)
            l = QLabel(text)
            l.setObjectName("section-label")
            l.setFixedHeight(16)
            l.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(l)
            lay.addSpacing(3)

        slbl(_("scheduler_channel"), top=0)
        self.sched_channel = QLineEdit(); self.sched_channel.setFixedHeight(38); lay.addWidget(self.sched_channel)

        slbl(_("scheduler_time"))
        self.sched_time = QLineEdit(); self.sched_time.setPlaceholderText("14:30")
        self.sched_time.setFixedHeight(38); lay.addWidget(self.sched_time)

        slbl("📁 " + _("profile_folder"))
        sfr = QWidget(); sfl = QHBoxLayout(sfr); sfl.setContentsMargins(0,0,0,0); sfl.setSpacing(8)
        self.sched_folder = QLineEdit()
        self.sched_folder.setPlaceholderText(_("folder_placeholder")); self.sched_folder.setFixedHeight(38)
        sfl.addWidget(self.sched_folder)
        btn_sf = HoverButton(_("folder_select"), base="#2196F3", hover="#1565C0", radius=8)
        btn_sf.setFixedSize(88, 38); btn_sf.clicked.connect(self._select_sched_folder)
        sfl.addWidget(btn_sf); lay.addWidget(sfr)

        slbl(_("scheduler_quality"))
        self.sched_quality = QComboBox()
        self.sched_quality.addItems([_("quality_auto"),"best","1080p","720p","480p"])
        self.sched_quality.setFixedHeight(38); lay.addWidget(self.sched_quality)

        slbl(_("scheduler_days"))
        days_w = QWidget(); days_g = QGridLayout(days_w); days_g.setContentsMargins(0,0,0,0)
        days_list = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]
        self.day_cbs: dict[str, AnimatedCheckBox] = {}
        for i, day in enumerate(days_list):
            cb = AnimatedCheckBox(day)
            self.day_cbs[day] = cb
            days_g.addWidget(cb, i//3, i%3)
        lay.addWidget(days_w)

        lay.addSpacing(6)
        brow = QWidget(); brl = QHBoxLayout(brow); brl.setContentsMargins(0,0,0,0); brl.setSpacing(8)
        btn_add = HoverButton(_("scheduler_add"),    base="#4CAF50",hover="#2e7d32",radius=8); btn_add.setFixedHeight(36); btn_add.clicked.connect(self._add_scheduled_record)
        btn_del = HoverButton(_("scheduler_delete"), base="#f44336",hover="#c62828",radius=8); btn_del.setFixedHeight(36); btn_del.clicked.connect(self._del_scheduled_record)
        btn_stp = HoverButton(_("scheduler_stop"),   base="#FF9800",hover="#e65100",radius=8); btn_stp.setFixedHeight(36); btn_stp.clicked.connect(self._stop_current_recording)
        brl.addWidget(btn_add); brl.addWidget(btn_del); brl.addWidget(btn_stp); brl.addStretch()
        lay.addWidget(brow)

        outer.addWidget(card)

        # Liste
        list_lbl = QLabel(_("scheduler_list")); list_lbl.setObjectName("section-label")
        outer.addWidget(list_lbl)
        self.sched_scroll = QScrollArea(); self.sched_scroll.setWidgetResizable(True)
        self.sched_list_widget = QWidget()
        self.sched_list_widget.setStyleSheet("background: transparent;")
        self.sched_list_layout = QVBoxLayout(self.sched_list_widget)
        self.sched_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sched_list_layout.setSpacing(4)
        self.sched_scroll.setWidget(self.sched_list_widget)
        self.sched_scroll.setStyleSheet("background: #16213e; border-radius: 10px; border: 1px solid #0f3460;")
        outer.addWidget(self.sched_scroll, stretch=1)

        self.sched_btn_group = QButtonGroup(self)
        self._selected_sched_idx = -1
        return tab

    # ── PROFİLLER SEKMESİ ─────────────────────────────────────────────────────
    def _make_profiles_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab); outer.setContentsMargins(20,20,20,20); outer.setSpacing(10)

        card = QFrame(); card.setObjectName("card")
        lay = QVBoxLayout(card); lay.setContentsMargins(24,16,24,16); lay.setSpacing(2)

        def slbl(text):
            l = QLabel(text); l.setObjectName("section-label"); lay.addWidget(l)

        slbl(_("profile_channel"))
        self.prof_channel = QLineEdit(); self.prof_channel.setFixedHeight(38); lay.addWidget(self.prof_channel)

        slbl(_("profile_folder"))
        pfr = QWidget(); pfl = QHBoxLayout(pfr); pfl.setContentsMargins(0,0,0,0); pfl.setSpacing(8)
        self.prof_folder = QLineEdit()
        self.prof_folder.setPlaceholderText(_("folder_placeholder")); self.prof_folder.setFixedHeight(38)
        pfl.addWidget(self.prof_folder)
        btn_pf = HoverButton(_("folder_select"),base="#2196F3",hover="#1565C0",radius=8)
        btn_pf.setFixedSize(88,38); btn_pf.clicked.connect(self._select_profile_folder)
        pfl.addWidget(btn_pf); lay.addWidget(pfr)

        brow = QWidget(); brl = QHBoxLayout(brow); brl.setContentsMargins(0,0,0,0); brl.setSpacing(8)
        btn_save = HoverButton(_("profile_save"),  base="#4CAF50",hover="#2e7d32",radius=8); btn_save.setFixedHeight(36); btn_save.clicked.connect(self._add_profile)
        btn_del  = HoverButton(_("profile_delete"),base="#f44336",hover="#c62828",radius=8); btn_del.setFixedHeight(36);  btn_del.clicked.connect(self._delete_profile)
        brl.addWidget(btn_save); brl.addWidget(btn_del); brl.addStretch()
        lay.addWidget(brow)
        outer.addWidget(card)

        prof_lbl = QLabel(_("profiles_title")); prof_lbl.setObjectName("section-label")
        outer.addWidget(prof_lbl)
        self.prof_scroll = QScrollArea(); self.prof_scroll.setWidgetResizable(True)
        self.prof_list_widget = QWidget()
        self.prof_list_widget.setStyleSheet("background: transparent;")
        self.prof_list_layout = QVBoxLayout(self.prof_list_widget)
        self.prof_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.prof_list_layout.setSpacing(4)
        self.prof_scroll.setWidget(self.prof_list_widget)
        self.prof_scroll.setStyleSheet("background: #16213e; border-radius: 10px; border: 1px solid #0f3460;")
        outer.addWidget(self.prof_scroll, stretch=1)
        return tab

    # ── AYARLAR SEKMESİ ───────────────────────────────────────────────────────
    def _make_settings_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab); outer.setContentsMargins(20,20,20,20); outer.setSpacing(16)

        card = QFrame(); card.setObjectName("card")
        lay = QVBoxLayout(card); lay.setContentsMargins(28,20,28,20); lay.setSpacing(16)

        # Tema
        tr = QWidget(); tl = QHBoxLayout(tr); tl.setContentsMargins(0,0,0,0)
        tl.addWidget(QLabel(_("theme_label")))
        self._theme_map = {_("theme_dark"):"dark",_("theme_light"):"light",_("theme_system"):"system"}
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(self._theme_map.keys()))
        self.theme_combo.setFixedWidth(140); self.theme_combo.currentTextChanged.connect(self._change_theme)
        tl.addWidget(self.theme_combo); tl.addStretch(); lay.addWidget(tr)

        # Dil
        lr = QWidget(); ll = QHBoxLayout(lr); ll.setContentsMargins(0,0,0,0)
        ll.addWidget(QLabel(_("language_label")))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(LANGUAGES.keys()))
        self.lang_combo.setCurrentText(current_lang)
        self.lang_combo.setFixedWidth(160); self.lang_combo.currentTextChanged.connect(self._change_language)
        ll.addWidget(self.lang_combo); ll.addStretch(); lay.addWidget(lr)

        # Hakkında
        info = QLabel(
            f"<pre style='color:#4CAF50;font-family:Consolas;font-size:12px'>"
            f"  {'─'*42}\n"
            f"  Kick Canlı Yayın Kaydedici  {VERSION}\n"
            f"  Geliştirici : erneman26\n"
            f"  GitHub      : github.com/erneman26\n"
            f"  {'─'*42}"
            f"</pre>"
        )
        info.setStyleSheet("background:#0d0d1a; border-radius:8px; padding:12px;")
        lay.addWidget(info)

        outer.addWidget(card)
        outer.addStretch()
        return tab

    # ── LOGLAR SEKMESİ ────────────────────────────────────────────────────────
    def _make_logs_tab(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab); lay.setContentsMargins(20,20,20,20)
        self.log_box = QTextEdit(); self.log_box.setReadOnly(True)
        lay.addWidget(self.log_box)
        return tab

    # ── LOG & DURUM ───────────────────────────────────────────────────────────
    def _do_log(self, msg:str, color:str="white"):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        COLOR_MAP = {
            "green":"#4CAF50","red":"#f44336","orange":"#FF9800",
            "cyan":"#00BCD4","purple":"#9C27B0","blue":"#2196F3","white":"#c0c0c0",
        }
        hex_color = COLOR_MAP.get(color,"#c0c0c0")
        level = {"red":"error","orange":"warning"}.get(color,"info")
        getattr(log, level)(msg)
        self.log_box.append(f'<span style="color:#555">[{now}]</span> <span style="color:{hex_color}">{msg}</span>')
        sb = self.log_box.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _on_recording_size(self, mb: float):
        """Kayıt boyutu güncellenince çağrılır — geçmişi de yenile."""
        self.size_label.setText(f"💾 {mb:.2f} MB")

    def _do_status(self, text:str, color:str):
        self.status_label.setText(f"● {text}")
        self.status_label.setStyleSheet(f"color: {color}; margin-left: 8px;")


    def set_status(self, text:str, color:str):
        QTimer.singleShot(0, lambda: self._do_status(text, color))

    # ── TIMER'LAR ─────────────────────────────────────────────────────────────
    def _tick_timer(self):
        if self.rec_mgr.recording and self.rec_mgr.start_time:
            e = int(time.time()-self.rec_mgr.start_time)
            self.timer_label.setText(f"⏱ {e//3600:02}:{(e%3600)//60:02}:{e%60:02}")

    def _tick_size(self):
        fn = self.rec_mgr.current_filename
        if fn and os.path.exists(fn):
            self.size_label.setText(f"💾 {os.path.getsize(fn)/1_048_576:.2f} MB")

    def _schedule_profile_refresh(self):
        self.profile_mgr.refresh_async(self.rec_mgr)
        QTimer.singleShot(30_000, self._schedule_profile_refresh)

    # ── KAYIT KONTROL ─────────────────────────────────────────────────────────
    def _toggle_record(self):
        if self.rec_mgr.recording:
            # Durdurulmadan önce geçmişe kaydet
            self._save_current_to_history()
            self.rec_mgr.stop()
            self._do_status(_("status_stopped"), "#888")
            self.shutdown_after = False; self.close_app_after = False
            self.cb_shutdown.setChecked(False); self.cb_close_app.setChecked(False)
            self.toggle_btn.set_colors("#4CAF50","#2e7d32")
            self.toggle_btn.setText(_("button_start"))
            self.pulse.stop()
            self._do_log("⏹ Kayıt durduruldu","orange")
            QTimer.singleShot(300, self._refresh_history_panel)
        else:
            channel = self.channel_input.text().strip().lower()
            folder  = self.folder_input.text().strip()
            if not channel: self._do_log(_("error_channel"),"red"); return
            if not folder:  self._do_log(_("error_folder"),"red");  return
            self.rec_mgr.start(channel=channel, folder=folder,
                quality=self.quality_combo.currentText(),
                shutdown_cb  = self._shutdown_computer if self.shutdown_after else None,
                close_app_cb = self._close_app         if self.close_app_after else None)
            self._do_status(_("status_waiting"),"#FF9800")
            self.toggle_btn.set_colors("#f44336","#c62828")
            self.toggle_btn.setText(_("button_stop"))
            self.pulse.start()
            self._save_user_data()

    def _save_current_to_history(self):
        """Kullanıcı DURDUR'a basınca mevcut kaydı geçmişe yazar."""
        rm = self.rec_mgr
        if not rm.current_filename:
            return
        if not os.path.exists(rm.current_filename):
            return
        try:
            elapsed = int(time.time() - rm.start_time) if rm.start_time else 0
            size_mb = os.path.getsize(rm.current_filename) / 1_048_576
            channel = self.channel_input.text().strip().lower()
            rm._save_history(channel, elapsed, size_mb, rm.current_filename)
            self._do_log(f"📊 Geçmişe kaydedildi: {size_mb:.2f} MB", "green")
        except Exception as e:
            self._do_log(f"⚠ Geçmiş kaydedilemedi: {e}", "orange")

    def _shutdown_computer(self):
        self._do_log("⚠ 30s sonra bilgisayar kapanacak!","purple")
        for i in range(30,0,-1):
            if not self.shutdown_after: self._do_log("✅ Kapatma iptal.","green"); return
            if i%10==0 or i<=5: self._do_log(f"⏳ {i}s...","orange")
            time.sleep(1)
        if self.shutdown_after: os.system("shutdown /s /t 5")

    def _close_app(self):
        self._do_log("⚠ 10s sonra uygulama kapanacak!","purple")
        for i in range(10,0,-1):
            if not self.close_app_after: self._do_log("✅ Kapatma iptal.","green"); return
            if i<=3: self._do_log(f"⏳ {i}s...","orange")
            time.sleep(1)
        if self.close_app_after: QTimer.singleShot(0, self.close); os._exit(0)

    def _on_shutdown_toggle(self, checked:bool):
        if checked: self.cb_close_app.setChecked(False); self.close_app_after=False
        self.shutdown_after = checked
        if checked: self._do_log(_("shutdown_active"),"purple")
        self._save_user_data()

    def _on_close_app_toggle(self, checked:bool):
        if checked: self.cb_shutdown.setChecked(False); self.shutdown_after=False
        self.close_app_after = checked
        if checked: self._do_log(_("close_app_active"),"purple")
        self._save_user_data()

    # ── PLANLAYICI ────────────────────────────────────────────────────────────
    def _trigger_scheduled_record(self, channel:str, folder:str="", quality:str="best"):
        if self.rec_mgr.recording:
            self._do_log(f"⚠ Planlı kayıt tetiklendi ama kayıt var: {channel}","orange"); return
        self.channel_input.setText(channel)
        if folder: self.folder_input.setText(folder)
        if not self.folder_input.text().strip():
            self._do_log(f"❌ Klasör yok: {channel}","red"); return
        self.quality_combo.setCurrentText(quality)
        QTimer.singleShot(0, self._toggle_record)
        self._do_log(f"📅 Planlı kayıt başlatıldı: {channel}","green")

    def _add_scheduled_record(self):
        channel = self.sched_channel.text().strip().lower()
        t_str   = self.sched_time.text().strip()
        folder  = self.sched_folder.text().strip()
        quality = self.sched_quality.currentText()
        days    = [d for d,cb in self.day_cbs.items() if cb.isChecked()]
        if not channel: self._do_log(_("error_channel"),"red"); return
        if not re.match(r"^\d{2}:\d{2}$",t_str): self._do_log(_("error_time"),"red"); return
        if not days: self._do_log(_("error_days"),"red"); return
        self.sched_mgr.add(channel,t_str,days,folder,quality)
        self._render_sched_list()
        self._save_user_data()
        self._do_log(f"📅 Plan eklendi: {channel} {t_str}","green")
        self.sched_channel.clear(); self.sched_time.clear(); self.sched_folder.clear()
        for cb in self.day_cbs.values(): cb.setChecked(False)

    def _del_scheduled_record(self):
        idx = self._selected_sched_idx
        if 0 <= idx < len(self.sched_mgr.tasks):
            removed = self.sched_mgr.tasks[idx]
            self.sched_mgr.remove(idx)
            self._render_sched_list()
            self._save_user_data()
            self._do_log(f"❌ Plan silindi: {removed[0]}","orange")
            self._selected_sched_idx = -1
        else:
            self._do_log(_("error_no_selection"),"orange")

    def _render_sched_list(self):
        # Listeyi temizle
        while self.sched_list_layout.count():
            w = self.sched_list_layout.takeAt(0).widget()
            if w: w.deleteLater()

        if not self.sched_mgr.tasks:
            self.sched_list_layout.addWidget(QLabel(_("scheduler_empty"))); return

        self.sched_btn_group = QButtonGroup(self)
        for idx, task in enumerate(self.sched_mgr.tasks):
            days_s   = ", ".join(task[2])
            folder_s = os.path.basename(task[3]) if len(task)>3 and task[3] else ""
            quality_s= task[4] if len(task)>4 else "best"
            next_s   = self.sched_mgr.next_run_str(idx)
            parts = [f"📺 {task[0]}", f"⏰ {task[1]}", f"📅 {days_s}", f"⚙ {quality_s}"]
            if folder_s: parts.append(f"📁 {folder_s}")
            if next_s:   parts.append(f"⏭ {next_s}")

            row = QFrame(); row.setObjectName("card")
            row.setStyleSheet("QFrame#card { background:#1a2a3a; border-radius:8px; padding:4px; }")
            rl = QHBoxLayout(row); rl.setContentsMargins(12,6,12,6)
            lbl = QLabel("  |  ".join(parts)); lbl.setStyleSheet("color:#aaa; font-size:12px;")
            rb  = QRadioButton(); rb.setFixedWidth(20)
            rb.clicked.connect(lambda _, i=idx: setattr(self,"_selected_sched_idx",i))
            self.sched_btn_group.addButton(rb, idx)
            rl.addWidget(lbl); rl.addStretch(); rl.addWidget(rb)
            self.sched_list_layout.addWidget(row)

    def _stop_current_recording(self):
        if self.rec_mgr.recording:
            self.rec_mgr.stop()
            self._do_status(_("status_stopped"),"#888")
            self.toggle_btn.set_colors("#4CAF50","#2e7d32")
            self.toggle_btn.setText(_("button_start"))
            self.pulse.stop()
            self._do_log("⏹ Kayıt durduruldu","orange")
        else:
            self._do_log("⚠ Aktif kayıt yok!","orange")

    # ── PROFİLLER ─────────────────────────────────────────────────────────────
    def _add_profile(self):
        ch = self.prof_channel.text().strip().lower()
        fo = self.prof_folder.text().strip()
        if not ch: self._do_log(_("error_channel"),"red"); return
        if self.profile_mgr.add(ch, fo):
            self._save_user_data(); self._render_profiles()
            self._do_log(_("profile_added").format(ch),"green")
            self.prof_channel.clear(); self.prof_folder.clear()
        else:
            self._do_log(_("profile_exists").format(ch),"orange")

    def _delete_profile(self):
        removed = self.profile_mgr.remove_last()
        if removed:
            self._save_user_data(); self._render_profiles()
            self._do_log(_("profile_deleted").format(removed["channel"]),"orange")

    def _on_profile_click(self, channel:str, folder:str):
        if self.profile_mgr.active_channel == channel:
            self.profile_mgr.active_channel = None
            self.channel_input.clear(); self.folder_input.clear()
            self._do_log(f"❌ Seçim kaldırıldı: {channel}","orange")
        else:
            self.profile_mgr.active_channel = channel
            self.channel_input.setText(channel)
            if folder: self.folder_input.setText(folder)
            self._do_log(f"✅ Profil seçildi: {channel}","green")
        self._render_profiles(); self._save_user_data()

    def _on_profile_double_click(self, channel:str, folder:str):
        self.profile_mgr.active_channel = channel
        self.channel_input.setText(channel)
        if folder: self.folder_input.setText(folder)
        self._render_profiles()
        self.tabs.setCurrentIndex(0)
        if not self.rec_mgr.recording:
            self._toggle_record()

    def _render_profiles(self):
        while self.prof_list_layout.count():
            w = self.prof_list_layout.takeAt(0).widget()
            if w: w.deleteLater()

        if not self.profile_mgr.profiles:
            self.prof_list_layout.addWidget(QLabel(_("scheduler_empty"))); return

        for profile in self.profile_mgr.profiles:
            ch     = profile["channel"]
            folder = profile.get("folder","")
            fname  = os.path.basename(folder) if folder else ""
            cached = self.profile_mgr._cache.get(ch)
            is_live= cached[0] if cached else False
            is_act = (self.profile_mgr.active_channel == ch)

            bg = "#1a3a1a" if is_act else "#1a2a3a"
            border = "2px solid #4CAF50" if is_act else "1px solid #0f3460"
            row = QFrame()
            row.setStyleSheet(f"background:{bg}; border-radius:8px; border:{border}; padding:2px;")
            rl = QHBoxLayout(row); rl.setContentsMargins(12,6,12,6); rl.setSpacing(10)

            icon = "🟢" if is_live else "🔴"
            txt  = f"{icon} {ch}" + (f"  📁 {fname}" if fname else "")
            lbl  = QLabel(txt)
            lbl.setStyleSheet("font-size:13px; color:#ddd;")

            status_lbl = QLabel("CANLI" if is_live else "YOK")
            status_lbl.setStyleSheet(f"color:{'#4CAF50' if is_live else '#f44336'}; font-weight:600; font-size:11px; min-width:60px;")

            rl.addWidget(lbl); rl.addStretch(); rl.addWidget(status_lbl)
            if is_act:
                act_lbl = QLabel(_("active_profile"))
                act_lbl.setStyleSheet("color:#4CAF50; font-size:10px; font-weight:700;")
                rl.addWidget(act_lbl)

            # Tıklama olayları
            row.mousePressEvent       = lambda _, c=ch, f=folder: self._on_profile_click(c,f)
            row.mouseDoubleClickEvent = lambda _, c=ch, f=folder: self._on_profile_double_click(c,f)
            row.setCursor(Qt.CursorShape.PointingHandCursor)
            self.prof_list_layout.addWidget(row)

    # ── GEÇMİŞ ───────────────────────────────────────────────────────────────
    def _refresh_history_panel(self):
        """Geçmiş panelini dosyadan okuyup günceller."""
        # Mevcut satırları temizle
        while self.hist_layout.count():
            w = self.hist_layout.takeAt(0).widget()
            if w: w.deleteLater()

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        if not history:
            empty = QLabel("  Henüz kayıt yok.")
            empty.setStyleSheet("color:#444; font-size:12px;")
            self.hist_layout.addWidget(empty)
            return

        for idx, kayit in enumerate(reversed(history[-30:])):
            dosya = kayit.get("dosya", "")
            # Gerçek index (history listesinde) — reversed olduğu için
            real_idx = len(history) - 1 - idx

            row = QFrame()
            row.setStyleSheet("background:#1a1a2e; border-radius:6px; padding:2px;")
            row.setFixedHeight(34)
            rl = QHBoxLayout(row); rl.setContentsMargins(10, 0, 8, 0); rl.setSpacing(6)

            kanal = kayit.get("kanal", "?")
            sure  = kayit.get("sure",  "?")
            boyut = kayit.get("boyut", "?")
            tarih = kayit.get("tarih", "?")

            info = QLabel(
                f"<span style='color:#4CAF50;font-weight:600'>📺 {kanal}</span>"
                f"<span style='color:#555'>  |  </span>"
                f"<span style='color:#aaa'>⏱ {sure}</span>"
                f"<span style='color:#555'>  |  </span>"
                f"<span style='color:#aaa'>💾 {boyut}</span>"
                f"<span style='color:#555'>  |  </span>"
                f"<span style='color:#666'>📅 {tarih}</span>"
            )
            info.setTextFormat(Qt.TextFormat.RichText)
            info.setStyleSheet("font-size:12px;")
            rl.addWidget(info); rl.addStretch()

            # 📂 Klasörde aç butonu
            if dosya and os.path.exists(dosya):
                btn_open = HoverButton("📂", base="#2196F3", hover="#1565C0", radius=5)
                btn_open.setFixedSize(28, 24)
                btn_open.clicked.connect(lambda _, p=dosya: os.startfile(p))
                rl.addWidget(btn_open)

            # 🗑 Sil butonu — her zaman görünür
            btn_del = HoverButton("🗑", base="#c62828", hover="#b71c1c", radius=5)
            btn_del.setFixedSize(28, 24)
            btn_del.clicked.connect(lambda _, i=real_idx, k=kayit: self._delete_history_entry(i, k))
            rl.addWidget(btn_del)

            self.hist_layout.addWidget(row)

    def _delete_history_entry(self, idx: int, kayit: dict):
        """Geçmiş kaydını siler — isteğe bağlı olarak dosyayı da siler."""
        kanal = kayit.get("kanal", "?")
        dosya = kayit.get("dosya", "")

        msg = QMessageBox(self)
        msg.setWindowTitle("Kaydı Sil")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText(
            f"<b style='color:#e0e0e0;font-size:14px'>{kanal}</b> "
            f"<span style='color:#aaa;font-size:13px'>kanalının bu kaydını<br>geçmişten silmek istiyor musunuz?</span>"
        )
        msg.setInformativeText(
            f"<span style='color:#888;font-size:12px'>"
            f"📅 {kayit.get('tarih','')} &nbsp;|&nbsp; "
            f"⏱ {kayit.get('sure','')} &nbsp;|&nbsp; "
            f"💾 {kayit.get('boyut','')}"
            f"</span>"
        )
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a2e;
                color: #e0e0e0;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            QPushButton {
                background-color: #16213e;
                color: #e0e0e0;
                border: 1px solid #0f3460;
                border-radius: 6px;
                padding: 6px 20px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0f3460;
            }
        """)
        btn_evet = msg.addButton("✔  Evet", QMessageBox.ButtonRole.YesRole)
        btn_evet.setStyleSheet("background:#4CAF50; color:white; border:none; border-radius:6px; padding:6px 20px;")
        btn_hayir = msg.addButton("✘  Hayır", QMessageBox.ButtonRole.NoRole)
        btn_hayir.setStyleSheet("background:#f44336; color:white; border:none; border-radius:6px; padding:6px 20px;")
        msg.setDefaultButton(btn_hayir)
        msg.exec()
        if msg.clickedButton() != btn_evet:
            return

        # Dosyayı da silmek istiyor mu?
        if dosya and os.path.exists(dosya):
            msg2 = QMessageBox(self)
            msg2.setWindowTitle("Video Dosyası")
            msg2.setIcon(QMessageBox.Icon.Warning)
            msg2.setText(
                "<span style='color:#e0e0e0;font-size:13px'>"
                "Video dosyasını da <b>diskten</b> silmek istiyor musunuz?</span>"
            )
            msg2.setInformativeText(
                f"<span style='color:#888;font-size:11px'>{dosya}</span>"
            )
            msg2.setStyleSheet("""
                QMessageBox { background-color: #1a1a2e; color: #e0e0e0; }
                QMessageBox QLabel { color: #e0e0e0; font-size: 13px; }
                QPushButton {
                    background-color: #16213e; color: #e0e0e0;
                    border: 1px solid #0f3460; border-radius: 6px;
                    padding: 6px 20px; font-size: 13px; min-width: 80px;
                }
                QPushButton:hover { background-color: #0f3460; }
            """)
            b_evet2 = msg2.addButton("🗑  Evet, Sil", QMessageBox.ButtonRole.YesRole)
            b_evet2.setStyleSheet("background:#f44336; color:white; border:none; border-radius:6px; padding:6px 20px;")
            b_hayir2 = msg2.addButton("✘  Hayır", QMessageBox.ButtonRole.NoRole)
            b_hayir2.setStyleSheet("background:#555; color:white; border:none; border-radius:6px; padding:6px 20px;")
            msg2.setDefaultButton(b_hayir2)
            msg2.exec()
            if msg2.clickedButton() == b_evet2:
                try:
                    os.remove(dosya)
                    self._do_log(f"🗑 Dosya silindi: {os.path.basename(dosya)}", "orange")
                except Exception as e:
                    self._do_log(f"⚠ Dosya silinemedi: {e}", "red")

        # Geçmiş JSON'dan sil
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
            if 0 <= idx < len(history):
                history.pop(idx)
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            self._do_log(f"🗑 Geçmişten silindi: {kanal}", "orange")
        except Exception as e:
            self._do_log(f"⚠ Geçmiş güncellenemedi: {e}", "red")

        # Paneli yenile
        self._refresh_history_panel()

    def _show_history(self):
        """Eski uyumluluk için kaldı — artık kullanılmıyor."""
        self._refresh_history_panel()

    # ── GÜNCELLEME ────────────────────────────────────────────────────────────
    def _check_updates(self):
        try:
            self._do_log("🔄 Güncelleme kontrol ediliyor...","blue")
            r = requests.get("https://raw.githubusercontent.com/erneman26/Kick-Canli-Yayin-Kaydedici/main/version.json",timeout=5)
            if r.status_code==200:
                latest = r.json().get("version",VERSION)
                if latest > VERSION:
                    self._do_log(f"✨ Yeni sürüm: {latest}","green")
                    ans = QMessageBox.question(self,"Güncelleme",f"Sürüm {latest} mevcut. İndir?")
                    if ans == QMessageBox.StandardButton.Yes:
                        webbrowser.open("https://github.com/erneman26/Kick-Canli-Yayin-Kaydedici/releases/latest")
                else:
                    self._do_log("✅ Güncel sürümdesiniz.","green")
        except: self._do_log("⚠ Güncelleme kontrol edilemedi.","orange")

    # ── AYARLAR ───────────────────────────────────────────────────────────────
    def _change_theme(self, choice:str):
        # PyQt6'da sistem teması QPalette ile uygulanır
        mode = self._theme_map.get(choice,"dark")
        if mode == "light":
            QApplication.instance().setStyle("Fusion")
            p = QPalette(); p.setColor(QPalette.ColorRole.Window, QColor("#f5f5f5"))
            QApplication.instance().setPalette(p)
        else:
            QApplication.instance().setStyleSheet(APP_STYLE)
        self._save_user_data()

    def _change_language(self, choice:str):
        global current_lang
        self._save_user_data(); self.profile_mgr.save()
        current_lang = choice
        try:
            with open(LANG_SEL_FILE,"w",encoding="utf-8") as f: json.dump({"language":choice},f)
        except Exception as e: log.warning(f"Dil kaydedilemedi: {e}")
        QMessageBox.information(self, _("language_label"),
                                f"Dil '{choice}' seçildi. Yeniden başlatılıyor...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    # ── KLASÖR SEÇİMİ ─────────────────────────────────────────────────────────
    def _select_folder(self):
        f = QFileDialog.getExistingDirectory(self,"Kayıt Klasörü Seç")
        if f: self.folder_input.setText(f); self._do_log(f"📁 Klasör: {f}","green"); self._save_user_data()

    def _select_sched_folder(self):
        f = QFileDialog.getExistingDirectory(self,"Planlayıcı Klasörü Seç")
        if f: self.sched_folder.setText(f)

    def _select_profile_folder(self):
        f = QFileDialog.getExistingDirectory(self,"Profil Klasörü Seç")
        if f: self.prof_folder.setText(f)

    # ── VERİ KAYDETME / YÜKLEME ───────────────────────────────────────────────
    def _save_user_data(self):
        try:
            data = {
                "channel":   self.channel_input.text(),
                "folder":    self.folder_input.text(),
                "quality":   self.quality_combo.currentText(),
                "shutdown":  self.shutdown_after,
                "close_app": self.close_app_after,
                "profiles":  self.profile_mgr.profiles,
                "schedules": self.sched_mgr.tasks,
            }
            with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)
        except Exception as e: log.warning(f"Veri kaydedilemedi: {e}")

    def _load_user_data(self):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f: data = json.load(f)
            if data.get("channel"):   self.channel_input.setText(data["channel"])
            if data.get("folder"):    self.folder_input.setText(data["folder"])
            if data.get("quality"):   self.quality_combo.setCurrentText(data["quality"])
            if data.get("shutdown"):  self.cb_shutdown.setChecked(True);  self.shutdown_after=True
            if data.get("close_app"): self.cb_close_app.setChecked(True); self.close_app_after=True
            if "profiles"  in data:   self.profile_mgr.profiles = data["profiles"];  self._render_profiles()
            if "schedules" in data:
                self.sched_mgr.tasks = data["schedules"]; self.sched_mgr.rebuild(); self._render_sched_list()
            log.info("Kullanıcı verileri yüklendi.")
        except FileNotFoundError: log.info("İlk çalıştırma.")
        except Exception as e:    log.warning(f"Veri yüklenemedi: {e}")

    # ── SYSTEM TRAY ───────────────────────────────────────────────────────────
    def _init_tray(self):
        try:
            ico_path = "kick.ico"
            img = PilImage.open(ico_path) if os.path.exists(ico_path) \
                else PilImage.new("RGBA",(64,64),color=(76,175,80,255))
            menu = pystray.Menu(
                pystray.MenuItem("Göster",        lambda: QTimer.singleShot(0, self.show), default=True),
                pystray.MenuItem("Kaydı Durdur",  lambda: QTimer.singleShot(0, self._stop_current_recording)),
                pystray.MenuItem("Çıkış",         lambda: QTimer.singleShot(0, self.close)),
            )
            self._tray_icon = pystray.Icon("KickRecorder",img,f"Kick Recorder {VERSION}",menu)
            threading.Thread(target=self._tray_icon.run,daemon=True).start()
        except Exception as e: log.warning(f"Tray başlatılamadı: {e}")

    # ── KAPATMA ───────────────────────────────────────────────────────────────
    def closeEvent(self, event):
        if self.rec_mgr.recording:
            ans = QMessageBox.question(self,"Uyarı","Kayıt devam ediyor! Çıkmak istiyor musunuz?")
            if ans != QMessageBox.StandardButton.Yes:
                event.ignore(); return
        self._save_user_data(); self.profile_mgr.save()
        if self._tray_icon:
            try: self._tray_icon.stop()
            except: pass
        event.accept()

    def _on_window_close(self):
        """Tray varsa gizle, yoksa kapat."""
        if TRAY_OK and self._tray_icon: self.hide()
        else: self.close()


# ─── GİRİŞ ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(f"Kick Recorder {VERSION}")
    app.setStyleSheet(APP_STYLE)

    win = MainWindow()
    win.show()

    print(f"{R.BOLD}{R.YESIL}  ✔  {_('app_title')} {VERSION} hazır  |  🌍 {current_lang}{R.SON}\n")
    sys.exit(app.exec())
