import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                           QVBoxLayout, QWidget, QComboBox, 
                           QCalendarWidget, QHBoxLayout, QPushButton,
                           QTreeWidget, QTreeWidgetItem, QLineEdit,
                           QMenu)
from PyQt6.QtCore import QTimer, Qt, QDateTime, QDate
from PyQt6.QtGui import QFont, QPalette, QColor
import pytz
from collections import defaultdict
from datetime import datetime

class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)  # 移除左侧的周数
        self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)  # 使用单字母表示星期
        self.setNavigationBarVisible(True)
        self.setStyleSheet("""
            QCalendarWidget {
                background-color: #ffffff;
                color: #1c1e21;
                border: 1px solid #dddfe2;
                border-radius: 8px;
                padding: 10px;
            }
            /* 月份年份选择按钮 */
            QCalendarWidget QToolButton#qt_calendar_monthbutton,
            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                color: #1877f2;
                background-color: #ffffff;
                border: 1px solid #dddfe2;
                border-radius: 6px;
                padding: 8px 15px;
                min-width: 100px;
                min-height: 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton:hover,
            QCalendarWidget QToolButton#qt_calendar_yearbutton:hover {
                background-color: #f0f2f5;
            }
            /* 导航按钮样式 */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth,
            QCalendarWidget QToolButton#qt_calendar_prevyear,
            QCalendarWidget QToolButton#qt_calendar_nextyear {
                background-color: transparent;
                border: none;
                width: 24px;
                height: 24px;
                padding: 0px;
                margin: 0px;
                border-radius: 12px;
                transition: background-color 0.2s;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_prevyear:hover,
            QCalendarWidget QToolButton#qt_calendar_nextyear:hover {
                background-color: #e7f3ff;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth:pressed,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:pressed,
            QCalendarWidget QToolButton#qt_calendar_prevyear:pressed,
            QCalendarWidget QToolButton#qt_calendar_nextyear:pressed {
                background-color: #1877f2;
            }
            /* 自定义箭头样式 */
            QCalendarWidget QToolButton::menu-indicator {
                width: 16px;
                height: 16px;
                padding-top: 5px;
                padding-right: 5px;
            }
            QCalendarWidget QToolButton::menu-indicator:hover {
                background-color: #f0f2f5;
            }
            QCalendarWidget QSpinBox {
                min-width: 85px;
                max-width: 85px;
                font-size: 14px;
                padding: 4px;
            }
            /* 下拉菜单样式 */
            QCalendarWidget QMenu {
                background-color: #ffffff;
                color: #1c1e21;
                border: 1px solid #dddfe2;
                border-radius: 6px;
                padding: 5px;
                min-width: 150px;
            }
            QCalendarWidget QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                min-width: 100px;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #e7f3ff;
                color: #1877f2;
            }
            /* 日历表格样式 */
            QCalendarWidget QTableView {
                background-color: #ffffff;
                alternate-background-color: #f0f2f5;
                selection-background-color: #e7f3ff;
                selection-color: #1877f2;
                border: none;
                font-size: 14px;
                gridline-color: transparent;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #1c1e21;
                font-size: 14px;
                selection-background-color: #e7f3ff;
                selection-color: #1877f2;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #606770;
            }
            /* 滚动条样式 */
            QScrollBar:vertical {
                border: none;
                background: #f0f2f5;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #1877f2;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # 设置年份范围
        self.setDateRange(
            QDate(1900, 1, 1),
            QDate(2100, 12, 31)
        )
        
        # 设置当前日期
        self.setSelectedDate(QDate.currentDate())
        
    def showPopup(self):
        # 重写弹出菜单方法，限制年份显示数量
        menu = self.findChild(QMenu)
        if menu:
            current_year = self.selectedDate().year()
            actions = menu.actions()
            for action in actions:
                if action.text().isdigit():
                    year = int(action.text())
                    if abs(year - current_year) > 6:
                        action.setVisible(False)
                    else:
                        action.setVisible(True)

class TimezoneSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # 添加搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索时区...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #f0f2f5;
                border: 1px solid #dddfe2;
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 14px;
                color: #1c1e21;
            }
            QLineEdit:focus {
                border-color: #1877f2;
                background-color: #ffffff;
            }
        """)
        self.search_box.textChanged.connect(self.filter_timezones)
        layout.addWidget(self.search_box)
        
        # 创建时区树
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #ffffff;
                color: #1c1e21;
                border: 1px solid #dddfe2;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QTreeWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 6px;
            }
            QTreeWidget::item:selected {
                background-color: #e7f3ff;
                color: #1877f2;
            }
            QTreeWidget::item:hover {
                background-color: #f0f2f5;
            }
            QTreeWidget::branch {
                background-color: #ffffff;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzE4NzdmMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTAgMTdsMi01IDItNW0tMiA1bC0yLTUiIHN0cm9rZT0iIzE4NzdmMiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48L3N2Zz4=);
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzE4NzdmMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTkgOWwtNyA3LTctNyIgc3Ryb2tlPSIjMTg3N2YyIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg==);
            }
        """)
        
        # 组织时区数据
        self.timezone_dict = defaultdict(list)
        for tz in pytz.all_timezones:
            parts = tz.split('/')
            if len(parts) > 1:
                self.timezone_dict[parts[0]].append('/'.join(parts[1:]))
        
        # 填充树
        self.populate_tree()
        
        layout.addWidget(self.tree)
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)
        
        # 展开所有项
        self.tree.expandAll()
        
        # 当前选中的时区
        self.current_timezone = 'Asia/Shanghai'
        
        # 选中默认时区
        self.select_timezone(self.current_timezone)
    
    def populate_tree(self, filter_text=""):
        self.tree.clear()
        filter_text = filter_text.lower()
        
        for region, zones in sorted(self.timezone_dict.items()):
            matching_zones = []
            for zone in sorted(zones):
                full_zone = f"{region}/{zone}"
                if filter_text in full_zone.lower():
                    matching_zones.append(zone)
            
            if matching_zones:
                region_item = QTreeWidgetItem([region])
                self.tree.addTopLevelItem(region_item)
                for zone in matching_zones:
                    zone_item = QTreeWidgetItem([zone])
                    region_item.addChild(zone_item)
    
    def filter_timezones(self, text):
        self.populate_tree(text)
        if text:
            self.tree.expandAll()
        
    def select_timezone(self, timezone):
        parts = timezone.split('/')
        if len(parts) > 1:
            for i in range(self.tree.topLevelItemCount()):
                region_item = self.tree.topLevelItem(i)
                if region_item.text(0) == parts[0]:
                    for j in range(region_item.childCount()):
                        zone_item = region_item.child(j)
                        if zone_item.text(0) == '/'.join(parts[1:]):
                            self.tree.setCurrentItem(zone_item)
                            return
    
    def on_selection_changed(self):
        item = self.tree.currentItem()
        if item and item.parent():  # 确保选中的是子项（具体时区）
            self.current_timezone = f"{item.parent().text(0)}/{item.text(0)}"

class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数字时钟")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        
        # 初始化语言设置
        self.current_language = 'zh'  # 默认中文
        self.translations = {
            'zh': {
                'title': '数字时钟',
                'timezone_label': '时区选择',
                'calendar_label': '日历',
                'language_button': '切换到英文',
                'date_format': '%Y年%m月%d日 %A'
            },
            'en': {
                'title': 'Digital Clock',
                'timezone_label': 'Timezone',
                'calendar_label': 'Calendar',
                'language_button': 'Switch to Chinese',
                'date_format': '%Y-%m-%d %A'
            }
        }
        
        # 设置黑色背景
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('black'))
        palette.setColor(QPalette.ColorRole.WindowText, QColor('white'))
        self.setPalette(palette)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(30)
        
        layout.addStretch(2)
        
        # 时间显示
        self.time_label = QLabel()
        self.time_label.setFont(QFont('Arial', 200))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("color: white;")
        layout.addWidget(self.time_label)
        
        # 日期显示
        self.date_label = QLabel()
        self.date_label.setFont(QFont('Arial', 50))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("color: white;")
        layout.addWidget(self.date_label)
        
        layout.addStretch(3)
        
        # 控制面板
        self.control_panel = QWidget()
        control_layout = QHBoxLayout(self.control_panel)
        control_layout.setSpacing(40)
        control_layout.setContentsMargins(50, 20, 50, 20)
        
        # 时区选择
        timezone_container = QWidget()
        timezone_layout = QVBoxLayout(timezone_container)
        self.timezone_label = QLabel(self.translations[self.current_language]['timezone_label'])
        self.timezone_label.setStyleSheet("""
            QLabel {
                color: #1877f2;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        timezone_layout.addWidget(self.timezone_label)
        self.timezone_selector = TimezoneSelector()
        timezone_layout.addWidget(self.timezone_selector)
        control_layout.addWidget(timezone_container)
        
        # 日历
        calendar_container = QWidget()
        calendar_layout = QVBoxLayout(calendar_container)
        self.calendar_label = QLabel(self.translations[self.current_language]['calendar_label'])
        self.calendar_label.setStyleSheet("""
            QLabel {
                color: #1877f2;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        calendar_layout.addWidget(self.calendar_label)
        self.calendar = CustomCalendar()
        calendar_layout.addWidget(self.calendar)
        control_layout.addWidget(calendar_container)
        
        # 语言切换按钮
        self.language_button = QPushButton(self.translations[self.current_language]['language_button'])
        self.language_button.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QPushButton:pressed {
                background-color: #145fd2;
            }
        """)
        self.language_button.clicked.connect(self.toggle_language)
        control_layout.addWidget(self.language_button)
        
        self.control_panel.hide()
        layout.addWidget(self.control_panel)
        
        # 设置控制面板背景
        self.control_panel.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
            }
        """)
        
        # 设置定时器更新时间
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # 添加星期转换字典
        self.weekday_translations = {
            'zh': {
                'Monday': '星期一',
                'Tuesday': '星期二',
                'Wednesday': '星期三',
                'Thursday': '星期四',
                'Friday': '星期五',
                'Saturday': '星期六',
                'Sunday': '星期日'
            }
        }
        
        # 更新时间显示
        self.update_time()
    
    def toggle_language(self):
        # 切换语言
        self.current_language = 'en' if self.current_language == 'zh' else 'zh'
        
        # 更新界面文本
        self.setWindowTitle(self.translations[self.current_language]['title'])
        self.timezone_label.setText(self.translations[self.current_language]['timezone_label'])
        self.calendar_label.setText(self.translations[self.current_language]['calendar_label'])
        self.language_button.setText(self.translations[self.current_language]['language_button'])
        
        # 更新时间显示
        self.update_time()
    
    def format_date(self, current_date):
        if self.current_language == 'zh':
            # 获取英文星期
            weekday_en = current_date.strftime('%A')
            # 转换为中文星期
            weekday_zh = self.weekday_translations['zh'][weekday_en]
            # 格式化日期，不包含星期
            date_only = current_date.strftime('%Y年%m月%d日')
            return f"{date_only} {weekday_zh}"
        else:
            return current_date.strftime(self.translations['en']['date_format'])
    
    def update_time(self):
        tz = pytz.timezone(self.timezone_selector.current_timezone)
        current = datetime.now(tz)
        
        # 更新时间显示
        time_str = current.strftime("%H:%M:%S")
        self.time_label.setText(time_str)
        
        # 使用新的日期格式化方法
        self.date_label.setText(self.format_date(current))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.control_panel.setVisible(not self.control_panel.isVisible())
        event.accept()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        event.accept()

if __name__ == '__main__':
    def main():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        clock = Clock()
        clock.show()
        sys.exit(app.exec())
    
    main()
else:
    def main():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        clock = Clock()
        clock.show()
        sys.exit(app.exec()) 