|Type|Source Name|OBS Source Type|Setting|Value|Category|Description|
|:--- |:---|:---|:---|:---|:---|:---|
|sourceName| SB_FlagW|Image| sourceSettings|file: C:\\Users\\IEUser\\Documents\\IIFtoOBS\\flags\\ned_m.jpg|White| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|sourceName| SB_FlagB|Image| sourceSettings|file: C:\\Users\\IEUser\\Documents\\IIFtoOBS\\flags\\ned_m.jpg|Blue| Image source will be set to the 3 char country code substituted with directory and jpg filename|
|item| SB_GoldenScore|Group| visible| True/False|Generic|Group is visible if Golden Score is active|
|item| SB_IpponW|Group| visible| True/False|White|Group is visible if Ippon is active|
|item| SB_IpponB|Group| visible| True/False|Blue|Group is visible if Ippon is active|
|item| SB_PinTimerW|Group| visible| True/False|White|Group is visible if pin/lock timer is active|
|item| SB_PinTimerB|Group| visible| True/False|Blue|Group is visible if pin/lock timer is active|
|item| SB_MatchStarted|Group| visible| True/False|Generic|Group is visible if IJF scorebooard is active (not in setup mode)|
|source| SB_EventName|Text (GDI+)| text| scoreboard_testevent|Generic|Text that displayes IJF event name|
|source| SB_Gender|Text (GDI+)| text| "Mens"|Generic|Text will discplay "Men's" or " Woman's"|
|source| SB_Category|Text (GDI+)| text| -73 kg|Generic|Text will display the wight class + "kg"
|source| SB_MatchType|Text (GDI+)| text| Quarter Final|Generic|Text will display match type: "Elimination..to..Final"
|source| SB_Time|Text (GDI+)| text| 0:00|Generic| Text will display the (remaining) match time|
|source| SB_Winner|Text (GDI+)| text| Blue/White|Generic|Text will discplay the match winner:"Blue or White"| 
|source| SB_CountryW|Text (GDI+)| text| NED|White|3 digit country abbreviation|
|source| SB_WrlW|Text (GDI+)| text||White|Text displays World Rank of contender|
|source| SB_FamilyNameW|Text (GDI+)| text||White|Text displays name of contender|
|source| SB_WazaAriW|Text (GDI+)| text| 0|White|Text/number to display WazaAri point|
|source| SB_PinTimeW|Text (GDI+)| text| 00|White|Text to display the hold/lock timer|
|source| SB_CountryB|Text (GDI+)| text| NED|Blue|3 digit country abbreviation||
|source| SB_WrlB|Text (GDI+)| text|    |Blue|Text displays World Rank of contender|
|source| SB_FamilyNameB|Text (GDI+)| text||Blue|Text displays name of contender|
|source| SB_WazaAriB|Text (GDI+)| text| 0|Blue|Text/number to display WazaAri point|
|source| SB_PinTimeB|Text (GDI+)| text| 00|Blue|Text to display the hold/lock timer|
|item| SB_ShidoW1|Color Source| visible| True/False|White|Visibility of Shido as OBS color Source = first yellow card|
|item| SB_ShidoW2|Color Source| visible| True/False|White|Visibility of 2nd Shido as OBS color Source = second yellow card|
|item| SB_HansokumakeW|Color Source| visible| True/False|White|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|
|item| SB_ShidoB1|Color Source| visible| True/False|Blue|Visibility of Shido as OBS color Source = first yellow card|
|item| SB_ShidoB2|Color Source| visible| True/False|Blue|Visibility of 2nd Shido as OBS color Source = second yellow card|
|item| SB_HansokumakeB|Color Source| visible| True/False|Blue|Visibility of 3rd Shido or Hansokumake as OBS color Source = red card (yellow cards will hide)|
