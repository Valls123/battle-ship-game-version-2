import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from enum import Enum
import random
import sqlite3
from datetime import datetime
from styles import *
from windows import StatsWindow, AboutWindow, SettingsWindow

DB_NAME = "battleship.db"


class GameState(Enum):
    PLACEMENT = 1
    PLAYING = 2
    GAME_OVER = 3


class BattleShipGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Морской Бой")
        self.setGeometry(300, 300, 900, 600)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        # ===== Настройки кораблей =====
        self.ship_types = {4: 1, 3: 2, 2: 3, 1: 4}
        self.current_ship_length = 4
        self.current_ship_count = 0
        self.current_orientation = "H"

        self.ai_targets = []
        self.current_target_hits = []
        self.hunting_mode = False
        self.player_turn = True

        self.game_state = GameState.PLACEMENT

        # Таймер для анимации огоньков
        self.fire_animation_timer = QTimer()
        self.fire_animation_timer.timeout.connect(self.animate_fires)
        self.fire_animation_state = 0
        self.sunken_ships_player = []
        self.sunken_ships_ai = []

        # ===== Создание UI =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # === ВЕРХНЯЯ ЧАСТЬ С ЛОГОТИПОМ В ПРАВОМ УГЛУ ===
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Левая часть - растягивающееся пространство
        top_layout.addStretch()

        # Правая часть - логотип
        try:
            logo_label = QLabel()
            logo_pixmap = QPixmap("assets/Logo.png")
            if not logo_pixmap.isNull():
                logo_pixmap = logo_pixmap.scaled(
                    120, 60,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_label.setPixmap(logo_pixmap)
            else:
                logo_label = QLabel("⚓")
                logo_label.setStyleSheet("font-size: 24px;")
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            logo_label = QLabel("⚓")
            logo_label.setStyleSheet("font-size: 24px;")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        logo_label.setStyleSheet(LOGO_CORNER_STYLE)
        top_layout.addWidget(logo_label)

        self.layout.addWidget(top_widget)

        # Заголовок и подзаголовок
        title = QLabel("МОРСКОЙ БОЙ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(TITLE_STYLE)
        self.layout.addWidget(title)

        subtitle = QLabel("Тут командуешь ты!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(SUBTITLE_STYLE)
        self.layout.addWidget(subtitle)

        self.set_fields()

        # Кнопки управления
        self.restart_button = QPushButton("Начать заново")
        self.restart_button.setFixedSize(200, 40)
        self.restart_button.setStyleSheet(CONTROL_BUTTON_STYLE)

        self.orientation_btn = QPushButton("Повернуть корабль")
        self.orientation_btn.setFixedSize(200, 40)
        self.orientation_btn.setStyleSheet(CONTROL_BUTTON_STYLE)

        self.stats_button = QPushButton("Статистика")
        self.stats_button.setFixedSize(200, 40)
        self.stats_button.setStyleSheet(STATS_BUTTON_STYLE)

        self.about_button = QPushButton("О программе")
        self.about_button.setFixedSize(200, 40)
        self.about_button.setStyleSheet(CONTROL_BUTTON_STYLE)

        self.settings_button = QPushButton("Настройки")
        self.settings_button.setFixedSize(200, 40)
        self.settings_button.setStyleSheet(CONTROL_BUTTON_STYLE)

        # Контейнер для кнопок
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.orientation_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.settings_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.stats_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.about_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.restart_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        # Автор
        autor = QLabel("Created by Shpakov Kirill")
        autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_autor = QFont("Arial", 10)
        font_autor.setItalic(True)
        autor.setFont(font_autor)
        autor.setStyleSheet(AUTHOR_STYLE)
        self.layout.addWidget(autor)

        # Подключаем сигналы
        self.restart_button.clicked.connect(self.restart_game)
        self.orientation_btn.clicked.connect(self.rotate_ship)
        self.stats_button.clicked.connect(self.show_stats)
        self.about_button.clicked.connect(self.show_about)
        self.settings_button.clicked.connect(self.show_settings)

        self.statusBar().showMessage("Сейчас расставляем корабли")

        # Инициализация
        self.init_db()
        self.setup_ai_ships()
        self.fire_animation_timer.start(500)

    # ===== Функции БД =====

    def init_db(self):
        """Инициализация базы данных."""
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outcome TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_result(self, outcome: str):
        """Добавление результата игры в БД."""
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO results (outcome, date) VALUES (?, ?)",
            (outcome, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()

    def get_stats(self):
        """Получение статистики из БД."""
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM results WHERE outcome = 'win'")
        wins = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM results WHERE outcome = 'lose'")
        losses = cur.fetchone()[0]
        conn.close()
        return wins, losses

    # ===== Функции игры =====

    def animate_fires(self):
        """Анимация огня на потопленных кораблях."""
        self.fire_animation_state = (self.fire_animation_state + 1) % 3
        current_style = FIRE_ANIMATION_STYLES[self.fire_animation_state]

        for ship_cells in self.sunken_ships_player + self.sunken_ships_ai:
            for btn in ship_cells:
                btn.setStyleSheet(current_style)

    def mark_ship_as_sunken(self, ship_cells, is_player_ship=False):
        """Пометить корабль как потопленный."""
        if is_player_ship:
            self.sunken_ships_player.append(ship_cells)
        else:
            self.sunken_ships_ai.append(ship_cells)

        for btn in ship_cells:
            btn.setStyleSheet(FIRE_ANIMATION_STYLES[0])

    def mark_around_ship_as_checked(self, ship_cells):
        """Пометить клетки вокруг корабля как проверенные."""
        checked_cells = set()

        for cell in ship_cells:
            row, col = self.get_button_coords(cell, is_enemy=False)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 10 and 0 <= nc < 10:
                        btn = self.player_buttons[nr][nc]
                        if not getattr(btn, "shot", False):
                            btn.shot = True
                            btn.setStyleSheet(MISS_BUTTON_STYLE)
                            checked_cells.add((nr, nc))

        self.ai_targets = [
            pos for pos in self.ai_targets if pos not in checked_cells
        ]
        return checked_cells

    def rotate_ship(self):
        """Поворот ориентации корабля."""
        if self.current_orientation == "H":
            self.current_orientation = "V"
            self.statusBar().showMessage("Текущая ориентация: вертикально")
        else:
            self.current_orientation = "H"
            self.statusBar().showMessage("Текущая ориентация: горизонтально")

    def restart_game(self):
        """Перезапуск игры."""
        self.fire_animation_timer.stop()

        for row in self.player_buttons + self.enemy_buttons:
            for btn in row:
                btn.setText("")
                btn.setProperty("has_ship", False)
                btn.setStyleSheet(BUTTON_STYLE)
                if hasattr(btn, "shot"):
                    delattr(btn, "shot")

        self.game_state = GameState.PLACEMENT
        self.current_ship_length = 4
        self.current_ship_count = 0
        self.ai_targets.clear()
        self.current_target_hits.clear()
        self.hunting_mode = False
        self.player_turn = True
        self.sunken_ships_player.clear()
        self.sunken_ships_ai.clear()
        self.fire_animation_state = 0

        self.setup_ai_ships()
        self.fire_animation_timer.start(500)
        self.statusBar().showMessage("Сейчас расставляем корабли")

    def create_field(self, title_text: str, is_enemy=False):
        """Создание игрового поля."""
        group_box = QGroupBox(title_text)
        vbox = QVBoxLayout(group_box)
        group_box.setStyleSheet(FIELD_GROUP_STYLE)

        grid = QGridLayout()
        grid.setSpacing(1)

        # Заголовки столбцов
        for col, bukva in enumerate("АБВГДЕЖЗИК", start=1):
            label = QLabel(bukva)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(GRID_LABEL_STYLE)
            grid.addWidget(label, 0, col)

        buttons = []
        for row in range(1, 11):
            # Заголовки строк
            num_label = QLabel(str(row))
            num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_label.setStyleSheet(GRID_LABEL_STYLE)
            grid.addWidget(num_label, row, 0)

            row_buttons = []
            for col in range(1, 11):
                btn = QPushButton()
                btn.setFixedSize(35, 35)
                btn.setProperty("has_ship", False)
                btn.clicked.connect(
                    lambda checked, b=btn: self.cell_clicked(b, is_enemy)
                )
                btn.setStyleSheet(BUTTON_STYLE)
                grid.addWidget(btn, row, col)
                row_buttons.append(btn)
            buttons.append(row_buttons)

        vbox.addLayout(grid)
        grid.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        return group_box, buttons

    def set_fields(self):
        """Установка игровых полей."""
        layout = QHBoxLayout()
        self.player_field, self.player_buttons = self.create_field(
            "Твоё поле", is_enemy=False
        )
        self.enemy_field, self.enemy_buttons = self.create_field(
            "Поле соперника", is_enemy=True
        )
        layout.addWidget(self.player_field)
        layout.addSpacing(50)
        layout.addWidget(self.enemy_field)
        self.layout.addLayout(layout)

    def set_ship_on_button(self, btn):
        """Установка корабля на кнопку."""
        btn.setProperty("has_ship", True)
        btn.setStyleSheet(SHIP_BUTTON_STYLE)

    def btn_has_ship(self, btn):
        """Проверка наличия корабля на кнопке."""
        return btn.property("has_ship")

    def get_button_coords(self, btn, is_enemy):
        """Получение координат кнопки."""
        field_buttons = self.enemy_buttons if is_enemy else self.player_buttons
        for r in range(10):
            for c in range(10):
                if field_buttons[r][c] == btn:
                    return r, c
        return -1, -1

    def can_place_ship(self, row, col, length, orientation, field_buttons):
        """Проверка возможности размещения корабля."""
        for i in range(length):
            r = row + i if orientation == "V" else row
            c = col + i if orientation == "H" else col
            if r >= 10 or c >= 10:
                return False

            if field_buttons[r][c].property("has_ship"):
                return False

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10:
                        if field_buttons[nr][nc].property("has_ship"):
                            return False
        return True

    def place_ship_player(self, row, col):
        """Размещение корабля игроком."""
        length = self.current_ship_length
        if not self.can_place_ship(
                row, col, length, self.current_orientation, self.player_buttons
        ):
            self.statusBar().showMessage("Нельзя поставить корабль здесь!")
            return False

        for i in range(length):
            r = row + i if self.current_orientation == "V" else row
            c = col + i if self.current_orientation == "H" else col
            self.set_ship_on_button(self.player_buttons[r][c])

        self.current_ship_count += 1

        if self.current_ship_count >= self.ship_types[self.current_ship_length]:
            if self.current_ship_length == 4:
                self.current_ship_length = 3
            elif self.current_ship_length == 3:
                self.current_ship_length = 2
            elif self.current_ship_length == 2:
                self.current_ship_length = 1
            else:
                self.game_state = GameState.PLAYING
                self.statusBar().showMessage(
                    "Все корабли расставлены! Ходите на поле соперника."
                )
                return True

            self.current_ship_count = 0
            self.statusBar().showMessage(
                f"Ставьте {self.current_ship_length}-палубный корабль"
            )
        else:
            remaining = (
                    self.ship_types[self.current_ship_length] - self.current_ship_count
            )
            self.statusBar().showMessage(
                f"{self.current_ship_length}-палубный корабль поставлен! "
                f"Осталось: {remaining}"
            )

        return True

    def cell_clicked(self, btn, is_enemy=False):
        """Обработка клика по клетке."""
        row, col = self.get_button_coords(btn, is_enemy)
        if row == -1 or col == -1:
            return

        if self.game_state == GameState.PLACEMENT and not is_enemy:
            self.place_ship_player(row, col)
            return

        if not self.player_turn or self.game_state != GameState.PLAYING:
            return

        if not is_enemy:
            self.statusBar().showMessage("Стрельба по своему полю невозможна!")
            return

        if getattr(btn, "shot", False):
            self.statusBar().showMessage("Вы уже стреляли сюда!")
            return

        btn.shot = True
        hit = self.btn_has_ship(btn)

        if hit:
            btn.setText("✕")
            btn.setStyleSheet(HIT_BUTTON_STYLE)
            self.statusBar().showMessage("Попадание! Ходите ещё раз!")

            ship_cells = self.get_ship_cells(row, col, is_enemy=True)
            if ship_cells and all(
                    getattr(cell, "shot", False) for cell in ship_cells
            ):
                self.mark_ship_as_sunken(ship_cells, is_player_ship=False)
                self.statusBar().showMessage(
                    "Корабль противника потоплен! 🔥 Ходите ещё раз!"
                )

            self.player_turn = True
        else:
            btn.setText("•")
            btn.setStyleSheet(MISS_BUTTON_STYLE)
            self.statusBar().showMessage("Промах! Ход переходит к ИИ")
            self.player_turn = False
            QTimer.singleShot(800, self.ai_move)

        self.check_game_over()

    def get_ship_cells(self, row, col, is_enemy=False):
        """Получение всех клеток корабля."""
        field_buttons = self.enemy_buttons if is_enemy else self.player_buttons

        if not field_buttons[row][col].property("has_ship"):
            return None

        ship_cells = []

        # Проверяем горизонтальное расположение
        r, c = row, col
        while c >= 0 and field_buttons[r][c].property("has_ship"):
            ship_cells.append(field_buttons[r][c])
            c -= 1

        c = col + 1
        while c < 10 and field_buttons[r][c].property("has_ship"):
            ship_cells.append(field_buttons[r][c])
            c += 1

        if len(ship_cells) > 1:
            return ship_cells

        # Проверяем вертикальное расположение
        ship_cells = []
        r, c = row, col
        while r >= 0 and field_buttons[r][c].property("has_ship"):
            ship_cells.append(field_buttons[r][c])
            r -= 1

        r = row + 1
        while r < 10 and field_buttons[r][c].property("has_ship"):
            ship_cells.append(field_buttons[r][c])
            r += 1

        return ship_cells

    def place_ship_ai(self, length):
        """Размещение корабля ИИ."""
        attempts = 0
        while attempts < 100:
            attempts += 1
            orientation = random.choice(["H", "V"])
            if orientation == "H":
                row = random.randint(0, 9)
                col = random.randint(0, 10 - length)
            else:
                row = random.randint(0, 10 - length)
                col = random.randint(0, 9)

            can_place = True
            for i in range(length):
                r = row + i if orientation == "V" else row
                c = col + i if orientation == "H" else col

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 10 and 0 <= nc < 10:
                            if self.enemy_buttons[nr][nc].property("has_ship"):
                                can_place = False
                                break
                    if not can_place:
                        break
                if not can_place:
                    break

            if can_place:
                for i in range(length):
                    r = row + i if orientation == "V" else row
                    c = col + i if orientation == "H" else col
                    self.enemy_buttons[r][c].setProperty("has_ship", True)
                return True

        return False

    def setup_ai_ships(self):
        """Размещение всех кораблей ИИ."""
        for length, count in self.ship_types.items():
            for _ in range(count):
                self.place_ship_ai(length)

    def get_possible_directions(self, row, col):
        """Получение возможных направлений для стрельбы."""
        directions = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 10 and 0 <= nc < 10:
                btn = self.player_buttons[nr][nc]
                if not getattr(btn, "shot", False):
                    directions.append((nr, nc))
        return directions

    def get_ship_orientation(self):
        """Определение ориентации корабля."""
        if len(self.current_target_hits) < 2:
            return None

        sorted_hits = sorted(self.current_target_hits)
        first_hit = sorted_hits[0]
        second_hit = sorted_hits[1]

        if first_hit[0] == second_hit[0]:
            return "H"
        elif first_hit[1] == second_hit[1]:
            return "V"
        return None

    def get_targets_along_orientation(self, orientation):
        """Получение целей вдоль ориентации корабля."""
        targets = []

        if orientation == "H":
            min_col = min(hit[1] for hit in self.current_target_hits)
            max_col = max(hit[1] for hit in self.current_target_hits)
            row = self.current_target_hits[0][0]

            left_col = min_col - 1
            if (left_col >= 0 and not getattr(
                    self.player_buttons[row][left_col], "shot", False
            )):
                targets.append((row, left_col))

            right_col = max_col + 1
            if (right_col < 10 and not getattr(
                    self.player_buttons[row][right_col], "shot", False
            )):
                targets.append((row, right_col))

        elif orientation == "V":
            min_row = min(hit[0] for hit in self.current_target_hits)
            max_row = max(hit[0] for hit in self.current_target_hits)
            col = self.current_target_hits[0][1]

            top_row = min_row - 1
            if (top_row >= 0 and not getattr(
                    self.player_buttons[top_row][col], "shot", False
            )):
                targets.append((top_row, col))

            bottom_row = max_row + 1
            if (bottom_row < 10 and not getattr(
                    self.player_buttons[bottom_row][col], "shot", False
            )):
                targets.append((bottom_row, col))

        return targets

    def ai_move(self):
        """Ход искусственного интеллекта."""
        if self.player_turn or self.game_state != GameState.PLAYING:
            return

        if self.hunting_mode and self.ai_targets:
            row, col = self.ai_targets.pop(0)
        elif self.hunting_mode:
            orientation = self.get_ship_orientation()
            if orientation:
                self.ai_targets = self.get_targets_along_orientation(orientation)
                if self.ai_targets:
                    row, col = self.ai_targets.pop(0)
                else:
                    self.hunting_mode = False
                    row, col = self.get_random_cell()
            else:
                all_directions = []
                for hit in self.current_target_hits:
                    directions = self.get_possible_directions(hit[0], hit[1])
                    all_directions.extend(directions)

                self.ai_targets = list(set(all_directions))
                if self.ai_targets:
                    row, col = self.ai_targets.pop(0)
                else:
                    self.hunting_mode = False
                    row, col = self.get_random_cell()
        else:
            row, col = self.get_random_cell()

        btn = self.player_buttons[row][col]
        btn.shot = True

        if self.btn_has_ship(btn):
            btn.setText("✕")
            btn.setStyleSheet(HIT_BUTTON_STYLE)
            self.statusBar().showMessage("ИИ попал! Он ходит ещё раз!")

            self.current_target_hits.append((row, col))
            self.hunting_mode = True

            orientation = self.get_ship_orientation()
            if orientation:
                self.ai_targets = self.get_targets_along_orientation(orientation)
            else:
                new_directions = self.get_possible_directions(row, col)
                self.ai_targets.extend(new_directions)

            self.ai_targets = list(set(self.ai_targets))

            ship_cells = self.get_ship_cells(row, col, is_enemy=False)
            if ship_cells and all(
                    getattr(cell, "shot", False) for cell in ship_cells
            ):
                self.mark_ship_as_sunken(ship_cells, is_player_ship=True)
                self.mark_around_ship_as_checked(ship_cells)
                self.statusBar().showMessage(
                    "ИИ потопил ваш корабль! 🔥 Он ходит ещё раз!"
                )
                self.current_target_hits.clear()
                self.ai_targets.clear()
                self.hunting_mode = False

            self.player_turn = False
            QTimer.singleShot(800, self.ai_move)
        else:
            btn.setText("•")
            btn.setStyleSheet(MISS_BUTTON_STYLE)
            self.statusBar().showMessage("ИИ промахнулся! Ваш ход!")
            self.player_turn = True

        self.check_game_over()

    def get_random_cell(self):
        """Получение случайной клетки для выстрела."""
        possible_cells = [
            (r, c) for r in range(10) for c in range(10)
            if not getattr(self.player_buttons[r][c], "shot", False)
        ]
        return random.choice(possible_cells) if possible_cells else (0, 0)

    def show_stats(self):
        """Показать окно статистики."""
        stats_window = StatsWindow(self)
        stats_window.exec()

    def show_about(self):
        """Показать окно 'О программе'."""
        about_window = AboutWindow(self)
        about_window.exec()

    def show_settings(self):
        """Показать окно настроек."""
        settings_window = SettingsWindow(self)
        settings_window.exec()

    def check_game_over(self):
        """Проверка окончания игры."""
        player_ships_left = any(
            self.player_buttons[r][c].property("has_ship") and
            not getattr(self.player_buttons[r][c], "shot", False)
            for r in range(10) for c in range(10)
        )
        enemy_ships_left = any(
            self.enemy_buttons[r][c].property("has_ship") and
            not getattr(self.enemy_buttons[r][c], "shot", False)
            for r in range(10) for c in range(10)
        )

        if not player_ships_left:
            self.game_state = GameState.GAME_OVER
            self.add_result("lose")
            wins, losses = self.get_stats()
            QMessageBox.information(
                self, "Игра окончена",
                f"ИИ победил!\n\nСтатистика:\nПобед: {wins}\nПоражений: {losses}"
            )
        elif not enemy_ships_left:
            self.game_state = GameState.GAME_OVER
            self.add_result("win")
            wins, losses = self.get_stats()
            QMessageBox.information(
                self, "Игра окончена",
                f"Вы победили!\n\nСтатистика:\nПобед: {wins}\nПоражений: {losses}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BattleShipGame()
    window.show()
    sys.exit(app.exec())
