"""
- todo list:

Hard reset use external file

fix shutting down from client, make it log in respective areas

work out how to handle bad lag and so on maybe divert everything to a webdriverwait
or add a sleep then webdriverwait idk try doing some testing with bad lag or ping
check to allow bot to run or not

implement proper leave of the mining spot where we cant mine (go back) and the quests (after we finish performing quest)
make it so if the mouse is already hovering over next button dont need 3 curve trips instead just click
sometimes go to the button before it loads sometimes after
implement breaks
make time farmed stop when u pause or have a break
notify when break starts and ends
make breaks a random range in settings like 15-25 range
"""

import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("[ SLEEP ] Beta Build v(0.01)")

import os
import json
import bezier
import tkinter
import requests
import keyboard
import pyautogui
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
from time import time as tick
from datetime import datetime
from playsound import playsound
from threading import Thread
from random import randint
from random import uniform as randfloat
from discord_webhook import DiscordWebhook

def cls():
    os.system("cls")

sleep_logo = """
                  ██████  ██▓    ▓█████ ▓█████  ██▓███  
                ▒██    ▒ ▓██▒    ▓█   ▀ ▓█   ▀ ▓██░  ██▒
                ░ ▓██▄   ▒██░    ▒███   ▒███   ▓██░ ██▓▒
                  ▒   ██▒▒██░    ▒▓█  ▄ ▒▓█  ▄ ▒██▄█▓▒ ▒
                ▒██████▒▒░██████▒░▒████▒░▒████▒▒██▒ ░  ░
                ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░░ ▒░ ░░░ ▒░ ░▒▓▒░ ░  ░
                ░ ░▒  ░ ░░ ░ ▒  ░ ░ ░  ░ ░ ░  ░░▒ ░     
                ░  ░  ░    ░ ░      ░      ░   ░░       
                      ░      ░  ░   ░  ░   ░  ░
"""

format_1 = []
for line in open("settings.txt", "r").readlines():
  stripped_line = line.strip()
  if stripped_line != "":
    format_1.append(stripped_line)

settings = {}
for item in format_1:
  settings[item.split("[")[1].split("]")[0]] = item.split("[")[1].split("]")[1].strip("=")

print(sleep_logo,"[ SLEEP ] Settings.\n")
for value, index in settings.items():
    print("\t",value,"=",index)

if not input("\n [ SLEEP ] Press enter if settings are correct or close the program. ") == "":
    exit()

cls()

# log func
should_log = settings["discord_logging"] == "true"
logging_url = settings["discord_logging_webhook"]
commands_url = settings["commands_webhook"]
def log(msg, iscom=False):
    if iscom:
        try:
            webhook = DiscordWebhook(url=commands_url, content=msg)
            webhook.execute()
        except:
            pass
    else:
        try:
            webhook = DiscordWebhook(url=logging_url, content=msg+" "+datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
            webhook.execute()
        except:
            pass

# human verif func

human_verifs = 0
last_human_verif = 0

def temp_mouse_move(location, size):
    x, relY = location["x"], location["y"]
    absY = relY + driver.execute_script('return window.outerHeight - window.innerHeight;')
    w, h = size["width"], size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = x+randfloat((w/4), wCenter+(w/4)), absY+randfloat((h/2), (hCenter)+(h/4))

    x2 = (start[0] + end[0])/2 
    y2 = (start[1] + end[1]) / 2

    control1X = (start[0] + x2)/2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    control1 = control1X, y2 
    control2 = control2X, y2

    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])

    degree = 3
    curve = bezier.Curve(points, degree)
    
    delay = 0.003
    curve_steps = max(int(abs(end[0]/start[0])), int(abs(end[1]/start[1])))
    
    if curve_steps < 2:
        curve_steps += randint(1,2)
        delay = 0.02
    elif curve_steps < 70 and curve_steps >= 30:
        delay = 0.002
        curve_steps -= 15
    elif curve_steps >= 70:
        curve_steps -= 30
        delay = 0.002

    for j in range(1, curve_steps + 1):
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)
        pyautogui.sleep(delay)

    pyautogui.click(clicks=1)

