#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:21:54 2022

@author: singla
"""
from singla_backend import Singla
# from PyJEM import TEM3
import multiprocessing as mp
import time


class SinglaCmdline:
    "command line front end for convenient commands for SINGLA"
    def __init__(self, ip="172.17.41.23", vers="1.8.0", port = 80):
        self.detector = Singla(ip, vers, port)   
        self.armID = -1
        
    """
        Basic setup up. This will At startup, the detector has to be initialized first"
    """
    def setup(self, frame_time=0.1):
        "Basic settings"
        # delay for trigger cmd to allow rotation to start and stabilise
        self.triggerdelay = 0.5 #seconds
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
        
    """
    set the stem of the output files. It will be amended by timestamp 
    just before data collection
    """
    def stem(self, name_stem):
        "Set the stem of the output file"
        self.name_stem = name_stem
    
    """
    trigger the detector after specified number of seconds delay
    delay allows the stage rotation to reach the final speed, hence 
    should be small, e.g. 0.5
    """
    def detector_trigger(self, delay):
        "Trigger the detector after delay seconds"
        time.sleep(delay)
        self.detector.send_command("trigger")
                
    """
    Short cut for viewing w/o recording files:
    - disarm singla (to ensure consistent state)
    - disable filewriter 
    - set nimages to very high number
    - arm
    - trigger as background process
    """
    def view(self):
        "Disable writing and setup for viewing"
        self.detector.send_command("disarm")
        self.detector.set_config("mode", "disabled", "filewriter")
        self.detector.set_config("nimages", 1000000, "detector")
        self.arm()
        triggerproc = mp.Process(target=self.detector_trigger, args=(0.0, ))
        triggerproc.start()
    
    """
    start recording of data by enabling file writer
    if nimages<0, nimages is calculated as
    |phi1-phi0|/(phidot*frame_time)
    if nimages>0, this is used as number of images
    """
    def record(self, stage, phi1=60):
        "Disarm Singla, enable filewriter, arm, and triffer"
        ft = self.detector.get_config("frame_time", "detector")
        phi0 = stage.GetPos()[3]
        stageRates = [ 10.0, 2.0, 1.0, 0.5]
        phidotidx = stage.Getf1OverRateTxNum()
        phidot = stageRates[phidotidx]
        # calculate number of images, take delay into account
        nimgs = (abs(phi1-phi0)/phidot - self.triggerdelay) /ft
        nimgs = round(nimgs)
        print(phidot, nimgs)
        self.detector.send_command("disarm")
        self.detector.set_config("mode", "enabled", "filewriter")
        self.set_name_pattern()
        self.detector.set_config("nimages", nimgs, "detector")
        self.arm()
        triggerproc = mp.Process(target=self.detector_trigger, args=(self.triggerdelay, ))
        triggerproc.start()
        stage.SetTiltXAngle(phi1)
        #triggerproc.join()
        #self.view()
        
    """ 
    wrapper for armingnthe detector which updates the sequence id as variable for 
    self
    """
    def arm(self):
        res = self.detector.send_command("arm")
        self.armID = res["sequence id"]
        print ("Current $id = {:d}".format(self.armID))
        
    def stop(self):
        "Short cut to disarm the detector"
        # interrupt rotation
        self.detector.send_command("disarm")

    """
    record data for a certain time periond (seconds). Appends '_still' 
    to current name pattern and resets it afterwards. Meant to record
    images from crystals
    """
    def still(self, seconds=5):
        "Record data for seconds seconds"
        mystem = self.name_stem
        frate = self.detector.get_config("frame_time", "detector")

        self.name_stem = mystem+"_still"
        self.set_name_pattern()
        self.name_stem = mystem

        nimages = round(seconds/frate)

        self.detector.send_command("disarm")
        self.detector.set_config("mode", "enabled", "filewriter")
        self.detector.set_config("nimages", nimages, "detector")
        self.arm()
        triggerproc = mp.Process(target=self.detector_trigger, args=(0.0, ))
        triggerproc.start()
        triggerproc.join()
        # revert original pattern
        self.view()
        
    """
    write out experimental parameters to a text file
    """
    def statusfile(self, filename):
        print("statusfile is not yet implemented")
        
    """
    Shortcut for writer. Assumes that filepattern is set
    """
    def set_name_pattern(self):
        "append timestamp and id to name_stem and set name_pattern"
        now = time.strftime("_%Y-%m-%d_%H%M%S")
        name_pattern = self.name_stem+"_ID-$id"+now
        self.detector.set_config("name_pattern", name_pattern, "filewriter")
            
            
if __name__ == '__main__':
    # univie = Singla(SIP, SPORT, SVERS)
    print ("error: SinglaCmdline should be importet and not run directly\n")
    exit(1)
