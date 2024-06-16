import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QCalendarWidget, QDialog, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QDate, Qt, QRect

class CalendarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)
        self.setLayout(layout)

class SystemTrayApp(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip(QDate.currentDate().toString("yyyy MMMM dd"))

        # Create context menu
        self.menu = QMenu(parent)
        self.exit_action = QAction("Exit/Quit", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)

        # Connect the activation signal to the slot
        self.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            self.show_calendar()

    def show_calendar(self):
        self.calendar_dialog = CalendarDialog()
        self.calendar_dialog.exec_()

def create_tray_icon_with_date():
    # Load base icon
    base_icon = QPixmap("icon.png")

    # Create QPainter to draw text
    painter = QPainter(base_icon)
    painter.setFont(QFont("Arial", 18, QFont.Bold))
    painter.setPen(QColor("black"))

    # Draw month and day text on the icon
    current_date = QDate.currentDate()
    month = current_date.toString("MMMM").upper()
    day = current_date.toString("dd")

    # Calculate positions for text
    # These positions are based on the design of the original image
    # Adjust the positions according to your image specifics
    month_rect = QRect(0, 20, base_icon.width(), 50)  # adjust as needed
    day_rect = QRect(0, base_icon.height() // 2, base_icon.width(), 100)  # adjust as needed

    painter.drawText(month_rect, Qt.AlignHCenter, month)
    painter.drawText(day_rect, Qt.AlignHCenter, day)

    painter.end()

    return QIcon(base_icon)

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create the icon with date text
    icon = create_tray_icon_with_date()

    tray = SystemTrayApp(icon)
    tray.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