def take_ss_and_send():
    myScreenshot = pyautogui.screenshot(region=(450,150, 1280, 350))
    myScreenshot.save(r'your_path_here\Desktop\simple mmo\captcha.png')

    webhook = DiscordWebhook(url=settings["discord_webhook"], content="<@382634269618470923> | "+datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))

    with open(r"your_path_here\Desktop\simple mmo\captcha.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='captcha.png')

    webhook.execute()

def killtabs():
    amount_of_tabs = len(driver.window_handles)
    for i in range(amount_of_tabs):
        current_tab_numb = amount_of_tabs-(i+1)
        if current_tab_numb != 0:
            driver.switch_to.window(driver.window_handles[current_tab_numb])
            driver.close()
    driver.switch_to.window(driver.window_handles[0])

def open_and_switch(link):
    driver.execute_script("window.open('{}','_blank')".format(link))
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

def human_verif():
    global last_human_verif, human_verifs
    
    if ((tick()-last_human_verif)/60) < 6:
        return
    
    global human_verifs
    
    human_verification = False
    human_verif_detection = None
    
    try:
        human_verif_detection = driver.find_element(By.XPATH, "//*[contains(text(),'We just need to make sure that you are a human.')]")
        if human_verif_detection:
            human_verification = True
    except:
        pass

    try:
        human_verif_detection = driver.find_element(By.XPATH, "//*[contains(text(),'Please complete the human verification.')]")
        if human_verif_detection:
            human_verification = True
    except:
        pass

    try:
        human_verif_detection = driver.find_element(By.XPATH, "//*[text()='Press here to verify']")
        if human_verif_detection:
            human_verification = True
    except:
        pass

    if human_verification:
        log("**!!** Human verification started **!!**")
        human_verifs += 1
        if settings["human_verification_mode"] == "sound":
            for i in range(int(settings["amount_of_times_to_play"])):
                try: playsound(settings["sound_file_name"])
                except Exception as e: print(" [ SLEEP ] Error occured whilst playing sound:", e)
            input("\n [ SLEEP ] Human verification detected! Press enter once verified. ")
            last_human_verif = tick()
            print()
        elif settings["human_verification_mode"] == "screen_flash":
            for i in range(int(settings["flash_amount_of_times"])):
                root = tkinter.Tk()
                root.configure(bg='red')
                root.overrideredirect(True)
                root.state('zoomed')
                root.attributes("-topmost", True)
                root.after(int(settings["flash_duration"].strip("s"))*1000, root.destroy)
                root.mainloop()
            input("\n [ SLEEP ] Human verification detected! Press enter once verified. ")
            last_human_verif = tick()
            print()
        elif settings["human_verification_mode"] == "discord":
            completed = False
            temp_mouse_move(human_verif_detection.location, human_verif_detection.size)
                
            while not completed: 
                sleep(randint(2,3))
                
                take_ss_and_send()

                received_input, final_response = False, "0"

                while not received_input:
                    response = None
                    try: response = str(requests.get("your_url_here/simplemmo/captcha.php?task=captcha&state=receive").text)
                    except: pass
                        
                    if response != "0" and response != "refresh":
                        final_response = response
                        received_input = True

                    if response == "refresh":
                        killtabs()
                        sleep(.1)
                        open_and_switch("https://web.simple-mmo.com/i-am-not-a-bot")
                        sleep(1)
                        take_ss_and_send()
                        
                    sleep(1)

                chosen_image = None

                driver.switch_to.window(driver.window_handles[1])
                imgs = driver.find_elements(By.XPATH, "//img")
                for img in imgs:
                    if img.get_attribute("src") == "https://web.simple-mmo.com/i-am-not-a-bot/generate_image?uid="+str(int(final_response)-1):
                        chosen_image = img
                        break

                temp_mouse_move(chosen_image.location, chosen_image.size)

                sleep(randint(1,2))
                
                try:
                    if driver.find_element(By.XPATH, "//*[text()='Retry']"):
                        retrybtn = driver.find_element(By.XPATH, "//*[text()='Retry']")
                        temp_mouse_move(retrybtn.location, retrybtn.size)
                    webhook = DiscordWebhook(url=settings["discord_webhook"], content="Failure.")
                    webhook.execute()
                except:
                    completed = True

                    killtabs()
                    
                    webhook = DiscordWebhook(url=settings["discord_webhook"], content="Success.")
                    webhook.execute()
                    last_human_verif = tick()
            
        sleep(.5)
        log("**!!** Human verification ended **!!**")


# mouse func

def bezier_mouse(location, size, isquest=False):
    x, relY = location["x"], location["y"]
    absY = relY + driver.execute_script('return window.outerHeight - window.innerHeight;')
    w, h = size["width"], size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = x+randfloat((w/4), wCenter+(w/4)), absY+randfloat((h/2), (hCenter)+(h/4))

    x2 = (start[0] + end[0])/2 
    y2 = (start[1] + end[1]) / 2

    control1X = (start[0] + x2)/2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    control1 = control1X, y2 
    control2 = control2X, y2

    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])

    degree = 3
    curve = bezier.Curve(points, degree)
    
    delay = 0.003
    curve_steps = max(int(abs(end[0]/start[0])), int(abs(end[1]/start[1])))
    
    if curve_steps < 2:
        curve_steps += randint(1,2)
        delay = 0.02
    elif curve_steps < 70 and curve_steps >= 30:
        delay = 0.002
        curve_steps -= 15
    elif curve_steps >= 70:
        curve_steps -= 30
        delay = 0.002

    for j in range(1, curve_steps + 1):
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)
        pyautogui.sleep(delay)

    if isquest:
        current_pos = pyautogui.position()
        pyautogui.moveTo(current_pos[0], current_pos[1]+15)

    pyautogui.click(clicks=1)

    human_verif()

