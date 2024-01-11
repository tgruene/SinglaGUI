import math

from PyQt6.QtCore import QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from pyqtgraph import TargetItem, RectROI

from config import load_config_files
from control_worker import *
from ui.main_window_ui import *
from ui.status_bar_ui import *


class StatusBarContainer(QtWidgets.QWidget, Ui_status_bar):
    """
    a wrapper class to contain the status bar and its widgets
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The main UI window of the singla GUI
    """

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.config = load_config_files()

        self.setWindowIcon(QIcon("share/DECTRIS_SINGLA-product_photo.png"))

        self.status_bar_container = StatusBarContainer(self)
        self.statusbar.addWidget(self.status_bar_container)
        self.status_bar_container.sb_progress_bar.setVisible(False)

        self.control_thread = QThread()
        self.control = ControlWorker(self)

        # connect all slots
        self.btn_select_data_directory.clicked.connect(self.select_data_dir)
        self.btn_select_work_directory.clicked.connect(self.select_work_dir)
        self.btn_record.clicked.connect(self.onclick_record)
        self.btn_view.clicked.connect(self.onclick_view)
        self.btn_still.clicked.connect(self.onclick_still)
        self.btn_stop.clicked.connect(self.onclick_stop)
        self.btn_stop.clicked.connect(self.control.stop)
        self.btn_download.clicked.connect(self.onclick_download)
        self.btn_quit.clicked.connect(self.onclick_quit)
        # self.btn_quit.clicked.connect(self.control.shutdown)
        self.btn_tem_cmd.clicked.connect(self.onclick_tem_cmd)
        self.btn_singla_interface.clicked.connect(self.actionWebinterface.triggered)

        self.btn_qnm_0deg.clicked.connect(
            lambda: self.control.send.emit(self.control.with_max_speed("stage.SetTiltXAngle(0)")))
        self.btn_qnm_m10um.clicked.connect(lambda: self.control.send.emit("stage.SetXRel(-10.0)"))
        self.btn_qnm_p10um.clicked.connect(lambda: self.control.send.emit("stage.SetXRel(+10.0)"))
        self.btn_qnm_m10deg.clicked.connect(
            lambda: self.control.send.emit(self.control.with_max_speed("stage.SetTXRel(-10.0)")))
        self.btn_qnm_p10deg.clicked.connect(
            lambda: self.control.send.emit(self.control.with_max_speed("stage.SetTXRel(+10.0)")))

        self.rb_speed_05.clicked.connect(lambda: self.control.send.emit("stage.Setf1OverRateTxNum(3)"))
        self.rb_speed_1.clicked.connect(lambda: self.control.send.emit("stage.Setf1OverRateTxNum(2)"))
        self.rb_speed_2.clicked.connect(lambda: self.control.send.emit("stage.Setf1OverRateTxNum(1)"))
        self.rb_speed_10.clicked.connect(lambda: self.control.send.emit("stage.Setf1OverRateTxNum(0)"))

        self.actionInitialize.triggered.connect(self.onclick_detector_initialize)
        self.actionSet_frame_time.triggered.connect(self.onclick_set_frame_time)
        self.actionSend_Tem_Command.triggered.connect(self.onclick_tem_cmd)
        self.actionAbout.triggered.connect(self.onclick_help_about)
        self.actionFit_Beam.triggered.connect(self.control.start_beam_fit)

        self.actionWebinterface.triggered.connect(lambda: QDesktopServices.openUrl(self.control.singla_url))

        self.control.finished_task.connect(self.on_task_finished)

        self.control.stream_receiver.image_decoded.connect(self.on_stream_image)

        self.control.finished.connect(self.control_thread.quit)
        self.control.finished.connect(self.control.deleteLater)
        self.control_thread.finished.connect(self.control_thread.deleteLater)

        self.control.received.connect(self.label_dump.setText)
        self.control.updated.connect(self.on_tem_update)
        self.control.tem_socket_status.connect(self.on_sockstatus_change)
        self.control.singla_status.connect(self.on_singla_status_change)
        self.control.issue_message_box.connect(self.show_message_box)
        self.control.task_progress.connect(
            lambda progress: self.status_bar_container.sb_progress_bar.setValue(round(progress * 100)))

        # start other threads
        self.control.moveToThread(self.control_thread)
        self.control_thread.start()
        self.control.init.emit()

        if self.config["FULLSCREEN"]:
            self.showMaximized()

        self.last_tem_command = "print('Hello, World!')"
        self.input_databasedir.setText(self.config["data_root"])
        self.input_workbasedir.setText(self.config["work_dir_root"])

        self.stream_view.setHistogramLabel("Intensity")
        self.stream_view.getImageItem().setOpts(axisOrder="row-major")
        self.target_item = TargetItem((-10000, 0), movable=False, pen="c")
        self.roi = RectROI((520, 570), (80, 80), rotatable=False, pen="r")
        self.stream_view.getView().addItem(self.roi)
        self.stream_view.getView().addItem(self.target_item)

        # mark optical axis
        radius = 25
        optaxis_W = 543
        optaxis_H = 549
        optaxis= QGraphicsEllipseItem(optaxis_W-radius, optaxis_H-radius, 2*radius, 2*radius)
        optaxis.setPen(QPen(Qt.GlobalColor.yellow))
        self.stream_view.addItem(optaxis)

        # mark jump from X1200 to X20k
        radius = 35
        lmjump_W = 703
        lmjump_H = 455
        lmjump = QGraphicsEllipseItem(lmjump_W-radius, lmjump_H-radius, 2*radius, 2*radius)
        lmjump.setPen(QPen(Qt.GlobalColor.green))
        self.stream_view.addItem(lmjump)

        # frame around entire detector
        W = 1028
        H = 1062
        frm = QGraphicsRectItem(0, 0, W, H)
        frm.setPen(QPen(Qt.GlobalColor.red))
        self.stream_view.addItem(frm)

        gap = QGraphicsRectItem(0, 513, W, 36)
        gap.setPen(QPen(QColor(255, 255, 255)))
        self.stream_view.addItem(gap)


        # self.stream_view.roi = RectROI((50, 50), (200, 200), rotatable=False, pen='g')
        # self.stream_view.getHistogramWidget().disableAutoHistogramRange()
        # self.input_workbasedir.setText(os.path)

    @pyqtSlot()
    def select_data_dir(self):
        """
            open a file dialog to select the base directory for the record file
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select data directory", self.input_databasedir.text())
        if dir_path:
            self.input_databasedir.setText(dir_path)

    @pyqtSlot()
    def select_work_dir(self):
        """
            open a file dialog to select the working directory
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select work directory", self.input_workbasedir.text())
        if dir_path:
            self.input_workbasedir.setText(dir_path)

    @pyqtSlot()
    def onclick_record(self):
        """
            Start the recording Process. Triggered when 'record' is clicked
        """
        self.control.trigger_record.emit()

        self.btn_record.setEnabled(False)
        self.btn_view.setEnabled(False)
        self.btn_still.setEnabled(False)
        self.status_bar_container.sb_progress_bar.setVisible(True)

    @pyqtSlot()
    def onclick_view(self):
        """
           Trigger detector view. Triggered when 'View' is clicked
        """
        self.control.trigger_view.emit()

        self.btn_view.setEnabled(False)

    @pyqtSlot()
    def onclick_still(self):
        """
           Trigger detector still. Triggered when 'Still' is clicked
        """
        self.control.trigger_still.emit()

        self.btn_record.setEnabled(False)
        self.btn_view.setEnabled(False)
        self.btn_still.setEnabled(False)
        self.status_bar_container.sb_progress_bar.setVisible(True)

    @pyqtSlot()
    def onclick_stop(self):
        """
            Stop recording. Triggered when 'Stop' is clicked
        """
        pass
        # self.btn_record.setEnabled(True)

    @pyqtSlot()
    def onclick_quit(self):
        """
           Quit the application. Triggered when 'Quit' is clicked
        """
        logging.info("Quitting...")
        self.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.control.trigger_shutdown.emit()
        event.accept()

    @pyqtSlot()
    def onclick_download(self):
        """
           Start the download of the files. Triggered when 'Download' is clicked
        """
        self.control.trigger_download.emit()

    @pyqtSlot()
    def on_task_finished(self):
        """
            Triggered when a task is finished
        """
        self.btn_record.setEnabled(True)
        self.btn_view.setEnabled(True)
        self.btn_still.setEnabled(True)
        self.input_dataset_id.setValue(self.control.arm_id)
        self.status_bar_container.sb_progress_bar.setVisible(False)
        self.status_bar_container.sb_progress_bar.setValue(0)

    @pyqtSlot()
    def onclick_tem_cmd(self):
        """
            Triggered when the 'TEM Command' button is pressed
        """
        command, ok = QInputDialog.getText(self, 'TEM Command', 'Enter TEM command', text=self.last_tem_command)
        if ok:
            self.control.send.emit(command)
            self.last_tem_command = command

    @pyqtSlot(int, str)
    def on_sockstatus_change(self, state, error_msg):
        """
            Triggered when the status of the TEM TCP socket changes. Updates the status bar correspondingly
        """
        if state == QAbstractSocket.SocketState.ConnectedState:
            message, color = "Connected", "green"
        elif state == QAbstractSocket.SocketState.ConnectingState:
            message, color = "Connecting", "orange"
        elif error_msg:
            message = "Error (" + error_msg + ")"
            color = "red"
        else:
            message, color = "Disconnected", "red"

        self.status_bar_container.sb_label_tem.setText(f'TEM Status: <font color="{color}">{message}</font>')

    @pyqtSlot(str)
    def on_singla_status_change(self, state):
        """
        Updates the detector status indicator
        """
        COLORS = {"na": "red", "idle": "green", "ready": "green", "acquire": "darkgreen", "configure": "orange",
                  "initialize": "orange", "error": "red"}
        if state in COLORS:
            color = COLORS[state]
            state = state.capitalize()
        else:
            color = "red"
        self.status_bar_container.sb_label_singla.setText(f'SINGLA Status: <font color="{color}">{state}</font>')

    @pyqtSlot()
    def on_tem_update(self):
        """
        Updates information about the TEM microscope. Called whenever information from the TEM is received
        """
        angle_x = self.control.tem_status["stage.GetPos"][3]
        self.input_start_angle.setValue(angle_x)

        if self.control.tem_status["eos.GetFunctionMode"][0] in [0, 1, 2]:
            magnification = self.control.tem_status["eos.GetMagValue"][2]
            self.input_magnification.setText(magnification)

        if self.control.tem_status["eos.GetFunctionMode"][0] == 4:
            detector_distance = self.control.tem_status["eos.GetMagValue"][2]
            self.input_det_distance.setText(detector_distance)

        rotation_speed_index = self.control.tem_status["stage.Getf1OverRateTxNum"]
        if rotation_speed_index == 0:
            self.rb_speed_10.setChecked(True)
        elif rotation_speed_index == 1:
            self.rb_speed_2.setChecked(True)
        elif rotation_speed_index == 2:
            self.rb_speed_1.setChecked(True)
        elif rotation_speed_index == 3:
            self.rb_speed_05.setChecked(True)

    @pyqtSlot(str, str, int)
    def show_message_box(self, title, text, icon):
        """
        show a message box (can be triggered from other threads)
        """
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.exec()

    @pyqtSlot()
    def onclick_detector_initialize(self):
        """
        send the command 'initialize' to the detector
        """
        reply = QMessageBox.question(self, "Initialize detector", "Do you want to initialize the detector")
        if reply == QMessageBox.Ok:
            self.control.detector.send_command("initialize")

    @pyqtSlot()
    def onclick_help_about(self):
        """
        Display an 'About' popup window
        """
        import main
        QMessageBox.about(self, "Singla GUI - About", main.get_about_info())
        print(self.stream_view.roi.getArraySlice(self.control.stream_receiver.image, self.stream_view.image))

    @pyqtSlot()
    def onclick_set_frame_time(self):
        """
        Prompt frame time dialog
        """
        frame_time = self.control.detector.get_config("frame_time", "detector")
        reply, ok = QInputDialog.getDouble(self, "Frame Time", "Enter frame time (seconds)", frame_time, 0.0003)
        if ok:
            self.control.detector.set_config("frame_time", reply, "detector")

    @pyqtSlot()
    def on_stream_image(self):
        """
        callback method to display a new image in the stream display field
        this also updates the fit data text field
        """
        self.stream_view.setImage(self.control.stream_receiver.image, autoRange=False,
                                  autoLevels=False, autoHistogramRange=False)  # axes={"x": 1, "y": 0}))

        if self.checkbox_fit_beam.isChecked() and (self.control.tem_status["eos.GetFunctionMode"][0] == 4):
            self.target_item._bounds = QRectF(0, 0, 1, 1)
            fit = self.control.stream_receiver.fit
            ratio = max(abs(fit[3]), abs(fit[4])) / min(abs(fit[3]), abs(fit[4]))
            eccentricity = math.sqrt( 1-ratio**(-2))
            self.label_stream_info.setText(
                f"height: {fit[0]:13.2f}, x: {fit[1]:6.1f}, y: {fit[2]:6.1f}, width_x: {fit[3]:6.3f}, width_y: {fit[4]:6.3f}, theta:{(fit[5] % 180):6.1f} \neccentricity {eccentricity:6.3f} ratio {ratio:6.3f} time: {self.control.stream_receiver.fitting_duration :.4f} difference {self.control.stream_receiver.difference / self.control.stream_receiver.image.size} ")

            center_x = self.roi.pos()[0] + fit[2]
            center_y = self.roi.pos()[1] + fit[1]
            self.target_item.setPos((center_x, center_y))
        else:
            self.target_item._bounds = QRectF(0, 0, 0, 0)
