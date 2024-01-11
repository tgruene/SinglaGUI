import json
import logging
import socket as socketlib
import struct
import threading
import time

import bitshuffle
import lz4.block
import numpy as np
import zmq
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

from dectris2xds.fit2d import fitgaussian


class StreamReceiver(QObject):
    init = pyqtSignal()
    image_decoded = pyqtSignal()

    def __init__(self, control_worker):
        super().__init__()
        self.fitting_duration = 0
        self.fit = [0, 0, 0, 0, 0]
        self.control = control_worker
        self.init.connect(self.receive)
        self.image = np.zeros((1, 1), int)

    @pyqtSlot()
    def receive(self):
        """
            connect to the SINGLA stream interface and start receiving the stream images
        """
        threading.current_thread().setName("StreamThread")
        logging.info("starting receiving stream data")

        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect(f"tcp://{self.control.config['SINGLA_IP']}:{self.control.config['SINGLA_STREAM_PORT']}")

        if socketlib.gethostname() == "A526-wirth":
            return

        while True:
            packet = socket.recv()
            if packet[0] == 123:  # if the packet begins with "{" character:
                packet = json.loads(packet)
            else:

                continue

            if packet["htype"] == "dheader-1.0":
                if packet["header_detail"] == "all" or packet["header_detail"] == "basic":
                    config_params = socket.recv_json()

                if packet["header_detail"] == "all":
                    flatfield_header = socket.recv_json()
                    flatfield_data = socket.recv()

                    pixelmask_header = socket.recv_json()
                    pixelmask_data = socket.recv()

                    countrate_header = socket.recv_json()
                    countrate_data = socket.recv()

            if packet["htype"] == "dimage-1.0":

                data_header = socket.recv_json()
                encoding = data_header["encoding"]
                data_type = data_header["type"]
                shape = data_header["shape"][1], data_header["shape"][0]
                image_data = socket.recv()

                if encoding == "lz4<":
                    image = readLZ4(image_data, shape, data_type)
                elif encoding.startswith("bs"):
                    image = readBSLZ4(image_data, shape, data_type)
                else:
                    return

                # code taken from strela viewer
                # workaround strange pyqtgraph/np bug, where histogram cannot be built for empty data
                image[0, 0] = -1
                image[-1, 0] = -1
                image[0, -1] = -1
                image[-1, -1] = -1

                if self.control.window.checkbox_fit_beam.isChecked() and \
                        (self.control.tem_status["eos.GetFunctionMode"][0] == 4):
                    start_time = time.time()
                    max_pos = np.argmax(image)
                    roi = self.control.window.roi
                    region = roi.getArrayRegion(image,
                                                self.control.window.stream_view.getImageItem())

                    self.fit, success = fitgaussian(region, maxfev=1400, overflow_value=(2 ** (8 * image.itemsize) - 1))
                    self.fitting_duration = time.time() - start_time
                    # (fitgaussian(image[max_pos[0]-50:max_pos[1]+50, max_pos[1]-50:max_pos[1]+50]))

                # set overflow values to 0 for better contrast
                # typecasting to signed int might be better...
                image[image == (2 ** (8 * image.itemsize) - 1)] = 0
                self.image_decoded.emit()
                self.difference = np.sum(np.abs(image - self.image))
                self.image = image
                config_header = socket.recv_json()


def readBSLZ4(data, shape, dtype):
    """
           Decompression routine taken from
            https://github.com/SaschaAndresGrimm/STRELA/blob/main/tools/compression.py

        print(packet[0])
        unpack bitshuffle-lz4 compressed frame and return np array image data
        frame: zmq data blob frame
        shape: image shape
        dtype: image data type
        """

    blob = np.fromstring(data[12:], dtype=np.uint8)
    dtype = np.dtype(dtype)
    # blocksize is big endian uint32 starting at byte 8, divided by element size
    blocksize = int(np.ndarray(shape=(), dtype=">u4", buffer=data[8:12]) / dtype.itemsize)
    imgData = bitshuffle.decompress_lz4(blob, shape, dtype, blocksize)

    return imgData


def readLZ4(data, shape, dtype):
    """
        Decompression routine taken from
        https://github.com/SaschaAndresGrimm/STRELA/blob/main/tools/compression.py
        unpack lz4 compressed frame and return np array image data
        frame: zmq data blob frame
        shape: image shape
        dtype:image data type
    """

    dtype = np.dtype(dtype)
    dataSize = dtype.itemsize * shape[0] * shape[1]  # bytes * image size

    imgData = lz4.block.decompress(struct.pack('<I', dataSize) + data)

    return np.reshape(np.fromstring(imgData, dtype=dtype), shape)