def has_numbers(inputString):
  return any(char.isdigit() for char in inputString)

def getinfo():
    open_and_switch("https://web.simple-mmo.com/api/web-app")
    data = json.loads("{"+driver.page_source.split("{")[1].split("}")[0]+"}")
    killtabs()
    return data

def attack_mob():
    attack_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "attackButton")))
    lasthp = int(driver.find_element(By.ID, "opponent-hp").text)
    error_interval_attack=0
    while int(driver.find_element(By.ID, "opponent-hp").text) != 0:
        bezier_mouse(attack_btn.location, attack_btn.size)
        sleep(randfloat(.5, 1.25))
        if lasthp==int(driver.find_element(By.ID, "opponent-hp").text):
            error_interval_attack+=1
        if error_interval_attack == 3:
            break

    close_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Close']")))
    bezier_mouse(close_btn.location, close_btn.size)

    return True

# setting up chrome

print(sleep_logo,"[ SLEEP ] Setting up secure chrome.")
chrome_options = Options()

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'disable-popup-blocking', 'enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--start-fullscreen')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

# login stage

print(" [ SLEEP ] Opening login page.")
driver.get("https://web.simple-mmo.com/travel")

if settings["auto_login"] == "true":
    email = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'password')))

    print(" [ SLEEP ] Auto logging in.")
    
    for letter in settings["email"]:
        sleep(randfloat(.05, .29))
        email.send_keys(letter)
    
    for letter in settings["password"]:
        sleep(randfloat(.05, .29))
        password.send_keys(letter)

    login = driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]")
    bezier_mouse(login.location, login.size)

    if driver.current_url == "https://web.simple-mmo.com/travel":
        print(" [ SLEEP ] Successfully automatically logged in.")
    else:
        print("\n [ SLEEP ] An issue occured, make sure your login is correct.")
        sleep(3)
        driver.quit()
        quit()
else:
    if input(" [ SLEEP ] Manual login, press enter once logged in. ") != "" or driver.current_url != "https://web.simple-mmo.com/travel":
        print("\n [ SLEEP ] An issue occured, make sure you logged in.")
        sleep(3)
        driver.quit()
        quit()
    elif driver.current_url == "https://web.simple-mmo.com/travel":
        print(" [ SLEEP ] Successfully automatically logged in.")

cls()            


#main

print(sleep_logo, "[ SLEEP ] Farming starting up.")

Toggle = False
shutting_down = False
remote_toggle = "false"

remote_control = settings["remote_control"] == "true"

if remote_control:
    print(" [ SLEEP ] Detected remote control, waiting for activation.")
else:
    requests.get("your_url_here/simplemmo/captcha.php?task=remote&state=send&value=false")

old_remote_state = "false"
def backend_func():
    global Toggle
    global shutting_down
    global remote_control
    global remote_toggle
    global old_remote_state
    
    while True:
        try:
            if keyboard.is_pressed("f9"):
                Toggle = True
                sleep(.5)
        except: pass

        try:
            if keyboard.is_pressed("f2") and not shutting_down:
                shutting_down = True
                print(" [ SLEEP ] Shutting down safely.")
                log(" **<> Ending auto farm <>**")
        except: pass

        if remote_control:
            remote_toggle = old_remote_state
            try: remote_toggle = str(requests.get("your_url_here/simplemmo/captcha.php?task=remote&state=receive").text)
            except: pass
            
            if remote_toggle != old_remote_state:
                log("Successfully set autofarm status to: {}".format(remote_toggle), True)
                old_remote_state = remote_toggle
                print(" [ SLEEP ] Remotely changed autofarm status to",remote_toggle)
            sleep(1)
        else:
            sleep(.2)
                

        

