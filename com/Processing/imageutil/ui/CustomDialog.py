

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QButtonGroup


class ContrastDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setStyleSheet("background-color: #3a3a3a; color: #fff;")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        Dialog.setMinimumSize(QtCore.QSize(300, 200))
        Dialog.setMaximumSize(QtCore.QSize(300, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_auto = QtWidgets.QRadioButton(Dialog)
        self.btn_auto.setObjectName("btn_auto")
        self.btn_auto.setStyleSheet('''
        QRadioButton {
            background-color: #3a3a3a;
            color: #fff;    
        }
        ''')
        self.horizontalLayout_2.addWidget(self.btn_auto)
        self.btn_custom = QtWidgets.QRadioButton(Dialog)
        self.btn_custom.setObjectName("btn_custom")
        self.btn_custom.setStyleSheet('''
                QRadioButton {
                    background-color: #3a3a3a;
                    color: #fff;    
                }
                ''')
        self.horizontalLayout_2.addWidget(self.btn_custom)
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn_auto)
        self.btn_group.addButton(self.btn_custom)
        self.btn_custom.toggled.connect(lambda  checked: self.widget_custom.setVisible(checked))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.widget_custom = QtWidgets.QWidget(Dialog)
        self.widget_custom.setObjectName("widget_custom")
        self.widget_custom.setVisible(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_custom)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_custom)
        self.horizontalSlider.setMaximumSize(QtCore.QSize(200, 16777215))
        self.horizontalSlider.setMinimum(-100)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.spinBox = QtWidgets.QSpinBox(self.widget_custom)
        self.spinBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox.setMinimum(-100)
        self.spinBox.setMaximum(100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalSlider.valueChanged.connect(lambda value: self.spinBox.setValue(value))
        self.spinBox.valueChanged.connect(lambda value:self.horizontalSlider.setValue(value))
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addWidget(self.widget_custom)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setMaximumSize(QtCore.QSize(150, 40))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_3.addWidget(self.btn_save)
        self.btn_save.setStyleSheet('''
            QPushButton {
                background-color: #5a5a5a;
                color: #fff;
            }
        ''')
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.btn_save.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Contrast Adjustment"))
        self.btn_auto.setText(_translate("Dialog", "Auto Change"))
        self.btn_custom.setText(_translate("Dialog", "Custom Change"))
        self.btn_save.setText(_translate("Dialog", "Start Processing"))

    def get_contrast_result(self):
        # return self.
        if self.btn_auto.isChecked():
            return "auto", 0
        else:
            # when user modified the slider or the spinbox, get the back value from them
            return "custom", self.horizontalSlider.value()

class LightDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setStyleSheet("background-color: #3a3a3a; color: #fff;")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        Dialog.setMinimumSize(QtCore.QSize(300, 200))
        Dialog.setMaximumSize(QtCore.QSize(300, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_auto = QtWidgets.QRadioButton(Dialog)
        self.btn_auto.setObjectName("btn_auto")
        self.btn_auto.setStyleSheet('''
                QRadioButton {
                    background-color: #3a3a3a;
                    color: #fff;    
                }
                ''')
        self.horizontalLayout_2.addWidget(self.btn_auto)
        self.btn_custom = QtWidgets.QRadioButton(Dialog)
        self.btn_custom.setObjectName("btn_custom")
        self.btn_custom.setStyleSheet('''
                        QRadioButton {
                            background-color: #3a3a3a;
                            color: #fff;    
                        }
                        ''')
        self.horizontalLayout_2.addWidget(self.btn_custom)
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn_auto)
        self.btn_group.addButton(self.btn_custom)
        self.btn_custom.toggled.connect(lambda  checked: self.widget_custom.setVisible(checked))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.widget_custom = QtWidgets.QWidget(Dialog)
        self.widget_custom.setObjectName("widget_custom")
        self.widget_custom.setVisible(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_custom)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_custom)
        self.horizontalSlider.setMaximumSize(QtCore.QSize(200, 16777215))
        self.horizontalSlider.setMinimum(-100)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.spinBox = QtWidgets.QSpinBox(self.widget_custom)
        self.spinBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox.setMinimum(-100)
        self.spinBox.setMaximum(100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalSlider.valueChanged.connect(lambda value: self.spinBox.setValue(value))
        self.spinBox.valueChanged.connect(lambda value:self.horizontalSlider.setValue(value))
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addWidget(self.widget_custom)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setMaximumSize(QtCore.QSize(150, 40))
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setStyleSheet('''
                    QPushButton {
                        background-color: #5a5a5a;
                        color: #fff;
                    }
                ''')
        self.horizontalLayout_3.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.btn_save.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lightness Adjustment"))
        self.btn_auto.setText(_translate("Dialog", "Auto Change"))
        self.btn_custom.setText(_translate("Dialog", "Custom Change"))
        self.btn_save.setText(_translate("Dialog", "Start Processing"))

    def get_lightness_result(self):
        # return self.
        if self.btn_auto.isChecked():
            return "auto", 0
        else:
            # when user modified the slider or the spinbox, get the back value from them
            return "custom", self.horizontalSlider.value()

class SrDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setStyleSheet("background-color: #3a3a3a; color: #fff;")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 150)
        Dialog.setMinimumSize(QtCore.QSize(400, 150))
        Dialog.setMaximumSize(QtCore.QSize(400, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_scale2 = QtWidgets.QRadioButton(Dialog)
        self.btn_scale2.setObjectName("btn_scale2")
        self.horizontalLayout_2.addWidget(self.btn_scale2)
        self.btn_scale3 = QtWidgets.QRadioButton(Dialog)
        self.btn_scale3.setObjectName("btn_scale3")
        self.horizontalLayout_2.addWidget(self.btn_scale3)
        self.btn_scale4 = QtWidgets.QRadioButton(Dialog)
        self.btn_scale4.setObjectName("btn_scale4")
        self.horizontalLayout_2.addWidget(self.btn_scale4)
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn_scale2)
        self.btn_group.addButton(self.btn_scale3)
        self.btn_group.addButton(self.btn_scale4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setMaximumSize(QtCore.QSize(150, 40))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_3.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.btn_save.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Super Resolution Scale"))
        self.btn_scale2.setText(_translate("Dialog", "scale = 2"))
        self.btn_scale3.setText(_translate("Dialog", "scale = 3"))
        self.btn_scale4.setText(_translate("Dialog", "scale = 4"))
        self.btn_save.setText(_translate("Dialog", "Start Processing"))


    def get_sr_result(self):
        if self.btn_scale2.isChecked():
            return 2
        elif self.btn_scale3.isChecked():
            return 3
        elif self.btn_scale4.isChecked():
            return 4
        else:
            return 0

class RotateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setStyleSheet("background-color: #3a3a3a; color: #fff;")
        self.setStyleSheet("QWidget { border: 1px solid black; }")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 150)
        Dialog.setMinimumSize(QtCore.QSize(600, 150))
        Dialog.setMaximumSize(QtCore.QSize(600, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_2.setStyleSheet("QHBoxLayout { border: 1px solid black }")
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_rotate1 = QtWidgets.QRadioButton(Dialog)
        self.btn_rotate1.setObjectName("btn_rotate1")
        self.horizontalLayout_2.addWidget(self.btn_rotate1)
        self.btn_rotate2 = QtWidgets.QRadioButton(Dialog)
        self.btn_rotate2.setObjectName("btn_rotate2")
        self.horizontalLayout_2.addWidget(self.btn_rotate2)
        self.btn_rotate3 = QtWidgets.QRadioButton(Dialog)
        self.btn_rotate3.setObjectName("btn_rotate3")
        self.horizontalLayout_2.addWidget(self.btn_rotate3)
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn_rotate1)
        self.btn_group.addButton(self.btn_rotate2)
        self.btn_group.addButton(self.btn_rotate3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setMaximumSize(QtCore.QSize(150, 40))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_3.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.btn_save.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Rotation Adjustment"))
        self.btn_rotate1.setText(_translate("Dialog", "Rotate 90 Clockwise"))
        self.btn_rotate2.setText(_translate("Dialog", "180 degree rotate"))
        self.btn_rotate3.setText(_translate("Dialog", "Rotate 90 Counter-Clockwise"))
        self.btn_save.setText(_translate("Dialog", "Start Processing"))

    def get_rotate_result(self):
        if self.btn_rotate1.isChecked():
            return 1
        elif self.btn_rotate2.isChecked():
            return 3
        elif self.btn_rotate3.isChecked():
            return 2
        else:
            return 0

class MirrorDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setStyleSheet("background-color: #3a3a3a; color: #fff;")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 150)
        Dialog.setMinimumSize(QtCore.QSize(300, 150))
        Dialog.setMaximumSize(QtCore.QSize(300, 150))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_rotate1 = QtWidgets.QRadioButton(Dialog)
        self.btn_rotate1.setObjectName("btn_rotate1")
        self.horizontalLayout_2.addWidget(self.btn_rotate1)
        self.btn_rotate2 = QtWidgets.QRadioButton(Dialog)
        self.btn_rotate2.setObjectName("btn_rotate2")
        self.horizontalLayout_2.addWidget(self.btn_rotate2)
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn_rotate1)
        self.btn_group.addButton(self.btn_rotate2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setMaximumSize(QtCore.QSize(150, 40))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_3.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.btn_save.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Mirror Adjustment"))
        self.btn_rotate1.setText(_translate("Dialog", "Horizontal Flip"))
        self.btn_rotate2.setText(_translate("Dialog", "Vertical Flip"))
        self.btn_save.setText(_translate("Dialog", "Start Processing"))

    def get_mirror_dir(self):
        if self.btn_rotate1.isChecked():
            return 1
        elif self.btn_rotate2.isChecked():
            return 2
        else:
            return 0