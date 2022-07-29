# SimpleMMO-Bot

This was a small project I made in my spare time, called SLEEP. Automatically battled, did quests, waved to users, and stepped for you.
Please note though, I no longer maintain this project so it may be outdated. 

## How are captcha's handled?

I setup 3 different methods in order to handle captchas, unfortunately none are completely automatic however they all are extremely useful in their respective areas.

The first method is the most favoured and advanced one, called "discord". It takes a screenshot of a captcha and sends it to a webhook of your choosing. It then waits for your response between 1-4 and clicks accordingly. I have also added repeated captchas in case of making a mistake.

The second method is more simplistic, it plays a sound through whatever the output audio is at the time and you can configure both the amount of times the audio is played and the actual audio played.

The last method is similar to the second method, however instead of an audio notification it is a visual notification. It will flash a red screen over your current screen and you can configure both the duration of each flash and how many times it flashes. 

Note for the last two methods after you select the correct captcha it will continue to work auto farm like normal.

## What is remote control?

I implemented remote control for fun and to make SLEEP look even more legit, essentially with remote control it allows you to enable or disable the auto farm away from your pc. In the next sub heading Ill explain how I setup communication between client-server and why you should remake it.

## How to setup client-server communication for remote control and discord captcha handling?

The approach I took to create the above is extremely inefficient, I used a web server that had a php file that allowed a request to go through to set a variable to either true/false and another url that received the state of that variable. Now this isn't the best way to achieve communication because there are far more effective ways such as using your pc's file system instead. However if you want to replicate my method Ill leave the code to the php files and the url's in the code.

## How does auto quest setting work?

The settings for the auto quest folder look something like the following

[auto_quest]=true
[quest_name]=Read_a_cursed_book

Essentially put the name of the quest in the quest name section, however instead of spaces use underscores. Also be sure to only choose a quest that you can actually complete.

## Where to download the chrome driver?

https://chromedriver.chromium.org/downloads

## Final notes

Please do not expect this to work out of the box, I've left out the code for the discord bot and you still need to change the source code to your configuration. This is meant for other developers that would like to create their own bots for this game.
