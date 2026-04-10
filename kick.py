import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import datetime
import os
import time
import requests
import sys
import ctypes
import json
import webbrowser
from PIL import Image
import re
import schedule
import locale

# ---------- SİSTEM DİLİNİ OTOMATİK ALGILA ----------
def detect_system_language():
    try:
        if sys.platform == "win32":
            try:
                windll = ctypes.windll.kernel32
                lang_id = windll.GetUserDefaultUILanguage()
                lang_map = {
                    1055: "Türkçe", 1033: "English", 1031: "Deutsch",
                    1036: "Français", 1034: "Español", 1040: "Italiano",
                    1046: "Português", 1049: "Русский", 1041: "日本語",
                    1042: "한국어", 2052: "中文"
                }
                if lang_id in lang_map:
                    return lang_map[lang_id]
            except:
                pass
        return "Türkçe"
    except:
        return "Türkçe"

# ---------- VERSİYON ----------
VERSION = "v1.3"

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
print("▶ Programı kapatmak için arayüzdeki X butonunu kullanın")
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

# ---------- DİL DOSYASI (11 DİL) ----------
LANGUAGES = {
    "Türkçe": {
        "app_title": "Kick Canlı Yayın Kaydedici",
        "tab_record": "🎬 KAYIT",
        "tab_scheduler": "📅 PLANLAYICI",
        "tab_profiles": "⭐ PROFİLLER",
        "tab_settings": "⚙ AYARLAR",
        "tab_logs": "📋 LOGLAR",
        "channel_placeholder": "Kanal adı",
        "quality_auto": "otomatik",
        "quality_best": "en iyi",
        "folder_placeholder": "Kayıt klasörü",
        "folder_select": "📁 Seç",
        "shutdown_option": "Yayın bitince bilgisayarı kapat",
        "close_app_option": "Yayın bitince uygulamayı kapat",
        "button_start": "▶ BAŞLAT",
        "button_stop": "⏹ DURDUR",
        "button_history": "📜 Geçmiş",
        "button_update": "🔄 Güncelle",
        "status_ready": "HAZIR",
        "status_waiting": "YAYIN BEKLENİYOR",
        "status_online": "🔴 KAYIT YAPILIYOR",
        "status_offline": "⚫ ÇEVRİMDIŞI",
        "status_stopped": "⏸ DURDU",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Program başlatıldı",
        "scheduler_empty": "Plan yok",
        "profile_saved": "✅ Profil başarıyla kaydedildi!",
        "profile_added": "✅ Profil eklendi: {}",
        "profile_deleted": "❌ Profil silindi: {}",
        "profile_exists": "⚠ {} zaten profillerde",
        "error_channel": "Lütfen kanal adı girin",
        "error_folder": "Lütfen kayıt klasörü seçin",
        "error_time": "Geçersiz saat formatı! Örnek: 14:30",
        "error_days": "Lütfen en az bir gün seçin!",
        "error_no_selection": "Lütfen bir plan seçin!",
        "shutdown_active": "Yayın bitince bilgisayar KAPATMA özelliği AKTİF",
        "close_app_active": "Yayın bitince uygulama KAPATMA özelliği AKTİF",
        "shutdown_cancel": "Bilgisayar kapatma iptal edildi",
        "close_app_cancel": "Uygulama kapatma iptal edildi",
        "lang_detected": "🌍 Sistem dili algılandı: {}",
        "log_scheduler": "Planlayıcı başlatıldı",
        "log_instruction": "Kanal adını girin ve BAŞLAT'a tıklayın",
        "profiles_title": "Kayıtlı Kanallar",
        "profiles_list": "Kanallar",
        "profile_channel": "Kanal Adı:",
        "profile_folder": "Klasör:",
        "profile_save": "💾 Kaydet",
        "profile_delete": "🗑 Sil",
        "theme_label": "Tema",
        "theme_dark": "Koyu",
        "theme_light": "Açık",
        "theme_system": "Sistem",
        "language_label": "Dil",
        "scheduler_channel": "Kanal",
        "scheduler_time": "Saat",
        "scheduler_days": "Günler",
        "scheduler_add": "➕ Ekle",
        "scheduler_delete": "❌ Sil",
        "scheduler_stop": "⏹ Kaydı Durdur",
        "scheduler_list": "Planlanan Kayıtlar",
        "active_profile": "✅ SEÇİLİ",
    },
    "English": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 RECORD",
        "tab_scheduler": "📅 SCHEDULER",
        "tab_profiles": "⭐ PROFILES",
        "tab_settings": "⚙ SETTINGS",
        "tab_logs": "📋 LOGS",
        "channel_placeholder": "Channel name",
        "quality_auto": "auto",
        "quality_best": "best",
        "folder_placeholder": "Save folder",
        "folder_select": "📁 Browse",
        "shutdown_option": "Shutdown computer when stream ends",
        "close_app_option": "Close app when stream ends",
        "button_start": "▶ START",
        "button_stop": "⏹ STOP",
        "button_history": "📜 History",
        "button_update": "🔄 Update",
        "status_ready": "READY",
        "status_waiting": "WAITING",
        "status_online": "🔴 RECORDING",
        "status_offline": "⚫ OFFLINE",
        "status_stopped": "⏸ STOPPED",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Program started",
        "scheduler_empty": "No schedule",
        "profile_saved": "✅ Profile saved successfully!",
        "profile_added": "✅ Profile added: {}",
        "profile_deleted": "❌ Profile deleted: {}",
        "profile_exists": "⚠ {} already in profiles",
        "error_channel": "Please enter channel name",
        "error_folder": "Please select save folder",
        "error_time": "Invalid time format! Example: 14:30",
        "error_days": "Please select at least one day!",
        "error_no_selection": "Please select a schedule!",
        "shutdown_active": "Shutdown after stream ACTIVE",
        "close_app_active": "Close app after stream ACTIVE",
        "shutdown_cancel": "Shutdown cancelled",
        "close_app_cancel": "App close cancelled",
        "lang_detected": "🌍 System language detected: {}",
        "log_scheduler": "Scheduler started",
        "log_instruction": "Enter channel name and click START",
        "profiles_title": "Saved Channels",
        "profiles_list": "Channels",
        "profile_channel": "Channel Name:",
        "profile_folder": "Folder:",
        "profile_save": "💾 Save",
        "profile_delete": "🗑 Delete",
        "theme_label": "Theme",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "theme_system": "System",
        "language_label": "Language",
        "scheduler_channel": "Channel",
        "scheduler_time": "Time",
        "scheduler_days": "Days",
        "scheduler_add": "➕ Add",
        "scheduler_delete": "❌ Delete",
        "scheduler_stop": "⏹ Stop Recording",
        "scheduler_list": "Scheduled Records",
        "active_profile": "✅ SELECTED",
    },
    "Deutsch": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 AUFNAHME",
        "tab_scheduler": "📅 PLANER",
        "tab_profiles": "⭐ PROFIL",
        "tab_settings": "⚙ EINSTELLUNGEN",
        "tab_logs": "📋 PROTOKOLL",
        "channel_placeholder": "Kanalname",
        "quality_auto": "auto",
        "quality_best": "beste",
        "folder_placeholder": "Speicherordner",
        "folder_select": "📁 Wählen",
        "shutdown_option": "Computer ausschalten",
        "close_app_option": "App schließen",
        "button_start": "▶ START",
        "button_stop": "⏹ STOP",
        "button_history": "📜 Verlauf",
        "button_update": "🔄 Update",
        "status_ready": "BEREIT",
        "status_waiting": "WARTEN",
        "status_online": "🔴 AUFNAHME",
        "status_offline": "⚫ OFFLINE",
        "status_stopped": "⏸ GESTOPPT",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programm gestartet",
        "scheduler_empty": "Keine Pläne",
        "profile_saved": "✅ Profil erfolgreich gespeichert!",
        "profile_added": "✅ Profil hinzugefügt: {}",
        "profile_deleted": "❌ Profil gelöscht: {}",
        "profile_exists": "⚠ {} bereits in Profilen",
        "error_channel": "Bitte Kanalnamen eingeben",
        "error_folder": "Bitte Speicherordner wählen",
        "error_time": "Ungültiges Zeitformat! Beispiel: 14:30",
        "error_days": "Bitte mindestens einen Tag auswählen!",
        "error_no_selection": "Bitte einen Plan auswählen!",
        "shutdown_active": "Ausschalten nach Stream AKTIV",
        "close_app_active": "App schließen nach Stream AKTIV",
        "shutdown_cancel": "Ausschalten abgebrochen",
        "close_app_cancel": "Schließen abgebrochen",
        "lang_detected": "🌍 Systemsprache erkannt: {}",
        "log_scheduler": "Planer gestartet",
        "log_instruction": "Kanalnamen eingeben und START klicken",
        "profiles_title": "Gespeicherte Kanäle",
        "profiles_list": "Profile",
        "profile_channel": "Kanalname:",
        "profile_folder": "Ordner:",
        "profile_save": "💾 Speichern",
        "profile_delete": "🗑 Löschen",
        "theme_label": "Design",
        "theme_dark": "Dunkel",
        "theme_light": "Hell",
        "theme_system": "System",
        "language_label": "Sprache",
        "scheduler_channel": "Kanal",
        "scheduler_time": "Uhrzeit",
        "scheduler_days": "Tage",
        "scheduler_add": "➕ Hinzufügen",
        "scheduler_delete": "❌ Löschen",
        "scheduler_stop": "⏹ Aufnahme stoppen",
        "scheduler_list": "Geplante Aufnahmen",
        "active_profile": "✅ AUSGEWÄHLT",
    },
    "Français": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 ENREGISTREMENT",
        "tab_scheduler": "📅 PLANIFICATEUR",
        "tab_profiles": "⭐ PROFILS",
        "tab_settings": "⚙ PARAMÈTRES",
        "tab_logs": "📋 JOURNAUX",
        "channel_placeholder": "Nom de la chaîne",
        "quality_auto": "auto",
        "quality_best": "meilleure",
        "folder_placeholder": "Dossier de sauvegarde",
        "folder_select": "📁 Choisir",
        "shutdown_option": "Éteindre l'ordinateur",
        "close_app_option": "Fermer l'application",
        "button_start": "▶ DÉMARRER",
        "button_stop": "⏹ ARRÊTER",
        "button_history": "📜 Historique",
        "button_update": "🔄 Mettre à jour",
        "status_ready": "PRÊT",
        "status_waiting": "ATTENTE",
        "status_online": "🔴 ENREGISTREMENT",
        "status_offline": "⚫ HORS LIGNE",
        "status_stopped": "⏸ ARRÊTÉ",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programme démarré",
        "scheduler_empty": "Aucun plan",
        "profile_saved": "✅ Profil enregistré avec succès!",
        "profile_added": "✅ Profil ajouté: {}",
        "profile_deleted": "❌ Profil supprimé: {}",
        "profile_exists": "⚠ {} déjà dans les profils",
        "error_channel": "Veuillez entrer le nom de la chaîne",
        "error_folder": "Veuillez sélectionner le dossier de sauvegarde",
        "error_time": "Format d'heure invalide! Exemple: 14:30",
        "error_days": "Veuillez sélectionner au moins un jour!",
        "error_no_selection": "Veuillez sélectionner un plan!",
        "shutdown_active": "Extinction après stream ACTIVE",
        "close_app_active": "Fermeture après stream ACTIVE",
        "shutdown_cancel": "Extinction annulée",
        "close_app_cancel": "Fermeture annulée",
        "lang_detected": "🌍 Langue système détectée: {}",
        "log_scheduler": "Planificateur démarré",
        "log_instruction": "Entrez le nom de la chaîne et cliquez sur DÉMARRER",
        "profiles_title": "Chaînes enregistrées",
        "profiles_list": "Profils",
        "profile_channel": "Nom de la chaîne:",
        "profile_folder": "Dossier:",
        "profile_save": "💾 Enregistrer",
        "profile_delete": "🗑 Supprimer",
        "theme_label": "Thème",
        "theme_dark": "Sombre",
        "theme_light": "Clair",
        "theme_system": "Système",
        "language_label": "Langue",
        "scheduler_channel": "Chaîne",
        "scheduler_time": "Heure",
        "scheduler_days": "Jours",
        "scheduler_add": "➕ Ajouter",
        "scheduler_delete": "❌ Supprimer",
        "scheduler_stop": "⏹ Arrêter l'enregistrement",
        "scheduler_list": "Enregistrements planifiés",
        "active_profile": "✅ SÉLECTIONNÉ",
    },
    "Español": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 GRABACIÓN",
        "tab_scheduler": "📅 PROGRAMADOR",
        "tab_profiles": "⭐ PERFILES",
        "tab_settings": "⚙ AJUSTES",
        "tab_logs": "📋 REGISTROS",
        "channel_placeholder": "Nombre del canal",
        "quality_auto": "auto",
        "quality_best": "mejor",
        "folder_placeholder": "Carpeta de guardado",
        "folder_select": "📁 Seleccionar",
        "shutdown_option": "Apagar la PC",
        "close_app_option": "Cerrar la aplicación",
        "button_start": "▶ INICIAR",
        "button_stop": "⏹ DETENER",
        "button_history": "📜 Historial",
        "button_update": "🔄 Actualizar",
        "status_ready": "LISTO",
        "status_waiting": "ESPERANDO",
        "status_online": "🔴 GRABANDO",
        "status_offline": "⚫ DESCONECTADO",
        "status_stopped": "⏸ DETENIDO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programa iniciado",
        "scheduler_empty": "Sin programación",
        "profile_saved": "✅ Perfil guardado exitosamente!",
        "profile_added": "✅ Perfil agregado: {}",
        "profile_deleted": "❌ Perfil eliminado: {}",
        "profile_exists": "⚠ {} ya está en perfiles",
        "error_channel": "Por favor ingrese nombre del canal",
        "error_folder": "Por favor seleccione carpeta de guardado",
        "error_time": "Formato de hora inválido! Ejemplo: 14:30",
        "error_days": "Por favor seleccione al menos un día!",
        "error_no_selection": "Por favor seleccione un plan!",
        "shutdown_active": "Apagado después del stream ACTIVO",
        "close_app_active": "Cierre después del stream ACTIVO",
        "shutdown_cancel": "Apagado cancelado",
        "close_app_cancel": "Cierre cancelado",
        "lang_detected": "🌍 Idioma del sistema detectado: {}",
        "log_scheduler": "Programador iniciado",
        "log_instruction": "Ingrese nombre del canal y haga clic en INICIAR",
        "profiles_title": "Canales guardados",
        "profiles_list": "Perfiles",
        "profile_channel": "Nombre del canal:",
        "profile_folder": "Carpeta:",
        "profile_save": "💾 Guardar",
        "profile_delete": "🗑 Eliminar",
        "theme_label": "Tema",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "language_label": "Idioma",
        "scheduler_channel": "Canal",
        "scheduler_time": "Hora",
        "scheduler_days": "Días",
        "scheduler_add": "➕ Agregar",
        "scheduler_delete": "❌ Eliminar",
        "scheduler_stop": "⏹ Detener Grabación",
        "scheduler_list": "Grabaciones programadas",
        "active_profile": "✅ SELECCIONADO",
    },
    "Italiano": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 REGISTRAZIONE",
        "tab_scheduler": "📅 PIANIFICATORE",
        "tab_profiles": "⭐ PROFILI",
        "tab_settings": "⚙ IMPOSTAZIONI",
        "tab_logs": "📋 REGISTRI",
        "channel_placeholder": "Nome canale",
        "quality_auto": "auto",
        "quality_best": "migliore",
        "folder_placeholder": "Cartella salvataggio",
        "folder_select": "📁 Scegli",
        "shutdown_option": "Spegni PC",
        "close_app_option": "Chiudi app",
        "button_start": "▶ AVVIA",
        "button_stop": "⏹ FERMA",
        "button_history": "📜 Cronologia",
        "button_update": "🔄 Aggiorna",
        "status_ready": "PRONTO",
        "status_waiting": "IN ATTESA",
        "status_online": "🔴 REGISTRAZIONE",
        "status_offline": "⚫ OFFLINE",
        "status_stopped": "⏸ FERMATO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programma avviato",
        "scheduler_empty": "Nessuna pianificazione",
        "profile_saved": "✅ Profilo salvato con successo!",
        "profile_added": "✅ Profilo aggiunto: {}",
        "profile_deleted": "❌ Profilo eliminato: {}",
        "profile_exists": "⚠ {} già nei profili",
        "error_channel": "Inserisci nome canale",
        "error_folder": "Seleziona cartella salvataggio",
        "error_time": "Formato ora non valido! Esempio: 14:30",
        "error_days": "Seleziona almeno un giorno!",
        "error_no_selection": "Seleziona un piano!",
        "shutdown_active": "Spegnimento dopo stream ATTIVO",
        "close_app_active": "Chiusura app dopo stream ATTIVA",
        "shutdown_cancel": "Spegnimento annullato",
        "close_app_cancel": "Chiusura annullata",
        "lang_detected": "🌍 Lingua di sistema rilevata: {}",
        "log_scheduler": "Pianificatore avviato",
        "log_instruction": "Inserisci nome canale e clicca AVVIA",
        "profiles_title": "Canali salvati",
        "profiles_list": "Profili",
        "profile_channel": "Nome canale:",
        "profile_folder": "Cartella:",
        "profile_save": "💾 Salva",
        "profile_delete": "🗑 Elimina",
        "theme_label": "Tema",
        "theme_dark": "Scuro",
        "theme_light": "Chiaro",
        "theme_system": "Sistema",
        "language_label": "Lingua",
        "scheduler_channel": "Canale",
        "scheduler_time": "Ora",
        "scheduler_days": "Giorni",
        "scheduler_add": "➕ Aggiungi",
        "scheduler_delete": "❌ Elimina",
        "scheduler_stop": "⏹ Ferma Registrazione",
        "scheduler_list": "Registrazioni pianificate",
        "active_profile": "✅ SELEZIONATO",
    },
    "Português": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 GRAVAÇÃO",
        "tab_scheduler": "📅 AGENDADOR",
        "tab_profiles": "⭐ PERFIS",
        "tab_settings": "⚙ CONFIGURAÇÕES",
        "tab_logs": "📋 REGISTROS",
        "channel_placeholder": "Nome do canal",
        "quality_auto": "auto",
        "quality_best": "melhor",
        "folder_placeholder": "Pasta de salvamento",
        "folder_select": "📁 Escolher",
        "shutdown_option": "Desligar PC",
        "close_app_option": "Fechar app",
        "button_start": "▶ INICIAR",
        "button_stop": "⏹ PARAR",
        "button_history": "📜 Histórico",
        "button_update": "🔄 Atualizar",
        "status_ready": "PRONTO",
        "status_waiting": "AGUARDANDO",
        "status_online": "🔴 GRAVANDO",
        "status_offline": "⚫ OFFLINE",
        "status_stopped": "⏸ PARADO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programa iniciado",
        "scheduler_empty": "Sem agendamento",
        "profile_saved": "✅ Perfil salvo com sucesso!",
        "profile_added": "✅ Perfil adicionado: {}",
        "profile_deleted": "❌ Perfil excluído: {}",
        "profile_exists": "⚠ {} já está nos perfis",
        "error_channel": "Digite nome do canal",
        "error_folder": "Selecione pasta de salvamento",
        "error_time": "Formato de horário inválido! Exemplo: 14:30",
        "error_days": "Selecione pelo menos um dia!",
        "error_no_selection": "Selecione um plano!",
        "shutdown_active": "Desligar após stream ATIVO",
        "close_app_active": "Fechar app após stream ATIVA",
        "shutdown_cancel": "Desligamento cancelado",
        "close_app_cancel": "Fechamento cancelado",
        "lang_detected": "🌍 Idioma do sistema detectado: {}",
        "log_scheduler": "Agendador iniciado",
        "log_instruction": "Digite nome do canal e clique em INICIAR",
        "profiles_title": "Canais salvos",
        "profiles_list": "Perfis",
        "profile_channel": "Nome do canal:",
        "profile_folder": "Pasta:",
        "profile_save": "💾 Salvar",
        "profile_delete": "🗑 Excluir",
        "theme_label": "Tema",
        "theme_dark": "Escuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "language_label": "Idioma",
        "scheduler_channel": "Canal",
        "scheduler_time": "Horário",
        "scheduler_days": "Dias",
        "scheduler_add": "➕ Adicionar",
        "scheduler_delete": "❌ Excluir",
        "scheduler_stop": "⏹ Parar Gravação",
        "scheduler_list": "Gravações agendadas",
        "active_profile": "✅ SELECIONADO",
    },
    "Русский": {
        "app_title": "Kick Live Stream Recorder",
        "tab_record": "🎬 ЗАПИСЬ",
        "tab_scheduler": "📅 ПЛАНИРОВЩИК",
        "tab_profiles": "⭐ ПРОФИЛИ",
        "tab_settings": "⚙ НАСТРОЙКИ",
        "tab_logs": "📋 ЖУРНАЛЫ",
        "channel_placeholder": "Название канала",
        "quality_auto": "авто",
        "quality_best": "лучшее",
        "folder_placeholder": "Папка сохранения",
        "folder_select": "📁 Выбрать",
        "shutdown_option": "Выключить ПК",
        "close_app_option": "Закрыть приложение",
        "button_start": "▶ СТАРТ",
        "button_stop": "⏹ СТОП",
        "button_history": "📜 История",
        "button_update": "🔄 Обновить",
        "status_ready": "ГОТОВ",
        "status_waiting": "ОЖИДАНИЕ",
        "status_online": "🔴 ЗАПИСЬ",
        "status_offline": "⚫ ОФФЛАЙН",
        "status_stopped": "⏸ ОСТАНОВЛЕНО",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Программа запущена",
        "scheduler_empty": "Нет планов",
        "profile_saved": "✅ Профиль успешно сохранен!",
        "profile_added": "✅ Профиль добавлен: {}",
        "profile_deleted": "❌ Профиль удален: {}",
        "profile_exists": "⚠ {} уже в профилях",
        "error_channel": "Введите название канала",
        "error_folder": "Выберите папку сохранения",
        "error_time": "Неверный формат времени! Пример: 14:30",
        "error_days": "Выберите хотя бы один день!",
        "error_no_selection": "Выберите план!",
        "shutdown_active": "Выключение после стрима АКТИВНО",
        "close_app_active": "Закрытие после стрима АКТИВНО",
        "shutdown_cancel": "Выключение отменено",
        "close_app_cancel": "Закрытие отменено",
        "lang_detected": "🌍 Обнаружен системный язык: {}",
        "log_scheduler": "Планировщик запущен",
        "log_instruction": "Введите название канала и нажмите СТАРТ",
        "profiles_title": "Сохраненные каналы",
        "profiles_list": "Профили",
        "profile_channel": "Название канала:",
        "profile_folder": "Папка:",
        "profile_save": "💾 Сохранить",
        "profile_delete": "🗑 Удалить",
        "theme_label": "Тема",
        "theme_dark": "Тёмная",
        "theme_light": "Светлая",
        "theme_system": "Системная",
        "language_label": "Язык",
        "scheduler_channel": "Канал",
        "scheduler_time": "Время",
        "scheduler_days": "Дни",
        "scheduler_add": "➕ Добавить",
        "scheduler_delete": "❌ Удалить",
        "scheduler_stop": "⏹ Остановить запись",
        "scheduler_list": "Запланированные записи",
        "active_profile": "✅ ВЫБРАН",
    },
    "日本語": {
        "app_title": "Kickライブストリームレコーダー",
        "tab_record": "🎬 録画",
        "tab_scheduler": "📅 予約",
        "tab_profiles": "⭐ プロフィール",
        "tab_settings": "⚙ 設定",
        "tab_logs": "📋 ログ",
        "channel_placeholder": "チャンネル名",
        "quality_auto": "自動",
        "quality_best": "最高",
        "folder_placeholder": "保存先",
        "folder_select": "📁 選択",
        "shutdown_option": "PCをシャットダウン",
        "close_app_option": "アプリを閉じる",
        "button_start": "▶ 開始",
        "button_stop": "⏹ 停止",
        "button_history": "📜 履歴",
        "button_update": "🔄 更新",
        "status_ready": "準備完了",
        "status_waiting": "待機中",
        "status_online": "🔴 録画中",
        "status_offline": "⚫ オフライン",
        "status_stopped": "⏸ 停止",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "プログラム起動",
        "scheduler_empty": "予約なし",
        "profile_saved": "✅ プロフィールを保存しました！",
        "profile_added": "✅ プロフィール追加: {}",
        "profile_deleted": "❌ プロフィール削除: {}",
        "profile_exists": "⚠ {} は既に登録されています",
        "error_channel": "チャンネル名を入力してください",
        "error_folder": "保存先を選択してください",
        "error_time": "時刻形式が無効です！例: 14:30",
        "error_days": "少なくとも1日を選択してください！",
        "error_no_selection": "予約を選択してください！",
        "shutdown_active": "終了時シャットダウンON",
        "close_app_active": "終了時アプリ終了ON",
        "shutdown_cancel": "シャットダウンキャンセル",
        "close_app_cancel": "アプリ終了キャンセル",
        "lang_detected": "🌍 システム言語を検出: {}",
        "log_scheduler": "予約開始",
        "log_instruction": "チャンネル名を入力して開始をクリック",
        "profiles_title": "保存されたチャンネル",
        "profiles_list": "プロフィール",
        "profile_channel": "チャンネル名:",
        "profile_folder": "フォルダ:",
        "profile_save": "💾 保存",
        "profile_delete": "🗑 削除",
        "theme_label": "テーマ",
        "theme_dark": "ダーク",
        "theme_light": "ライト",
        "theme_system": "システム",
        "language_label": "言語",
        "scheduler_channel": "チャンネル",
        "scheduler_time": "時刻",
        "scheduler_days": "曜日",
        "scheduler_add": "➕ 追加",
        "scheduler_delete": "❌ 削除",
        "scheduler_stop": "⏹ 録画停止",
        "scheduler_list": "予約リスト",
        "active_profile": "✅ 選択中",
    },
    "한국어": {
        "app_title": "Kick 라이브 스트림 레코더",
        "tab_record": "🎬 녹화",
        "tab_scheduler": "📅 예약",
        "tab_profiles": "⭐ 프로필",
        "tab_settings": "⚙ 설정",
        "tab_logs": "📋 로그",
        "channel_placeholder": "채널명",
        "quality_auto": "자동",
        "quality_best": "최고",
        "folder_placeholder": "저장 폴더",
        "folder_select": "📁 선택",
        "shutdown_option": "PC 종료",
        "close_app_option": "앱 종료",
        "button_start": "▶ 시작",
        "button_stop": "⏹ 중지",
        "button_history": "📜 기록",
        "button_update": "🔄 업데이트",
        "status_ready": "준비",
        "status_waiting": "대기중",
        "status_online": "🔴 녹화중",
        "status_offline": "⚫ 오프라인",
        "status_stopped": "⏸ 중지됨",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "프로그램 시작",
        "scheduler_empty": "예약 없음",
        "profile_saved": "✅ 프로필이 저장되었습니다!",
        "profile_added": "✅ 프로필 추가됨: {}",
        "profile_deleted": "❌ 프로필 삭제됨: {}",
        "profile_exists": "⚠ {} 이미 프로필에 있음",
        "error_channel": "채널명을 입력하세요",
        "error_folder": "저장 폴더를 선택하세요",
        "error_time": "시간 형식이 잘못되었습니다! 예: 14:30",
        "error_days": "최소 하나의 요일을 선택하세요!",
        "error_no_selection": "예약을 선택하세요!",
        "shutdown_active": "종료 시 PC 종료 활성화",
        "close_app_active": "종료 시 앱 종료 활성화",
        "shutdown_cancel": "PC 종료 취소",
        "close_app_cancel": "앱 종료 취소",
        "lang_detected": "🌍 시스템 언어 감지됨: {}",
        "log_scheduler": "예약 시작",
        "log_instruction": "채널명 입력 후 시작 클릭",
        "profiles_title": "저장된 채널",
        "profiles_list": "프로필",
        "profile_channel": "채널명:",
        "profile_folder": "폴더:",
        "profile_save": "💾 저장",
        "profile_delete": "🗑 삭제",
        "theme_label": "테마",
        "theme_dark": "다크",
        "theme_light": "라이트",
        "theme_system": "시스템",
        "language_label": "언어",
        "scheduler_channel": "채널",
        "scheduler_time": "시간",
        "scheduler_days": "요일",
        "scheduler_add": "➕ 추가",
        "scheduler_delete": "❌ 삭제",
        "scheduler_stop": "⏹ 녹화 중지",
        "scheduler_list": "예약 목록",
        "active_profile": "✅ 선택됨",
    },
    "中文": {
        "app_title": "Kick直播录制器",
        "tab_record": "🎬 录制",
        "tab_scheduler": "📅 预约",
        "tab_profiles": "⭐ 配置文件",
        "tab_settings": "⚙ 设置",
        "tab_logs": "📋 日志",
        "channel_placeholder": "频道名称",
        "quality_auto": "自动",
        "quality_best": "最佳",
        "folder_placeholder": "保存文件夹",
        "folder_select": "📁 选择",
        "shutdown_option": "关闭电脑",
        "close_app_option": "关闭应用",
        "button_start": "▶ 开始",
        "button_stop": "⏹ 停止",
        "button_history": "📜 历史",
        "button_update": "🔄 更新",
        "status_ready": "就绪",
        "status_waiting": "等待中",
        "status_online": "🔴 录制中",
        "status_offline": "⚫ 离线",
        "status_stopped": "⏸ 已停止",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "程序已启动",
        "scheduler_empty": "无预约",
        "profile_saved": "✅ 配置已保存！",
        "profile_added": "✅ 配置已添加: {}",
        "profile_deleted": "❌ 配置已删除: {}",
        "profile_exists": "⚠ {} 已存在",
        "error_channel": "请输入频道名称",
        "error_folder": "请选择保存文件夹",
        "error_time": "时间格式无效！示例: 14:30",
        "error_days": "请至少选择一个星期！",
        "error_no_selection": "请选择一个预约！",
        "shutdown_active": "结束后关机已激活",
        "close_app_active": "结束后关闭应用已激活",
        "shutdown_cancel": "关机已取消",
        "close_app_cancel": "关闭已取消",
        "lang_detected": "🌍 检测到系统语言: {}",
        "log_scheduler": "预约开始",
        "log_instruction": "输入频道名称并点击开始",
        "profiles_title": "已保存频道",
        "profiles_list": "配置文件",
        "profile_channel": "频道名称:",
        "profile_folder": "文件夹:",
        "profile_save": "💾 保存",
        "profile_delete": "🗑 删除",
        "theme_label": "主题",
        "theme_dark": "深色",
        "theme_light": "浅色",
        "theme_system": "系统",
        "language_label": "语言",
        "scheduler_channel": "频道",
        "scheduler_time": "时间",
        "scheduler_days": "星期",
        "scheduler_add": "➕ 添加",
        "scheduler_delete": "❌ 删除",
        "scheduler_stop": "⏹ 停止录制",
        "scheduler_list": "预约列表",
        "active_profile": "✅ 已选择",
    }
}

