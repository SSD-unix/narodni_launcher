import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Пути к ресурсам
RES_PATH = os.path.join(os.path.dirname(__file__), "res")
PANORAMA_PATH = os.path.join(RES_PATH, "lenta.png")
LOGO_PATH = os.path.join(RES_PATH, "logo.png")
START_BTN_PATH = os.path.join(RES_PATH, "start.png")

REMOTE_LIST_URL = "https://ssdunix.xyz/mcservers.html"

# Пути для Java и Minecraft
JAVA_PATH = "java"  # если java в PATH
JAR_PATH = "a1.1.2_01.jar"
NATIVE_PATH = "libs/nativate"
LIBS_PATH = "libs/*"


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setFixedSize(1200, 720)

        # Панорама
        if not os.path.exists(PANORAMA_PATH):
            raise SystemExit(f"Не найден файл: {PANORAMA_PATH}")
        self.panorama = QPixmap(PANORAMA_PATH)
        self.offset = 0
        self.speed = 2
        self.fps = 30
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(int(1000 / self.fps))

        # Основной вертикальный layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Логотип сверху
        if os.path.exists(LOGO_PATH):
            logo_lbl = QLabel()
            logo_pm = QPixmap(LOGO_PATH).scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(logo_pm)
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            main_layout.addWidget(logo_lbl)

        # WebView по центру
        self.webview = QWebEngineView()
        self.webview.setStyleSheet("background: transparent;")
        try:
            self.webview.page().setBackgroundColor(Qt.GlobalColor.transparent)
        except Exception:
            pass
        self.webview.setUrl(QUrl(REMOTE_LIST_URL))
        main_layout.addWidget(self.webview, stretch=1)

        # Кнопки снизу
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        # Nickname
        self.nick_input = QLineEdit()
        self.nick_input.setPlaceholderText("Nickname")
        self.nick_input.setFixedWidth(240)
        self.nick_input.setStyleSheet("padding:6px; background:#2b2b2b; color:white; border-radius:8px;")
        bottom_layout.addWidget(self.nick_input)

        # Start Game кнопка с картинкой
        self.start_btn = QPushButton()
        if os.path.exists(START_BTN_PATH):
            pm = QPixmap(START_BTN_PATH)
            target_width = 180
            target_height = int(pm.height() * (target_width / pm.width()))
            pm_scaled = pm.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.start_btn.setFixedSize(pm_scaled.size())
            self.start_btn.setIconSize(pm_scaled.size())
            self.start_btn.setIcon(QIcon(pm_scaled))
        else:
            self.start_btn.setText("Start Game")
            self.start_btn.setStyleSheet(
                "background-color:#00aa55; color:white; padding:8px 14px; border-radius:8px; font-weight:600;"
            )
        self.start_btn.clicked.connect(self.start_game)
        bottom_layout.addWidget(self.start_btn)
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)

    def paintEvent(self, event):
        # Рисуем прокручивающуюся панораму
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

    def start_game(self):
        nick = self.nick_input.text().strip() or "Player"
        print(f"[LAUNCH] Starting Minecraft with nick: {nick}")

        cmd = [
            JAVA_PATH,
            f"-Djava.library.path={NATIVE_PATH}",
            "-cp", f"{JAR_PATH}:{LIBS_PATH}",
            "net.minecraft.client.Minecraft",
            nick,
            "0"
        ]
        try:
            subprocess.Popen(cmd)
            print("[LAUNCH] Minecraft process started.")
        except Exception as e:
            print("[ERROR] Failed to start Minecraft:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())
