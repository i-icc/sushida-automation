"""
寿司打の自動化アプリ
"""
import cv2
import pyautogui
import pyocr
from time import sleep
from selenium import webdriver
from PIL import Image
import numpy as np


def main():
    # 文字起こしのために準備
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("no file")
        return
    tool = tools[0]

    # 寿司打サイトのurlを指定して開く
    driver_path = './chromedriver'
    driver = webdriver.Chrome(driver_path)
    window = (1000, 1000)
    driver.set_window_size(*window)
    target_url = 'http://typingx0.net/sushida/play.html'
    driver.get(target_url)
    # 開くの待ち
    sleep(8)

    # 位置確認
    x, y = pyautogui.locateCenterOnScreen("title.png")
    # pyautogui取得座標と指定座標がズレるため調整
    # retinaディスプレイの画面出力数が通常ディスプレイの２倍あることが原因らしい
    # 通常ディスプレイの場合は以下に行をコメントアウトする
    x //= 2
    y //= 2
    pyautogui.click(x, y+100)
    sleep(2)
    pyautogui.click(x, y+100)
    pyautogui.typewrite(" ")
    sleep(2)

    # 文字部分の幅高さ
    width = 215
    height = 30
    # retina なら１つ目 通常ディスプレイなら2つ目
    region = (x*2-width, y*2+146, width*2, height*2)
    # region = (x-width//2, y+73, width, height)

    # 文字が読み込めなくなるまで
    res = "-1"
    while res != "":
        sc = pyautogui.screenshot(region=region)
        moji = np.array(sc) 
        ret, out = cv2.threshold(moji, 100, 255, cv2.THRESH_BINARY)
        out = cv2.bitwise_not(out)
        res = tool.image_to_string(Image.fromarray(
            out), lang="eng", builder=pyocr.builders.TextBuilder())
        pyautogui.typewrite(res)

    input("エンターを押せば終了します")
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