current_lang = detect_system_language()

# Kaydedilmiş dili yükle
try:
    with open("language.json", "r", encoding="utf-8") as f:
        saved = json.load(f)
        if saved.get("language") in LANGUAGES:
            current_lang = saved.get("language")
            print(f"💾 Kaydedilmiş dil yüklendi: {current_lang}")
except:
    pass

if current_lang not in LANGUAGES:
    current_lang = "Türkçe"

def _(key):
    return LANGUAGES[current_lang].get(key, LANGUAGES["Türkçe"].get(key, key))

# ---------- KONSOL LOG FONKSİYONU ----------
def console_log(msg, renk="beyaz"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
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

# ---------- MODERN ANİMASYONLU BUTON SINIFI ----------
class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_color = self.cget("fg_color")
        
    def on_enter(self, event):
        if isinstance(self.default_color, tuple):
            new_color = tuple(min(255, int(c * 1.2)) for c in self.default_color)
            self.configure(fg_color=new_color)
        else:
            self.configure(fg_color=self.default_color)
        
    def on_leave(self, event):
        self.configure(fg_color=self.default_color)

# ---------- MODERN CARD FRAME SINIFI ----------
class CardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=15, border_width=0, **kwargs)
        self.configure(fg_color=("#2b2b2b", "#1e1e1e"))

