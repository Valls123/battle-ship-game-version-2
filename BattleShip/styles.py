# styles.py

# Основные стили кнопок
BUTTON_STYLE = """
    QPushButton {
        background-color: #e8f4f8;
        border: 2px solid #b8d8e8;
        border-radius: 3px;
    }
    QPushButton:hover { 
        background-color: #d4edf7; 
        border: 2px solid #7ec8e3;
    }
    QPushButton:pressed { 
        background-color: #b8e2f4; 
    }
"""

# Стили для кнопок с кораблями
SHIP_BUTTON_STYLE = """
    QPushButton {
        background-color: #5d8aa8;
        border: 2px solid #3a6186;
        border-radius: 3px;
    }
    QPushButton:hover { 
        background-color: #4a7a9a; 
        border: 2px solid #2a4c6e;
    }
"""

# Стили для попаданий
HIT_BUTTON_STYLE = """
    QPushButton {
        background-color: #ff6b6b;
        border: 2px solid #ff5252;
        border-radius: 3px;
        color: #8b0000;
        font-size: 18px;
        font-weight: bold;
    }
"""

# Стили для промахов
MISS_BUTTON_STYLE = """
    QPushButton {
        background-color: #e8f4f8;
        border: 2px solid #b8d8e8;
        border-radius: 3px;
        color: #666666;
        font-size: 18px;
        font-weight: bold;
    }
"""

# Стили для анимации огня (3 состояния)
FIRE_ANIMATION_STYLES = [
    """
    QPushButton {
        background-color: #ff8c00;
        border: 2px solid #ff4500;
        border-radius: 3px;
        color: #8b0000;
        font-size: 18px;
        font-weight: bold;
    }
    """,
    """
    QPushButton {
        background-color: #ff4500;
        border: 2px solid #ff0000;
        border-radius: 3px;
        color: #8b0000;
        font-size: 18px;
        font-weight: bold;
    }
    """,
    """
    QPushButton {
        background-color: #ff6347;
        border: 2px solid #ff8c00;
        border-radius: 3px;
        color: #8b0000;
        font-size: 18px;
        font-weight: bold;
    }
    """
]

# Стили для управляющих кнопок
CONTROL_BUTTON_STYLE = """
    QPushButton {
        background-color: #0078d7;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px;
    }
    QPushButton:hover { 
        background-color: #005fa3; 
    }
"""

# Стиль для кнопки статистики
STATS_BUTTON_STYLE = """
    QPushButton {
        background-color: #28a745;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px;
    }
    QPushButton:hover { 
        background-color: #218838; 
    }
"""

# Стили для групповых рамок (полей)
FIELD_GROUP_STYLE = """
    QGroupBox { 
        border: 2px solid #003C8F; 
        border-radius: 8px; 
        margin-top: 10px; 
        font-weight: bold; 
        background-color: white;
    }
    QGroupBox::title { 
        subcontrol-origin: margin; 
        left: 10px; 
        padding: 0 5px; 
        color: #003C8F; 
    }
"""

# Стили для заголовков
TITLE_STYLE = "font-size: 24px; font-weight: bold; margin-bottom: 10px;"
SUBTITLE_STYLE = "font-size: 12px; font-style: italic; margin-bottom: 15px;"

# Стиль для автора
AUTHOR_STYLE = "color: gray; margin-top: 10px; margin-bottom: 5px;"

# Стиль для основного окна
MAIN_WINDOW_STYLE = "background-color: #C0C0C0;"

# Стили для заголовков столбцов и строк
GRID_LABEL_STYLE = "font-weight: bold; color: #003C8F;"

# Стили для логотипа
LOGO_IMAGE_STYLE = "margin: 10px;"
LOGO_CONTAINER_STYLE = "background-color: transparent;"

# Стили для логотипа в правом верхнем углу
LOGO_CORNER_STYLE = """
    QLabel {
        background-color: transparent;
        margin: 5px;
    }
"""

# styles.py

# ... существующие стили ...

# Стили для дополнительных окон

# Окно статистики
STATS_TITLE_STYLE = "font-size: 20px; font-weight: bold; color: #003C8F; margin: 10px;"
STATS_TEXT_STYLE = "background-color: white; border: 1px solid #CCC; border-radius: 8px; padding: 15px;"

# Окно "О программе"
ABOUT_TITLE_STYLE = "font-size: 18px; font-weight: bold;"
ABOUT_INFO_STYLE = "background-color: white; border-radius: 8px; padding: 15px; margin: 10px;"

# Окно настроек
SETTINGS_TITLE_STYLE = "font-size: 18px; font-weight: bold; margin: 10px;"
SETTINGS_TEXT_STYLE = "background-color: white; border-radius: 8px; padding: 15px;"

# Стиль для основного окна (фона) дополнительных окон
DIALOG_STYLE = "background-color: #F0F0F0;"

# Текстовое содержимое для окон
STATS_TEXT_TEMPLATE = """
<div style='font-size: 14px; line-height: 1.8;'>
<b>Общая статистика:</b><br>
• Всего игр: <b>{total_games}</b><br>
• Побед: <b style='color: green;'>{wins}</b><br>
• Поражений: <b style='color: red;'>{losses}</b><br>
• Процент побед: <b>{win_rate:.1f}%</b><br><br>

<b>Рекорды:</b><br>
• Самая длинная серия побед: <b>в разработке</b><br>
• Лучшее время игры: <b>в разработке</b>
</div>
"""

ABOUT_TEXT = """
<div style='text-align: center; line-height: 1.6;'>
<h3>Морской Бой</h3>
<p><b>Версия 1.0</b></p>

<p>Классическая игра "Морской бой" с 
ии и системой 
статистики.</p>

<p><b>Разработчик:</b><br>
Шпаков Кирилл</p>

<p><b>Особенности:</b><br>
• Умный ИИ противник<br>
• Система статистики<br>
• Анимации попаданий<br>
• База данных результатов</p>

<p style='color: #666; font-size: 12px;'>
© 2024 Все права защищены
</p>
</div>
"""

SETTINGS_TEXT = """
<div style='background-color: white; border-radius: 8px; padding: 15px;'>
<p><b>Настройки в разработке</b></p>
<p>В будущих версиях здесь можно будет:</p>
<ul>
<li>Изменять сложность ИИ</li>
<li>Настраивать цвета</li>
<li>Включать/выключать анимации</li>
<li>Изменять размер поля</li>
</ul>
</div>
"""
