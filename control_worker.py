import json
import logging
import os
import threading
import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QTimer, QUrl
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket
from PyQt6.QtWidgets import QMessageBox

from stream.stream_receiver import StreamReceiver
from task.beam_fit_task import BeamFitTask
from task.download_task import DownloadTask
from task.still_task import StillTask
from task.record_task import RecordTask
from singla_backend import Singla
from task.task import Task
from task.view_task import ViewTask


class ControlWorker(QObject):
    """
    The 'ControlWorker' object is instantiated once and moved to a separate thread.
    It controls communication with the TEM over a TCP channel and redirects requests to the detector, from which it also regularly
    (UPDATE_TIMER_MS) fetches information.
    It also coordinates the execution of tasks.
    """
    # TEM_IP, TEM_PORT = "temserver", 12345

    # SINGLA_IP, SINGLA_PORT, SINGLA_VERSION = "singla-dcu", 8000, "1.8.0"  # "172.17.41.23"

    UPDATE_TIMER_MS = 1000

    # define some signals
    finished = pyqtSignal()
    updated = pyqtSignal()  # called when the state of the TEM has been updated
    received = pyqtSignal(str)
    send = pyqtSignal(str)
    init = pyqtSignal()
    finished_task = pyqtSignal()
    tem_socket_status = pyqtSignal(int, str)
    singla_status = pyqtSignal(str)
    task_progress = pyqtSignal(float)
    issue_message_box = pyqtSignal(str, str, int)

    trigger_record = pyqtSignal()
    trigger_view = pyqtSignal()
    trigger_still = pyqtSignal()
    trigger_download = pyqtSignal()
    trigger_shutdown = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        # set some properties to 'None' that are set in the 'run' method thread-safely
        self.detector: Singla = None
        self.tem_socket: QTcpSocket = None
        self.task = Task(self, "Dummy")
        self.task_thread = QThread()
        self.stream_thread = QThread()
        self.stream_receiver = StreamReceiver(self)
        self.timer: QTimer = None
        self.window = main_window
        self.config = main_window.config
        self.last_task: Task = None

        self.setObjectName("control Thread")
        self.arm_id = -1

        self.init.connect(self._init)
        self.send.connect(self.send_to_tem)
        self.trigger_record.connect(self.start_record)
        self.trigger_still.connect(self.start_still)
        self.trigger_view.connect(self.start_view)
        self.trigger_download.connect(self.start_download)
        self.trigger_shutdown.connect(self.shutdown)

        self.tem_status = {"GetPos ": [0.0, 0.0, 0.0, 0.0, 0.0], "Getf1OverRateTxNum": 0.5,
                           "eos.GetFunctionMode": [-1, -1]}
        self.tem_update_times = {}
        self.triggerdelay_ms = 500

        self.stream_receiver.moveToThread(self.stream_thread)
        # self.stream_thread.started.connect(self.stream_receiver.receive)
        self.stream_thread.start()
        self.stream_receiver.init.emit()

        # self.setup()

    @pyqtSlot()
    def _init(self):
        """
        initialize the control thread. this code must not be in the constructor as it should run in a separate thread
        """
        threading.current_thread().setName("ControlThread")
        logging.info("initializing control thread...")

        self.tem_socket = QTcpSocket()
        self.tem_socket.readyRead.connect(self.on_tem_receive)
        self.tem_socket.stateChanged.connect(
            lambda state: self.tem_socket_status.emit(state, self.tem_socket.errorString()))
        self.tem_socket.errorOccurred.connect(
            lambda state: self.tem_socket_status.emit(self.tem_socket.state(), self.tem_socket.errorString()))
        self.connect()

        self.detector = Singla(self.config["SINGLA_IP"], self.config["SINGLA_VERSION"], self.config["SINGLA_PORT"])
        self.setup()

        self.timer = QTimer()
        self.timer.timeout.connect(self.ontimer)
        self.timer.start(self.UPDATE_TIMER_MS)
        self.task_thread.start()
        self.ontimer()

        # set the default rotation speed to 1 deg/s
        self.send.emit("stage.Setf1OverRateTxNum(2)")

        logging.info("initialized control thread")
        # self.exec()

    def start_task(self, task):
        """
        run the specified task in a separate thread and connect signals
        """
        self.last_task = self.task
        self.task = task
        self.task.finished.connect(self.on_task_finished)
        self.task.moveToThread(self.task_thread)
        self.task.start.emit()

    @pyqtSlot()
    def on_task_finished(self):
        """
        triggered when the current task is finished
        """
        # self.task_thread = None
        self.finished_task.emit()

    def connect(self):
        """
        connect via a TCP socket to the TEM microscope
        """
        self.tem_socket.connectToHost(self.config["TEM_IP"], self.config["TEM_PORT"])  # ("a526-hodgkin", 12344)

    @pyqtSlot()
    def on_tem_receive(self):
        """
        Triggered when the TEM has sent data that can be read
        """
        data = self.tem_socket.readAll()
        #logging.warning("receiving data")
        # logging.info(data)
        # print("received", data)
        try:
            response = json.loads(bytes(data))
            for entry in response:
                self.tem_status[entry] = response[entry]["val"]
                self.tem_update_times[entry] = (response[entry]["tst_before"], response[entry]["tst_after"])
            self.updated.emit()
            if self.task.running:
                self.task.on_tem_receive()
        except json.JSONDecodeError:
            pass

    @pyqtSlot()
    def shutdown(self):
        logging.info("shutting down control")
        try:
            self.tem_socket.close()
            self.timer.stop()
            self.task_thread.quit()
            self.stream_thread.quit()
        except:
            pass

    @pyqtSlot(str)
    def send_to_tem(self, message):
        """
        Send the command 'message' to the TEM microscope. Can be triggered from other threads
        """
        logging.warning("sending data")
        logging.info("attempting to send " + message)
        if self.tem_socket.state() == QAbstractSocket.SocketState.ConnectedState:
            self.tem_socket.write(message.encode())
            self.tem_socket.flush()
        else:
            logging.info("invalid socket state" + str(self.tem_socket.state()))

    def setup(self, frame_time=0.1):
        """
        Basic configuration od the detector.
        """
        # "Basic settings"

        # we always use trigger mote 'ints'
        self.detector.set_config("trigger_mode", "ints", "detector")
        # save 10,000 frames per HDF5 file
        self.detector.set_config("nimages_per_file", value=10000, iface="filewriter")
        # set to a very high number for continuous viewing
        self.detector.set_config("nimages", 1000000, iface="detector")
        # default count and frame time: 100Hz
        self.detector.set_config("count_time", value=frame_time, iface="detector")
        self.detector.set_config("frame_time", value=frame_time, iface="detector")
        # enable stream for STRELA viewer
        self.detector.set_config("mode", "enabled", iface="stream")

    def arm(self):
        """
        arm the detector
        """
        res = self.detector.send_command("arm")
        self.arm_id = res["sequence id"]

    @pyqtSlot()
    def stop(self):
        """
        disarm the detector and halt rotations
        """

        self.send_to_tem("stage.Stop()")
        self.detector.send_command("disarm")
        # TODO halt the current task
        # self.task_thread.quit()
        self.finished_task.emit()
        pass

    @pyqtSlot()
    def start_record(self, ):
        """
        start the 'record' task. triggered when the 'record' button is clicked
        """
        if self.task.running:
            self.stop()

        end_angle = self.window.input_end_angle.value()
        task = RecordTask(self, end_angle)
        self.start_task(task)

    @pyqtSlot()
    def start_still(self, ):
        """
        start the 'still' task. triggered when the 'still' button is clicked
        """
        if self.task.running:
            self.stop()

        task = StillTask(self)
        self.start_task(task)

    @pyqtSlot()
    def start_view(self):
        """
        start the 'view' task. triggered when the 'view' button is clicked
        """
        if self.task.running:
            logging.warning("task already running")
            return
        task = ViewTask(self)
        self.start_task(task)

    @pyqtSlot()
    def start_beam_fit(self):
        """
            start the 'beam_fit' task. triggered when the 'view' button is clicked
        """
        if self.task.running:
            logging.warning("task already running")
            return
        task = BeamFitTask(self)
        self.start_task(task)

    def start_download(self):
        """
            start the 'download' task. triggered when the 'download' button is clicked
        """
        if self.task.running and self.task.task_name != "View":
            self.issue_message_box.emit("Task Running", f"Task {self.task.task_name} already running",
                                        QMessageBox.Warning)
            return

        task = DownloadTask(self, self.window.input_databasedir.text(), self.window.input_workbasedir.text())
        self.start_task(task)

    @pyqtSlot()
    def ontimer(self):
        """
            timer callback function to fetch information from the detector
        """
        # self.send_to_tem("#info")
        singla_state = self.detector.get_status("state")
        if singla_state == -1:
            singla_state = self.detector.response_status
        # print("ping")
        self.singla_status.emit(singla_state)
        if self.task and self.task.running:
            self.task_progress.emit(self.task.get_progress())

    @property
    def singla_url(self):
        """
            getter method to return the URL string for the singla detector interface
        """
        return QUrl(self.detector.get_url())

    def get_record_file_name(self, suffix=""):
        """
            return the full record file name and a short sample name
        """
        basedir = self.window.input_databasedir.text()
        sample_name = self.window.input_sampleid.text().strip()
        xtal_id = self.window.input_xtal_id.value()
        magnification = self.window.input_magnification.text()
        det_distance = self.window.input_det_distance.text().replace(" ", "")

        base_dir = os.path.abspath(os.path.expanduser(basedir))
        dataset_id = self.arm_id + 1  # self.input_dataset_id.value()
        timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.gmtime())

        filepath_long = os.path.join(base_dir,
                                     f"{sample_name}_{magnification}_D{det_distance}_x{xtal_id:02}_ID-{dataset_id}{suffix}_{timestamp}")
        short_name = f"x{xtal_id:02}_ID-{dataset_id}{suffix}"
        return filepath_long, short_name

    def get_corrected_detector_distance(self, distance, with_unit=True):
        """
            this method returns the corrected detector distance by lookup from the config
        """
        for entry in self.config["distances"]:
            if distance == entry["displayed"]:
                if with_unit:
                    return str(entry["calibrated"]) + entry["unit"]
                else:
                    return str(entry["calibrated"])
        return distance

    def with_max_speed(self, tem_command):
        """
            encapsulates a TEM command with setting maximal rotation speed and then restoring the initial rotation speed
        """
        return "speed=stage.Getf1OverRateTxNum(); stage.Setf1OverRateTxNum(0); " + tem_command \
            + "; stage.Setf1OverRateTxNum(speed)"
