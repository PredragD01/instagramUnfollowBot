from selenium import webdriver
import time
from sys import exit
import os


driver = webdriver.Chrome(executable_path=r'chromedriver.exe')

def getUsers():
    print("PROCESS: CREATING LIST OF LIKES")
    time.sleep(3)
    driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/button')[0].click()
    likes = int(driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/button/span')[0].text) + 1
    time.sleep(2)
    newlist = []
    match = False

    while match==False:
        lastElem = None
        lista = driver.find_elements_by_xpath("//div[@class='                   Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                                              ']")
        for elem in lista:
            newlist.append(elem.text)
            lastElem = elem
        newlist = list(dict.fromkeys(newlist))
        if(len(newlist) in range(likes-6, likes + 10)):
            match = True
        else:
            driver.execute_script("return arguments[0].scrollIntoView();",lastElem)
        time.sleep(2)
    
    print("ZAVRSHEN PROCES")
    print("---------------")
    return newlist
    

def main():
    # Go to your page url
    driver.get('https://www.instagram.com/pedzo.exe/')
    time.sleep(1)

    driver.find_element_by_partial_link_text('Log In').click()
    print('LOGIRANJE...')
    time.sleep(2)
    driver.find_element_by_name('username').send_keys('USERNAME HERE')
    time.sleep(1)
    driver.find_element_by_name('password').send_keys('PASSWORD HERE')
    print('ENTERED USERNAME & PASSWORD')
    time.sleep(1)
    driver.find_element_by_name('password').submit()
    time.sleep(5)
    driver.get('https://www.instagram.com/<add your profile here>/')

    if(os.path.exists("users.txt")):
        if(os.path.exists("followingUsers.txt")):
            gettheuserstounfollow()
        else:
            getfollowing()
    else:
        listaSliki = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
        print(len(listaSliki))
        time.sleep(3)
        listaFinalna = []
        listaSliki2 = []
        for link in listaSliki:
            listaSliki2.append(link.find_elements_by_tag_name('a')[0].get_attribute('href'))

        counter = 0
        for linknew in listaSliki2:
            print(linknew)
            time.sleep(2)
            driver.get(linknew)
            listforLikes = []
            listforLikes = getUsers()
            for user in listforLikes:
                listaFinalna.append(user)
            counter += 1
            if (counter == 11):
                break
        listaFinalna = list(dict.fromkeys(listaFinalna))
        print(" ========================= Done with pictures =========================")
        print("NUMBER OF USERS " , len(listaFinalna))
        file = open("users.txt", "w")
        for korisnik in listaFinalna:
            print(file.write(korisnik + ";"))

        
        getfollowing()


def getfollowing():
    time.sleep(2)
    numberOfFollowing = int(driver.find_elements_by_xpath("//span[@class='g47SY ']")[2].text.replace(',', ''))
    driver.find_element_by_partial_link_text('following').click()
    time.sleep(3)
    match = False
    listOfUsers = []
    
    while match==False:
        lista = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")
        for elem in lista:
            listOfUsers.append(elem.get_attribute('title'))
        
        listOfUsers = list(dict.fromkeys(listOfUsers))
        print(len(listOfUsers))
        if(len(listOfUsers) == numberOfFollowing):
            match = True
        else:
            driver.execute_script("return arguments[0].scrollIntoView();",elem)
        time.sleep(0.5)
        
    print("Done with getting the following")
    file = open("followingUsers.txt", "w")
    for followingUser in listOfUsers:
        file.write(followingUser + ";")

    #####
def gettheuserstounfollow():
    f = open("users.txt", "r")  #READING A FILE
    listOfUsers = f.read().split(";")
    
    f = open("followingUsers.txt", "r")  #READING A FILE
    listOfUsersFollowing = f.read().split(";")
    numberOfMaxPeopleUnfollowedbyday = 100
    finalListOfUsersToUnfollow = list(set(listOfUsersFollowing) - set(listOfUsers))
    counter = 0
    for userUn in finalListOfUsersToUnfollow[1:]:
        if(numberOfMaxPeopleUnfollowedbyday == counter):
            print("we r done for today bruh...")
            raise SystemExit(0)
        else:
            if(counter == 14):
                print("Waiting TEN minutes so we can start unfollowing again...")
                time.sleep(600)
                counter = 0
            driver.get('https://www.instagram.com/' + userUn)
            time.sleep(3)
            numberOfFollowing = int(driver.find_elements_by_xpath("//span[@class='g47SY ']")[1].get_attribute('title').replace(",",""))
            if(numberOfFollowing > 40000):
                print("We dont't unfollow: ", userUn)
            else:
                buttons = driver.find_elements_by_tag_name("button")
                if(buttons[1].text == "Follow" or buttons[1].text == "Follow Back" or buttons[0].text == "Follow" or buttons[0].text == "Follow Back"):
                    print("mrsh...")
                else:
                    buttons[1].click()
                    time.sleep(3)
                    driver.find_element_by_xpath('//button[@class="aOOlW -Cab_   "]').click()
                    print("BYE BYE " , userUn)
                    counter += 1
                    numberOfMaxPeopleUnfollowedbyday += 1
        


if __name__ == "__main__":
    main()
