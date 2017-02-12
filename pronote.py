# -*- coding: utf-8 -*-
# @Author: Stormix - Anas Mazouni
# @Date:   2017-02-12 23:04:51
# @Last Modified by:   Stormiix
# @Last Modified time: 2017-02-12 23:42:12
# @Website: https://stormix.co

#Import Some Python Modules

import inspect, sys
import os
import time 
import urllib

#Import Selenium modules

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Declare Variables

#Targeted Website : Pronote
website = "https://e212073y.index-education.net/pronote/eleve.html"
username = "MAZOUNI"
password = "~~~~~~~"
#Username Text Input ID:
user_input = "GInterface.Instances[0].idIdentification.bouton_Edit"
#Password Text Input ID:
password_input = "GInterface.Instances[0]_password"
#Form submit button ID:
connect_button = "GInterface.Instances[0].idBtnConnexion"

contenu_cour = "GInterface.Instances[0].Instances[7]_Combo0"

#Initiate the selenium webdriver
currentfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
selenium = webdriver.Chrome(currentfolder+"/chromedriver")

#Login Function
def login(username,password,website):
    """A procedure used to login into Pronote using the students credentials
    Params:
        username : str
        password : str
        website : str
    """
    #Open Pronote
    selenium.get(website) 
    print("Loaded .. "+website)
    #Sleep to wait for the slow-loading website !
    time.sleep(3)     
    #Fill in the login form
    username_log = selenium.find_element_by_id(user_input)
    password_log = selenium.find_element_by_id(password_input)
    username_log.send_keys(username)
    password_log.send_keys(password)
    #Click the connect buttun
    selenium.find_element_by_id(connect_button).click()
    print("Logging in ... ")

def fetch_docs():
    time.sleep(3) #Let's wait again for Pronote to load .. pff
    print("Look for the diffrent subjects , please wait ...")
    #Go to the files/contenu de cour section
    selenium.find_element_by_id(contenu_cour).click()
    print("Opened > Ressources pédagogiques ....")
    #I had to use this loop because pronote kicks me out after download the first few files ... frustrating :'(
    for i in range(9): # I used 9 , since I already how many subjects we have, but u can always edit this , or code a function to dynamically fetch the number.
        #Let's look for some files to download :D
        scan_docs(i)

def scan_docs(i):
    #Rest a bit python , this is too much for ya!
    time.sleep(3)
    print("Subject : ")
    #This variable holds the diffrent subjects ids, contact me if u want to know how I got it! 
    ids = "id_140_mat_"+str(i)+"_-1"
    #Alright , now that we got the id , let's get into work
    element = selenium.find_element_by_id(ids)
    current_subject  = element.text #Fetch the subject name !
    print(current_subject) #print it :D
    print("Searching for files to download ...")
    Hover = ActionChains(selenium).move_to_element(element) # Pronote has this 'nice' animation when u try to open a certain subject
    #It's a page flip animation , and I needed to simulate a mouse hovering on the subject to trigger this animation
    #So I did just that 
    Hover.click().perform()
    #Sleep a bit m8
    time.sleep(1)
    #Now click on the 'Documents Joints' link
    element.click()
    #Sleep again :D
    time.sleep(2)
    # Eyy , let's download the files now , I've checked the source code and found out that all the files links have the same class : lel , let's exploit that
    all_files = selenium.find_elements_by_xpath("//a[@class='Texte10 Maigre SouligneSurvol SouligneSurvol AvecMenuContextuel']")
    # Selenium 'find_elements_by_xpath' will fetch all these classes and put them into a list
    time.sleep(3)
    # Let's loop through each file
    for file in all_files:
        #Let's get the link from the <a> element
        link = file.get_attribute("href")
        #Let's get the file name
        filename = file.text
        # Download !
        download_files(current_subject,link,filename)
    #After downloading all these files , let's go back and start over ->
    reset()

def reset():
    """
    Refreshes the visited website and logs in
    """
    print("Going back  ....")
    #Refreshs the website
    selenium.refresh();
    #Pronote hates bots , so it kicks us out , let's re-login | we could solve this problem by using cookies , since Pronote uses them to check if the user is connected
    login(username,password,website)
    time.sleep(1)
    #Let's go back to Ressources pédagogiques
    selenium.find_element_by_id(contenu_cour).click()

def download_files(folder,link,filename):
    #check if the subject folder already exists
    if not os.path.isdir(folder):
        #If not , make a new one
        os.makedirs(folder)
    #Check if the file already exists , if not download it
    if not os.path.exists(folder+"/"+filename):
        down = urllib.URLopener()
        # Urllib is love , Urllib is life !
        down.retrieve(link, folder+"/"+filename)
        print(filename+"... Downloaded !")
    else:
        print(filename+"... Already Exists !")

#Main Program
login(username,password,website)
fetch_docs()