import os
import time

from PyQt6.QtWidgets import QMessageBox

import downloader
from task.task import Task




class StillTask(Task):
    """
         record data for a certain time period (seconds). Appends '_still'
         to current name pattern and resets it afterwards. Meant to record
         images from crystals
    """
    def __init__(self, control_worker, durations_secs=5):
        super().__init__(control_worker, "Still")
        self.duration_s = durations_secs
        self.estimated_duration_s = self.duration_s + 0.1
        self.sample_name = ""

    def run(self):
        filename, self.sample_name = self.control.get_record_file_name()
        magnification = self.control.window.input_magnification.text()
        detector_distance = self.control.window.input_det_distance.text()

        if not (magnification and detector_distance):
            self.control.issue_message_box.emit("Magnification & Detector distance not set",
                                                "Please set TEM mode quickly to 'DIFF' or 'MAG1'", QMessageBox.Warning)
            return

        os.makedirs(filename, exist_ok=True)
        with open(filename + ".log", mode="a+") as logfile:
            logfile.writelines("TEM Still Record\n")
            logfile.writelines("TIMESTAMP: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
            logfile.write(f"magnification: {magnification}\n")
            logfile.write(f"detector distance: {detector_distance}\n")
            logfile.write(f"corrected distance: {self.control.get_corrected_detector_distance(detector_distance)}\n")
            logfile.write("Comment: " + self.control.window.input_comment.toPlainText() + "\n")

        frate = self.control.detector.get_config("frame_time", "detector")

        self.control.detector.set_config("name_pattern", filename, "filewriter")

        n_imgs = round(self.duration_s / frate)

        self.control.detector.send_command("disarm")
        self.control.detector.set_config("mode", "enabled", "filewriter")
        self.control.detector.set_config("nimages", n_imgs, "detector")
        self.control.arm()
        self.control.detector.send_command("trigger")
        # revert original pattern
        # self.view()

        self.control.window.input_xtal_id.setValue(self.control.window.input_xtal_id.value() + 1)
        time.sleep(self.control.config["DCU_WAIT_TIME_SECS"])

        if self.control.config["AUTO_INCREMENT_RECORD"]:
            self.control.window.input_xtal_id.setValue(self.control.window.input_xtal_id.value()+1)
        sample_filepath = os.path.abspath(
            os.path.expanduser(os.path.join(self.control.window.input_workbasedir.text(), self.sample_name)))
        master_filepath = downloader.download_files(self.control,
                                                    os.path.abspath(os.path.expanduser(
                                                        self.control.window.input_databasedir.text())),
                                                    sample_filepath,
                                                    os.path.basename(filename))
