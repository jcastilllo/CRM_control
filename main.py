from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import re
import json
from selenium import webdriver
import chromedriver_autoinstaller
import os
options = webdriver.ChromeOptions() 
 
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False)
 
# Changing the property of the navigator value for webdriver to undefined 
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
options.add_argument('--disable-notifications')
# js.executeScript("window.onbeforeunload = function() {};");
# Define default profiles folder

options.add_argument(r"user-data-dir=/Users/mitsonkyjecrois/Library/Application Support/Google/Chrome/Profile 1")
# # Define profile folder, profile number
# options.add_argument(r"profile-directory=Profile 2")

#  options.add_argument(r"user-data-dir=/home/jorge/.config/google-chrome/"))
# # Define profile folder, profile number
# options.add_argument(r"profile-directory=Profile 1"))
#########################################################################################
#                                                                                       #
#                SECTION FOR SAVE AND LOAD CHECK POINTS                                 #
#                                                                                       #
#########################################################################################
def saveCheckPoint(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def loadCheckPoint(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:        
        json_object = json.load(openfile)
    return json_object

#########################################################################################
#                                                                                       #
#                                   MAIN FUNCTINS                                       #
#                                                                                       #
#########################################################################################
def giveClickRecents(filterword = 'Recents'):
    buttonfilter = driver.find_element(By.CLASS_NAME, '-mb-px.flex.place-content-evenly.space-x-4')

    listbuttons = buttonfilter.find_elements(By.CSS_SELECTOR,'a')

    for button in listbuttons:

        if filterword in button.text:
            button.click()

def loadmoreClicks():
    blockconversation = driver.find_element(By.CLASS_NAME, 'hl_conversations--messages-list-v2.relative.border-r.border-gray-200')
    totalconversation = blockconversation.find_element(By.CLASS_NAME, "flex.items-center.h-5")
    totalResults = int(re.search(r'\d+',totalconversation.text).group(0))
    return int(totalResults//20)


def clickLoadMore(numbload = 10):
    loadmore = True
    batch = 0
    while loadmore:
        try:
            for n in range(0, numbload):
                loadmore = driver.find_element(By.XPATH,"//*[text()='Load More']")
                loadmore.click()
                time.sleep(1.5)
                batch +=1
                if batch ==10:
                    batch = 0
                    userinput = input("Confirmt to continue type: y")
                    if userinput!='y':
                        loadmore = False
                        break
            loadmore = False
        except:
            time.sleep(0.5)

def getConversatinBlock():
    class_conversation = 'ml-1.message-list--avatar.avatar'
    conversations = driver.find_elements(By.CLASS_NAME, class_conversation)
    return conversations

def getNameRight():
    try:
        bodyside = driver.find_element(By.CLASS_NAME, 'message-body--aside')
        nameright = bodyside.find_element(By.CLASS_NAME, 'avatar_img').text
        return nameright
    except:
        return ""

def waitNewContactName(nameleft, nameright):
    while nameleft != nameright:
        nameright = getNameRight()
        time.sleep(0.2)

def getAllMessages():
    global listMSGObject
    flagloop = True
    print("GET ALL MESSAGES")
    while flagloop:
        print('-GAMSG-', end='')
        try:
            listMSGObject = driver.find_elements(By.CLASS_NAME, 'messages-single.--own-message')
            if len(listMSGObject)!= 0:
                flagloop = False
            time.sleep(0.5)
        except:
            time.sleep(1)

def getPendinIndexMessageList():
    global listMSGSentText, msgdontsentindexs, listMSGObject
    msgdontsentindexs = []
    listMSGSentText = []
    msgEmpty = True
    print("-Updationg linsts-")
    while msgEmpty:
        print('-UDATE-LISTS-')
        # getAllMessages()
        msgEmpty = False
        for msgnumber, message in enumerate(listMSGObject):

            # GET THE ID NUMBER OF MESSAGES FAILED
            if 'Unsuccessful' in message.text:
                msgdontsentindexs.append(msgnumber)
                print("msgnumber", msgnumber)

            # ELSE BUILD A LIST WITH THE MESSAGES SENT SUCCESSFULLY
            else:
                msg = message.find_element(By.CLASS_NAME, 'message-bubble').text
                listMSGSentText.append(cleanMessage(msg))

            # TO MAKE SURE THAT THE MESSAGE IS NOT EMPTY, IF FIND AN EMPTY MESSAGE IT REPEAT THE PROCESS.
            if len(message.text) ==0:
                msgEmpty = True
        time.sleep(1)
        

    msgdontsentindexs_copy = msgdontsentindexs.copy()    
    
    for i, KEY in enumerate(msgdontsentindexs):        
        messagetext = cleanMessage(listMSGObject[KEY].find_element(By.CLASS_NAME, 'message-bubble').text)
        
        if messagetext in listMSGSentText:
           msgdontsentindexs_copy.remove(KEY)               
    
    print("--msgdontsentindexs---", msgdontsentindexs)
    if len(msgdontsentindexs) == 0:
        print("--NOT ISSUES--",end='-')
    return msgdontsentindexs_copy
    
def trySendAgain(timewait= 1):
    global listMSGObject, msgdontsentindexs, listMSGSentText 
    message = listMSGObject[msgdontsentindexs[0]]
    buttontryagain = message.find_element(By.CLASS_NAME, 'fa.fa-sm.fa-redo.pointer')
    buttontryagain.click()
    time.sleep(timewait)

def getemail():
    email = driver.find_element(By.CLASS_NAME, "multiple-to-email")
    return email.text

    """This function make the next steps:
        - Check if there are pending message
        - Create a list of the message sent successfully
        - If the message pending has not been sending before,
          it will try to send again the other way it doesn't make nothing.
        - It will repeat the process, check, click again repeat the cycle 
          until there are no pending messages."""

def loopSendMessages(maxtry = 30):
    
    global msgdontsentindexs, listMSGSentText, listMSGObject, KEY, dictfails, nameleft
    count = 0
    trysentEnable = True

    print("FLAG trysentEnable: ", trysentEnable)
    while len(msgdontsentindexs)!= 0:
        try:            
            print("FLAG trysentEnable: INIT LOOP", trysentEnable)
            if trysentEnable:
                print("BEFORE trySendAgain()")
                trySendAgain()# CLICK EN EACH MESSAGE THAT FAIL BEFORE.                
                print("trySendAgain() READY")
                trysentEnable = False
                userInput = input("Confirm to estop loop: type 'y': ")                
                if userInput =='y':
                    break
            # ONLY INIT THE PROCCESS IF COUN VALUE IS MINOR TO MAXTRY
            if count < maxtry:
                # GET LIST OF ALL MESSAGE SENT INCLUDING FALLING MESSAGES
                getAllMessages()                
                # BUILD A LIST WITH THE INDEX OF FAIL MESSAGE AND A LIST WITH  THE MESSAGE SENT SUCCESSFULLY                
                msgdontsentindexs = getPendinIndexMessageList()
                #########################################################################            
                #   IF msgdontsentindexs AND listMSGSentText IS UPDATE IT  ENABLE TO    #
                #   TRY TO SEND ANOTHER PENDING MESSAGE                                 #
                #########################################################################
                trysentEnable = True
                count +=1
            # ELSE SAVE IN A FILE JSON ISSUES MESSAGES
            else:
                email = getemail()
                dictfails[KEY] = {'name':nameleft, 'email': email, 'state':'FAIL'}
                print("############## MAX COUNT REACHED, THEN TRY SENT FUNCTION IT WILL STOP ##################")
                saveCheckPoint('messagesfail.json', dictfails)
                msgdontsentindexs = []
            
        except:
            print("Additional wait")
            time.sleep(1)
            count +=1
            if count > maxtry:
                userinput = input("Confirm to stop: type 'y' ")
                count = 0
                if userinput =='y':
                    msgdontsentindexs = []
                    email = getemail()
                    dictfails[KEY] = {'name':nameleft, 'email': email, 'state':'FAIL'}
                    print("############## MAX COUNT REACHED, THEN TRY SENT FUNCTION IT WILL STOP ##################")
                    saveCheckPoint('messagesfail.json', dictfails)
                    msgdontsentindexs = []
        
        print("COUNT #########", count)
#######################################################################################

def loopSendMessages2(maxtry = 30):
    
    global msgdontsentindexs, listMSGSentText, listMSGObject, KEY, dictfails, nameleft
    count = 0
    trysentEnable = True

    while len(msgdontsentindexs)!= 0:

            print("FLAG trysentEnable: INIT LOOP", trysentEnable)
            if trysentEnable:            
                trySendAgain()# CLICK EN EACH MESSAGE THAT FAIL BEFORE.                
                print("trySendAgain() READY")
                trysentEnable = False
                userInput = input("Confirm to estop loop: type 'y': ")                
                if userInput =='y':
                    break
            # ONLY INIT THE PROCCESS IF COUN VALUE IS MINOR TO MAXTRY
            if count < maxtry:
                # GET LIST OF ALL MESSAGE SENT INCLUDING FALLING MESSAGES
                getAllMessages()                
                # BUILD A LIST WITH THE INDEX OF FAIL MESSAGE AND A LIST WITH  THE MESSAGE SENT SUCCESSFULLY                
                msgdontsentindexs = getPendinIndexMessageList()
                #########################################################################            
                #   IF msgdontsentindexs AND listMSGSentText IS UPDATE IT  ENABLE TO    #
                #   TRY TO SEND ANOTHER PENDING MESSAGE                                 #
                #########################################################################
                trysentEnable = True
                count +=1
            # ELSE SAVE IN A FILE JSON ISSUES MESSAGES
            else:
                email = getemail()
                dictfails[KEY] = {'name':nameleft, 'email': email, 'state':'FAIL'}
                print("############## MAX COUNT REACHED, THEN TRY SENT FUNCTION IT WILL STOP ##################")
                saveCheckPoint('messagesfail.json', dictfails)
                msgdontsentindexs = []
            maxtry += 1


#     print("pending index", msgdontsentindexs)
#################################################################
#                       SECTION CLEAN TEXT                      #
#################################################################
def cleanMessage(msg):    
    msg = msg.lower()
    msg = re.sub(r'[^\w\s]', '', msg)
    msg = ' '.join((msg.split()))
    return msg

#################################################################
#                   SECTION FOR SENT OTHER MESSAGE              #
#################################################################
def sentNewMessage():
    textarea = driver.find_element(By.NAME, 'editor')
    textarea.clear()
    textarea.send_keys('text 1 proof')
    
def clickSent():
    sendbutton = driver.find_element(By.ID, 'buttonGroupSpanSms')
    print(sendbutton.text)
#########################################################################################
#                             MAIN                                                      #
#########################################################################################
def main():
    global listMSGObject, KEY, dictfails
    if os.path.isfile('messagesfail.json'):
        loadCheckPoint('messagesfail.json')
    else:
        dictfails = {}


    name = ""
    while name =="":
        name = getNameRight()
        time.sleep(0.5)
        print("#", end = ' ')
    time.sleep(1)

    giveClickRecents()
    name2 = getNameRight()
    count  = 0
    while name == name2 or name2 == "" :
        name2 = getNameRight()
        time.sleep(0.5)
        print("#", end = ' ')    
        count +=1
        if count == 5:
            name2 = '***'
    time.sleep(1)
    clickLoadMore(numbload = loadmoreClicks())
    time.sleep(1)

    while True:
        conversations = getConversatinBlock()
        print(len(conversations))

        for KEY, conversation in enumerate(conversations):
            print("Client name: ", KEY, conversation.text)
            # flagclickfirst, currentcontacname = checkConversationSideBar(firstname)
            # if i != 0:
            #     conversation.click()
            # else:
            #     if flagclickfirst:
            ################################################################
            #                   CLICK ON NEW CONVERSATION                  #    
            ################################################################
            conversation.click()
            ###############################################################
            #   SECTION TO LOAD CONTACT NAME FROM LEFT AND RIGHT SIDE     #    
            ###############################################################
            
            nameright = getNameRight()
            nameleft = conversation.text
            #####################################################     
            #   SECTION TO WAIT UNTIL LOAD NEW CONVERSATION     #    
            #####################################################
            waitNewContactName(nameleft, nameright)

            ##################################################### 
            #                                                   #
            #       SECTION TO CHECK PENDING MESSAGES           #
            #                                                   #
            #####################################################
            # INITIALIZATION
            msgdontsentindexs = []  # INDEX OF MESSAGE WITH ISSUES (GLOBAL VARIABLES)
            listMSGSentText = []        # MESSAGE SENT PREVIOUSLY (GLOBAL VARIABLES)
            # count = 0

            getAllMessages() # GET A LIST OF MY OWN MESSAGES.
            getPendinIndexMessageList()
            loopSendMessages(maxtry = 20)
#########################################################################################
#                          GLOBAL VARIABLES                                             #
#########################################################################################
driver = webdriver.Chrome(options=options)

driver.get('https://app.rmhgo.com/v2/location/OgPuXhkvOkbRC0zerxQP/conversations/conversations/xxj8duklLmHcPja93udc')
# input('Confirm to continue: ')

msgdontsentindexs = []
listMSGSentText = []
listMSGObject = []
count = 0
dictFallSend = {}
if __name__ == "__main__":
    main()