# ---------- ANA UYGULAMA ----------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"{_('app_title')} {VERSION}")
        self.geometry("1000x950")
        self.minsize(900, 800)
        
        # Değişkenler
        self.recording = False
        self.process = None
        self.start_time = None
        self.shutdown_after = False
        self.close_app_after = False
        self.was_recording = False
        self.current_filename = None
        self.channel_profiles = []
        self.active_profile_channel = None
        self.scheduled_tasks = []
        
        # İkon ayarı
        self.set_app_icon()
        
        # Tema ayarı
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Ana container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Üst bar
        self.create_title_bar()
        
        # Tabview
        self.create_tabview()
        
        # Timer güncelleme
        self.update_timer()
        self.update_file_size()
        
        # Güncelleme kontrolü
        threading.Thread(target=self.check_for_updates, daemon=True).start()
        
        # Profil listesini her 30 saniyede bir yenile
        def auto_refresh_profiles():
            self.update_profiles_list()
            self.after(30000, auto_refresh_profiles)
        auto_refresh_profiles()
        
        # Kullanıcı verilerini yükle
        self.load_user_data()
        
        # Başlangıç logları
        self.log(_("lang_detected").format(current_lang), "cyan")
        self.log(f"🎥 {_('app_title')} {VERSION} {_('log_start')}", "green")
        self.log("="*50, "white")
        self.log(f"✅ Tek buton sistemi aktif", "purple")
        self.log(f"✅ Otomatik kalite seçimi", "cyan")
        self.log(f"✅ 11 dil desteği!", "cyan")
        self.log(f"👉 {_('log_instruction')}", "cyan")
        
    def create_title_bar(self):
        title_bar = ctk.CTkFrame(self.main_container, height=60, corner_radius=15, fg_color=("#1a1a1a", "#0d0d0d"))
        title_bar.pack(fill="x", pady=(0, 15))
        title_bar.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(title_bar, text=f"🎬 {_('app_title')} {VERSION}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#4CAF50")
        self.title_label.pack(side="left", padx=20, pady=15)
        
        self.status_label = ctk.CTkLabel(title_bar, text=f"● {_('status_ready')}", font=ctk.CTkFont(size=13), text_color="gray")
        self.status_label.pack(side="right", padx=20)
        
    def create_tabview(self):
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=15)
        self.tabview.pack(fill="both", expand=True)
        
        # Sekmeleri dinamik isimlerle ekle
        self.tabview.add(_("tab_record"))
        self.tabview.add(_("tab_scheduler"))
        self.tabview.add(_("tab_profiles"))
        self.tabview.add(_("tab_settings"))
        self.tabview.add(_("tab_logs"))
        
        # Sekme stilleri
        for tab_name in [_("tab_record"), _("tab_scheduler"), _("tab_profiles"), _("tab_settings"), _("tab_logs")]:
            self.tabview.tab(tab_name).configure(fg_color=("#2d2d2d", "#1e1e1e"))
        
        self.create_record_tab()
        self.create_scheduler_tab()
        self.create_profiles_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
    def create_record_tab(self):
        record_tab = self.tabview.tab(_("tab_record"))
        main_card = CardFrame(record_tab)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Kanal girişi
        self.channel_label = ctk.CTkLabel(main_card, text="📺 KANAL ADI", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.channel_label.pack(anchor="w", padx=30, pady=(20, 5))
        
        self.channel_entry = ctk.CTkEntry(main_card, placeholder_text=_("channel_placeholder"), height=45, font=ctk.CTkFont(size=14), corner_radius=10)
        self.channel_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Kalite
        self.quality_label = ctk.CTkLabel(main_card, text="⚙ KALİTE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.quality_label.pack(anchor="w", padx=30, pady=(0, 5))
        
        self.quality_menu = ctk.CTkOptionMenu(main_card, values=[_("quality_auto"), "best", "1080p", "720p", "480p"], height=40, corner_radius=10)
        self.quality_menu.set(_("quality_auto"))
        self.quality_menu.pack(fill="x", padx=30, pady=(0, 15))
        
        # Klasör
        self.folder_label = ctk.CTkLabel(main_card, text="📁 KAYIT KLASÖRÜ", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.folder_label.pack(anchor="w", padx=30, pady=(0, 5))
        
        folder_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        folder_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        self.folder_entry = ctk.CTkEntry(folder_frame, placeholder_text=_("folder_placeholder"), height=40, corner_radius=10)
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.folder_button = AnimatedButton(folder_frame, text=_("folder_select"), width=80, height=40, corner_radius=10, fg_color="#2196F3")
        self.folder_button.configure(command=self.select_folder)
        self.folder_button.pack(side="right")
        
        # Seçenekler
        options_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        options_frame.pack(fill="x", padx=30, pady=10)
        
        self.shutdown_var = ctk.BooleanVar(value=False)
        self.close_app_var = ctk.BooleanVar(value=False)
        
        self.shutdown_check = ctk.CTkCheckBox(options_frame, text=_("shutdown_option"), variable=self.shutdown_var, command=self.on_shutdown_toggle)
        self.shutdown_check.pack(anchor="w", pady=5)
        self.close_app_check = ctk.CTkCheckBox(options_frame, text=_("close_app_option"), variable=self.close_app_var, command=self.on_close_app_toggle)
        self.close_app_check.pack(anchor="w", pady=5)
        
        # Ana buton
        self.toggle_button = AnimatedButton(main_card, text=_("button_start"), height=60, corner_radius=15, font=ctk.CTkFont(size=18, weight="bold"), fg_color="#4CAF50")
        self.toggle_button.configure(command=self.toggle_record)
        self.toggle_button.pack(fill="x", padx=30, pady=20)
        
        # Bilgi çubuğu
        info_bar = ctk.CTkFrame(main_card, height=40, corner_radius=10, fg_color=("#1a1a1a", "#0d0d0d"))
        info_bar.pack(fill="x", padx=30, pady=(10, 20))
        info_bar.pack_propagate(False)
        
        self.timer_label = ctk.CTkLabel(info_bar, text=f"{_('timer')} 00:00:00", font=ctk.CTkFont(size=14))
        self.timer_label.pack(side="left", padx=15, pady=10)
        self.size_label = ctk.CTkLabel(info_bar, text=f"{_('filesize')} -", font=ctk.CTkFont(size=14))
        self.size_label.pack(side="right", padx=15, pady=10)
        
        # Alt butonlar
        bottom_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.history_button = AnimatedButton(bottom_frame, text=_("button_history"), width=120, height=40, corner_radius=10, fg_color="#9C27B0")
        self.history_button.configure(command=self.show_history)
        self.history_button.pack(side="left", padx=5)
        
        self.update_button = AnimatedButton(bottom_frame, text=_("button_update"), width=120, height=40, corner_radius=10, fg_color="#FF9800")
        self.update_button.configure(command=lambda: threading.Thread(target=self.check_for_updates, daemon=True).start())
        self.update_button.pack(side="left", padx=5)
        
    def create_scheduler_tab(self):
        scheduler_tab = self.tabview.tab(_("tab_scheduler"))
        main_card = CardFrame(scheduler_tab)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)
        
        add_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        add_frame.pack(fill="x", padx=20, pady=20)
        
        self.scheduler_channel_label = ctk.CTkLabel(add_frame, text=_("scheduler_channel"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.scheduler_channel_label.pack(anchor="w")
        self.scheduler_channel_entry = ctk.CTkEntry(add_frame, height=40, corner_radius=10)
        self.scheduler_channel_entry.pack(fill="x", pady=(0, 10))
        
        self.scheduler_time_label = ctk.CTkLabel(add_frame, text=_("scheduler_time"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.scheduler_time_label.pack(anchor="w")
        self.scheduler_time_entry = ctk.CTkEntry(add_frame, height=40, corner_radius=10, placeholder_text="14:30")
        self.scheduler_time_entry.pack(fill="x", pady=(0, 10))
        
        self.scheduler_days_label = ctk.CTkLabel(add_frame, text=_("scheduler_days"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.scheduler_days_label.pack(anchor="w")
        
        days_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        days_frame.pack(fill="x", pady=5)
        
        self.day_vars = {}
        days_list = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for i, day in enumerate(days_list):
            self.day_vars[day] = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(days_frame, text=day, variable=self.day_vars[day])
            cb.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
        
        btn_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        
        self.scheduler_add_button = AnimatedButton(btn_frame, text=_("scheduler_add"), width=100, height=35, corner_radius=8, fg_color="#4CAF50")
        self.scheduler_add_button.configure(command=self.add_scheduled_record)
        self.scheduler_add_button.pack(side="left", padx=5)
        
        self.scheduler_delete_button = AnimatedButton(btn_frame, text=_("scheduler_delete"), width=100, height=35, corner_radius=8, fg_color="#f44336")
        self.scheduler_delete_button.configure(command=self.delete_scheduled_record)
        self.scheduler_delete_button.pack(side="left", padx=5)
        
        self.scheduler_stop_button = AnimatedButton(btn_frame, text=_("scheduler_stop"), width=120, height=35, corner_radius=8, fg_color="#FF9800")
        self.scheduler_stop_button.configure(command=self.stop_current_recording)
        self.scheduler_stop_button.pack(side="left", padx=5)
        
        self.scheduler_list_title = ctk.CTkLabel(main_card, text=_("scheduler_list"), font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50")
        self.scheduler_list_title.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.scheduler_listbox = ctk.CTkScrollableFrame(main_card, height=250, corner_radius=10)
        self.scheduler_listbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.scheduler_selected_var = ctk.IntVar(value=-1)
        
    def create_profiles_tab(self):
        profiles_tab = self.tabview.tab(_("tab_profiles"))
        main_card = CardFrame(profiles_tab)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)
        
        add_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        add_frame.pack(fill="x", padx=20, pady=20)
        
        self.profile_channel_label = ctk.CTkLabel(add_frame, text=_("profile_channel"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.profile_channel_label.pack(anchor="w")
        self.profile_channel_entry = ctk.CTkEntry(add_frame, height=40, corner_radius=10)
        self.profile_channel_entry.pack(fill="x", pady=(0, 10))
        
        self.profile_folder_label = ctk.CTkLabel(add_frame, text=_("profile_folder"), font=ctk.CTkFont(size=12, weight="bold"), text_color="#4CAF50")
        self.profile_folder_label.pack(anchor="w")
        folder_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        folder_frame.pack(fill="x", pady=(0, 10))
        
        self.profile_folder_entry = ctk.CTkEntry(folder_frame, placeholder_text=_("folder_placeholder"), height=40, corner_radius=10)
        self.profile_folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.profile_folder_button = AnimatedButton(folder_frame, text=_("folder_select"), width=80, height=40, corner_radius=10, fg_color="#2196F3")
        self.profile_folder_button.configure(command=self.select_profile_folder)
        self.profile_folder_button.pack(side="right")
        
        self.profile_save_button = AnimatedButton(add_frame, text=_("profile_save"), height=40, corner_radius=10, fg_color="#4CAF50")
        self.profile_save_button.configure(command=self.add_profile)
        self.profile_save_button.pack(fill="x", pady=10)
        
        self.profiles_title = ctk.CTkLabel(main_card, text=_("profiles_title"), font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50")
        self.profiles_title.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.profiles_listbox = ctk.CTkScrollableFrame(main_card, height=300, corner_radius=10)
        self.profiles_listbox.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.profiles_delete_button = AnimatedButton(btn_frame, text=_("profile_delete"), width=120, height=40, corner_radius=10, fg_color="#f44336")
        self.profiles_delete_button.configure(command=self.delete_profile)
        self.profiles_delete_button.pack(side="left", padx=5)
        
    def create_settings_tab(self):
        settings_tab = self.tabview.tab(_("tab_settings"))
        main_card = CardFrame(settings_tab)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)
        
        theme_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        theme_frame.pack(fill="x", padx=30, pady=20)
        self.theme_label = ctk.CTkLabel(theme_frame, text=_("theme_label"), font=ctk.CTkFont(size=13, weight="bold"))
        self.theme_label.pack(side="left", padx=10)
        self.theme_menu = ctk.CTkOptionMenu(theme_frame, values=[_("theme_dark"), _("theme_light"), _("theme_system")], width=120, corner_radius=8)
        self.theme_menu.set(_("theme_dark"))
        self.theme_menu.configure(command=self.change_theme)
        self.theme_menu.pack(side="left", padx=10)
        
        lang_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        lang_frame.pack(fill="x", padx=30, pady=20)
        self.language_label = ctk.CTkLabel(lang_frame, text=_("language_label"), font=ctk.CTkFont(size=13, weight="bold"))
        self.language_label.pack(side="left", padx=10)
        self.lang_menu = ctk.CTkOptionMenu(lang_frame, values=list(LANGUAGES.keys()), width=150, corner_radius=8)
        self.lang_menu.set(current_lang)
        self.lang_menu.configure(command=self.change_language)
        self.lang_menu.pack(side="left", padx=10)
        
        info_card = ctk.CTkFrame(main_card, corner_radius=10, fg_color=("#1a1a1a", "#0d0d0d"))
        info_card.pack(pady=30, padx=30, fill="x")
        
        info_text = f"""
    ╔══════════════════════════════════════════╗
    ║        KICK CANLI YAYIN KAYDEDİCİ        ║
    ║                                          ║
    ║      Versiyon: {VERSION}                    ║
    ║      Geliştirici: erneman26              ║
    ║      Dil desteği: 11 dil                 ║
    ║                                          ║
    ║      GitHub: github.com/erneman26        ║
    ╚══════════════════════════════════════════╝
        """
        info_label = ctk.CTkLabel(info_card, text=info_text, font=ctk.CTkFont(size=12, family="Consolas"), justify="left", text_color="#4CAF50")
        info_label.pack(pady=20, padx=20)
        
    def create_logs_tab(self):
        logs_tab = self.tabview.tab(_("tab_logs"))
        self.log_box = ctk.CTkTextbox(logs_tab, corner_radius=10, font=ctk.CTkFont(size=12))
        self.log_box.pack(fill="both", expand=True, padx=20, pady=20)
        self.log_box.configure(state="disabled")
        
    # ---------- FONKSİYONLAR ----------
    def log(self, msg, color="white"):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        console_log(msg, color)
        try:
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"[{now}] {msg}\n", color)
            self.log_box.tag_config(color, foreground=color)
            self.log_box.configure(state="disabled")
            self.log_box.see("end")
        except:
            pass
            
    def set_status(self, text, color):
        try:
            self.status_label.configure(text=f"● {text}", text_color=color)
        except:
            pass
            
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.log(f"📁 Klasör seçildi: {folder}", "green")
            self.save_user_data()
            
    def select_profile_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.profile_folder_entry.delete(0, "end")
            self.profile_folder_entry.insert(0, folder)
            self.log(f"📁 Profil klasörü seçildi: {folder}", "green")
            
    def on_shutdown_toggle(self):
        if self.shutdown_var.get():
            self.close_app_var.set(False)
            self.shutdown_after = True
            self.log(_("shutdown_active"), "purple")
        else:
            self.shutdown_after = False
        self.save_user_data()
            
    def on_close_app_toggle(self):
        if self.close_app_var.get():
            self.shutdown_var.set(False)
            self.close_app_after = True
            self.log(_("close_app_active"), "purple")
        else:
            self.close_app_after = False
        self.save_user_data()
        
    def shutdown_computer(self):
        self.log(f"⚠ Bilgisayar 30 saniye sonra KAPANACAK!", "purple")
        self.log(f"⏰ Kapatmayı iptal etmek için DURDUR butonuna basın!", "orange")
        
        for i in range(30, 0, -1):
            if not self.shutdown_after or not self.was_recording:
                self.log(f"✅ Bilgisayar kapatma iptal edildi!", "green")
                return
            if i % 10 == 0 or i <= 5:
                self.log(f"⏳ Kapatmaya {i} saniye kaldı...", "orange")
            time.sleep(1)
        
        if self.shutdown_after and self.was_recording:
            self.log(f"💻 Bilgisayar kapatılıyor...", "purple")
            os.system("shutdown /s /t 5")
            
    def close_app(self):
        self.log(f"⚠ Uygulama 10 saniye sonra KAPANACAK!", "purple")
        self.log(f"⏰ Kapatmayı iptal etmek için DURDUR butonuna basın!", "orange")
        
        for i in range(10, 0, -1):
            if not self.close_app_after or not self.was_recording:
                self.log(f"✅ Uygulama kapatma iptal edildi!", "green")
                return
            if i <= 3:
                self.log(f"⏳ Uygulama {i} saniye sonra kapanacak...", "orange")
            time.sleep(1)
        
        if self.close_app_after and self.was_recording:
            self.log(f"👋 Uygulama kapatılıyor...", "purple")
            self.quit()
            os._exit(0)
            
    def check_live_simple(self, channel):
        try:
            url = f"https://kick.com/api/v2/channels/{channel}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://kick.com/"
            }
            r = requests.get(url, headers=headers, timeout=8)
            
            if r.status_code == 200:
                data = r.json()
                if "livestream" in data and data["livestream"] is not None:
                    if data["livestream"].get("is_live") == True:
                        return True
                if data.get("is_live") == True:
                    return True
            
            url = f"https://kick.com/{channel}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            if r.status_code == 200:
                html = r.text
                if '"is_live":true' in html or 'isLive":true' in html:
                    return True
                if 'data-testid="live-badge"' in html or 'Live now' in html:
                    return True
            
            result = subprocess.run(
                ["streamlink", f"https://kick.com/{channel}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if "Available streams:" in result.stdout:
                return True
                
            return False
            
        except Exception as e:
            console_log(f"⚠ Canlı kontrol hatası ({channel}): {e}", "orange")
            return False
            
    def find_best_quality(self, channel, selected_quality=None):
        try:
            result = subprocess.run(["streamlink", f"https://kick.com/{channel}"], capture_output=True, text=True, timeout=15)
            available_streams = []
            if "Available streams:" in result.stdout:
                streams_section = result.stdout.split("Available streams:")[1].strip()
                for line in streams_section.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("("):
                        quality = line.split(" ")[0].strip()
                        if quality and quality not in ["worst", "best"]:
                            available_streams.append(quality)
                if "best" in streams_section or "(best)" in streams_section:
                    available_streams.insert(0, "best")
            
            quality_order = ["best", "1080p60", "1080p", "720p60", "720p", "480p", "360p", "160p"]
            available_sorted = [q for q in quality_order if q in available_streams]
            
            if selected_quality and selected_quality not in ["otomatik", "auto", "best"]:
                if selected_quality in available_streams:
                    return selected_quality
                elif available_sorted:
                    return available_sorted[0]
            
            if "best" in available_sorted:
                return "best"
            elif available_sorted:
                return available_sorted[0]
            return "best"
        except:
            return "best"
            
    def start_record(self):
        self.recording = True
        self.was_recording = False
        self.current_filename = None
        self.log(f"🎬 {_('log_start')}", "cyan")
        self.set_status(_("status_waiting"), "orange")
        
        def record_loop():
            channel = self.channel_entry.get().strip().lower()
            selected_quality = self.quality_menu.get()
            folder = self.folder_entry.get()
            
            if selected_quality in ["otomatik", "auto"]:
                quality = self.find_best_quality(channel)
                self.log(f"⚙ Otomatik kalite: {quality}", "green")
            else:
                quality = self.find_best_quality(channel, selected_quality)
                if quality != selected_quality:
                    self.log(f"⚠ '{selected_quality}' mevcut değil, '{quality}' kullanılıyor", "orange")
            
            was_live_before = False
            
            while self.recording:
                try:
                    is_live = self.check_live_simple(channel)
                    
                    if not is_live:
                        self.set_status("ÇEVRİMDIŞI", "red")
                        if was_live_before:
                            self.log(f"📴 Yayın sona erdi! {channel} artık çevrimdışı", "orange")
                            if self.shutdown_after and self.was_recording:
                                threading.Thread(target=self.shutdown_computer, daemon=True).start()
                            elif self.close_app_after and self.was_recording:
                                threading.Thread(target=self.close_app, daemon=True).start()
                            was_live_before = False
                        time.sleep(10)
                        continue
                    else:
                        if not was_live_before:
                            was_live_before = True
                            self.was_recording = True
                            self.log(f"🔴 CANLI YAYIN BAŞLADI! Kayıt alınıyor...", "green")
                            
                            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            channel_folder = os.path.join(folder, channel)
                            if not os.path.exists(channel_folder):
                                os.makedirs(channel_folder)
                            
                            self.current_filename = os.path.join(channel_folder, f"{channel}_{now}.mp4")
                            self.start_time = time.time()
                            self.set_status(_("status_online"), "green")
                            self.log(f"📁 Dosya: {os.path.basename(self.current_filename)}", "cyan")
                            
                            self.process = subprocess.Popen([
                                "streamlink", f"https://kick.com/{channel}", quality, "-o", self.current_filename, "--quiet"
                            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            
                            self.process.wait()
                            
                            if self.current_filename and os.path.exists(self.current_filename):
                                size = os.path.getsize(self.current_filename) / (1024*1024)
                                self.log(f"📊 Kayıt tamamlandı: {size:.2f} MB", "green")
                            
                            self.start_time = None
                            time.sleep(5)
                        else:
                            self.set_status(_("status_online"), "green")
                            time.sleep(1)
                            
                except Exception as e:
                    self.log(f"❌ Döngü hatası: {e}", "red")
                    time.sleep(10)
        
        threading.Thread(target=record_loop, daemon=True).start()
        self.save_user_data()
        
    def stop_record(self):
        self.recording = False
        
        if self.shutdown_after:
            self.shutdown_after = False
            self.shutdown_var.set(False)
        if self.close_app_after:
            self.close_app_after = False
            self.close_app_var.set(False)
        
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except:
                pass
            self.process = None
        
        self.set_status(_("status_stopped"), "gray")
        self.timer_label.configure(text=f"{_('timer')} 00:00:00")
        self.log(f"⏹ Kayıt durduruldu", "orange")
        self.save_user_data()
        
    def toggle_record(self):
        if self.recording:
            self.stop_record()
            self.toggle_button.configure(text=_("button_start"), fg_color="#4CAF50")
        else:
            if not self.channel_entry.get():
                self.log(_("error_channel"), "red")
                return
            if not self.folder_entry.get():
                self.log(_("error_folder"), "red")
                return
            self.start_record()
            self.toggle_button.configure(text=_("button_stop"), fg_color="#f44336")
            
    def update_timer(self):
        if self.recording and self.start_time:
            elapsed = int(time.time() - self.start_time)
            hrs = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            self.timer_label.configure(text=f"⏱ {hrs:02}:{mins:02}:{secs:02}")
        self.after(1000, self.update_timer)
        
    def update_file_size(self):
        if self.recording and self.current_filename and os.path.exists(self.current_filename):
            size = os.path.getsize(self.current_filename) / (1024*1024)
            self.size_label.configure(text=f"💾 {size:.2f} MB")
        self.after(2000, self.update_file_size)
        
    def show_history(self):
        history_file = "kayit_gecmisi.json"
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            messagebox.showinfo("Bilgi", "Henüz kayıt yok")
            return
        
        history_window = ctk.CTkToplevel(self)
        history_window.title("Yayın Geçmişi")
        history_window.geometry("600x400")
        
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for kayit in reversed(history[-50:]):
            info = f"📺 {kayit['kanal']} | ⏱ {kayit.get('sure', '?')} | 💾 {kayit.get('boyut', '?')} | 📅 {kayit['tarih']}"
            ctk.CTkLabel(scroll_frame, text=info, anchor="w").pack(fill="x", pady=2)
            
    def check_for_updates(self):
        try:
            self.log(f"🔄 Güncelleme kontrol ediliyor...", "blue")
            response = requests.get("https://raw.githubusercontent.com/erneman26/Kick-Canli-Yayin-Kaydedici/main/version.json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest = data.get("version", VERSION)
                if latest > VERSION:
                    self.log(f"✨ YENİ VERSİYON MEVCUT: {latest}", "green")
                    if messagebox.askyesno("Güncelleme", f"Yeni versiyon {latest} mevcut. İndirmek ister misiniz?"):
                        webbrowser.open("https://github.com/erneman26/Kick-Canli-Yayin-Kaydedici/releases/latest")
                else:
                    self.log(f"✅ Uygulamanız güncel!", "green")
        except:
            self.log(f"⚠ Güncelleme kontrol edilemedi", "orange")
            
    def change_language(self, choice):
        global current_lang
        
        self.save_user_data()
        self.save_profiles()
        
        current_lang = choice
        
        try:
            with open("language.json", "w", encoding="utf-8") as f:
                json.dump({"language": choice}, f)
        except:
            pass
        
        messagebox.showinfo(_("language_label"), f"Dil '{choice}' olarak değiştirildi. Program yeniden başlatılıyor...")
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    def change_theme(self, choice):
        theme_map = {"Koyu": "dark", "Açık": "light", "Sistem": "system"}
        ctk.set_appearance_mode(theme_map.get(choice, "dark"))
        self.save_user_data()
        
    def load_user_data(self):
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
                if "channel" in data and data["channel"]:
                    self.channel_entry.insert(0, data["channel"])
                if "folder" in data and data["folder"]:
                    self.folder_entry.insert(0, data["folder"])
                if "quality" in data:
                    self.quality_menu.set(data["quality"])
                if "shutdown" in data:
                    self.shutdown_var.set(data["shutdown"])
                    if data["shutdown"]:
                        self.shutdown_after = True
                if "close_app" in data:
                    self.close_app_var.set(data["close_app"])
                    if data["close_app"]:
                        self.close_app_after = True
                if "profiles" in data:
                    self.channel_profiles = data["profiles"]
                    self.update_profiles_list()
                if "schedules" in data:
                    self.scheduled_tasks = data["schedules"]
                    self.update_scheduler_list()
                    
                print("✅ Kullanıcı verileri yüklendi")
        except FileNotFoundError:
            print("⚠ Kullanıcı verileri bulunamadı (ilk çalıştırma)")
        except Exception as e:
            print(f"⚠ Kullanıcı verileri yüklenemedi: {e}")
            
    def save_user_data(self):
        try:
            data = {
                "channel": self.channel_entry.get(),
                "folder": self.folder_entry.get(),
                "quality": self.quality_menu.get(),
                "shutdown": self.shutdown_var.get(),
                "close_app": self.close_app_var.get(),
                "profiles": self.channel_profiles,
                "schedules": self.scheduled_tasks
            }
            with open("user_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("✅ Kullanıcı verileri kaydedildi")
        except Exception as e:
            print(f"⚠ Veri kaydedilemedi: {e}")
            
    def load_profiles(self):
        try:
            if os.path.exists(PROFILES_FILE):
                with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                    self.channel_profiles = json.load(f)
                self.update_profiles_list()
        except:
            self.channel_profiles = []
            
    def save_profiles(self):
        try:
            with open(PROFILES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.channel_profiles, f, indent=2, ensure_ascii=False)
        except:
            pass
            
    def add_profile(self):
        channel = self.profile_channel_entry.get().strip().lower()
        folder = self.profile_folder_entry.get().strip()
        
        if not channel:
            self.log(_("error_channel"), "red")
            return
        
        for p in self.channel_profiles:
            if p['channel'] == channel:
                self.log(_("profile_exists").format(channel), "orange")
                return
        
        self.channel_profiles.append({"channel": channel, "folder": folder})
        self.save_profiles()
        self.save_user_data()
        self.update_profiles_list()
        self.log(_("profile_added").format(channel), "green")
        self.profile_channel_entry.delete(0, "end")
        self.profile_folder_entry.delete(0, "end")
        
    def delete_profile(self):
        if self.channel_profiles:
            removed = self.channel_profiles.pop()
            if self.active_profile_channel == removed['channel']:
                self.active_profile_channel = None
                self.channel_entry.delete(0, "end")
                self.folder_entry.delete(0, "end")
            self.save_profiles()
            self.save_user_data()
            self.update_profiles_list()
            self.log(_("profile_deleted").format(removed['channel']), "orange")
            
    def on_profile_click(self, channel, folder):
        if self.active_profile_channel == channel:
            self.active_profile_channel = None
            self.channel_entry.delete(0, "end")
            self.folder_entry.delete(0, "end")
            self.log(f"❌ Seçim kaldırıldı: {channel}", "orange")
        else:
            self.active_profile_channel = channel
            self.channel_entry.delete(0, "end")
            self.channel_entry.insert(0, channel)
            if folder:
                self.folder_entry.delete(0, "end")
                self.folder_entry.insert(0, folder)
            self.log(f"✅ Profil seçildi: {channel}", "green")
        self.update_profiles_list()
        self.save_user_data()
        
    def update_profiles_list(self):
        for widget in self.profiles_listbox.winfo_children():
            widget.destroy()
        
        if self.channel_profiles:
            for profile in self.channel_profiles:
                channel_name = profile['channel']
                folder_name = os.path.basename(profile.get('folder', '')) if profile.get('folder') else ""
                is_live = self.check_live_simple(channel_name)
                is_active = (self.active_profile_channel == channel_name)
                
                if is_live:
                    status_icon = "🟢"
                    status_text = "CANLI"
                    status_color = "#4CAF50"
                else:
                    status_icon = "🔴"
                    status_text = "YAYINDA DEĞİL"
                    status_color = "#f44336"
                
                if is_active:
                    frame = ctk.CTkFrame(self.profiles_listbox, corner_radius=8, fg_color=("#2a4a2a", "#1a3a1a"), border_width=2, border_color="#4CAF50")
                else:
                    frame = ctk.CTkFrame(self.profiles_listbox, corner_radius=8, fg_color=("#3a3a3a", "#2a2a2a"))
                frame.pack(fill="x", padx=5, pady=3)
                frame.bind("<Button-1>", lambda e, ch=channel_name, f=profile.get('folder', ''): self.on_profile_click(ch, f))
                
                name_label = ctk.CTkLabel(frame, text=f"{status_icon} {channel_name}" + (f"  📁 {folder_name}" if folder_name else ""), anchor="w", font=ctk.CTkFont(size=13))
                name_label.pack(side="left", fill="x", expand=True, padx=10, pady=8)
                name_label.bind("<Button-1>", lambda e, ch=channel_name, f=profile.get('folder', ''): self.on_profile_click(ch, f))
                
                if is_active:
                    active_label = ctk.CTkLabel(frame, text=_("active_profile"), text_color="#4CAF50", font=ctk.CTkFont(size=10, weight="bold"), width=60)
                    active_label.pack(side="right", padx=5)
                    active_label.bind("<Button-1>", lambda e, ch=channel_name, f=profile.get('folder', ''): self.on_profile_click(ch, f))
                
                status_label = ctk.CTkLabel(frame, text=status_text, text_color=status_color, font=ctk.CTkFont(size=11, weight="bold"), width=80)
                status_label.pack(side="right", padx=10)
                status_label.bind("<Button-1>", lambda e, ch=channel_name, f=profile.get('folder', ''): self.on_profile_click(ch, f))
        else:
            empty_label = ctk.CTkLabel(self.profiles_listbox, text=_("scheduler_empty"), anchor="w")
            empty_label.pack(fill="x", padx=5, pady=2)
            
    def add_scheduled_record(self):
        channel = self.scheduler_channel_entry.get().strip().lower()
        time_str = self.scheduler_time_entry.get().strip()
        selected_days = [day for day, var in self.day_vars.items() if var.get()]
        
        if not channel or not time_str or not selected_days:
            self.log("Lütfen tüm alanları doldurun!", "red")
            return
        
        self.scheduled_tasks.append([channel, time_str, selected_days])
        self.update_scheduler_list()
        self.save_user_data()
        self.log(f"📅 Plan eklendi: {channel} - {time_str}", "green")
        
        self.scheduler_channel_entry.delete(0, "end")
        self.scheduler_time_entry.delete(0, "end")
        for var in self.day_vars.values():
            var.set(False)
            
    def delete_scheduled_record(self):
        if self.scheduler_selected_var.get() >= 0:
            idx = self.scheduler_selected_var.get()
            if 0 <= idx < len(self.scheduled_tasks):
                removed = self.scheduled_tasks.pop(idx)
                self.update_scheduler_list()
                self.save_user_data()
                self.log(f"❌ Plan silindi: {removed[0]}", "orange")
                
    def update_scheduler_list(self):
        for widget in self.scheduler_listbox.winfo_children():
            widget.destroy()
        
        for idx, task in enumerate(self.scheduled_tasks):
            days_str = ", ".join(task[2])
            frame = ctk.CTkFrame(self.scheduler_listbox, corner_radius=8, fg_color=("#3a3a3a", "#2a2a2a"))
            frame.pack(fill="x", padx=5, pady=3)
            
            text = f"📺 {task[0]} | ⏰ {task[1]} | 📅 {days_str}"
            label = ctk.CTkLabel(frame, text=text, anchor="w", font=ctk.CTkFont(size=12))
            label.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            radio = ctk.CTkRadioButton(frame, text="", variable=self.scheduler_selected_var, value=idx, width=20)
            radio.pack(side="right", padx=10)
            
    def stop_current_recording(self):
        if self.recording:
            self.stop_record()
            self.log("⏹ Kayıt durduruldu", "orange")
            self.toggle_button.configure(text=_("button_start"), fg_color="#4CAF50")
        else:
            self.log("⚠ Aktif kayıt yok!", "orange")
            
    def set_app_icon(self):
        try:
            if getattr(sys, 'frozen', False):
                path = sys._MEIPASS
            else:
                path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(path, "kick.ico")
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    console_log("✅ İkon yüklendi", "green")
                except:
                    pass
        except:
            pass
    
    def on_closing(self):
        if self.recording:
            if messagebox.askyesno("Uyarı", "Kayıt devam ediyor! Gerçekten çıkmak istiyor musunuz?"):
                self.save_user_data()
                self.save_profiles()
                self.destroy()
        else:
            self.save_user_data()
            self.save_profiles()
            self.destroy()

# ---------- UYGULAMAYI BAŞLAT ----------
PROFILES_FILE = "profiller.json"

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print(Renkler.YESIL + "\n" + "-"*70)
    print(f"✅ {_('app_title')} {VERSION} başlatıldı")
    print(f"🌍 Sistem dili: {current_lang}")
    print("-"*70 + "\n" + Renkler.SON)
    
    app.mainloop()
