import logging
import os

import requests


def download_file(url, filepath):
    """
    download a single file from 'url' to 'filepath'
    """
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def download_files(control, data_directory, sample_directory, filebasename):
    """
    Downloads the files from the detector that match the filebasename
    returns the absolute file path of the "master.h5" file
    """
    work_directory = os.path.abspath(os.path.join(sample_directory, os.path.pardir))
    try:
        os.makedirs(sample_directory, exist_ok=True)
        os.makedirs(data_directory, exist_ok=True)
    except FileExistsError:
        pass

    # create symlinks
    try:
        os.symlink(data_directory, os.path.join(sample_directory, "data"), target_is_directory=True)
        os.symlink(data_directory, os.path.join(work_directory, "data"), target_is_directory=True)
    except FileExistsError:
        pass

    # get a list of files to download
    filelist = control.detector.get_status("files", iface="filewriter")
    filelist = filter(lambda name: filebasename in name, filelist)
    master_filepath = ""

    for filename in filelist:
        logging.info(f"downloading file {filename}")
        if "master.h5" in filename:
            master_filepath = os.path.join(data_directory, os.path.basename(filename))
        download_file(control.detector.get_url() + "/data/" + filename,
                      os.path.join(data_directory, os.path.basename(filename)))

    return master_filepath
