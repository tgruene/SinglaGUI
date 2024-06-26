# Singla GUI - A graphical user interface for the SINGLA detector and TEM
## License
SINGLAGUI © 2023 by Julian Maisriml and Tim Gruene is licensed under Creative Commons Attribution 4.0 International 
Until a scientific publication becomes available, 'appropiate credit' is given with a link to
this github repository. Once a scientific publication is available, this site will be updated accordingly.
## General usage:
The current detector image is displayed in the stream window display as a grayscale image. Located next to the image is
a histogram of the intensity data. There one can also set the contrast and overall brightness by moving the yellow
strips with the mouse.
Overlayed on the stream display are several widgets: a white bar indicating the insensitive region of the detector,
yellow and green circles indicating the locations of focus for different magnification modes and the outer boundary of
the detector image in red. Also, there is a red rectangle to adjust the region of interest for fitting the beam to a
gaussian shape. It can be moved with the mouse and scaled by dragging the lower right corner.
When the TEM is in diffraction mode and the 'Fit Beam' checkbox is set, the program tries to fit a rotated and
asymmetric 2D gaussian function to the intensities within the region of interest. The parameters of this fit are
displayed below the stream window. They include the amplitude, the position of the peak (x,y) the standard deviations
(width_x, width_y) as well as their ratio and the elliptic eccentricity as well as the angle (theta). In addition, the
time for processing the fit is shown.

The GUI is intended to perform several tasks which can be started with the corresponding buttons:
- 'Record':              Rotate the stage from the current to the desired ('End Angle' input field) angle with the
                         selected rotation speed. Afterwards, a log file of the process is written to the 'work'
                         directory and the .hd5 files are downloaded from the detector and stored in the 'data'
                         directory. In addition, an INPUT.XDS file is created with the selected parameters.
- 'Still':               The detector records an image for 5 seconds and the also downloads the corresponding data but
                         does not generate an INPUT.XDS file.
- 'View':                Switch back to only displaying the stream.
- 'Stop':                Halt all movements and current recordings.
- 'TEM Command':         directly send a command to the PyJEM interface. Should be used with caution.
- 'Singla Webinterface': Open the singla webinterface in browser.
- 'Quit':                Quit the application
-  Quick moves:          Move the stage of the TEM

## Internal workings:
The Application serves as a front end for the TEM and SINGLA detector. Communication with the detector happens over the
SIMPLON REST interface via http protocol. The address and port can be specified in the config file. The detector status
is queried on a regular interval (~200ms) and commands are sent by the application.
The stream is queried over a ZeroMQ channel via port 9999.
The communication with the TEM Center happens over a TCP channel which is opened by the application on startup as a
client and accepted by the 'relay_fork.py' process which should be running on the TEM Center. The communication over
this TCP channel is bidirectional. The client sends python commands which are executed on the server-side and should
utilize the PyJEM interface. Every ~200 ms the server sends a JSON dictionary of status data such as stage position,
rotation speed or magnification mode.

## Installation:
```bash
$ pip install -r requirements.txt
```

## Configuration:
The Application can be configured with a config file called 'singlaui_confi.json' which is searched in the 'etc'
subdirectory of the application and in '~/.local' in this order. The configuration in '~/.local' can override other
entries. The configuration contains a dictionary for replacing detector distances in the INPUT.XDS file, default values
for input fields as well as port and host configurations for the network interfaces.

## Starting the GUI
```bash
$ python main.py
```
