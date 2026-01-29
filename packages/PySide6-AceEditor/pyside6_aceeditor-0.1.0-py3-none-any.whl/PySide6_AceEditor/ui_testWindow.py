# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testWindowrTLIAX.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

try:
    from code_frame import AceCodeWidget
except (ImportError, ModuleNotFoundError):
    try:
        from . import code_frame

        AceCodeWidget = code_frame.AceCodeWidget
    except (ImportError, ModuleNotFoundError):
        from PySide6_AceEditor.code_frame import AceCodeWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 578)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = AceCodeWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.widget)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.pushButton_copy = QPushButton(self.tab)
        self.pushButton_copy.setObjectName("pushButton_copy")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.pushButton_copy.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_copy.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.pushButton_copy)

        self.pushButton_paste = QPushButton(self.tab)
        self.pushButton_paste.setObjectName("pushButton_paste")

        self.horizontalLayout.addWidget(self.pushButton_paste)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_readonly = QCheckBox(self.tab)
        self.checkBox_readonly.setObjectName("checkBox_readonly")

        self.horizontalLayout_2.addWidget(self.checkBox_readonly)

        self.pushButton_cpro = QPushButton(self.tab)
        self.pushButton_cpro.setObjectName("pushButton_cpro")

        self.horizontalLayout_2.addWidget(self.pushButton_cpro)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_clr_anno = QPushButton(self.tab_2)
        self.pushButton_clr_anno.setObjectName("pushButton_clr_anno")

        self.horizontalLayout_4.addWidget(self.pushButton_clr_anno)

        self.pushButton_copyanno = QPushButton(self.tab_2)
        self.pushButton_copyanno.setObjectName("pushButton_copyanno")

        self.horizontalLayout_4.addWidget(self.pushButton_copyanno)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QLabel(self.tab_2)
        self.label.setObjectName("label")

        self.horizontalLayout_3.addWidget(self.label)

        self.spinBox_row = QSpinBox(self.tab_2)
        self.spinBox_row.setObjectName("spinBox_row")

        self.horizontalLayout_3.addWidget(self.spinBox_row)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.spinBox_col = QSpinBox(self.tab_2)
        self.spinBox_col.setObjectName("spinBox_col")

        self.horizontalLayout_3.addWidget(self.spinBox_col)

        self.comboBox_annotype = QComboBox(self.tab_2)
        self.comboBox_annotype.addItem("")
        self.comboBox_annotype.addItem("")
        self.comboBox_annotype.addItem("")
        self.comboBox_annotype.setObjectName("comboBox_annotype")

        self.horizontalLayout_3.addWidget(self.comboBox_annotype)

        self.lineEdit_anno = QLineEdit(self.tab_2)
        self.lineEdit_anno.setObjectName("lineEdit_anno")

        self.horizontalLayout_3.addWidget(self.lineEdit_anno)

        self.pushButton_addanno = QPushButton(self.tab_2)
        self.pushButton_addanno.setObjectName("pushButton_addanno")

        self.horizontalLayout_3.addWidget(self.pushButton_addanno)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QScrollArea(self.tab_3)
        self.scrollArea.setObjectName("scrollArea")
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMaximumSize(QSize(16777215, 100))
        self.scrollArea.setBaseSize(QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -52, 742, 148))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_copy_cur_pos = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_copy_cur_pos.setObjectName("pushButton_copy_cur_pos")

        self.horizontalLayout_8.addWidget(self.pushButton_copy_cur_pos)

        self.pushButton_copy_anch_pos = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_copy_anch_pos.setObjectName("pushButton_copy_anch_pos")

        self.horizontalLayout_8.addWidget(self.pushButton_copy_anch_pos)

        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.pushButton_cur_up = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_cur_up.setObjectName("pushButton_cur_up")

        self.horizontalLayout_5.addWidget(self.pushButton_cur_up)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.pushButton_cur_left = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_cur_left.setObjectName("pushButton_cur_left")

        self.horizontalLayout_6.addWidget(self.pushButton_cur_left)

        self.checkBox_selecting = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_selecting.setObjectName("checkBox_selecting")

        self.horizontalLayout_6.addWidget(self.checkBox_selecting)

        self.pushButton_cur_right = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_cur_right.setObjectName("pushButton_cur_right")

        self.horizontalLayout_6.addWidget(self.pushButton_cur_right)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalSpacer_7 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.pushButton_cur_down = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_cur_down.setObjectName("pushButton_cur_down")

        self.horizontalLayout_7.addWidget(self.pushButton_cur_down)

        self.horizontalSpacer_6 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.pushButton_copy.setText(
            QCoreApplication.translate("MainWindow", "Copy", None)
        )
        self.pushButton_paste.setText(
            QCoreApplication.translate("MainWindow", "Paste", None)
        )
        self.checkBox_readonly.setText(
            QCoreApplication.translate("MainWindow", "ReadOnly", None)
        )
        self.pushButton_cpro.setText(
            QCoreApplication.translate("MainWindow", "Copy isReadOnly", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("MainWindow", "Edit", None),
        )
        self.pushButton_clr_anno.setText(
            QCoreApplication.translate("MainWindow", "Clear Annotations", None)
        )
        self.pushButton_copyanno.setText(
            QCoreApplication.translate("MainWindow", "Copy Annotations", None)
        )
        self.label.setText(QCoreApplication.translate("MainWindow", "Row:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Column:", None))
        self.comboBox_annotype.setItemText(
            0, QCoreApplication.translate("MainWindow", "error", None)
        )
        self.comboBox_annotype.setItemText(
            1, QCoreApplication.translate("MainWindow", "warning", None)
        )
        self.comboBox_annotype.setItemText(
            2, QCoreApplication.translate("MainWindow", "info", None)
        )

        self.pushButton_addanno.setText(
            QCoreApplication.translate("MainWindow", "Add", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("MainWindow", "Annotations", None),
        )
        self.pushButton_copy_cur_pos.setText(
            QCoreApplication.translate("MainWindow", "Copy Cursor Position", None)
        )
        self.pushButton_copy_anch_pos.setText(
            QCoreApplication.translate("MainWindow", "Copy Anchor Position", None)
        )
        self.pushButton_cur_up.setText(
            QCoreApplication.translate("MainWindow", "\u2191", None)
        )
        self.pushButton_cur_left.setText(
            QCoreApplication.translate("MainWindow", "\u2190", None)
        )
        self.checkBox_selecting.setText(
            QCoreApplication.translate("MainWindow", "Selecting", None)
        )
        self.pushButton_cur_right.setText(
            QCoreApplication.translate("MainWindow", "\u2192", None)
        )
        self.pushButton_cur_down.setText(
            QCoreApplication.translate("MainWindow", "\u2193", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            QCoreApplication.translate("MainWindow", "Cursor", None),
        )

    # retranslateUi
