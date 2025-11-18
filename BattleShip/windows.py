# windows.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from styles import *


class StatsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Статистика игр")
        self.setFixedSize(400, 300)
        self.setStyleSheet(DIALOG_STYLE)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("📊 Статистика игр")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(STATS_TITLE_STYLE)
        layout.addWidget(title)

        # Статистика
        if self.parent:
            wins, losses = self.parent.get_stats()
            total_games = wins + losses
            win_rate = (wins / total_games * 100) if total_games > 0 else 0

            stats_text = STATS_TEXT_TEMPLATE.format(
                total_games=total_games,
                wins=wins,
                losses=losses,
                win_rate=win_rate
            )
        else:
            stats_text = "<div>Не удалось загрузить статистику</div>"

        stats_label = QLabel(stats_text)
        stats_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stats_label.setStyleSheet(STATS_TEXT_STYLE)
        layout.addWidget(stats_label)

        # Кнопки
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("Очистить статистику")
        clear_btn.setStyleSheet(CONTROL_BUTTON_STYLE)
        clear_btn.clicked.connect(self.clear_stats)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet(CONTROL_BUTTON_STYLE)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def clear_stats(self):
        reply = QMessageBox.question(self, "Очистка статистики",
                                     "Вы уверены, что хотите очистить всю статистику?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Здесь будет код очистки статистики
            QMessageBox.information(self, "Статистика", "Статистика очищена!")
            self.close()


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(350, 400)
        self.setStyleSheet(DIALOG_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Логотип
        try:
            logo_label = QLabel()
            logo_pixmap = QPixmap("assets/Logo.png")
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaled(150, 75, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(logo_pixmap)
            else:
                logo_label = QLabel("🌊 МОРСКОЙ БОЙ 🌊")
                logo_label.setStyleSheet(ABOUT_TITLE_STYLE)
        except:
            logo_label = QLabel("🌊 МОРСКОЙ БОЙ 🌊")
            logo_label.setStyleSheet(ABOUT_TITLE_STYLE)

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Информация о программе
        info_label = QLabel(ABOUT_TEXT)
        info_label.setStyleSheet(ABOUT_INFO_STYLE)
        layout.addWidget(info_label)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet(CONTROL_BUTTON_STYLE)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(300, 250)
        self.setStyleSheet(DIALOG_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("⚙️ Настройки")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(SETTINGS_TITLE_STYLE)
        layout.addWidget(title)

        # Настройки
        settings_label = QLabel(SETTINGS_TEXT)
        settings_label.setStyleSheet(SETTINGS_TEXT_STYLE)
        layout.addWidget(settings_label)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet(CONTROL_BUTTON_STYLE)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)
