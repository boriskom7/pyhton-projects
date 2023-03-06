from PIL import Image
import pyautogui
import numpy as np
import time
import os        

URL = "https://elgoog.im/t-rex/?bot"

GAME_X = 660
#GAME_X = 980
GAME_Y = 315

def jump(size):
    
    if size < 2:
        pyautogui.keyDown("space")
        time.sleep(0.01)
        pyautogui.keyUp("space")
    else:   
        pyautogui.keyDown("space")
        time.sleep(0.1)
        pyautogui.keyUp("space")
    print(f"jump...{size} cactus")       

#im = pyautogui.screenshot("myscreenshot.png",region=(660, 315, 600, 150))
#im = pyautogui.screenshot("myscreenshot.png",region=(GAME_X, GAME_Y+129, 600, 1))
                      
#image = Image.open('myscreenshot.png').convert('1')

W = GAME_X + 70
H = GAME_Y + 130 #-16
search_area = 90    
game = True

while (game):         
    # categorize comming cactus
    cac_num = 0
    #im = pyautogui.screenshot("myscreenshot.png", region=(W,H, search_area, 1))  
    im = pyautogui.screenshot(region=(W,H, search_area, 1)) 

    np_image = np.array(im)[0]
    #print(np_image)
    first = np.where(np_image == 83)          
    last = np.where(np_image[::-1] == 83)
    
    try:
        if ((first[0][0]) - (search_area - last[0][-1]) < 6):   
            in_cac = False
            for pix in np_image:
                if in_cac:
                    if (pix[0] == 83 ):      
                        in_cac = True
                    else: 
                        in_cac = False
                        cac_num +=1
                else:
                    if (pix[0] == 83 ):   
                        in_cac = True  
            if cac_num > 0:
                jump(cac_num)
    except IndexError:
        pass

  
