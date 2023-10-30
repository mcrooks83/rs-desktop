# install

python version:  Python 3.7.13 - python --version
git clone https://github.com/mcrooks83/rs-desktop.git
pip3 install -r requirements.txt
python gui.py

## 

The Right Step desktop application is a python based software solution that allows users to connect to a “Movella Dot' (Dot) and observe the orientation, 3D acceleration and a projected xy coordinate view of the  yaw and pitch angles. 

The application is developed using the Tkinter UI framework and pure python making it deployable on both macOS and Windows.

### Sensors Class

The Sensors class is a local class that creates a SensorManager (from the sdk) and allows the UI to access the various functionality provided by the sensor_sdk. 

The SensorManager requires explicit callbacks to be implemented which are then hooked up to the Sensors Classes own callback functions.  These are set by calling UI components (primarily PlotFrame.py) in order to update the appropriate UI components.   This is somewhat problematic and can get complicated. 

### Config Class

The config class is simply a place that holds parameters that are used by the application.

### gui.py

This is the main entry point to the application.  It creates an instance of Config and Sensors along with the applications UI.  The UI is an instance of AppCanvas which consists of the left side and the main canvas (plot frame).   The Sensors and Config classes are passed into this app canvas and subsequently to any UI components that may need them.

### Sensor SDK

Note: this is the first iteration of a sensor sdk and a newer version can be found https://github.com/mcrooks83/RS-Sensor-SDK (this would require revisiting Sensors class)

This implementation is limited by the constants.py file

The sensor_sdk is an event driven implementation that on creation creates its own event loop.  This event loop listens for messages that it can action.

## 

see ideas.txt for ways to improve. 