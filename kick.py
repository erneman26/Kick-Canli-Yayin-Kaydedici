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

# ---------- DİL DOSYASI (TÜM DİLLER) ----------
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
    },
    "English": {
        "channel_placeholder": "Channel name",
        "quality_auto": "auto",
        "quality_best": "best",
        "folder_placeholder": "Save folder",
        "folder_select": "Browse",
        "shutdown_title": "SHUTDOWN OPTIONS (only one can be selected)",
        "shutdown_option": "Shutdown computer when stream ends",
        "close_app_option": "Close app when stream ends",
        "other_title": "OTHER SETTINGS",
        "theme_label": "Theme:",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "theme_system": "System",
        "button_start": "START",
        "button_stop": "STOP",
        "button_history": "Stream History",
        "button_update": "Update",
        "status_ready": "READY",
        "status_waiting": "WAITING",
        "status_online": "RECORDING",
        "status_offline": "OFFLINE",
        "status_stopped": "STOPPED",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Program started",
        "log_button": "Single button system active",
        "log_quality": "Auto quality selection",
        "log_internet": "Internet loss tolerance",
        "log_instruction": "Enter channel name and click START",
        "error_channel": "Please enter channel name",
        "error_folder": "Please select save folder",
        "shutdown_active": "Shutdown after stream ACTIVE",
        "close_app_active": "Close app after stream ACTIVE",
        "shutdown_cancel": "Shutdown cancelled",
        "close_app_cancel": "App close cancelled",
        "shutdown_warning": "Computer will SHUTDOWN in 30 seconds! Recording finished.",
        "close_app_warning": "App will CLOSE in 10 seconds! Recording finished.",
        "shutdown_countdown": "{} seconds until shutdown...",
        "close_app_countdown": "App closing in {} seconds...",
        "cancel_shutdown": "Press STOP to cancel!",
        "internet_lost": "Internet connection lost! Waiting...",
        "internet_back": "Internet connection restored!",
        "no_internet": "No internet, waiting 30 seconds...",
        "stream_ended": "Stream ended! {} is offline",
        "stream_started": "LIVE STREAM STARTED! Recording...",
        "folder_created": "Channel folder created: {}",
        "file_info": "File: {}",
        "file_size": "Saved file size: {}",
        "total_size": "Total file size: {}",
        "current_size": "Current file size: {}",
        "recording_stopped": "Recording stopped",
        "final_size": "Recording stopped - Final file size: {}",
        "update_check": "Checking for updates...",
        "update_available": "NEW VERSION AVAILABLE: {}",
        "update_current": "Your app is up to date!",
        "update_error": "Could not reach update server",
        "update_timeout": "Update check timed out",
        "update_connection_error": "No internet connection for update check",
        "update_download": "Download page opened",
        "update_later": "Update postponed",
        "update_question": "Open download page now?",
        "update_title": "UPDATE AVAILABLE",
        "update_downloaded": "Download page opened in your browser.",
        "update_complete": "Complete",
        "error_streamlink": "Streamlink not found! Download from https://streamlink.github.io/",
        "error_streamlink_title": "Error",
        "error_generic": "Streamlink error: {}",
        "exit_warning": "Recording in progress! Are you sure you want to exit?",
        "exit_title": "Warning",
        "exit_message": "Closing program...",
    },
    "Deutsch": {
        "channel_placeholder": "Kanalname",
        "quality_auto": "auto",
        "quality_best": "beste",
        "folder_placeholder": "Speicherordner",
        "folder_select": "Wählen",
        "shutdown_title": "AUSSCHALTEN (nur eine Option)",
        "shutdown_option": "Computer ausschalten",
        "close_app_option": "App schließen",
        "other_title": "WEITERE EINSTELLUNGEN",
        "theme_label": "Thema:",
        "theme_dark": "Dunkel",
        "theme_light": "Hell",
        "theme_system": "System",
        "button_start": "START",
        "button_stop": "STOP",
        "button_history": "Verlauf",
        "button_update": "Update",
        "status_ready": "BEREIT",
        "status_waiting": "WARTEN",
        "status_online": "AUFNAHME",
        "status_offline": "OFFLINE",
        "status_stopped": "GESTOPPT",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programm gestartet",
        "log_button": "Ein-Knopf-System aktiv",
        "log_quality": "Automatische Qualität",
        "log_internet": "Internetausfall Toleranz",
        "log_instruction": "Kanalnamen eingeben und START klicken",
        "error_channel": "Bitte Kanalnamen eingeben",
        "error_folder": "Bitte Speicherordner wählen",
        "shutdown_active": "Ausschalten nach Stream AKTIV",
        "close_app_active": "App schließen nach Stream AKTIV",
        "shutdown_cancel": "Ausschalten abgebrochen",
        "close_app_cancel": "Schließen abgebrochen",
        "shutdown_warning": "Computer wird in 30 Sekunden AUSGESCHALTET!",
        "close_app_warning": "App wird in 10 Sekunden GESCHLOSSEN!",
        "shutdown_countdown": "{} Sekunden bis zum Ausschalten...",
        "close_app_countdown": "App schließt in {} Sekunden...",
        "cancel_shutdown": "STOP drücken zum Abbrechen!",
        "internet_lost": "Internetverbindung verloren! Warten...",
        "internet_back": "Internetverbindung wiederhergestellt!",
        "no_internet": "Kein Internet, warte 30 Sekunden...",
        "stream_ended": "Stream beendet! {} ist offline",
        "stream_started": "LIVESTREAM GESTARTET! Aufnahme...",
        "folder_created": "Kanalordner erstellt: {}",
        "file_info": "Datei: {}",
        "file_size": "Gespeicherte Größe: {}",
        "total_size": "Gesamtgröße: {}",
        "current_size": "Aktuelle Größe: {}",
        "recording_stopped": "Aufnahme gestoppt",
        "final_size": "Aufnahme gestoppt - Endgültige Größe: {}",
        "update_check": "Suche nach Updates...",
        "update_available": "NEUE VERSION VERFÜGBAR: {}",
        "update_current": "Ihre App ist aktuell!",
        "update_error": "Update-Server nicht erreichbar",
        "update_timeout": "Update-Timeout",
        "update_connection_error": "Keine Internetverbindung",
        "update_download": "Download-Seite geöffnet",
        "update_later": "Update verschoben",
        "update_question": "Download-Seite jetzt öffnen?",
        "update_title": "UPDATE VERFÜGBAR",
        "update_downloaded": "Download-Seite im Browser geöffnet.",
        "update_complete": "Fertig",
        "error_streamlink": "Streamlink nicht gefunden! https://streamlink.github.io/",
        "error_streamlink_title": "Fehler",
        "error_generic": "Streamlink-Fehler: {}",
        "exit_warning": "Aufnahme läuft! Wirklich beenden?",
        "exit_title": "Warnung",
        "exit_message": "Programm wird geschlossen...",
    },
    "Français": {
        "channel_placeholder": "Nom de la chaîne",
        "quality_auto": "auto",
        "quality_best": "meilleure",
        "folder_placeholder": "Dossier de sauvegarde",
        "folder_select": "Choisir",
        "shutdown_title": "OPTIONS D'ARRÊT (une seule possible)",
        "shutdown_option": "Éteindre l'ordinateur",
        "close_app_option": "Fermer l'application",
        "other_title": "AUTRES PARAMÈTRES",
        "theme_label": "Thème:",
        "theme_dark": "Sombre",
        "theme_light": "Clair",
        "theme_system": "Système",
        "button_start": "DÉMARRER",
        "button_stop": "ARRÊTER",
        "button_history": "Historique",
        "button_update": "Mettre à jour",
        "status_ready": "PRÊT",
        "status_waiting": "ATTENTE",
        "status_online": "ENREGISTREMENT",
        "status_offline": "HORS LIGNE",
        "status_stopped": "ARRÊTÉ",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programme démarré",
        "log_button": "Système à un bouton actif",
        "log_quality": "Sélection automatique de la qualité",
        "log_internet": "Tolérance de perte Internet",
        "log_instruction": "Entrez le nom de la chaîne et cliquez sur DÉMARRER",
        "error_channel": "Veuillez entrer le nom de la chaîne",
        "error_folder": "Veuillez sélectionner le dossier de sauvegarde",
        "shutdown_active": "Extinction après le stream ACTIVE",
        "close_app_active": "Fermeture après le stream ACTIVE",
        "shutdown_cancel": "Extinction annulée",
        "close_app_cancel": "Fermeture annulée",
        "shutdown_warning": "L'ordinateur va s'ÉTEINDRE dans 30 secondes!",
        "close_app_warning": "L'application va se FERMER dans 10 secondes!",
        "shutdown_countdown": "{} secondes avant extinction...",
        "close_app_countdown": "Fermeture dans {} secondes...",
        "cancel_shutdown": "Appuyez sur ARRÊTER pour annuler!",
        "internet_lost": "Connexion Internet perdue! Attente...",
        "internet_back": "Connexion Internet rétablie!",
        "no_internet": "Pas d'Internet, attente 30 secondes...",
        "stream_ended": "Stream terminé! {} est hors ligne",
        "stream_started": "STREAM EN DIRECT DÉMARRÉ! Enregistrement...",
        "folder_created": "Dossier de chaîne créé: {}",
        "file_info": "Fichier: {}",
        "file_size": "Taille sauvegardée: {}",
        "total_size": "Taille totale: {}",
        "current_size": "Taille actuelle: {}",
        "recording_stopped": "Enregistrement arrêté",
        "final_size": "Enregistrement arrêté - Taille finale: {}",
        "update_check": "Vérification des mises à jour...",
        "update_available": "NOUVELLE VERSION DISPONIBLE: {}",
        "update_current": "Votre application est à jour!",
        "update_error": "Serveur de mise à jour inaccessible",
        "update_timeout": "Délai de vérification dépassé",
        "update_connection_error": "Pas de connexion Internet",
        "update_download": "Page de téléchargement ouverte",
        "update_later": "Mise à jour reportée",
        "update_question": "Ouvrir la page de téléchargement maintenant?",
        "update_title": "MISE À JOUR DISPONIBLE",
        "update_downloaded": "Page de téléchargement ouverte dans votre navigateur.",
        "update_complete": "Terminé",
        "error_streamlink": "Streamlink introuvable! https://streamlink.github.io/",
        "error_streamlink_title": "Erreur",
        "error_generic": "Erreur Streamlink: {}",
        "exit_warning": "Enregistrement en cours! Voulez-vous vraiment quitter?",
        "exit_title": "Avertissement",
        "exit_message": "Fermeture du programme...",
    },
    "Español": {
        "channel_placeholder": "Nombre del canal",
        "quality_auto": "auto",
        "quality_best": "mejor",
        "folder_placeholder": "Carpeta de guardado",
        "folder_select": "Seleccionar",
        "shutdown_title": "OPCIONES DE APAGADO (solo una)",
        "shutdown_option": "Apagar la PC",
        "close_app_option": "Cerrar la aplicación",
        "other_title": "OTRAS CONFIGURACIONES",
        "theme_label": "Tema:",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "button_start": "INICIAR",
        "button_stop": "DETENER",
        "button_history": "Historial",
        "button_update": "Actualizar",
        "status_ready": "LISTO",
        "status_waiting": "ESPERANDO",
        "status_online": "GRABANDO",
        "status_offline": "DESCONECTADO",
        "status_stopped": "DETENIDO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programa iniciado",
        "log_button": "Sistema de un botón activo",
        "log_quality": "Selección automática de calidad",
        "log_internet": "Tolerancia a pérdida de Internet",
        "log_instruction": "Ingrese nombre del canal y haga clic en INICIAR",
        "error_channel": "Por favor ingrese nombre del canal",
        "error_folder": "Por favor seleccione carpeta de guardado",
        "shutdown_active": "Apagado después del stream ACTIVO",
        "close_app_active": "Cierre después del stream ACTIVO",
        "shutdown_cancel": "Apagado cancelado",
        "close_app_cancel": "Cierre cancelado",
        "shutdown_warning": "La PC se APAGARÁ en 30 segundos!",
        "close_app_warning": "La aplicación se CERRARÁ en 10 segundos!",
        "shutdown_countdown": "{} segundos para apagado...",
        "close_app_countdown": "Cierre en {} segundos...",
        "cancel_shutdown": "Presione DETENER para cancelar!",
        "internet_lost": "Conexión a Internet perdida! Esperando...",
        "internet_back": "Conexión a Internet restablecida!",
        "no_internet": "Sin Internet, esperando 30 segundos...",
        "stream_ended": "Stream terminado! {} está desconectado",
        "stream_started": "STREAM EN VIVO INICIADO! Grabando...",
        "folder_created": "Carpeta de canal creada: {}",
        "file_info": "Archivo: {}",
        "file_size": "Tamaño guardado: {}",
        "total_size": "Tamaño total: {}",
        "current_size": "Tamaño actual: {}",
        "recording_stopped": "Grabación detenida",
        "final_size": "Grabación detenida - Tamaño final: {}",
        "update_check": "Buscando actualizaciones...",
        "update_available": "NUEVA VERSIÓN DISPONIBLE: {}",
        "update_current": "Su aplicación está actualizada!",
        "update_error": "No se pudo conectar al servidor",
        "update_timeout": "Tiempo de espera agotado",
        "update_connection_error": "Sin conexión a Internet",
        "update_download": "Página de descarga abierta",
        "update_later": "Actualización pospuesta",
        "update_question": "¿Abrir página de descarga ahora?",
        "update_title": "ACTUALIZACIÓN DISPONIBLE",
        "update_downloaded": "Página de descarga abierta en su navegador.",
        "update_complete": "Completado",
        "error_streamlink": "Streamlink no encontrado! https://streamlink.github.io/",
        "error_streamlink_title": "Error",
        "error_generic": "Error de Streamlink: {}",
        "exit_warning": "Grabación en curso! ¿Seguro que quiere salir?",
        "exit_title": "Advertencia",
        "exit_message": "Cerrando programa...",
    },
    "Italiano": {
        "channel_placeholder": "Nome canale",
        "quality_auto": "auto",
        "quality_best": "migliore",
        "folder_placeholder": "Cartella salvataggio",
        "folder_select": "Scegli",
        "shutdown_title": "OPZIONI SPEGNIMENTO (solo una)",
        "shutdown_option": "Spegni PC",
        "close_app_option": "Chiudi app",
        "other_title": "ALTRE IMPOSTAZIONI",
        "theme_label": "Tema:",
        "theme_dark": "Scuro",
        "theme_light": "Chiaro",
        "theme_system": "Sistema",
        "button_start": "AVVIA",
        "button_stop": "FERMA",
        "button_history": "Cronologia",
        "button_update": "Aggiorna",
        "status_ready": "PRONTO",
        "status_waiting": "IN ATTESA",
        "status_online": "REGISTRAZIONE",
        "status_offline": "OFFLINE",
        "status_stopped": "FERMATO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programma avviato",
        "log_button": "Sistema a pulsante singolo attivo",
        "log_quality": "Selezione qualità automatica",
        "log_internet": "Tolleranza perdita Internet",
        "log_instruction": "Inserisci nome canale e clicca AVVIA",
        "error_channel": "Inserisci nome canale",
        "error_folder": "Seleziona cartella salvataggio",
        "shutdown_active": "Spegnimento dopo stream ATTIVO",
        "close_app_active": "Chiusura app dopo stream ATTIVA",
        "shutdown_cancel": "Spegnimento annullato",
        "close_app_cancel": "Chiusura annullata",
        "shutdown_warning": "Il PC si SPEGNERÀ tra 30 secondi!",
        "close_app_warning": "L'app si CHIUDERÀ tra 10 secondi!",
        "shutdown_countdown": "{} secondi allo spegnimento...",
        "close_app_countdown": "Chiusura tra {} secondi...",
        "cancel_shutdown": "Premi FERMA per annullare!",
        "internet_lost": "Connessione Internet persa! Attesa...",
        "internet_back": "Connessione Internet ripristinata!",
        "no_internet": "Nessuna Internet, attesa 30 secondi...",
        "stream_ended": "Stream terminato! {} è offline",
        "stream_started": "STREAM LIVE INIZIATO! Registrazione...",
        "folder_created": "Cartella canale creata: {}",
        "file_info": "File: {}",
        "file_size": "Dimensione salvata: {}",
        "total_size": "Dimensione totale: {}",
        "current_size": "Dimensione attuale: {}",
        "recording_stopped": "Registrazione fermata",
        "final_size": "Registrazione fermata - Dimensione finale: {}",
        "update_check": "Controllo aggiornamenti...",
        "update_available": "NUOVA VERSIONE DISPONIBILE: {}",
        "update_current": "L'app è aggiornata!",
        "update_error": "Server aggiornamenti non raggiungibile",
        "update_timeout": "Timeout controllo",
        "update_connection_error": "Nessuna connessione Internet",
        "update_download": "Pagina download aperta",
        "update_later": "Aggiornamento posticipato",
        "update_question": "Aprire pagina download ora?",
        "update_title": "AGGIORNAMENTO DISPONIBILE",
        "update_downloaded": "Pagina download aperta nel browser.",
        "update_complete": "Completato",
        "error_streamlink": "Streamlink non trovato! https://streamlink.github.io/",
        "error_streamlink_title": "Errore",
        "error_generic": "Errore Streamlink: {}",
        "exit_warning": "Registrazione in corso! Uscire?",
        "exit_title": "Attenzione",
        "exit_message": "Chiusura programma...",
    },
    "Português": {
        "channel_placeholder": "Nome do canal",
        "quality_auto": "auto",
        "quality_best": "melhor",
        "folder_placeholder": "Pasta de salvamento",
        "folder_select": "Escolher",
        "shutdown_title": "OPÇÕES DE DESLIGAMENTO (apenas uma)",
        "shutdown_option": "Desligar PC",
        "close_app_option": "Fechar app",
        "other_title": "OUTRAS CONFIGURAÇÕES",
        "theme_label": "Tema:",
        "theme_dark": "Escuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "button_start": "INICIAR",
        "button_stop": "PARAR",
        "button_history": "Histórico",
        "button_update": "Atualizar",
        "status_ready": "PRONTO",
        "status_waiting": "AGUARDANDO",
        "status_online": "GRAVANDO",
        "status_offline": "OFFLINE",
        "status_stopped": "PARADO",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Programa iniciado",
        "log_button": "Sistema de botão único ativo",
        "log_quality": "Seleção automática de qualidade",
        "log_internet": "Tolerância a perda de Internet",
        "log_instruction": "Digite nome do canal e clique em INICIAR",
        "error_channel": "Digite nome do canal",
        "error_folder": "Selecione pasta de salvamento",
        "shutdown_active": "Desligar após stream ATIVO",
        "close_app_active": "Fechar app após stream ATIVA",
        "shutdown_cancel": "Desligamento cancelado",
        "close_app_cancel": "Fechamento cancelado",
        "shutdown_warning": "O PC DESLIGARÁ em 30 segundos!",
        "close_app_warning": "O app FECHARÁ em 10 segundos!",
        "shutdown_countdown": "{} segundos para desligar...",
        "close_app_countdown": "Fechamento em {} segundos...",
        "cancel_shutdown": "Pressione PARAR para cancelar!",
        "internet_lost": "Conexão perdida! Aguardando...",
        "internet_back": "Conexão restaurada!",
        "no_internet": "Sem Internet, aguardando 30 segundos...",
        "stream_ended": "Stream terminou! {} está offline",
        "stream_started": "STREAM AO VIVO INICIADO! Gravando...",
        "folder_created": "Pasta do canal criada: {}",
        "file_info": "Arquivo: {}",
        "file_size": "Tamanho salvo: {}",
        "total_size": "Tamanho total: {}",
        "current_size": "Tamanho atual: {}",
        "recording_stopped": "Gravação parada",
        "final_size": "Gravação parada - Tamanho final: {}",
        "update_check": "Verificando atualizações...",
        "update_available": "NOVA VERSÃO DISPONÍVEL: {}",
        "update_current": "Seu app está atualizado!",
        "update_error": "Servidor de atualização inacessível",
        "update_timeout": "Tempo limite excedido",
        "update_connection_error": "Sem conexão com Internet",
        "update_download": "Página de download aberta",
        "update_later": "Atualização adiada",
        "update_question": "Abrir página de download agora?",
        "update_title": "ATUALIZAÇÃO DISPONÍVEL",
        "update_downloaded": "Página de download aberta no navegador.",
        "update_complete": "Concluído",
        "error_streamlink": "Streamlink não encontrado! https://streamlink.github.io/",
        "error_streamlink_title": "Erro",
        "error_generic": "Erro Streamlink: {}",
        "exit_warning": "Gravação em andamento! Sair?",
        "exit_title": "Aviso",
        "exit_message": "Fechando programa...",
    },
    "Русский": {
        "channel_placeholder": "Название канала",
        "quality_auto": "авто",
        "quality_best": "лучшее",
        "folder_placeholder": "Папка сохранения",
        "folder_select": "Выбрать",
        "shutdown_title": "ЗАВЕРШЕНИЕ (только одно)",
        "shutdown_option": "Выключить ПК",
        "close_app_option": "Закрыть приложение",
        "other_title": "ДРУГИЕ НАСТРОЙКИ",
        "theme_label": "Тема:",
        "theme_dark": "Тёмная",
        "theme_light": "Светлая",
        "theme_system": "Системная",
        "button_start": "СТАРТ",
        "button_stop": "СТОП",
        "button_history": "История",
        "button_update": "Обновить",
        "status_ready": "ГОТОВ",
        "status_waiting": "ОЖИДАНИЕ",
        "status_online": "ЗАПИСЬ",
        "status_offline": "ОФФЛАЙН",
        "status_stopped": "ОСТАНОВЛЕНО",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "Программа запущена",
        "log_button": "Система одной кнопки активна",
        "log_quality": "Авто выбор качества",
        "log_internet": "Устойчивость к сбоям",
        "log_instruction": "Введите название канала и нажмите СТАРТ",
        "error_channel": "Введите название канала",
        "error_folder": "Выберите папку сохранения",
        "shutdown_active": "Выключение после стрима АКТИВНО",
        "close_app_active": "Закрытие после стрима АКТИВНО",
        "shutdown_cancel": "Выключение отменено",
        "close_app_cancel": "Закрытие отменено",
        "shutdown_warning": "ПК ВЫКЛЮЧИТСЯ через 30 сек!",
        "close_app_warning": "Приложение ЗАКРОЕТСЯ через 10 сек!",
        "shutdown_countdown": "{} сек до выключения...",
        "close_app_countdown": "Закрытие через {} сек...",
        "cancel_shutdown": "Нажмите СТОП для отмены!",
        "internet_lost": "Потеря интернета! Ожидание...",
        "internet_back": "Интернет восстановлен!",
        "no_internet": "Нет интернета, ждём 30 сек...",
        "stream_ended": "Стрим окончен! {} оффлайн",
        "stream_started": "СТРИМ НАЧАЛСЯ! Запись...",
        "folder_created": "Папка канала создана: {}",
        "file_info": "Файл: {}",
        "file_size": "Сохранённый размер: {}",
        "total_size": "Общий размер: {}",
        "current_size": "Текущий размер: {}",
        "recording_stopped": "Запись остановлена",
        "final_size": "Запись остановлена - Конечный размер: {}",
        "update_check": "Проверка обновлений...",
        "update_available": "ДОСТУПНА НОВАЯ ВЕРСИЯ: {}",
        "update_current": "Приложение обновлено!",
        "update_error": "Сервер недоступен",
        "update_timeout": "Таймаут проверки",
        "update_connection_error": "Нет интернета",
        "update_download": "Страница загрузки открыта",
        "update_later": "Обновление отложено",
        "update_question": "Открыть страницу загрузки?",
        "update_title": "ОБНОВЛЕНИЕ",
        "update_downloaded": "Страница открыта в браузере.",
        "update_complete": "Готово",
        "error_streamlink": "Streamlink не найден! https://streamlink.github.io/",
        "error_streamlink_title": "Ошибка",
        "error_generic": "Ошибка Streamlink: {}",
        "exit_warning": "Идёт запись! Выйти?",
        "exit_title": "Предупреждение",
        "exit_message": "Закрытие программы...",
    },
    "日本語": {
        "channel_placeholder": "チャンネル名",
        "quality_auto": "自動",
        "quality_best": "最高",
        "folder_placeholder": "保存先",
        "folder_select": "選択",
        "shutdown_title": "シャットダウン (1つだけ選択)",
        "shutdown_option": "PCをシャットダウン",
        "close_app_option": "アプリを閉じる",
        "other_title": "その他の設定",
        "theme_label": "テーマ:",
        "theme_dark": "ダーク",
        "theme_light": "ライト",
        "theme_system": "システム",
        "button_start": "開始",
        "button_stop": "停止",
        "button_history": "履歴",
        "button_update": "更新",
        "status_ready": "準備完了",
        "status_waiting": "待機中",
        "status_online": "録画中",
        "status_offline": "オフライン",
        "status_stopped": "停止",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "プログラム起動",
        "log_button": "シングルボタンシステム",
        "log_quality": "自動画質選択",
        "log_internet": "インターネット切断耐性",
        "log_instruction": "チャンネル名を入力して開始をクリック",
        "error_channel": "チャンネル名を入力してください",
        "error_folder": "保存先を選択してください",
        "shutdown_active": "終了時シャットダウンON",
        "close_app_active": "終了時アプリ終了ON",
        "shutdown_cancel": "シャットダウンキャンセル",
        "close_app_cancel": "アプリ終了キャンセル",
        "shutdown_warning": "30秒後にPCをシャットダウン",
        "close_app_warning": "10秒後にアプリを終了",
        "shutdown_countdown": "シャットダウンまで{}秒",
        "close_app_countdown": "アプリ終了まで{}秒",
        "cancel_shutdown": "停止ボタンでキャンセル",
        "internet_lost": "インターネット切断",
        "internet_back": "インターネット復旧",
        "no_internet": "インターネットなし",
        "stream_ended": "配信終了: {}",
        "stream_started": "配信開始! 録画中...",
        "folder_created": "フォルダ作成: {}",
        "file_info": "ファイル: {}",
        "file_size": "保存サイズ: {}",
        "total_size": "合計サイズ: {}",
        "current_size": "現在サイズ: {}",
        "recording_stopped": "録画停止",
        "final_size": "最終サイズ: {}",
        "update_check": "更新確認中...",
        "update_available": "新しいバージョン: {}",
        "update_current": "最新バージョン",
        "update_error": "サーバーに接続できません",
        "update_timeout": "タイムアウト",
        "update_connection_error": "インターネット接続なし",
        "update_download": "ダウンロードページを開きました",
        "update_later": "更新を後で実行",
        "update_question": "ダウンロードページを開きますか？",
        "update_title": "更新があります",
        "update_downloaded": "ダウンロードページを開きました",
        "update_complete": "完了",
        "error_streamlink": "Streamlinkが見つかりません",
        "error_streamlink_title": "エラー",
        "error_generic": "Streamlinkエラー: {}",
        "exit_warning": "録画中です。終了しますか？",
        "exit_title": "警告",
        "exit_message": "プログラムを終了します...",
    },
    "한국어": {
        "channel_placeholder": "채널명",
        "quality_auto": "자동",
        "quality_best": "최고",
        "folder_placeholder": "저장 폴더",
        "folder_select": "선택",
        "shutdown_title": "종료 옵션 (하나만 선택)",
        "shutdown_option": "PC 종료",
        "close_app_option": "앱 종료",
        "other_title": "기타 설정",
        "theme_label": "테마:",
        "theme_dark": "다크",
        "theme_light": "라이트",
        "theme_system": "시스템",
        "button_start": "시작",
        "button_stop": "중지",
        "button_history": "기록",
        "button_update": "업데이트",
        "status_ready": "준비",
        "status_waiting": "대기중",
        "status_online": "녹화중",
        "status_offline": "오프라인",
        "status_stopped": "중지됨",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "프로그램 시작",
        "log_button": "단일 버튼 시스템",
        "log_quality": "자동 화질 선택",
        "log_internet": "인터넷 끊김 대응",
        "log_instruction": "채널명 입력 후 시작 클릭",
        "error_channel": "채널명을 입력하세요",
        "error_folder": "저장 폴더를 선택하세요",
        "shutdown_active": "종료 시 PC 종료 활성화",
        "close_app_active": "종료 시 앱 종료 활성화",
        "shutdown_cancel": "PC 종료 취소",
        "close_app_cancel": "앱 종료 취소",
        "shutdown_warning": "30초 후 PC가 종료됩니다",
        "close_app_warning": "10초 후 앱이 종료됩니다",
        "shutdown_countdown": "종료까지 {}초",
        "close_app_countdown": "앱 종료까지 {}초",
        "cancel_shutdown": "중지 버튼으로 취소",
        "internet_lost": "인터넷 연결 끊김",
        "internet_back": "인터넷 연결 복구",
        "no_internet": "인터넷 없음",
        "stream_ended": "방송 종료: {}",
        "stream_started": "방송 시작! 녹화중...",
        "folder_created": "폴더 생성: {}",
        "file_info": "파일: {}",
        "file_size": "저장 크기: {}",
        "total_size": "총 크기: {}",
        "current_size": "현재 크기: {}",
        "recording_stopped": "녹화 중지",
        "final_size": "최종 크기: {}",
        "update_check": "업데이트 확인중...",
        "update_available": "새 버전 사용 가능: {}",
        "update_current": "최신 버전입니다",
        "update_error": "서버에 연결할 수 없습니다",
        "update_timeout": "시간 초과",
        "update_connection_error": "인터넷 연결 없음",
        "update_download": "다운로드 페이지 열림",
        "update_later": "업데이트 연기",
        "update_question": "다운로드 페이지를 여시겠습니까?",
        "update_title": "업데이트 사용 가능",
        "update_downloaded": "브라우저에서 다운로드 페이지가 열렸습니다",
        "update_complete": "완료",
        "error_streamlink": "Streamlink를 찾을 수 없습니다",
        "error_streamlink_title": "오류",
        "error_generic": "Streamlink 오류: {}",
        "exit_warning": "녹화 중입니다. 종료하시겠습니까?",
        "exit_title": "경고",
        "exit_message": "프로그램을 종료합니다...",
    },
    "中文": {
        "channel_placeholder": "频道名称",
        "quality_auto": "自动",
        "quality_best": "最佳",
        "folder_placeholder": "保存文件夹",
        "folder_select": "选择",
        "shutdown_title": "关闭选项 (只能选一个)",
        "shutdown_option": "关闭电脑",
        "close_app_option": "关闭应用",
        "other_title": "其他设置",
        "theme_label": "主题:",
        "theme_dark": "深色",
        "theme_light": "浅色",
        "theme_system": "系统",
        "button_start": "开始",
        "button_stop": "停止",
        "button_history": "历史",
        "button_update": "更新",
        "status_ready": "就绪",
        "status_waiting": "等待中",
        "status_online": "录制中",
        "status_offline": "离线",
        "status_stopped": "已停止",
        "timer": "⏱",
        "filesize": "💾",
        "log_start": "程序已启动",
        "log_button": "单按钮系统",
        "log_quality": "自动质量选择",
        "log_internet": "断网容忍",
        "log_instruction": "输入频道名称并点击开始",
        "error_channel": "请输入频道名称",
        "error_folder": "请选择保存文件夹",
        "shutdown_active": "结束后关机已激活",
        "close_app_active": "结束后关闭应用已激活",
        "shutdown_cancel": "关机已取消",
        "close_app_cancel": "关闭已取消",
        "shutdown_warning": "30秒后将关闭电脑!",
        "close_app_warning": "10秒后将关闭应用!",
        "shutdown_countdown": "关机倒计时 {} 秒...",
        "close_app_countdown": "关闭倒计时 {} 秒...",
        "cancel_shutdown": "按停止按钮取消!",
        "internet_lost": "网络连接丢失! 等待中...",
        "internet_back": "网络连接已恢复!",
        "no_internet": "无网络, 等待30秒...",
        "stream_ended": "直播结束! {} 已离线",
        "stream_started": "直播开始! 录制中...",
        "folder_created": "频道文件夹已创建: {}",
        "file_info": "文件: {}",
        "file_size": "已保存大小: {}",
        "total_size": "总大小: {}",
        "current_size": "当前大小: {}",
        "recording_stopped": "录制已停止",
        "final_size": "录制已停止 - 最终大小: {}",
        "update_check": "正在检查更新...",
        "update_available": "新版本可用: {}",
        "update_current": "您的应用已是最新!",
        "update_error": "无法连接到更新服务器",
        "update_timeout": "更新检查超时",
        "update_connection_error": "无网络连接",
        "update_download": "下载页面已打开",
        "update_later": "更新已推迟",
        "update_question": "现在打开下载页面?",
        "update_title": "更新可用",
        "update_downloaded": "下载页面已在浏览器中打开。",
        "update_complete": "完成",
        "error_streamlink": "未找到Streamlink! https://streamlink.github.io/",
        "error_streamlink_title": "错误",
        "error_generic": "Streamlink错误: {}",
        "exit_warning": "录制正在进行中! 确定要退出吗?",
        "exit_title": "警告",
        "exit_message": "正在关闭程序...",
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
    
    # Tema seçimini güncelle
    current_theme = theme_menu.get()
    theme_map = {
        "Koyu": _("theme_dark"), "Dark": _("theme_dark"), "Dunkel": _("theme_dark"),
        "Sombre": _("theme_dark"), "Oscuro": _("theme_dark"), "Scuro": _("theme_dark"),
        "Escuro": _("theme_dark"), "Тёмная": _("theme_dark"), "ダーク": _("theme_dark"),
        "다크": _("theme_dark"), "深色": _("theme_dark"),
        "Açık": _("theme_light"), "Light": _("theme_light"), "Hell": _("theme_light"),
        "Clair": _("theme_light"), "Claro": _("theme_light"), "Chiaro": _("theme_light"),
        "Светлая": _("theme_light"), "ライト": _("theme_light"), "라이트": _("theme_light"),
        "浅色": _("theme_light")
    }
    
    if current_theme in theme_map:
        theme_menu.set(theme_map[current_theme])
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
