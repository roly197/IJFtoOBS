# IJF2OBS
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

#### Install the SimpleOBSWS Python Libraries
The IJF2OBS software uses the non stanbdard Python library: simpleobsws. Can be found here: https://github.com/IRLToolkit/simpleobsws
To install this library: 
- In a command windows (open a commad terminal by typing 'cmd' in the Windows search bar) type: **pip install simpleobsws**
- This should return: 'Successfully installed simpleobsws.0.0.x websocket-10.1' (versions can differ).

### IJF2OBS interface installation
Now that Python is set up you can download/install the IJF2OBS interface software:
- With your preferred browser goto: https://github.com/roly197/IJFtoOBS 
- Now select the **Code** button and in the dropdown select **Download Zip** 
- The software downloads to your download folder. Navigate to that folder and unzip all files to your local filesystem (e.g. C:\Program Files)
- If you want to use te country flag, you can also unzip the 'flags.zip' to a directory on your harddrive. The path to this directory needs to be configured in the **ijf2obs.py** file.

###Confuguration
To configure the IJF2OBS software, select your favourite editor (can be Notepad) open the **ijf2obs.py* file in the installation directory and make the appropriate changes to the variables in the '''Setup variables''' section at the top of the file. 

```
udpPort = 5000                                                     #UDP listening port for IJF SB to connect to
udpIp = '192.168.2.3'                                              #UDP IP for IJF SB to connect to

wsPort = '4444'                                                    #Websocket port to connect to OBS Server
wsHost = '192.168.2.3'                                             #Websocket IP to connect to OBS Server
wsPass = 'judo'                                                    #Password to connect to OBS Server

defaultCountry = 'NED'                                             #Send default 3 digit country code when empty
flagsDirectory = 'C:\\Users\\IEUser\\Documents\\IIFtoOBS\\flags\\' #Local Directory where all country flags are unzipped
```

###Starting the IJF2OBS software
To start the IJF2OBS inerface software simply click the **ijf2obs.py** file in the installation dorectory. Leave the terminal session running in the background.
Only one instance of the interface can run on a single machine. 
**After startup the following OBS sources can be used: **

