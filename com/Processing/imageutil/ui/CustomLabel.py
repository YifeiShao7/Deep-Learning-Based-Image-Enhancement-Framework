from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets


class ImageLabel(QLabel):
    """"
    Label to show the images
    """

    # x0 = 0
    # y0 = 0
    # x1 = 0
    # y1 = 0
    # flag = False
    def __init__(self, parent=None):
        # super(ImageLabel, self).__init__(parent)
        super().__init__(parent)

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False  # 标记是否能够绘制矩形
        self.__isClear = False  # 标记是否是清除矩形
        self.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.setFrameShape(QtWidgets.QFrame.Box)  # 设置边框
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(218, 218, 218)")
        self.setText("")

        self.__w, self.__h = 0, 0
        self.pixmap_width, self.pixmap_height = 0, 0  # width & height of the pixmap
        self.pixmap_x_start, self.pixmap_y_start = 0, 0  # start point of the pixmap
        self.pixmap_x_end, self.pixmap_y_end = 0, 0  # end point of the image

        self.img_x_start, self.img_y_start = 0, 0  # start point of the image
        self.img_x_end, self.img_y_end = 0, 0  # end point of the image
        self.autoFillBackground()

    def clearRect(self):
        # clear
        self.__isClear = True
        self.update()
