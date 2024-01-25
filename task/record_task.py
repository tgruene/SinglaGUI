import logging
import os
import time

import h5py
import numpy as np
from PyQt6.QtWidgets import QMessageBox

import downloader
from dectris2xds.dectris2xds import XDSparams
from dectris2xds.fit2d import fitgaussian
from task.task import Task
from time import sleep


class RecordTask(Task):
    """
       start recording of data by enabling file writer
       if nimages<0, nimages is calculated as
       |phi1-phi0|/(phidot*frame_time)
       if nimages>0, this is used as number of images
    """

    def __init__(self, control_worker, end_angle):
        super().__init__(control_worker, "Record")
        self.detector_distance = None
        self.sample_name = ""
        self.phi_dot = 0
        self.control = control_worker
        self.end_angle = end_angle
        self.t0 = -1e10
        self.rotations_angles = []

    def run(self):
        filename, self.sample_name = self.control.get_record_file_name()

        magnification = self.control.window.input_magnification.text()
        self.detector_distance = self.control.window.input_det_distance.text()

        if not (magnification and self.detector_distance):
            self.control.issue_message_box.emit("Magnification & Detector distance not set",
                                                "Please set TEM mode quickly to 'DIFF' or 'MAG1'", QMessageBox.Icon.Warning)
            return

        ft = self.control.detector.get_config("frame_time", "detector")
        self.control.detector.set_config("name_pattern", os.path.basename(filename), "filewriter")
        phi0 = self.control.tem_status["stage.GetPos"][3]
        phi1 = self.end_angle
        stage_rates = [10.0, 2.0, 1.0, 0.5]
        phi_dot_idx = self.control.tem_status["stage.Getf1OverRateTxNum"]

        self.phi_dot = stage_rates[phi_dot_idx] * np.sign(phi1 - phi0)
        # calculate number of images, take delay into account
        n_imgs = (abs(phi1 - phi0) / abs(self.phi_dot) - self.control.triggerdelay_ms * 0.001) / ft
        n_imgs = round(n_imgs)
        logging.info(f"phidot: {self.phi_dot} deg/s, Delta Phi:{abs(phi1 - phi0)} deg, {n_imgs} images")
        self.estimated_duration_s = abs(phi1 - phi0) / abs(self.phi_dot)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename + ".log", mode="a+") as logfile:
            logfile.write("TEM Record\n")
            logfile.write("TIMESTAMP: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
            logfile.write(f"Initial Angle: {phi0} deg\n")
            logfile.write(f"Final Angle: {phi1} deg\n")
            logfile.write(f"angular Speed: {self.phi_dot} deg/s\n")
            logfile.write(f"#Images: {n_imgs}\n")
            logfile.write(f"magnification: {magnification}\n")
            logfile.write(f"detector distance: {self.detector_distance}\n")
            logfile.write(
                f"corrected distance: {self.control.get_corrected_detector_distance(self.detector_distance)}\n")
            logfile.write("Comment: " + self.control.window.input_comment.toPlainText() + "\n")

        #Disarm Singla, enable filewriter, arm, and trigger
        self.control.detector.send_command("disarm")
        self.control.detector.set_config("mode", "enabled", "filewriter")

        self.control.detector.set_config("nimages", n_imgs, "detector")
        self.control.arm()

        self.tem_command("stage", "SetTiltXAngle", [phi1])

        t0 = time.time()
        self.rotations_angles = []

        sleep(self.control.triggerdelay_ms / 1000)
        self.control.detector.send_command("trigger")

        if self.control.config["AUTO_INCREMENT_RECORD"]:
            self.control.window.input_xtal_id.setValue(self.control.window.input_xtal_id.value() + 1)
        sleep(self.control.config["DCU_WAIT_TIME_SECS"])

        with open(filename + ".log", mode="a+") as logfile:
            logfile.write("Rotation angles: timestamp before, angle, timestamp after\n")
            for (before, angle, after) in self.rotations_angles:
                logfile.write(f"{before - t0:.3f} {angle:.4f} {after - t0:.3f}\n")
        sample_filepath = os.path.abspath(
            os.path.expanduser(os.path.join(self.control.window.input_workbasedir.text(), self.sample_name)))
        master_filepath = downloader.download_files(self.control, os.path.abspath(
            os.path.expanduser(self.control.window.input_databasedir.text())), sample_filepath,
                                                    os.path.basename(filename))

        self.make_xds_file(master_filepath,
                           os.path.join(sample_filepath, "INPUT.XDS"),
                           self.control.config["XDS_template"])

    def on_tem_receive(self):
        self.rotations_angles.append((self.control.tem_update_times["stage.GetPos"][0],
                                      self.control.tem_status["stage.GetPos"][3],
                                      self.control.tem_update_times["stage.GetPos"][1]))

    def make_xds_file(self, master_filepath, xds_filepath, xds_template_filepath):
        """
        create an INPUT.XDS file in the work directory
        this reads the master.h5 file and tries to fit a gaussian distribution to get the center of the beam
        """

        master_file = h5py.File(master_filepath, "r")
        template_filepath = master_filepath.replace("master", "??????")
        frame_time = master_file['entry']['instrument']['detector']['frame_time'][()]
        oscillation_range = frame_time * self.phi_dot
        logging.info(f" OSCILLATION_RANGE= {oscillation_range} ! frame time {frame_time}")

        logging.info(f" NAME_TEMPLATE_OF_DATA_FRAMES= {template_filepath}")

        for dset in master_file["entry"]["data"]:
            nimages_dset = master_file["entry"]["data"][dset].shape[0]
            logging.info(f" DATA_RANGE= 1 {nimages_dset}")
            logging.info(f" BACKGROUND_RANGE= 1 {nimages_dset}")
            logging.info(f" SPOT_RANGE= 1 {nimages_dset}")
            h = master_file["entry"]["data"][dset].shape[2]
            w = master_file["entry"]["data"][dset].shape[1]
            for i in range(1):
                image = master_file["entry"]["data"][dset][i]
                logging.info(f"   !Image dimensions: {image.shape}, 1st value: {image[0]}")

                try:
                    org_x, org_y = fit_beam_center(image)
                except Exception as exc:
                    logging.warning("beam fitting failed: " + str(exc))
                    org_x, org_y = 0, 0

            break

        myxds = XDSparams(xdstempl=xds_template_filepath)
        myxds.update(org_x, org_y, template_filepath, nimages_dset, oscillation_range,
                     self.control.get_corrected_detector_distance(self.detector_distance, with_unit=False))
        myxds.xdswrite(filepath=xds_filepath)


def fit_beam_center(data):
    """
    Tries to fit a gaussian distribution to get the center of the beam.
    Can raise an Error
    """
    data[data == 2 ** 32 - 1] = 0

    m = np.amax(data)
    idx = np.where(data == m)
    xmax = idx[0][0]
    ymax = idx[1][0]
    logging.info(f"   ! unfitted maximum {m} at {xmax}, {ymax}")

    k = 10
    peak = data[xmax - k:xmax + k, ymax - k:ymax + k]

    p, success = fitgaussian(data=peak)
    orgx = ymax - k + p[2]
    orgy = xmax - k + p[1]
    logging.info(f"   !Maximum value {p[0]:.2e} at {p[1]:5.1f}/{p[2]:5.1f} +/- {p[3]:5.1f}/{p[4]:5.1f}")
    logging.info(f" ORGX= {orgx:5.1f} ORGY= {orgy:5.1f}")
    logging.info(f"   !Ellipse Angle = {180. / np.pi * p[5]:5.1f}")

    return orgx, orgy
