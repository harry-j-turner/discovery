# Installation

### Environment
I have tested this installation on Ubuntu 22.04. These instructions are written for that distro.
You will need:
 - python3.10
 - NodeJS (I tested with 18.17)
 - NPM (I tested with 9.6.7).

### Minecraft

You will need to purchase the game in order to run this project. Download Minecraft for the Debian distribution from [minecraft.net](https://www.minecraft.net/en-us/download). Locate the downloaded `.deb` file, right click and choose `Open with other application` then choose `Software Install` and follow the instructions. 

Now visit [Fabric Mod](https://fabricmc.net/use/installer/) and download the `.jar` file. Locate the `.jar` file and run `java -jar <your file>.jar` to install it. When prompted, choose Minecaft version 1.19. Next download the [Fabric API](https://modrinth.com/mod/fabric-api/version/0.58.0+1.19) mod, place the downloaded `.jar` file into `~/.minecraft/mods` or wherever else you installed it. 

Launch Minecraft. The first time can take a while as it downloads the files it needs. When prompted, login with your Microsoft account. Once the launcher opens, ensure you have selected Fabric Loader 1.19 in the bottom left, click Play. Once it's started, choose `Singleplayer`, then `Create New World`, choose `Game Mode: Creative` set the difficulty to `Peaceful` and allow cheats. Once the world is created you will be dropped into the game. Press escape to open the menu, choose `Open to LAN`, set the game mode to `Creative`, enable cheats, and click `Start LAN`. Make a note of the port number displayed on screen.


### Agent

From within the `agent` directory, run `npm install`. Then run `node agent.js <port>` where the port is the local minecraft server you noted down earlier. This should start the agent and a bot should appear in the minecraft world near your initial spawn location.

### Controller

In a separate terminal, from within the `controller` directory, run `python3.10 -m venv venv` to create a virtual environment and then run `source venv/bin/activate` to activate it. Run `python3.10 -m pip install -r requirements.txt` to install the dependencies, then run `python3.10 main.py` to start the controller. 
