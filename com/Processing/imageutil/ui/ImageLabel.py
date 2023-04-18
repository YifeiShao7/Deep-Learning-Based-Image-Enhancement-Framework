from PyQt5.QtCore import QRect, Qt, QPoint, QSize
from PyQt5.QtGui import QPainter, QPen, QPixmap, QPainterPath, QImage
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, QtGui, QtCore


class ImageLabel(QLabel):
    """"
    label to show the image
    """

    def __init__(self, parent=None):
        # super(ImageLabel, self).__init__(parent)
        super().__init__(parent)

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = 0  # 0: cannot draw, 1: draw the rectangle to crop, 2: draw the lines for the mask
        self.__isClear = False  # whether to clear the rectangle
        self.setAlignment(Qt.AlignCenter)  # align center
        self.setFrameShape(QtWidgets.QFrame.Box)  # set the border
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(218, 218, 218)")
        self.setText("")

        self.__w, self.__h = 0, 0
        self.pixmap_width, self.pixmap_height = 0, 0  # width, height of the pixmap
        self.pixmap_x_start, self.pixmap_y_start = 0, 0  # start point of the pixmap
        self.pixmap_x_end, self.pixmap_y_end = 0, 0  # end point of the pixmap

        self.img_x_start, self.img_y_start = 0, 0  # start point of the rectangle
        self.img_x_end, self.img_y_end = 0, 0  # end point of the rectangle
        self.autoFillBackground()

        self.pix = QPixmap()
        self.mask = QPixmap(self.size())
        self.mask.fill(Qt.white)

        self.painterPath = QPainterPath()

    # mouse press event
    def mousePressEvent(self, event):
        if self.flag == 1:
            # self.flag = True
            # press the mouse to start drawing
            self.__isClear = False
            self.x0 = event.x()
            self.y0 = event.y()

            # calculate the position of output pixmap
            self.__w, self.__h = self.width(), self.height()
            self.pixmap_x_start = (self.__w - self.pixmap_width) / 2
            self.pixmap_y_start = (self.__h - self.pixmap_height) / 2
            self.pixmap_x_end = self.pixmap_x_start + self.pixmap_width
            self.pixmap_y_end = self.pixmap_y_start + self.pixmap_height
        elif self.flag == 2:
            self.painterPath.moveTo(event.pos())
            self.update()

    # mouse release event
    def mouseReleaseEvent(self, event):
        if self.flag == 1:
            self.setCursor(Qt.ArrowCursor)  # release the mouse to finish the drawing
        elif self.flag == 2:
            self.painterPath.lineTo(event.pos())
            self.update()

    # mouse move event
    def mouseMoveEvent(self, event):
        if self.flag == 1:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
        elif self.flag == 2:
            self.painterPath.lineTo(event.pos())
            self.update()

    # override setPixmap method
    # update the width and height of the pixmap, and update the value on the mask image
    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.pixmap_width, self.pixmap_height = pixmap.width(), pixmap.height()
        self.pix = pixmap
        self.mask = self.mask.scaled(QSize(self.pixmap_width, self.pixmap_height))

    # paint event, called on each update
    # if flag == 1, to draw a rectangle for crop
    # if flag == 2, to draw lines to get the mask for inpaint
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag == 1:
            # determining whether to clear
            if self.__isClear:
                return

            # user can only start to draw the rect in the image
            if (self.pixmap_x_start <= self.x0 <= self.pixmap_x_end) \
                    and (self.pixmap_y_start <= self.y0 <= self.pixmap_y_end):
                # if the mouse released at the point out of the image, set the end point at the border of the image
                if self.x1 > self.pixmap_x_end:
                    self.x1 = self.pixmap_x_end
                elif self.x1 < self.pixmap_x_start:
                    self.x1 = self.pixmap_x_start

                if self.y1 > self.pixmap_y_end:
                    self.y1 = self.pixmap_y_end
                elif self.y1 < self.pixmap_y_start:
                    self.y1 = self.pixmap_y_start
                rect = QRect(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)

                painter = QPainter(self)
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                painter.drawRect(rect)

                # calculate the reserved section
                self.img_x_start = int(self.x0 - self.pixmap_x_start)
                self.img_x_end = int(self.x1 - self.pixmap_x_start)
                self.img_y_start = int(self.y0 - self.pixmap_y_start)
                self.img_y_end = int(self.y1 - self.pixmap_y_start)
        # drawlines both on the image shows on the label and the mask image with background color in white
        elif self.flag == 2:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 10))
            painter.drawPath(self.painterPath)
            painter.end()

            painter2 = QPainter(self.mask)
            painter2.setRenderHint(QPainter.Antialiasing)
            painter2.setPen(QtGui.QPen(QtCore.Qt.black, 10))
            painter2.drawPath(self.painterPath)
            painter2.end()

    # draw the line from the start point to the end point
    def drawLine(self, start_point, end_point):
        self.painterPath.moveTo(start_point)
        self.painterPath.lineTo(end_point)
        self.update()

    # clear the paint traces
    def clearRect(self):
        if self.flag == 1:
            self.__isClear = True
            self.img_x_start = 0
            self.img_x_end = 0
            self.img_y_start = 0
            self.img_y_end = 0
            self.update()
        elif self.flag == 2:
            self.mask.fill(Qt.white)
            self.painterPath = QPainterPath()
            self.update()