|Type|Source Name|OBS Source Type|Setting|Value <<"example">>|Category|Description|
|:--- |:---|:---|:---|:---|:---|:---|
|sourceName| SB_FlagW|Image| sourceSettings|file: ..ned_m.jpg|White| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|sourceName| SB_FlagB|Image| sourceSettings|file: ..ned_m.jpg|Blue| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|item| SB_GoldenScore|Group| visible| True/False|Generic|Group is visible if Golden Score is active|
|item| SB_IpponW|Group| visible| True/False|White|Group is visible if Ippon is active|
|item| SB_IpponB|Group| visible| True/False|Blue|Group is visible if Ippon is active|
|item| SB_PinTimerW|Group| visible| True/False|White|Group is visible if pin/lock timer is active|
|item| SB_PinTimerB|Group| visible| True/False|Blue|Group is visible if pin/lock timer is active|
|item| SB_MatchStarted|Group| visible| True/False|Generic|Group is visible if IJF scorebooard is active (not in setup mode)|
|source| SB_EventName|Text (GDI+)| text| <<scoreboard_testevent>>|Generic|Text that displayes IJF event name|
|source| SB_Gender|Text (GDI+)| text| <<Men's/Woman's>>|Generic|Text will discplay "Men's" or " Woman's"|
|source| SB_Category|Text (GDI+)| text| <<-73..>> kg|Generic|Text will display the wight class + "kg"
|source| SB_MatchType|Text (GDI+)| text| <<"Quarter Final">>|Generic|Text will display match type: "Elimination..to..Final"
|source| SB_Time|Text (GDI+)| text| <<0:00..9:99>>|Generic| Text will display the (remaining) match time|
|source| SB_Winner|Text (GDI+)| text| <<Blue/White>>|Generic|Text will discplay the match winner:"Blue or White"| 
|source| SB_CountryW|Text (GDI+)| text| <<NED..>>|White|3 digit country abbreviation|
|source| SB_WrlW|Text (GDI+)| text|<<0..999>>|White|Text displays World Rank of contender|
|source| SB_FamilyNameW|Text (GDI+)| text|<<a*..Z*>>|White|Text displays name of contender|
|source| SB_WazaAriW|Text (GDI+)| text| <<0-1>>|White|Text/number to display WazaAri point|
|source| SB_PinTimeW|Text (GDI+)| text| <<00-20>>|White|Text to display the hold/lock timer|
|source| SB_CountryB|Text (GDI+)| text| <<NED..>>|Blue|3 digit country abbreviation||
|source| SB_WrlB|Text (GDI+)| text|<<0..999>>|Blue|Text displays World Rank of contender|
|source| SB_FamilyNameB|Text (GDI+)| text|<<a*..Z*>>|Blue|Text displays name of contender|
|source| SB_WazaAriB|Text (GDI+)| text| <<0-1>>|Blue|Text/number to display WazaAri point|
|source| SB_PinTimeB|Text (GDI+)| text| <<00-20>>|Blue|Text to display the hold/lock timer|
|item| SB_ShidoW1|Color Source| visible| True/False|White|Visibility of Shido as OBS color Source = first yellow card|
|item| SB_ShidoW2|Color Source| visible| True/False|White|Visibility of 2nd Shido as OBS color Source = second yellow card|
|item| SB_HansokumakeW|Color Source| visible| True/False|White|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|
|item| SB_ShidoB1|Color Source| visible| True/False|Blue|Visibility of Shido as OBS color Source = first yellow card|
|item| SB_ShidoB2|Color Source| visible| True/False|Blue|Visibility of 2nd Shido as OBS color Source = second yellow card|
|item| SB_HansokumakeB|Color Source| visible| True/False|Blue|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|


###Stopping the IJF2OBS software
In the terminal session simply type '**Crtl-Z**' and '**Enter**'

## OBS Windows installation
If not installed already; Install the latest version of OBS server (version 27.1.3 at the time of writing) from here: https://obsproject.com/
The Windows installation link will download the OBS Server installation package. Follow the defauly installation instructions to install on your local machine.

### Example Scene Collection
In the folder OBS_Sources you will find example scoreboard Scene and source. 
- Open OBS server, navigate to : '**Scene Collection**' -> '**Import**' 
- In the newly opened window select the '**Collection Path**' '**...**'  field, navigate to the file '**..\OBS_Sources\OPS_IJF_ScoreBoard.json**' 
- now Click Import. The scoreboard overlay will load.

### OBS websocket plugin
OBS websocket plugin for OBS server allows remote control of your OBS instance over the network. 
The websocket plugin is used to push the IJF scoreboard dat to the OBS server video stream to overlay the video stream.

Current latest stable version of the obs-websocket plugin (version 4.9.1 at the time of writing) can be found here: https://github.com/obsproject/obs-websocket/releases/tag/4.9.1
#### OBS Websocket Windows installation:
Download the '..Windows-installer.exe' or '..Windows.zip' file from the Asset section at the bottom of the Github page. Then:
- Using the installer (recommended, works only with combined 32/64-bit installations) : download it, launch it and follow the instructions.
- Using the obs-websocket-4.9.1-Windows.zip archive : copy the contents of the archive to the root of your OBS Studio installation folder (either C:\Program Files\obs-studio or C:\Program Files (x86)\obs-studio).

#### Configure the plugin
To configure the Websocket plugin:
- Open OBS Server
- Navigate to the new menu item: '**Tools**' -> '**WebSocket Server Settings**'
- Enable Websockets server and configure the server port to **4444** (default)
- Enable Authentication and configure the Password: **judo** (default)
Other passwords and/or ports need to be configured in the **ijf2obs.py** file

Click 'Ok'.... done 
