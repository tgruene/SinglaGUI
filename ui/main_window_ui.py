# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1757, 1086)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.control_panel = QtWidgets.QWidget(parent=self.centralwidget)
        self.control_panel.setGeometry(QtCore.QRect(6, 6, 350, 849))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.control_panel.sizePolicy().hasHeightForWidth())
        self.control_panel.setSizePolicy(sizePolicy)
        self.control_panel.setMaximumSize(QtCore.QSize(350, 900))
        self.control_panel.setObjectName("control_panel")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.control_panel)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.checkbox_fit_beam = QtWidgets.QCheckBox(parent=self.control_panel)
        self.checkbox_fit_beam.setObjectName("checkbox_fit_beam")
        self.gridLayout_10.addWidget(self.checkbox_fit_beam, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=self.control_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_rotation_speed = QtWidgets.QGroupBox(parent=self.frame)
        self.groupBox_rotation_speed.setObjectName("groupBox_rotation_speed")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_rotation_speed)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rb_speed_10 = QtWidgets.QRadioButton(parent=self.groupBox_rotation_speed)
        self.rb_speed_10.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.rb_speed_10.setChecked(True)
        self.rb_speed_10.setObjectName("rb_speed_10")
        self.gridLayout_2.addWidget(self.rb_speed_10, 2, 2, 1, 1)
        self.rb_speed_2 = QtWidgets.QRadioButton(parent=self.groupBox_rotation_speed)
        self.rb_speed_2.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.rb_speed_2.setObjectName("rb_speed_2")
        self.gridLayout_2.addWidget(self.rb_speed_2, 1, 2, 1, 1)
        self.rb_speed_05 = QtWidgets.QRadioButton(parent=self.groupBox_rotation_speed)
        self.rb_speed_05.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.rb_speed_05.setObjectName("rb_speed_05")
        self.gridLayout_2.addWidget(self.rb_speed_05, 1, 1, 1, 1)
        self.rb_speed_1 = QtWidgets.QRadioButton(parent=self.groupBox_rotation_speed)
        self.rb_speed_1.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.rb_speed_1.setObjectName("rb_speed_1")
        self.gridLayout_2.addWidget(self.rb_speed_1, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_rotation_speed)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.frame)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.input_end_angle = QtWidgets.QDoubleSpinBox(parent=self.groupBox_3)
        self.input_end_angle.setMinimum(-120.0)
        self.input_end_angle.setMaximum(120.0)
        self.input_end_angle.setObjectName("input_end_angle")
        self.gridLayout_4.addWidget(self.input_end_angle, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 1, 1, 1)
        self.input_start_angle = QtWidgets.QDoubleSpinBox(parent=self.groupBox_3)
        self.input_start_angle.setEnabled(False)
        self.input_start_angle.setMinimum(-120.0)
        self.input_start_angle.setMaximum(120.0)
        self.input_start_angle.setObjectName("input_start_angle")
        self.gridLayout_4.addWidget(self.input_start_angle, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=self.frame)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.input_det_distance = QtWidgets.QLineEdit(parent=self.groupBox_5)
        self.input_det_distance.setText("")
        self.input_det_distance.setReadOnly(True)
        self.input_det_distance.setObjectName("input_det_distance")
        self.gridLayout_3.addWidget(self.input_det_distance, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_5)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
        self.input_magnification = QtWidgets.QLineEdit(parent=self.groupBox_5)
        self.input_magnification.setEnabled(True)
        self.input_magnification.setText("")
        self.input_magnification.setReadOnly(True)
        self.input_magnification.setObjectName("input_magnification")
        self.gridLayout_3.addWidget(self.input_magnification, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_5)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.frame)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.btn_qnm_p10um = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_qnm_p10um.setObjectName("btn_qnm_p10um")
        self.gridLayout_5.addWidget(self.btn_qnm_p10um, 0, 0, 1, 1)
        self.btn_qnm_p10deg = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_qnm_p10deg.setObjectName("btn_qnm_p10deg")
        self.gridLayout_5.addWidget(self.btn_qnm_p10deg, 0, 1, 1, 1)
        self.btn_qnm_0deg = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_qnm_0deg.setObjectName("btn_qnm_0deg")
        self.gridLayout_5.addWidget(self.btn_qnm_0deg, 0, 2, 1, 1)
        self.btn_qnm_m10um = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_qnm_m10um.setObjectName("btn_qnm_m10um")
        self.gridLayout_5.addWidget(self.btn_qnm_m10um, 1, 0, 1, 1)
        self.btn_qnm_m10deg = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_qnm_m10deg.setObjectName("btn_qnm_m10deg")
        self.gridLayout_5.addWidget(self.btn_qnm_m10deg, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.gridLayout_10.addWidget(self.frame, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=self.control_panel)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_8.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 0, 2, 1, 1)
        self.input_sampleid = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_sampleid.setObjectName("input_sampleid")
        self.gridLayout_8.addWidget(self.input_sampleid, 1, 0, 1, 1)
        self.input_xtal_id = QtWidgets.QSpinBox(parent=self.groupBox)
        self.input_xtal_id.setMaximum(500)
        self.input_xtal_id.setObjectName("input_xtal_id")
        self.gridLayout_8.addWidget(self.input_xtal_id, 1, 1, 1, 1)
        self.input_dataset_id = QtWidgets.QSpinBox(parent=self.groupBox)
        self.input_dataset_id.setEnabled(False)
        self.input_dataset_id.setMaximumSize(QtCore.QSize(80, 16777215))
        self.input_dataset_id.setReadOnly(True)
        self.input_dataset_id.setMaximum(1000)
        self.input_dataset_id.setObjectName("input_dataset_id")
        self.gridLayout_8.addWidget(self.input_dataset_id, 1, 2, 1, 1)
        self.widget_4 = QtWidgets.QWidget(parent=self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(parent=self.widget_4)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.btn_select_data_directory = QtWidgets.QPushButton(parent=self.widget_4)
        self.btn_select_data_directory.setObjectName("btn_select_data_directory")
        self.gridLayout_6.addWidget(self.btn_select_data_directory, 1, 2, 1, 1)
        self.btn_select_work_directory = QtWidgets.QPushButton(parent=self.widget_4)
        self.btn_select_work_directory.setObjectName("btn_select_work_directory")
        self.gridLayout_6.addWidget(self.btn_select_work_directory, 2, 2, 1, 1)
        self.input_databasedir = QtWidgets.QLineEdit(parent=self.widget_4)
        self.input_databasedir.setReadOnly(False)
        self.input_databasedir.setObjectName("input_databasedir")
        self.gridLayout_6.addWidget(self.input_databasedir, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.widget_4)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)
        self.input_workbasedir = QtWidgets.QLineEdit(parent=self.widget_4)
        self.input_workbasedir.setReadOnly(False)
        self.input_workbasedir.setObjectName("input_workbasedir")
        self.gridLayout_6.addWidget(self.input_workbasedir, 2, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.widget_4)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 2, 0, 1, 1)
        self.gridLayout_8.addWidget(self.widget_4, 2, 0, 1, 3)
        self.input_comment = QtWidgets.QPlainTextEdit(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_comment.sizePolicy().hasHeightForWidth())
        self.input_comment.setSizePolicy(sizePolicy)
        self.input_comment.setObjectName("input_comment")
        self.gridLayout_8.addWidget(self.input_comment, 3, 0, 1, 3)
        self.gridLayout_10.addWidget(self.groupBox, 0, 0, 1, 1)
        self.stream_view = ImageView(parent=self.centralwidget)
        self.stream_view.setGeometry(QtCore.QRect(362, 6, 1389, 849))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stream_view.sizePolicy().hasHeightForWidth())
        self.stream_view.setSizePolicy(sizePolicy)
        self.stream_view.setAutoFillBackground(False)
        self.stream_view.setStyleSheet("background-color:black;")
        self.stream_view.setObjectName("stream_view")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(780, 861, 971, 166))
        self.widget.setObjectName("widget")
        self.label_dump = QtWidgets.QLabel(parent=self.widget)
        self.label_dump.setGeometry(QtCore.QRect(698, 6, 16, 18))
        self.label_dump.setText("")
        self.label_dump.setObjectName("label_dump")
        self.label_stream_info = QtWidgets.QLabel(parent=self.widget)
        self.label_stream_info.setGeometry(QtCore.QRect(100, 20, 981, 61))
        self.label_stream_info.setObjectName("label_stream_info")
        self.widget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(10, 870, 815, 46))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_record = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_record.setEnabled(True)
        self.btn_record.setCheckable(False)
        self.btn_record.setObjectName("btn_record")
        self.horizontalLayout.addWidget(self.btn_record)
        self.btn_still = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_still.setObjectName("btn_still")
        self.horizontalLayout.addWidget(self.btn_still)
        self.btn_view = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_view.setCheckable(False)
        self.btn_view.setChecked(False)
        self.btn_view.setAutoRepeat(False)
        self.btn_view.setDefault(False)
        self.btn_view.setFlat(False)
        self.btn_view.setObjectName("btn_view")
        self.horizontalLayout.addWidget(self.btn_view)
        self.btn_stop = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout.addWidget(self.btn_stop)
        self.btn_download = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_download.setObjectName("btn_download")
        self.horizontalLayout.addWidget(self.btn_download)
        self.btn_singla_interface = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_singla_interface.setObjectName("btn_singla_interface")
        self.horizontalLayout.addWidget(self.btn_singla_interface)
        self.btn_tem_cmd = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_tem_cmd.setObjectName("btn_tem_cmd")
        self.horizontalLayout.addWidget(self.btn_tem_cmd)
        self.btn_quit = QtWidgets.QPushButton(parent=self.widget_2)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout.addWidget(self.btn_quit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1757, 30))
        self.menubar.setObjectName("menubar")
        self.menuDetector = QtWidgets.QMenu(parent=self.menubar)
        self.menuDetector.setObjectName("menuDetector")
        self.menuTEM = QtWidgets.QMenu(parent=self.menubar)
        self.menuTEM.setObjectName("menuTEM")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSend_Tem_Command = QtGui.QAction(parent=MainWindow)
        self.actionSend_Tem_Command.setObjectName("actionSend_Tem_Command")
        self.actionInitialize = QtGui.QAction(parent=MainWindow)
        self.actionInitialize.setObjectName("actionInitialize")
        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionWebinterface = QtGui.QAction(parent=MainWindow)
        self.actionWebinterface.setObjectName("actionWebinterface")
        self.actionSet_frame_time = QtGui.QAction(parent=MainWindow)
        self.actionSet_frame_time.setObjectName("actionSet_frame_time")
        self.actionFit_Beam = QtGui.QAction(parent=MainWindow)
        self.actionFit_Beam.setObjectName("actionFit_Beam")
        self.menuDetector.addAction(self.actionInitialize)
        self.menuDetector.addAction(self.actionWebinterface)
        self.menuDetector.addAction(self.actionSet_frame_time)
        self.menuTEM.addAction(self.actionSend_Tem_Command)
        self.menuTEM.addAction(self.actionFit_Beam)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuDetector.menuAction())
        self.menubar.addAction(self.menuTEM.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.input_start_angle, self.input_end_angle)
        MainWindow.setTabOrder(self.input_end_angle, self.btn_qnm_p10um)
        MainWindow.setTabOrder(self.btn_qnm_p10um, self.btn_qnm_p10deg)
        MainWindow.setTabOrder(self.btn_qnm_p10deg, self.btn_qnm_0deg)
        MainWindow.setTabOrder(self.btn_qnm_0deg, self.btn_qnm_m10um)
        MainWindow.setTabOrder(self.btn_qnm_m10um, self.btn_qnm_m10deg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Singla GUI"))
        self.checkbox_fit_beam.setText(_translate("MainWindow", "Fit Gaussian"))
        self.groupBox_rotation_speed.setTitle(_translate("MainWindow", "Rotation Speed"))
        self.rb_speed_10.setText(_translate("MainWindow", "10.0 deg/s"))
        self.rb_speed_2.setText(_translate("MainWindow", "2.0 deg/s"))
        self.rb_speed_05.setText(_translate("MainWindow", "0.5 deg/s"))
        self.rb_speed_1.setText(_translate("MainWindow", "1.0 deg/s"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Angles"))
        self.label_5.setText(_translate("MainWindow", "Start:"))
        self.label_6.setText(_translate("MainWindow", "End:"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Detector"))
        self.input_det_distance.setPlaceholderText(_translate("MainWindow", "fetching..."))
        self.label_8.setText(_translate("MainWindow", "Distance:"))
        self.input_magnification.setPlaceholderText(_translate("MainWindow", "fetching..."))
        self.label_7.setText(_translate("MainWindow", "Magnification:"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Quick Moves"))
        self.btn_qnm_p10um.setText(_translate("MainWindow", "+ 10 µm"))
        self.btn_qnm_p10deg.setText(_translate("MainWindow", "+ 10 deg"))
        self.btn_qnm_0deg.setText(_translate("MainWindow", "0 deg"))
        self.btn_qnm_m10um.setText(_translate("MainWindow", "- 10 µm"))
        self.btn_qnm_m10deg.setText(_translate("MainWindow", "- 10 deg"))
        self.groupBox.setTitle(_translate("MainWindow", "Sample Name"))
        self.label_4.setText(_translate("MainWindow", "Dataset ID"))
        self.label_3.setText(_translate("MainWindow", "Xtal ID"))
        self.label_2.setText(_translate("MainWindow", "Sample ID"))
        self.label.setText(_translate("MainWindow", "Directories"))
        self.btn_select_data_directory.setText(_translate("MainWindow", "Select"))
        self.btn_select_work_directory.setText(_translate("MainWindow", "Select"))
        self.input_databasedir.setText(_translate("MainWindow", "/data/jungfrau/users/singla"))
        self.label_9.setText(_translate("MainWindow", "Data Directory"))
        self.input_workbasedir.setText(_translate("MainWindow", "~/jem2100plus"))
        self.label_10.setText(_translate("MainWindow", "Work Directory"))
        self.input_comment.setPlaceholderText(_translate("MainWindow", "Comment"))
        self.label_stream_info.setText(_translate("MainWindow", "No stream fit"))
        self.btn_record.setText(_translate("MainWindow", "Record"))
        self.btn_still.setText(_translate("MainWindow", "Still"))
        self.btn_view.setText(_translate("MainWindow", "View"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
        self.btn_download.setText(_translate("MainWindow", "Download"))
        self.btn_singla_interface.setText(_translate("MainWindow", "SINGLA Webinterface"))
        self.btn_tem_cmd.setText(_translate("MainWindow", "TEM Command"))
        self.btn_quit.setText(_translate("MainWindow", "Quit"))
        self.menuDetector.setTitle(_translate("MainWindow", "Detector"))
        self.menuTEM.setTitle(_translate("MainWindow", "TEM"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSend_Tem_Command.setText(_translate("MainWindow", "Send Tem Command"))
        self.actionInitialize.setText(_translate("MainWindow", "Initialize"))
        self.actionInitialize.setToolTip(_translate("MainWindow", "Initialize the detector"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionWebinterface.setText(_translate("MainWindow", "Webinterface"))
        self.actionSet_frame_time.setText(_translate("MainWindow", "Set frame time"))
        self.actionFit_Beam.setText(_translate("MainWindow", "Fit Beam"))
from pyqtgraph import ImageView
