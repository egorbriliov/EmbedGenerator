# EmbedGenerator
EmbedGenerator is a free, open-source, extensible bot for Discord servers, built on top of <a href="https://github.com/DisnakeDev/disnake">disnake.py</a>. This bot is generally self-hosted either on a dedicated server (like a Raspberry Pi) or general cloud hosting like AWS etc. You can think of this bot as privacy focused, as you are in total control of the code, so you can be sure that your information is secure.

## Features:
This bot has been in development since 2024 and has only two command:

### General Commands

- `/help` -> Examples of bot usage.
- `/embed` -> Returns a view modal to setting and send embed

### Usage examples

`First steps:`  
To get started, you need to use /embedTo get started, you need to use /embed  
![First steps](https://media.discordapp.net/attachments/1262719342500384861/1263953249317158925/chrome_kLpriNSOYs.gif?ex=66ad3f31&is=66abedb1&hm=d4e5e9256017e255bb2bea5e543af4f2c715f010f6c012e66d1c3d0b09cdadaf&=&width=1004&height=480)

`Add something:`   
To add something, you need to click a button and fill out the modal window  
![Add something](https://media.discordapp.net/attachments/1262719342500384861/1263953248507658240/chrome_c3lv00QRtE.gif?ex=66ad3f31&is=66abedb1&hm=bf9101fc56fe09c40d0c0c8295562b7208d4feacc6d36495273c39f4f3f7462c&=&width=1004&height=480)

`Delete something:`  
To delete something, you need to click a button  
![Delete something](https://media.discordapp.net/attachments/1262719342500384861/1263953248927092869/chrome_dD06gFqCWc.gif?ex=66ad3f31&is=66abedb1&hm=fcf5bb604012f717e95c057f42709cd08ba100b1063524201680ef7ea90c85fc&=&width=1004&height=480)

`Send embed:`  
To send embed, you need to click button and choose method for send.  

If you choose “Send this channel”, embed will be sent in this channel.  
![Send this channel](https://media.discordapp.net/attachments/1262719342500384861/1263953248038158436/chrome_6f1YRGIFE2.gif?ex=66ad3f31&is=66abedb1&hm=95b791d943c14bc19b2715b30bcca5549064d1bdad3e7e36d6863ae501b79845&=&width=1004&height=480)

If you choose “Use webhook” you will need to past webhook URL.  
![Use webhook](https://media.discordapp.net/attachments/1262719342500384861/1263953249766215680/chrome_VydugmPsMQ.gif?ex=66afe231&is=66ae90b1&hm=fd4a5cd15e52f3578d239e2f1d7e61c50720f29ecd356030093874a075af835a&=&width=440&height=210)

`Input errors:`  
You don’t have to worry about data entry errors, because if they are not true, _**EmbedGenerator**_ will warn you!  
![Input errors](https://media.discordapp.net/attachments/1262719342500384861/1263953250407940096/chrome_Y6D5l3lD51.gif?ex=66ad3f32&is=66abedb2&hm=ced0429e04c2037bc2644d017a3771c64c2ec78cacb6392c25b5ed21f40e0953&=&width=1004&height=480)


## Installation

This bot runs on [Python](https://www.python.org/). You will need at least python 3.10.

### Windows

1. Install [Python](https://www.python.org/)
2. Activate venv in console `python -m venv venv`
3. Install all needed packages `pip install -r requirements.txt`. You can also delete `requirements.txt` after.
4. Configurate `.env` (Add your token).
5. Run `python main.py` to start bot.

### Running longterm
Once you've setup your keys and checked that the features you want are working, you have a couple of options for running the bot.

### Selfhosted
You could run the bot along side everything else on your pc. However it's probably a good idea to run your bot on a separate computer such as a linux server or a Raspberry Pi so it does not interfere with your normal operations and to keep it running even if you were to sleep or shutdown your PC. 

### Cloud Hosted
There is a number of cloud hosting providers that can run small Python applications like this. The following have been tested to work, you'll have to extrapolate if you want to use some other provider (AWS, etc)

### Running on Heroku
- Create heroku account, install heroku-cli, create a new Dyno.
- Git clone the repo and follow the instructions in the Deploy section to setup pushing to heroku
- Go to settings and setup Config Vars the name of the vars are exactly the same as the auth.json file. You **DO NOT** need the quotes around the values in config vars
- Run `heroku scale worker=1` in the bot installation directory to run the bot as a worker rather than a webserver.




