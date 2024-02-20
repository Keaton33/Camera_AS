from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFileDialog, QApplication, QDialog
from PyQt5.QtGui import QPolygonF, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF
from UI import automation
from UI.automation import Ui_Dialog


class CustomDialog(Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphics_scene = QGraphicsScene()
        self.graphicsView.setScene(self.graphics_scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)

        self.draw_button = self.pushButton
        self.draw_button.clicked.connect(self.draw_polygon)

    def draw_polygon(self):
        polygon = QPolygonF()
        polygon.append(QPointF(100.0, 100.0))
        polygon.append(QPointF(200.0, 100.0))
        polygon.append(QPointF(200.0, 200.0))
        polygon.append(QPointF(100.0, 200.0))

        brush = QBrush(Qt.green)
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        pen.setStyle(Qt.SolidLine)

        self.graphics_scene.addPolygon(polygon, pen, brush)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = CustomDialog()
    dialog.show()
    sys.exit(app.exec_())
