# main.py
import cv2
import pyautogui
from time import sleep
from selenium import webdriver
import pyocr
import pyocr.builders
import cv2
from PIL import Image
import sys

tools = pyocr.get_available_tools()

if len(tools) == 0:
    print("no file")
    sys.exit(1)

tool = tools[0]

driver_path = './chromedriver'

driver = webdriver.Chrome(driver_path)

window = (1000, 1000)
driver.set_window_size(*window)

target_url = 'http://typingx0.net/sushida/play.html'
driver.get(target_url)

sleep(10)
x,y=pyautogui.locateCenterOnScreen("title.png")
x //= 2
y //= 2
pyautogui.click(x,y+100)
sleep(2)
pyautogui.click(x,y+100)
pyautogui.typewrite(" ")
sleep(2)
for i in range(200):
    i += 1
    sc=pyautogui.screenshot(region=(800, 1000, 430, 60))
    sc.save("moji.png")
    moji=cv2.imread("moji.png",0)
    ret, out = cv2.threshold(moji, 100, 255, cv2.THRESH_BINARY)
    out=cv2.bitwise_not(out)
    cv2.imwrite("gray.png", out)
    res = tool.image_to_string(Image.open("gray.png"),lang="eng",builder=pyocr.builders.TextBuilder())
    pyautogui.typewrite(res)
    #sleep(0.2)


input("input")
driver.close()
driver.quit()