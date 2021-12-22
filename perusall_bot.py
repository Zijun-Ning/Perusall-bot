import cv2
import pyautogui
import time
import pytesseract
import numpy as np
import random
import pyperclip

##### USER INPUT AREA #####
retina_display = True              # Usually ture if you are using Apple computer/laptop
read_speed = 0                     # adjust this number to read faster or slower, recommend between 0 and 5
###########################

time.sleep(5)
pyautogui.PAUSE = 0.01
screenWidth, screenHeight = pyautogui.size()

#locate important things on the screen
taskbar_location = pyautogui.locateOnScreen('task_bar.png', confidence=0.85)
comment_location = pyautogui.locateOnScreen('comment_section.png', confidence=0.85)
perusall_big_location = pyautogui.locateOnScreen('perusall_big.png', confidence=0.85)
side_bar_location = pyautogui.locateOnScreen('side_bar.png', confidence=0.85)
conv_location = pyautogui.locateOnScreen('conv.png')
next_x = 0
next_y = 0

#setup screenshot area for text extraction
ss_area = [perusall_big_location[0] + perusall_big_location[2]]
ss_area.append(taskbar_location[1] + taskbar_location[3])
ss_area.append(comment_location[0] - ss_area[0])
ss_area.append(side_bar_location[3])

#REQUIRES:  image1 AND image2 ARE VALID cv2::mat
#EFFECTS:   RETURN True IF image1 AND image2 ARE THE SAME 
def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

#REQUIRES:  img is VALID cv2::mat
#EFFECTS:   RETURN THE TEXT CONTAINED img
def img_to_str(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return pytesseract.image_to_string(img)

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#           ss_area IS A VALID region
#EFFECTS:   TAKE A SCREENSHOT, SCROLL DOWN TAKE ANOTHER SCREENSHOT
#           RETURN TRUE IF THE TWO SCREENSHOTS ARE THE SAME
def is_done():
    img = pyautogui.screenshot(region=(ss_area))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    pyautogui.moveTo(screenWidth / 2, screenHeight / 2, duration=2, tween=pyautogui.easeInOutQuad)

    for i in range(0,random.randint(5, 15),1):
        pyautogui.scroll(-10)

    img1 = pyautogui.screenshot(region=(ss_area))
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)

    if is_similar(img, img1):
        return True
    else:
        return False

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#           comment_location IS A VALID region
#EFFECTS:   CLICK ON THE FIRST CONVERSATION IN PERUSALL
def find_first_conv():
    
    if(retina_display):
        pyautogui.moveTo(conv_location[0] / 2, conv_location[1] / 2)
    else:
        pyautogui.moveTo(conv_location[0], conv_location[1])
    
    pyautogui.click()
    pyautogui.move(-40, 0)

    while pyautogui.locateOnScreen('next.png', region=(comment_location)) is None:
        pyautogui.move(0, 10)
        pyautogui.click()
    pyautogui.click()
    global next_x, next_y
    next_pos = pyautogui.locateCenterOnScreen('next.png', region=(comment_location))
    next_x = next_pos.x
    next_y = next_pos.y

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#           CALLED find_first_conv AT LEAST ONCE BEFORE
#EFFECTS:   CLICK ON THE NEXT CONVERSATION IN PERUSALL
def next_conv():
    if(retina_display):
        pyautogui.moveTo(next_x / 2, next_y / 2)
    else:
        pyautogui.moveTo(next_x, next_y)
    pyautogui.click()

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#           comment_loaction IS A VALID region
#EFFECTS:   CLICK ON ALL THE LIKES CURRENTLY ON SCREEN
def like_in_conv():
    green_likes = pyautogui.locateAllOnScreen('green_like.png', region=(comment_location))
    if green_likes != None:
        for pos in green_likes:
            if retina_display:
                pyautogui.click(pos.left / 2, pos.top / 2)
            else:
                pyautogui.click(pos.left, pos.top)
    likes = pyautogui.locateAllOnScreen('like.png', region=(comment_location))
    if likes != None:
        for pos in likes:
            if retina_display: 
                pyautogui.click(pos.left / 2, pos.top / 2)
            else:
                pyautogui.click(pos.left, pos.top)
    questions = pyautogui.locateAllOnScreen('question.png', region=(comment_location))
    if questions != None:
        for pos in questions:
            if retina_display: 
                pyautogui.click(pos.left / 2, pos.top / 2)
            else:
                pyautogui.click(pos.left, pos.top)

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#EFFECTS:   EXTRACT THE TEXT ON THE DOCUMENT, WRITE IT INTO QUIILLBOT
#           CLICK ON THE SUMMARIZE BUTTON, COPY THE SUMMARY
#           DELTE THE TEXT IN THE INPUT BOX, AND RETURN TO PERUSALL
#           RETURN THE SUMMARY AS A string
def summarize():
    text = img_to_str(pyautogui.screenshot(region=(ss_area)))
    summary_location = pyautogui.locateCenterOnScreen('summary.png', region=(taskbar_location))
    if retina_display:
        pyautogui.click(summary_location.x / 2, summary_location.y / 2)
        paste_location = pyautogui.locateCenterOnScreen('summary_paste.png')
        if paste_location != None:
            pyautogui.click(paste_location.x / 2, paste_location.y / 2)
    else:
        pyautogui.click(summary_location.x, summary_location.y)
        if(pyautogui.locateCenterOnScreen('summary_paste.png') != None):
            pyautogui.click('summary_paste.png')
    process = text.replace("\n", " ")
    pyautogui.write(process)

    summarize_location = pyautogui.locateCenterOnScreen('summarize.png')
    if retina_display:
        pyautogui.click(summarize_location.x / 2, summarize_location.y / 2 )
        time.sleep(5)
        copy_location = pyautogui.locateCenterOnScreen('copy.png')
        pyautogui.click(copy_location.x / 2, copy_location.y / 2)

        pyautogui.click(screenWidth / 3, screenHeight / 2)
        pyautogui.hotkey('command', 'a')
        pyautogui.press('backspace')

        perusall_location = pyautogui.locateCenterOnScreen('Perusall.png')
        pyautogui.click(perusall_location.x / 2, perusall_location.y / 2)
        
    else:
        pyautogui.click(summarize_location.x, summarize_location.y)
        time.sleep(2)
        pyautogui.click('copy.png')
        
        pyautogui.click(screenWidth / 3, screenHeight / 2)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        
        pyautogui.click('Perusall.png')

    return pyperclip.paste()

