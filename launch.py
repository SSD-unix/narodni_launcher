import sys
import os
import subprocess
import requests
import re
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

RES_PATH = os.path.join(os.path.dirname(__file__), "res")
PANORAMA_PATH = os.path.join(RES_PATH, "lenta.png")
LOGO_PATH = os.path.join(RES_PATH, "logo.png")
START_BTN_PATH = os.path.join(RES_PATH, "start.png")

REMOTE_LIST_URL = "https://ssdunix.xyz/mcservers.html"
AUTHORS_URL = "https://ssdunix.xyz/mcautors.html"

JAVA_PATH = "java"
NATIVE_PATH = "libs/natives"
LIBS_PATH = "libs/*"

VERSIONS_GIST_RAW = "https://raw.githubusercontent.com/SSD-unix/SSDunix.xyz/refs/heads/main/download/minecraft-server-jar-downloads.md.txt"
DOWNLOAD_FOLDER = "versions"

CONFIG_FILE = "config.json"  # файл для сохранения ника и версии

class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setFixedSize(1200, 720)
        self.authors_open = False

        if not os.path.exists(PANORAMA_PATH):
            raise SystemExit(f"Не найден файл: {PANORAMA_PATH}")
        self.panorama = QPixmap(PANORAMA_PATH)
        self.offset = 0
        self.speed = 2
        self.fps = 30
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(int(1000 / self.fps))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Логотип
        if os.path.exists(LOGO_PATH):
            logo_lbl = QLabel()
            logo_pm = QPixmap(LOGO_PATH).scaledToWidth(
                400, Qt.TransformationMode.SmoothTransformation
            )
            logo_lbl.setPixmap(logo_pm)
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            main_layout.addWidget(logo_lbl)

        # WebView
        self.webview = QWebEngineView()
        self.webview.setStyleSheet("background: transparent;")
        try:
            self.webview.page().setBackgroundColor(Qt.GlobalColor.transparent)
        except Exception:
            pass
        self.webview.setUrl(QUrl(REMOTE_LIST_URL))
        main_layout.addWidget(self.webview, stretch=1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        # Ник
        self.nick_input = QLineEdit()
        self.nick_input.setPlaceholderText("Nickname")
        self.nick_input.setFixedWidth(240)
        self.nick_input.setStyleSheet(
            "padding:6px; background:#2b2b2b; color:white; border-radius:8px;"
        )
        bottom_layout.addWidget(self.nick_input)

        # Выпадающий список версий
        self.version_combo = QComboBox()
        bottom_layout.addWidget(self.version_combo)

        # Кнопка Authors
        self.authors_btn = QPushButton("Authors")
        self.authors_btn.clicked.connect(self.toggle_authors)
        bottom_layout.addWidget(self.authors_btn)

        # Кнопка запуска
        self.start_btn = QPushButton()
        if os.path.exists(START_BTN_PATH):
            pm = QPixmap(START_BTN_PATH)
            target_width = 180
            target_height = int(pm.height() * (target_width / pm.width()))
            pm_scaled = pm.scaled(
                target_width, target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.start_btn.setFixedSize(pm_scaled.size())
            self.start_btn.setIconSize(pm_scaled.size())
            self.start_btn.setIcon(QIcon(pm_scaled))
        else:
            self.start_btn.setText("Start Game")
        self.start_btn.clicked.connect(self.start_game)
        bottom_layout.addWidget(self.start_btn)
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        # Загружаем словарь версий
        self.versions_dict = self.load_versions()
        old_versions = [v for v in self.versions_dict if not v.startswith("1.")]
        self.version_combo.addItems(sorted(old_versions))

        # Загружаем сохранённые настройки
        self.load_config()

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        pano_h = self.panorama.height()
        pano_w = self.panorama.width()
        scale = h / pano_h
        scaled_w = int(pano_w * scale)
        scaled_h = h
        scaled = self.panorama.scaled(
            scaled_w, scaled_h,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        ox = self.offset % scaled.width()
        if ox + w > scaled.width():
            part1_w = scaled.width() - ox
            part1 = scaled.copy(ox, 0, part1_w, scaled_h)
            painter.drawPixmap(0, 0, part1)
            part2 = scaled.copy(0, 0, w - part1_w, scaled_h)
            painter.drawPixmap(part1_w, 0, part2)
        else:
            part = scaled.copy(ox, 0, w, scaled_h)
            painter.drawPixmap(0, 0, part)
        self.offset += self.speed
        if self.offset >= scaled.width():
            self.offset = 0
        painter.end()

    def toggle_authors(self):
        if not self.authors_open:
            self.webview.setUrl(QUrl(AUTHORS_URL))
            self.authors_open = True
        else:
            self.webview.setUrl(QUrl(REMOTE_LIST_URL))
            self.authors_open = False

    def load_versions(self):
        try:
            r = requests.get(VERSIONS_GIST_RAW)
            r.raise_for_status()
            md_text = r.text
            pattern = re.compile(r"^\| ?([^|]+) ?\| ?([^|]+) ?\| ?([^|]+) ?\|", re.MULTILINE)
            matches = pattern.findall(md_text)
            versions = {}
            for version, server_url, client_url in matches:
                version = version.strip()
                client_url = client_url.strip()
                if client_url == "" or client_url.lower() == "client.jar":
                    continue
                versions[version] = client_url
            return versions
        except Exception as e:
            print("Ошибка при загрузке версий:", e)
            return {}

    def download_version(self, version_name):
        if version_name not in self.versions_dict:
            print(f"Версия {version_name} не найдена")
            return None
        url = self.versions_dict[version_name]
        path = os.path.join(DOWNLOAD_FOLDER, version_name)
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{version_name}.jar")
        if os.path.exists(file_path):
            print(f"{version_name} уже скачана")
            return file_path
        print(f"Скачиваю {version_name}...")
        resp = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(resp.content)
        print(f"{version_name} готово!")
        return file_path

    def start_game(self):
        nick = self.nick_input.text().strip() or "bez_nika"
        version_name = self.version_combo.currentText()
        self.save_config(nick, version_name)  # сохраняем состояние
        jar_path = self.download_version(version_name)
        if not jar_path:
            return
        cmd = f'java -Dhttp.proxyHost=betacraft.uk -Dhttp.proxyPort=11702 "-Djava.library.path=libs\\natives" -cp "{jar_path};libs/*" net.minecraft.client.Minecraft {nick} 0'
        try:
            subprocess.Popen(cmd, shell=True)
            print(f"Minecraft {version_name} started with nick: {nick}")
        except Exception as e:
            print("Error:", e)

    def save_config(self, nick, version_name):
        data = {"nick": nick, "version": version_name}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                nick = data.get("nick", "")
                version_name = data.get("version", "")
                self.nick_input.setText(nick)
                if version_name in [self.version_combo.itemText(i) for i in range(self.version_combo.count())]:
                    self.version_combo.setCurrentText(version_name)
            except Exception as e:
                print("Ошибка при загрузке config:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())
