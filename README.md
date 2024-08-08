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
![First steps](https://media.discordapp.net/attachments/1262719342500384861/1263953249317158925/chrome_kLpriNSOYs.gif?ex=66b679b1&is=66b52831&hm=f456a3875fa5972e982c7f929a3690bcfea5d6d015749c793a8f0a23707686c9&=&width=1167&height=559)

`Add something:`   
To add something, you need to click a button and fill out the modal window  
![Add something](https://media.discordapp.net/attachments/1262719342500384861/1263953248507658240/chrome_c3lv00QRtE.gif?ex=66afe231&is=66ae90b1&hm=4ff1a57ee2138669c48f105eea84a91d68177faf44e04206243e9c7dc5f4ce81&=&width=718&height=344)

`Delete something:`  
To delete something, you need to click a button  
![Delete something](https://media.discordapp.net/attachments/1262719342500384861/1263953248927092869/chrome_dD06gFqCWc.gif?ex=66afe231&is=66ae90b1&hm=fa28ec8d4aab4bfa8430b1101d88d620301a81d4e7cd821aabca1ff4d80c32d2&=&width=718&height=344)

`Send embed:`  
To send embed, you need to click button and choose method for send.  

If you choose “Send this channel”, embed will be sent in this channel.  
![Send this channel](https://media.discordapp.net/attachments/1262719342500384861/1263953248038158436/chrome_6f1YRGIFE2.gif?ex=66afe231&is=66ae90b1&hm=0ab4d41fd49d13ed5ed13587fd32c5150a70d9f46201939c725169a530ca1c9c&=&width=718&height=344)

If you choose “Use webhook” you will need to past webhook URL.  
![Use webhook](https://media.discordapp.net/attachments/1262719342500384861/1263953249766215680/chrome_VydugmPsMQ.gif?ex=66afe231&is=66ae90b1&hm=fd4a5cd15e52f3578d239e2f1d7e61c50720f29ecd356030093874a075af835a&=&width=718&height=344)

`Input errors:`  
You don’t have to worry about data entry errors, because if they are not true, _**EmbedGenerator**_ will warn you!  
![Input errors](https://media.discordapp.net/attachments/1262719342500384861/1263953250407940096/chrome_Y6D5l3lD51.gif?ex=66afe232&is=66ae90b2&hm=38af9ffd82f120212c9d2229e1e080198e773e76fceae73dfb46833e3c05c002&=&width=718&height=344)


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