#REQUIRES:  THE BROWSER IS ON PERUSALL TAB
#           sum_str IS A VALID string
#           comment_location IS VALID
#EFFECTS:   WRITE sum_str INTO THE COMMENT BOX IN PERUSALL
def write_summary(sum_str):
    if retina_display:
        pyautogui.moveTo((comment_location[0] + comment_location[2]/2) / 2, (comment_location[1] + comment_location[3] / 2)/2)
        pyautogui.scroll(-100 * 100)
        time.sleep(2)
        comment_box = pyautogui.locateCenterOnScreen('comment.png', region= comment_location)
        pyautogui.click(comment_box.x / 2, comment_box.y / 2)
    else:
        pyautogui.moveTo(comment_location[0] + comment_location[2] / 2, comment_location[1] + comment_location[3])
        pyautogui.scroll(-100 * 100)
        time.sleep(2)
        pyautogui.click('comment.png')
    pyautogui.click()
    pyautogui.write(sum_str)        
    pyautogui.press('enter')





# MAIN DRIVER PROGRAM
# EFFECT:   SCROLL THROUGH THE DOCUMENT("READING")
#           AFTER READING START COMMENTING AND LIKING
# WARNING:  IF THERE IS NO COMMENT IN THE LAST FEW PAGE
#           THE BOT MIGHT GO TO THE NEXT CHAPTER OF
#           THE DOCUMENT BY CLICKING THE next BUTTON
def main():

    while not is_done():
        print("not done yet")
        time.sleep(read_speed * 30)

    find_first_conv()
    while not is_done():
        next_conv()
        rand_num = random.randint(1, 10)
        if(rand_num <= 4):
            like_in_conv()
        if(rand_num > 4 and rand_num <= 8):
            summary = summarize()
            print(summary)
            time.sleep(2)
            write_summary(summary)
    print("Done!")


main()
