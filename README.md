# IJFtoOBS
Application API to connect IJF Judo scoreboard UDP stream to OBS server websockets

## OBS installation
If no tinstalled already; Install the latest version of OBS server (version 27.1.3 at the time of writing) from here: https://obsproject.com/
### Windows installation
The Windows installation link will download the OBS Server installation package. Follow the defauly installation instructions to install on your local machine.

## OBS websocket plugin
OBS websocket plugin for OBS server allows remote control of your OBS instance over the network. 
The websocket plugin is used to push the IJF scoreboard dat to the OBS server video stream to overlay the video stream.

Current latest stable version of the obs-websocket plugin (version 4.9.1 at the time of writing) can be found here: https://github.com/obsproject/obs-websocket/releases/tag/4.9.1
### Windows installation:
Download the '..Windows-installer.exe' or '..Windows.zip' filr from the Asset section at the bottom of the Github page. Then:
- Using the installer (recommended, works only with combined 32/64-bit installations) : download it, launch it and follow the instructions.
- Using the obs-websocket-4.9.1-Windows.zip archive : copy the contents of the archive to the root of your OBS Studio installation folder (either C:\Program Files\obs-studio or C:\Program Files (x86)\obs-studio).

#### Configure the plugin
<<todo>>
