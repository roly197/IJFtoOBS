# IJF2OBS
Application API to connect IJF Judo scoreboard UDP stream to OBS server websockets.

## Release notes
new in release 1.1.0:
- Dynamic support for multiple mats 0..9 configured in IJF scoreboard configuration. Trailing identifier for the OBS objects has changed from SB_... to SB#.. where # is the configured mat number. Now listening to broadcast traffic from all IJF scoreboards.
- Team score is now supported. Team score is passed in the 'GDI+ Text' object: SB#_TeamScoreW and SB#_TeamScoreB
- Flags directory is now automatically configured to the python execution directory. Just unzip the 'flags.zip' to a sub-folder in the install directory. 

## Index
- [IJF2OBS installation](#IJF2OBS-installation)
  * [Python Windows installation](#Python-Windows-installation)
    + [Install the SimpleOBSWS Python Libraries](#Install-the-SimpleOBSWS-Python-Libraries)
  * [IJF2OBS interface installation](#IJF2OBS-interface-installation)
    + [Confuguration](#Confuguration)
  * [Starting the IJF2OBS software](#Starting-the-IJF2OBS-software)
  * [Stopping the IJF2OBS software](#Stopping-the-IJF2OBS-software)
- [OBS Windows installation](#OBS-Windows-installation)
  * [Example Scene Collection](#Example-Scene-Collection)
  * [OBS websocket plugin](#OBS-websocket-plugin)
  * [OBS Websocket Windows installation](#OBS-Websocket-Windows-installation)
    + [Configure the plugin](#Configure-the-plugin)

## Overview image
![alt text](https://github.com/roly197/IJFtoOBS/blob/main/images/IJF2OBS1.0.x.jpg)

NOTE: All network computers have to be in the same IP range and switch network. IJF Scoreboard uses UDP broadcast to publish match data. 

## IJF2OBS installation
The IJF2 OBS interface is build in Python for easy readability and support. First thing to to is download and install the Python interpreter:

### Python Windows installation 
In your preferred webbrowser navigate to the Python download link: https://www.python.org/downloads/ and download-and-run the latest Python version installer (version 3.10.1 at the time of writing).
Select:
- 'Install launcher for all users (recommended')'  and,
- During the installation enablele:'Add Python 3.10 to PATH'
Accept all defaults in the installation wizard and finish the installation.
To check a succesful installation: 
- open a commad terminal by typing 'cmd' in the Windows search bar
- In the command terminal type '**python --version**' 
- This will output somthing like: 'Python 3.10.x' 

### Install IJF2OBS dependencies
The IJF2OBS has a dependency on the following external modules:
- simpleobsws
- websockets

Install these modules by opening a 'CMD prompt' and type: 
```
pip install simpleobsws
```

### IJF2OBS interface installation
Now that Python is set up you can download/install the IJF2OBS interface software:
- With your preferred browser goto: https://github.com/roly197/IJFtoOBS 
- Now select the **Code** button and in the dropdown select **Download Zip** 
- The software downloads to your download folder. Navigate to that folder and unzip all files to your local filesystem (e.g. C:\Program Files)
- If you want to use te country flag, you can also unzip the 'flags.zip' to a directory on the 'flags' sub-folder of the install directory.

#### Configuration
From version 1.0.4 configuration changes should not be nessecary. Only edit when you know what you are doing.
To configure the IJF2OBS software, select your favourite editor (can be Notepad) open the **ijf2obs(version).py* file in the installation directory. 

```
'''---------------------------------Setup variables-------------------------'''
udpPort = 5000                                                     #UDP listening port for IJF SB to connect to
udpIp = ""                                                         #UDP IP for IJF SB to connect to. Keep empty to listen to te bradcast address,

wsPort = '4444'                                                    #Websocket port to connect to OBS Server
wsHost = '127.0.0.1'                                               #Websocket IP to connect to OBS Server
wsPass = 'judo'                                                    #Password to connect to OBS Server

defaultCountry = 'NED'                                             #Send default 3 digit country code when empty
#flagsDirectory = '/Users/user/Projects/IJFtoOBS/flags/'           #Local Directory where all country flags are unzipped
flagsDirectory = os.getcwd()+'\\flags\\'                           #Automatically find the flags directory as a subdir to the executable location. Do not change!
'''--------------------------------------------------------------------------'''
```

### Starting the IJF2OBS software
To start the IJF2OBS inerface software simply click the **ijf2obs(version).py** file in the installation directory. Leave the terminal session running in the background.
Only one instance of the interface can run on a single machine. 

** After startup the following OBS sources can be used: ** 
Also have a look and import the example source collection in the OBS_Sources directory. All sources are available in this example.

|Source Name # = 0..9|OBS Source Type|Setting|Value <<"example">>|Category|Description|
|:---|:---|:---|:---|:---|:---|
|SB#_GoldenScore|Text (GDI+)| render| True/False|Generic|Group is visible if Golden Score is active|
|SB#_MatchStarted|Group| render| True/False|Generic|Group is visible if IJF scorebooard is active (not in setup mode)|
|SB#_EventName|Text (GDI+)| text| <<scoreboard_testevent>>|Generic|Text that displayes IJF event name|
|SB#_Gender|Text (GDI+)| text| <<Men's/Woman's>>|Generic|Text will discplay "Men's" or " Woman's"|
|SB#_Category|Text (GDI+)| text| <<-73..>> kg|Generic|Text will display the weight class + "kg"
|SB#_MatchType|Text (GDI+)| text| <<"Quarter Final">>|Generic|Text will display match type: "Elimination..to..Final"
|SB#_Time|Text (GDI+)| text| <<0:00..9:99>>|Generic| Text will display the (remaining) match time|
|SB#_Winner|Text (GDI+)| text| <<Blue/White>>|Generic|Text will display the match winner:"Blue or White"| 
||
|SB#_FlagW|Image| sourceSettings|file: ..ned_m.jpg|White| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|SB#_IpponW|Text (GDI+)| render| True/False|White|Group is visible if Ippon is active|
|SB#_PinTimerW|Text (GDI+)| render| True/False|White|Group is visible if pin/lock timer is active|
|SB#_CountryW|Text (GDI+)| text| <<NED..>>|White|3 digit country abbreviation|
|SB#_WrlW|Text (GDI+)| text|<<0..999>>|White|Text displays World Rank of contender|
|SB#_FamilyNameW|Text (GDI+)| text|<<a*..Z*>>|White|Text displays name of contender|
|SB#_WazaAriW|Text (GDI+)| text| <<0-1>>|White|Text/number to display WazaAri point|
|SB#_PinTimeW|Text (GDI+)| text| <<00-20>>|White|Text to display the hold/lock timer|
|SB#_TeamScoreW|Text (GDI+)| text| <<0-9>>|White|Text to display the team score when in team mode|
|SB#_ShidoW1|Color Source| render| True/False|White|Visibility of Shido as OBS color Source = first yellow card|
|SB#_ShidoW2|Color Source| render| True/False|White|Visibility of 2nd Shido as OBS color Source = second yellow card|
|SB#_HansokumakeW|Color Source| render| True/False|White|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|
||
|SB#_FlagB|Image| sourceSettings|file: ..ned_m.jpg|Blue| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|SB#_IpponB|Text (GDI+)| render| True/False|Blue|Group is visible if Ippon is active|
|SB#_PinTimerB|Text (GDI+)| render| True/False|Blue|Group is visible if pin/lock timer is active|
|SB#_CountryB|Text (GDI+)| text| <<NED..>>|Blue|3 digit country abbreviation|
|SB#_WrlB|Text (GDI+)| text|<<0..999>>|Blue|Text displays World Rank of contender|
|SB#_FamilyNameB|Text (GDI+)| text|<<a*..Z*>>|Blue|Text displays name of contender|
|SB#_WazaAriB|Text (GDI+)| text| <<0-1>>|Blue|Text/number to display WazaAri point|
|SB#_PinTimeB|Text (GDI+)| text| <<00-20>>|Blue|Text to display the hold/lock timer|
|SB#_TeamScoreB|Text (GDI+)| text| <<0-9>>|Blue|Text to display the team score when in team mode|
|SB#_ShidoB1|Color Source| render| True/False|Blue|Visibility of Shido as OBS color Source = first yellow card|
|SB#_ShidoB2|Color Source| render| True/False|Blue|Visibility of 2nd Shido as OBS color Source = second yellow card|
|SB#_HansokumakeB|Color Source| render| True/False|Blue|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|


### Stopping the IJF2OBS software
In the terminal session simply type '**Ctrl-C**' and '**Enter**'

## OBS Windows installation
If not installed already; Install the latest version of OBS server (version 27.1.3 at the time of writing) from here: https://obsproject.com/
The Windows installation link will download the OBS Server installation package. Follow the defauly installation instructions to install on your local machine.

### Example Scene Collection
In the folder OBS_Sources you will find example scoreboard Scene and source. 
- Open OBS server, navigate to : '**Scene Collection**' -> '**Import**' 
- In the newly opened window select the '**Collection Path**' '**...**'  field, navigate to the file '**..\OBS_Sources\OPS_IJF_ScoreBoard....json**' 
- now Click Import. The scoreboard overlay will load.

### OBS websocket plugin
OBS websocket plugin for OBS server allows remote control of your OBS instance over the network. 
The websocket plugin is used to push the IJF scoreboard dat to the OBS server video stream to overlay the video stream.

Current latest stable version of the obs-websocket plugin (version 4.9.1 at the time of writing) can be found here: https://github.com/obsproject/obs-websocket/releases/tag/4.9.1
### OBS Websocket Windows installation
Download the '..Windows-installer.exe' or '..Windows.zip' file from the Asset section at the bottom of the Github page. Then:
- Using the installer (recommended, works only with combined 32/64-bit installations) : download it, launch it and follow the instructions.
- Using the obs-websocket-4.9.1-Windows.zip archive : copy the contents of the archive to the root of your OBS Studio installation folder (either C:\Program Files\obs-studio or C:\Program Files (x86)\obs-studio).

#### Configure the plugin
To configure the Websocket plugin:
- Open OBS Server
- Navigate to the new menu item: '**Tools**' -> '**WebSocket Server Settings**'
- Enable Websockets server and configure the server port to **4444** (default)
- Enable Authentication and configure the Password: **judo** (default)
Other passwords and/or ports need to be configured in the **ijf2obs(version).py** file

Click 'Ok'.... done 

## IJF scoreboard configuration
The IJF scoreboards need at least two configuration settings: 
- Set 'Live data on' to start broadcasting the scoreboard information to the network
- Set the 'mat number'. This number will corespond to the mat number picked up from the network and send to OBS sources with the prefix **SB#_xxxxxxxx**, where # is the mat number.

![alt text](https://github.com/roly197/IJFtoOBS/blob/main/images/IJFconfiguration.jpg)
