import logging
import threading
import time
import traceback
from typing import Union

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMessageBox


class Task(QObject):
    """
        Abstract Task class that represents a sequence of potentially blocking calls.
        It is executed in a separate thread
    """
    send_tem_command = pyqtSignal(str)
    start = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, control_worker, name):
        super().__init__()

        self.running = False
        self.estimated_duration_s = 1e10
        self.setObjectName(name)
        self.task_name = name
        self.control = control_worker
        self.send_tem_command.connect(control_worker.send_to_tem)
        self.start.connect(self._start)
        threading.current_thread().setName(name + "Thread")

    def run(self):
        """
            this method contains the actual task. it can for example call this.detector.send_command or self.tem_command or wait
        """
        pass

    @pyqtSlot()
    def _start(self):
        """
            start the task and do housekeeping
        """
        logging.info("Starting task " + self.task_name + "...")
        self.running = True
        self.start_time = time.monotonic()
        try:
            self.run()
        except Exception as exc:
            logging.error("Exception occurred in task " + self.task_name + ": " + traceback.format_exc())
            self.control.issue_message_box.emit("Error",
                                                "Exception occurred in task " + self.task_name + ": " + str(exc),
                                                QMessageBox.Icon.Warning)
        self.running = False
        logging.info("Finished task " + self.task_name)
        self.finished.emit()

    def tem_command(self, module, cmd, args):
        """
            send a command to the TEM microscope
        """
        self.send_tem_command.emit(module + "." + cmd + "(" + str(args)[1: -1] + ")")

    def get_progress(self):
        """
            return the progress of the task as a float between 0 and 1
            default implementation is via monotonic clocks and self.estimated_duration_s
        """
        if not self.running:
            return 0
        percentage = abs(self.start_time - time.monotonic()) / self.estimated_duration_s
        return max(0.0, min(percentage, 1.0))

    def on_tem_receive(self):
        """
            perform an action every time data from the TEM is received
        """
        pass
