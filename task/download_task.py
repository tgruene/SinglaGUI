import logging
import os

import h5py
import numpy as np
import requests
from PyQt6.QtWidgets import QMessageBox

from dectris2xds.dectris2xds import XDSparams
from dectris2xds.fit2d import fitgaussian
from task.record_task import RecordTask
from task.still_task import StillTask
from task.task import Task


def fit_beam_center(d):
    d[d == 2 ** 32 - 1] = 0

    m = np.amax(d)
    idx = np.where(d == m)
    xmax = idx[0][0]
    ymax = idx[1][0]
    logging.info(f"   ! unfitted maximum {m} at {xmax}, {ymax}")

    k = 10
    peak = d[xmax - k:xmax + k, ymax - k:ymax + k]

    p,success = fitgaussian(data=peak)
    orgx = ymax - k + p[2]
    orgy = xmax - k + p[1]
    logging.info(f"   !Maximum value {p[0]:.2e} at {p[1]:5.1f}/{p[2]:5.1f} +/- {p[3]:5.1f}/{p[4]:5.1f}")
    logging.info(f" ORGX= {orgx:5.1f} ORGY= {orgy:5.1f}")
    logging.info(f"   !Ellipse Angle = {180. / np.pi * p[5]:5.1f}")

    return orgx, orgy


class DownloadTask(Task):
    def __init__(self, control_worker, data_directory, work_directory):
        super().__init__(control_worker, "Download")
        self.data_directory = os.path.expanduser(data_directory)
        self.work_directory = os.path.expanduser(work_directory)

    def run(self):
        if not isinstance(self.control.last_task, RecordTask) or isinstance(self.control.last_task, StillTask):
            self.control.issue_message_box.emit("Error", "Nothing to download", QMessageBox.Icon.Warning)
            return

        sample_suffix = self.control.last_task.sample_name  # f"x{self.xtal_id}_ID-{self.arm_id}"
        sample_directory = os.path.join(self.work_directory, sample_suffix)
        try:
            os.makedirs(sample_directory)
        except FileExistsError:
            pass

        # create symlinks
        try:
            os.symlink(self.data_directory, os.path.join(sample_directory, "data"), target_is_directory=True)
            os.symlink(self.data_directory, os.path.join(self.work_directory, "data"), target_is_directory=True)
        except FileExistsError:
            pass

        # get a list of files to download
        filelist = self.control.detector.get_status("files", iface="filewriter")
        filelist = filter(lambda name: sample_suffix in name, filelist)
        master_filepath = ""

        for filename in filelist:
            logging.info(f"downloading file {filename}")
            if "master.h5" in filename:
                master_filepath = os.path.join(self.data_directory, os.path.basename(filename))
            self.download_file(self.control.detector.get_url() + "/data/" + filename, os.path.basename(filename))

        if isinstance(self.control.last_task, RecordTask):
            self.make_xds_file(master_filepath, self.control.config["XDS_template"]) # os.path.join(self.work_directory, "etc/INPUT.XDS"))

    def download_file(self, url, filename):
        # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(os.path.join(self.data_directory, filename), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

    def make_xds_file(self, master_filepath, xds_template_filepath):

        master_file = h5py.File(master_filepath, "r")
        template_filepath = master_filepath.replace("master", "??????")
        frame_time = master_file['entry']['instrument']['detector']['frame_time'][()]
        oscillation_range = frame_time * self.control.last_task.phi_dot
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

                org_x, org_y = fit_beam_center(image)

            break

        myxds = XDSparams(xdstempl=xds_template_filepath)
        myxds.update(org_x, org_y, template_filepath, nimages_dset, oscillation_range,
                     self.control.last_task.detector_distance)
        myxds.xdswrite()
