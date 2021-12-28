# IJFtoOBS
Application API to connect IJF Judo scoreboard UDP stream to OBS server websockets

![alt text](https://github.com/roly197/IJFtoOBS/blob/main/images/IJF2OBS.jpg)

## IJF2OBS installation
The IJF2 OBS interface is build in Python for easy readability and support. Firt thing to to is download and install the Python interpreter:

### Python Windows installation 
In your preferred webbrowser navigate to the Python download link: https://www.python.org/downloads/ and download-and-run the latest Python version installer (version 3.10.1 at the time of writing).
Select:
- 'Install launcher for all users (recommended')'  and,
- 'Add Python 3.10 to PATH' 
Accept all defaults in the installation wizard and finish the installation.
To check a succesful installation: 
- open a commad terminal by typing 'cmd' in the Windows search bar
- In the command terminal type '**python --version**' 
- This will output somthing like: 'Python 3.10.x' 

### Install the SimpleOBSWS Python Libraries
The IJF2OBS software uses the non stanbdard library: simpleobsws. Can be found here: https://github.com/IRLToolkit/simpleobsws
To install this library: 
- In the command windows (open a commad terminal by typing 'cmd' in the Windows search bar) type: **pip install simpleobsws**
- This should return: 'Successfully installed simpleobsws.0.0.x websocket-10.1' (versions can differ).

## IJF2OBS interface installation
Now that Python is set up you can download/install the IJF2OBS interface software:
- With your preferred browser goto: https://github.com/roly197/IJFtoOBS 
- Now select the **Code** button and in the dropdown select **Download Zip** 
- The software downloads to your download folder. Navigate to that folder and unzip all files to your local filesystem (e.g. C:\Program Files)
- If you want to use te coutry flag, you can also unzip the 'flags.zip' to a directory on your harddrive. Te path to this directory needs to be configured in the **ijfSBtoOBS.py** file.

###Confuguration
To configure the IJF2OBS software, select your favourite editor (can be Notepad) open the **ijfSBtoOBS.py* file in the installation directory and make the appropriate changes t the variables in the '''Setup variables''' section at the top of te file. 

###Starting the IJF2OBS software
To start the IJF2OBS inerface software simply click the **ijfSBtoOBS.py** file in the installation dorectory. 
Only one instance of the interface can run on a single machine. 

### OBS Windows installation
If not installed already; Install the latest version of OBS server (version 27.1.3 at the time of writing) from here: https://obsproject.com/
The Windows installation link will download the OBS Server installation package. Follow the defauly installation instructions to install on your local machine.

#### Example Scene Collection
In the folder OBS_Sources you will find example scoreboard Scene and source. 
- Open OBS server, navigate to : '**Scene Collection**' -> '**Import**' 
- In the newly opened window select the '**Collection Path**' '**...**'  field, navigate to the file '**..\OBS_Sources\OPS_IJF_ScoreBoard.json**' 
- now Click Import. The scoreboard overlay will load.

### OBS websocket plugin
OBS websocket plugin for OBS server allows remote control of your OBS instance over the network. 
The websocket plugin is used to push the IJF scoreboard dat to the OBS server video stream to overlay the video stream.

Current latest stable version of the obs-websocket plugin (version 4.9.1 at the time of writing) can be found here: https://github.com/obsproject/obs-websocket/releases/tag/4.9.1
### OBS Websocket Windows installation:
Download the '..Windows-installer.exe' or '..Windows.zip' file from the Asset section at the bottom of the Github page. Then:
- Using the installer (recommended, works only with combined 32/64-bit installations) : download it, launch it and follow the instructions.
- Using the obs-websocket-4.9.1-Windows.zip archive : copy the contents of the archive to the root of your OBS Studio installation folder (either C:\Program Files\obs-studio or C:\Program Files (x86)\obs-studio).

#### Configure the plugin
To configure the Websocket plugin:
- Open OBS Server
- Navigate to the new menu item: '**Tools**' -> '**WebSocket Server Settings**'
- Enable Websockets server and configure the server port to **4444** (default)
- Enable Authentication and configure the Password: **judo** (default)
Other passwords and/or ports need to be configured in the **ijfSBtoOBS.py** file

Click 'Ok'.... done 