def main_func():
    global Toggle
    global human_verifs
    global shutting_down
    global remote_toggle
    
    steps_done = 0
    mobs_attacked = 0
    waved_users = 0
    tools_used = 0

    battles_done = 0
    quests_done = 0

    error_interval = 0
    
    time_began = tick()
    api_last_called = tick()
    current_random_delay = randint(5, 25)

    current_data = getinfo()
    while True:
        #remote control
        if remote_control:
            if remote_toggle == "false":
                if driver.current_url != "https://www.google.com/":
                    driver.get("https://www.google.com/")
                continue
            elif remote_toggle == "true":
                if driver.current_url == "https://www.google.com/":
                    driver.get("https://web.simple-mmo.com/travel")
            
        #shutting down
        if shutting_down:
            print(" [ SLEEP ] Successfully shut down.")
            driver.quit()
            sleep(1)
            quit()
        
        #keybind toggle
        if Toggle:
            if input(" [ SLEEP ] Farming paused. Press enter to resume or (1) for stats. ") == "1":
                print("\n\tSteps Done: {}\n\tMobs Attacked: {}\n\tUsers Waved: {}\n\tUsed Tools: {}\n\n\tHuman Verifications: {}\n\n\tBattles Done: {}\n\tQuests Done: {}\n\n\tTime Farmed: {}m\n".format(steps_done, mobs_attacked, waved_users, tools_used, human_verifs, battles_done, quests_done, int((tick()-time_began)/60)))
                continue
            else:
                Toggle = False
                print(" [ SLEEP ] Farming resumed.")
                continue

        human_verif()

        if ((tick()-api_last_called)/60) > current_random_delay:
            current_data = getinfo()
            api_last_called = tick()
            current_random_delay = randint(5, 25)

        #handle battle arena
        try:
            if int(current_data["energy"]) > 0 and settings["auto_battle"] == "true":
                battle_btn = driver.find_element(By.XPATH, "//*[text()='Battle']")
                bezier_mouse(battle_btn.location, battle_btn.size)

                sleep(randfloat(.5, 1.25))
                while int(current_data["energy"]) != 0:
                    generate_enemy = driver.find_element(By.XPATH, "//button[contains(text(), 'Generate a')]")
                    bezier_mouse(generate_enemy.location, generate_enemy.size)

                    sleep(randfloat(.25, .75))
                    
                    confirm_btn = driver.find_element(By.XPATH, "//*[text()='Yes, generate a enemy']")
                    bezier_mouse(confirm_btn.location, confirm_btn.size)

                    sleep(randfloat(.25, .75))
                    
                    attack_btn = driver.find_element(By.XPATH, "//*[text()='Attack']")
                    bezier_mouse(attack_btn.location, attack_btn.size)

                    sleep(randfloat(.5, 1))

                    attack_mob()

                    sleep(randfloat(.5, 1.25))

                    battles_done += 1

                    if should_log:
                        log("Completed battle arena |")

                    current_data["energy"] = str(int(current_data["energy"])-1)

                driver.get("https://web.simple-mmo.com/travel")
                sleep(randfloat(.5, 1))

                continue
        except:
            pass

        #handle quests
        try:
            if int(current_data["quest_points"]) > 0 and settings["auto_quest"] == "true":
                quest_btn = driver.find_element(By.XPATH, "//*[text()='Quests']")
                bezier_mouse(quest_btn.location, quest_btn.size)

                sleep(randfloat(.5, 1.25))

                relative_quest = driver.find_element(By.XPATH, "//*[contains(text(), '{}')]".format(settings["quest_name"].replace("_", " ")))

                if relative_quest:
                    driver.execute_script("arguments[0].scrollIntoView(true);", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '{}')]".format(settings["quest_name"].replace("_", " "))))))
                    bezier_mouse(relative_quest.location, relative_quest.size, True)
                    

                    sleep(randfloat(.5, 1.25))
                    perform_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Perform Quest')]")
                    while int(current_data["quest_points"]) != 0:
                        bezier_mouse(perform_button.location, perform_button.size)
                        sleep(randfloat(.75, 1.5))

                        quests_done += 1

                        if should_log:
                            log("Completed quest |")

                        current_data["quest_points"] = str(int(current_data["quest_points"])-1)

                    sleep(randfloat(.5, 1.25))
                    
                    driver.get("https://web.simple-mmo.com/travel")
                    sleep(randfloat(.5, 1))

                    continue
        except:
            pass
                
