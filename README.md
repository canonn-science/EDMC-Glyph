# EDMC-Glyph
EDMC Plugin to capture thargoid glyph data

# Usage

The Glyph scanner will remain dormant until you use the xeno scanner to scan a Thargoid interceptor and the Thargoid Glyph appears on your hud.

![Glyph User Interface](docimages/glyphui.png)

Left clicking on the displyed glyph will cycle through the inner symbols. The thargoid image next to it will switch to an the known type for the selected inner glyph.

Right clicking on the displayed glyph will cycle through the outer symbols. 

One you have matched the Glyph displayed on your hud, you can override the Interceptor type by clicking on its image.

Once you have made your selection you can click the submit button and it will send the following information to a speadheet.

* Commander Name
* System Name
* x,y,z coordinates
* id64 
* The Interceptor Type
* The glyph identification code.



The captured data can be found at [Thargoid Glyph Sheet](https://canonn.fyi/glyphsheet)

## How to install. 
First you must install [Elite Dangerous Market Connector](https://github.com/Marginal/EDMarketConnector/blob/master/README.md)

Load the application and go to the plugins tab of the settings screen. This will show you where you will need to install the EDMC-Glyph plugin. 

![EDMC Settings Plugins Tab](https://i.imgur.com/3yxKUnO.png)

Download the Source Code zip file for [the latest release](https://github.com/canonn-science/EDMC-Glyph/releases/latest) and extract the folder into the plugins directory. (this can be found under *Assets* near the bottom of the release page.

Restart EDMC
