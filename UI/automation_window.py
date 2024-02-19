import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPolygon, QColor
from PyQt5.QtWidgets import QApplication, QDialog
from UI import automation


class AutoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = automation.Ui_Dialog()
        self.ui.setupUi(self)
        # self.ui.graphicsView.paintEvent()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the points of the polygon as tuples
        points = QPolygon([
            QPoint(50, 50),
            QPoint(200, 50),
            QPoint(200, 200),
            QPoint(100, 100),
            QPoint(50, 200)
        ])

        # Set the color of the polygon
        color = QColor(255, 0, 0)
        painter.setBrush(color)

        # Draw the polygon
        painter.drawPolygon(points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auto = AutoWindow()
    auto.show()
    sys.exit(app.exec_())