"""
        #first time check
        try:
            first_time = driver.find_element(By.XPATH, "//button[contains(text(),'Take a step')]")
            if first_time:
                bezier_mouse(first_time.location, first_time.size)
                steps_done += 1
                if should_log:
                    log("Stepped |")
                continue
        except:
            pass
"""
        #attack mob
        try:
            attack_btn = driver.find_element(By.XPATH, "//*[text()='Attack']")
            if attack_btn and settings["auto_battle_mob"] == "true":
                bezier_mouse(attack_btn.location, attack_btn.size)
                sleep(randfloat(.5, 1.25))

                attack_mob()

                mobs_attacked += 1

                if should_log:
                    log("Attacked a mob |")

                continue
        except:
            pass

        #farming w tools
        try:
            tool_btn = False
            try: tool_btn = driver.find_element(By.XPATH, "//button[text()='Catch']")
            except: pass
            try: tool_btn = driver.find_element(By.XPATH, "//button[text()='Salvage']")
            except: pass
            try: tool_btn = driver.find_element(By.XPATH, "//button[text()='Chop']")
            except: pass
            try: tool_btn = driver.find_element(By.XPATH, "//button[text()='Mine']")
            except: pass
            try: tool_btn = driver.find_element(By.XPATH, "//button[text()='Open']") # for easter event
            except: pass

            if tool_btn and settings["auto_tool_use"] == "true":
                bezier_mouse(tool_btn.location, tool_btn.size)
                sleep(randfloat(.5, 2))

                gather_btn = driver.find_element(By.ID, "crafting_button")

                if not gather_btn.is_enabled():
                    driver.get("https://web.simple-mmo.com/travel")
                    sleep(randfloat(.5, 1))

                    continue
                    
                while driver.find_element(By.ID, "crafting_button").text != "Press here to close":
                    bezier_mouse(gather_btn.location, gather_btn.size)
                    sleep(randfloat(.5, 1.25))

                sleep(randfloat(.5, 1.25))
                bezier_mouse(gather_btn.location, gather_btn.size)
                tools_used += 1
                if should_log:
                    log("Used tools |")

                continue
        except Exception as e:
            print("using toolls error:", e)

        #wave to player
        try:
            wave_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Wave')]")
            if wave_btn and settings["auto_wave"] == "true":
                bezier_mouse(wave_btn.location, wave_btn.size)
                sleep(randfloat(.5, 2))

                second_wave_btn = driver.find_element(By.XPATH, "//button[text()='Wave']")
                bezier_mouse(second_wave_btn.location, second_wave_btn.size)
                sleep(randfloat(.5, 2))
                
                success = False
                try:
                    success_msg = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Success!']")))
                    if success_msg:
                        success = True
                except:
                    pass

                ok_msg = driver.find_element(By.XPATH, "//button[text()='OK']")
                bezier_mouse(ok_msg.location, ok_msg.size)
                
                if success:
                    waved_users += 1
                    if should_log:
                        log("Waved |")
        except:
            pass
                

        #take normal step
        try:
            bar = driver.find_element(By.ID, "loadingBar")
            if bar:
                while int(float(bar.get_attribute("style").split("width: ")[-1].split("%")[0])) != 0:
                    sleep(randfloat(.2, .5))
                step_btn = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Take a step')]")))
                if step_btn and settings["auto_step"] == "true":
                    bezier_mouse(step_btn.location, step_btn.size)

                    steps_done += 1
                    if should_log:
                        log("Stepped |")
                    sleep(randint(1, 2))
                    
                    continue
        except:
            pass
        
        
        sleep(randfloat(.5, 1))

        error_interval += 1
        if error_interval > 3:
            log("Error detected, auto fixing program.")
            driver.get("https://web.simple-mmo.com/travel")
            error_interval = 0
            sleep(1)
            current_data = getinfo()
                
                

        
                

backend_thread = Thread(target=backend_func)
main_thread = Thread(target=main_func)

log(" **<> Starting auto farm <>**")

if remote_control:
    log("Waiting for remote control.")

backend_thread.start()
main_thread.start()
