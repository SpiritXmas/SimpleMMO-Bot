# SimpleMMO-Bot

This was a small project I made in my spare time, called SLEEP. Automatically battled, did quests, and stepped for you.
Please note though, I no longer maintain this project so it may be outdated. 

## How are captcha's handled?

I setup 3 different methods in order to handle captchas, unfortunately none are completely automatic however they all are extremely useful in their respective areas.

The first method is the most favoured and advanced one, called "discord". It takes a screenshot of a captcha and sends it to a webhook of your choosing. It then waits for your response between 1-4 and clicks accordingly. I have also added repeated captchas in case of making a mistake.

The second method is more simplistic, it plays a sound through whatever the output audio is at the time and you can configure both the amount of times the audio is played and the actual audio played.

The last method is similar to the second method, however instead of an audio notification it is a visual notification. It will flash a red screen over your current screen and you can configure both the duration of each flash and how many times it flashes. 

Note for the last two methods after you select the correct captcha it will continue to work auto farm like normal.