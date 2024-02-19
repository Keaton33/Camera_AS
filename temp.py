import sys
from PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import QPainter, QPolygonF, QColor
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene
from UI import automation


class PolygonWidget(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def drawPolygon(self):
        # Define the points of the polygon as QPointF
        # points = QPolygonF([
        #     QPointF(50, 50),
        #     QPointF(200, 50),
        #     QPointF(200, 200),
        #     QPointF(100, 100),
        #     QPointF(50, 200)
        # ])
        points_list = [[-100, 50],[200, 50],[200, 200],[100, 100],[50, 200]]
        polygon = QPolygonF()

        # 将坐标列表转换为 QPointF 对象，并添加到 QPolygonF 中
        for i in points_list:
            point = QPoint(i[0] , i[1])
            polygon.append(point)

        # Set the color of the polygon
        color = QColor(255, 0, 0)
        self.addPolygon(polygon, color)


class AutoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = automation.Ui_Dialog()
        self.ui.setupUi(self)

        # Create a QGraphicsScene object and set its parent to the graphicsView
        self.scene = PolygonWidget()
        self.ui.graphicsView.setScene(self.scene)
        self.scene.drawPolygon()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auto = AutoWindow()
    auto.show()
    sys.exit(app.exec_())
