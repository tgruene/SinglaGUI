#!/usr/bin/env python3
import argparse

import h5py
import numpy as np

from dectris2xds.fit2d import fitgaussian


class XDSparams:
    """
Stores parameters for XDS and creates the template XDS.INP in the current directory
"""

    def __init__(self, xdstempl):
        self.xdstempl = xdstempl

    def update(self, orgx, orgy, templ, d_range, osc_range, dist):
        """
           replace parameters for ORGX/ORGY, TEMPLATE, OSCILLATION_RANGE,
           DATA_RANGE, SPOT_RANGE, BACKGROUND_RANGE, STARTING_ANGLE(?)
        """
        self.xdsinp = []
        with open(self.xdstempl, 'r') as f:
            for line in f:
                [keyw, rem] = self.uncomment(line)
                if "ORGX=" in keyw or "ORGY=" in keyw:
                    self.xdsinp.append(f" ORGX= {orgx:.1f} ORGY= {orgy:.1f}\n")
                    continue
                if "ROTATION_AXIS" in keyw:
                    axis = np.fromstring(keyw.split("=")[1].strip(), sep=" ")
                    axis = np.sign(osc_range) * axis
                    keyw = self.replace(keyw, "ROTATION_AXIS=", np.array2string(axis, separator=" ")[1:-1])
                keyw = self.replace(keyw, "OSCILLATION_RANGE=", abs(osc_range))
                keyw = self.replace(keyw, "DETECTOR_DISTANCE=", dist)
                keyw = self.replace(keyw, "NAME_TEMPLATE_OF_DATA_FRAMES=", templ)
                keyw = self.replace(keyw, "DATA_RANGE=", f"1 {d_range}")
                keyw = self.replace(keyw, "SPOT_RANGE=", f"1 {d_range}")
                keyw = self.replace(keyw, "BACKGROUND_RANGE=", f"1 {d_range}")

                self.xdsinp.append(keyw + ' ' + rem)

    def xdswrite(self, filepath="XDS.INP"):
        "write lines of keywords to XDS.INP in local directory"
        with open(filepath, 'w') as f:
            for l in self.xdsinp:
                f.write(l)

    def uncomment(self, line):
        "returns keyword part and comment part in line"
        if ("!" in line):
            idx = line.index("!")
            keyw = line[:idx]
            rem = line[idx:]
        else:
            keyw = line
            rem = ""
        return [keyw, rem]

    def replace(self, line, keyw, val):
        """
        checks whether keyw is present in line (including '=') and replaces the value
        with val
        """
        if (keyw in line):
            line = ' ' + keyw + ' ' + str(val)
        else:
            line = line
        return line


def getslope(fn):
    """
    extract slope from log file provided as fn
    """
    print(f" ! Opening file {fn}")
    with open(fn, encoding="utf-8") as log:
        line = log.readline()
        while line.find("=======================") == -1:
            line = log.readline()
            # print (line)
            continue
        slope = log.readline()
        log.close()
    x = slope.split()
    slope = x[2]
    print(f" ! slope: {slope}")
    return float(slope)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HDF5 info extractor for XDS parameters")
    parser.add_argument("-m", "--masterfile", help="hdf5 master file")
    parser.add_argument("-s", "--stagelog", help="phi angle log file for oscillation width", default="null")
    parser.add_argument("-t", "--xdstemplate", help="Template for XDS.INP",
                        default="/xtal/Integration/XDS/CCSA-templates/XDS-SINGLA.INP")
    parser.add_argument("-D", "--distance", help="effective detector distance",
                        default=860)

    args = parser.parse_args()
    if (args.stagelog == "null"):
        print("No stage log given, assuming 1 deg/s")
        slope = 1.0
    else:
        slope = getslope(args.stagelog)

    f = h5py.File(args.masterfile, "r")
    templ = args.masterfile.replace("master", "??????")
    frame_time = f['entry']['instrument']['detector']['frame_time'][()]
    oscw = frame_time * slope
    print(f" OSCILLATION_RANGE= {oscw} ! frame time {frame_time}")

    print(f" NAME_TEMPLATE_OF_DATA_FRAMES= {templ}")

    for dset in f["entry"]["data"]:
        nimages_dset = f["entry"]["data"][dset].shape[0]
        print(f" DATA_RANGE= 1 {nimages_dset}")
        print(f" BACKGROUND_RANGE= 1 {nimages_dset}")
        print(f" SPOT_RANGE= 1 {nimages_dset}")
        h = f["entry"]["data"][dset].shape[2]
        w = f["entry"]["data"][dset].shape[1]
        for i in range(1):
            image = f["entry"]["data"][dset][i]
            print(f"   !Image dimensions: {image.shape}, 1st value: {image[0]}")
            d = image
            d[d == 2 ** 32 - 1] = 0

            m = np.amax(d)
            idx = np.where(d == m)
            xmax = idx[0][0]
            ymax = idx[1][0]
            print(f"   ! unfitted maximum {m} at {xmax}, {ymax}")

            k = 10
            peak = d[xmax - k:xmax + k, ymax - k:ymax + k]

            p,success = fitgaussian(data=peak)
            orgx = ymax - k + p[2]
            orgy = xmax - k + p[1]
            print(f"   !Maximum value {p[0]:.2e} at {p[1]:5.1f}/{p[2]:5.1f} +/- {p[3]:5.1f}/{p[4]:5.1f}")
            print(f" ORGX= {orgx:5.1f} ORGY= {orgy:5.1f}")
            print(f"   !Ellipse Angle = {180. / np.pi * p[5]:5.1f}")
        break

    myxds = XDSparams(xdstempl=args.xdstemplate)
    myxds.update(orgx, orgy, templ, nimages_dset, oscw, args.distance)
    myxds.xdswrite()
