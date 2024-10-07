# LazyMudae

This selfbot interacts with the Mudae bot to automate certain tasks like:
- Automatically rolling a set number of times when a claim is available.
- Automatically claiming kakera and reacting to specific emojis like kakeraY, kakeraO, etc.
- Automatically sending `$tu`, `$dk`, and `$daily` commands when available.

You can configure different parameters in the code to adjust how and when the bot should perform its actions, including:
- Kakera claim thresholds.
- Which emojis the bot should react to.
- The username the bot should monitor for automatic actions.

## Features
- Automatically rolls for characters when Mudae allows you to claim.
- Automatically sends `$daily` and `$dk` commands when they are available.
- Reacts to kakera collection emojis.
- Adjustable time intervals for sending the `$tu` command.

## Requirements

- **Python** installed.
- **discord.py-self** (this specific version) installed. Newer versions of `discord.py` will not work as they do not support selfbots.
- Python IDLE, VSCode, Notepad++ - Whatever you have to edit code. 

## Installation & Setup

1. **Install Python**:
   Download and install latest Python from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install discord.py-self from their github.**:
   Open a terminal or command prompt, change to the directory of the bot and run:
   ```bash
   pip install git+https://github.com/dolfies/discord.py-self.git


## Getting Your Discord Token
-Open Discord in a browser.
-Press F12 or Ctrl+Shift+I to open Developer Tools.
-Go to the Application tab.
-Under Storage, look for Local Storage and click on https://discord.com.
-In the filter/search bar, search for token.
-Copy the value of the token field

Warning: Never share your Discord token with anyone.

## Find the Channel ID:

-Right-click on the channel where Mudae interacts (you must have Developer Mode enabled in Discord to see this option).
Click on Copy Channel ID.

## Configuration
You can configure the following variables in the bot.py script:

token: Your Discord token.
1. CHANNEL_ID: The ID of the Discord channel where Mudae interacts.
2. desiredKakera: The threshold for automatically claiming kakera with heart-related emojis.
3. always_click_emojis: The list of kakera emojis the bot will always click.
4. claim_emojis: A list of emojis the bot will monitor for claiming characters (can be customized for specific server setups).
5. tu_interval: The time interval for sending the $tu command, default is 2 hours.
