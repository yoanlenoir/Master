"""
Récupération des backup du site de Airbnb. 

Variables : 
- Nombre de voyageurs désiré
- Liste des villes 

Fonctions : 
- recup_backup
"""

from bs4 import BeautifulSoup as BS
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
import os
from time import sleep, time

def recup_backup(nbr_voys:int,nom_ville:list) -> str:
    """Récupère les backup html des pages du site Airbnb
    nbr_voys : Donner le nombre de changement de voyageurs que vous souhaitez (2 en 2).
    nom_ville : Lister les villes pour récupérer les annonces de celles-ci.
    
    Exemple: 
    >>> nom_ville = ["Lille, "Marseille"]
    >>> final(2, nom_ville)
    >>> .../voyageurs1/villeLille/page1.html
    """
    
    DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get("https://www.airbnb.fr/s/Paris/homes?place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&refinement_paths%5B%5D=%2Fhomes&checkin=2022-03-15&checkout=2022-03-16&adults=2&children=0&infants=0&pets=0&search_type=AUTOSUGGEST")
    
    sleep(2)
    cookies=driver.find_element(By.CLASS_NAME, "_1qbm6oii") 
    cookies.click()
    sleep(3)

    for num_voy in range(nbr_voys):
        path="C:/Users/yoanl/MecenS3/Airbnb"
        os.mkdir(f"voyageurs{num_voy+5}")
        path1= path + "/" + f"voyageurs{num_voy+5}"
        for n_ville in nom_ville: 
            os.mkdir(path1 + f"/ville{n_ville}")
            path2= path1 + "/" + f"/ville{n_ville}"
            bouton_ville=driver.find_elements(By.CLASS_NAME,"_b2fxuo")[0]
            bouton_ville.click()
            sleep(4)
            effacer=driver.find_elements(By.CLASS_NAME,"_1amgc4z")[0]
            effacer.click()
            ville=driver.find_element(By.ID, 'bigsearch-query-location-input')
            ville.send_keys(n_ville)
            sleep(4)
            recherche=driver.find_element(By.CLASS_NAME, '_1mzhry13')
            recherche.click()
            sleep(4)
            i=0
            while True:
                i=i+1
                with open( path2 + f"/page{i}.html", "w", encoding="utf8") as fichier:
                    fichier.write(driver.page_source)
                try: 
                    page_suiv=driver.find_elements(By.XPATH,"//a[@aria-label='Suivant']")[0]
                    page_suiv.click()
                    sleep(3)
                except: 
                    break
        bouton_voy=driver.find_elements(By.CLASS_NAME,"_b2fxuo")[2]
        bouton_voy.click()
        sleep(3)
        plus=driver.find_elements(By.CLASS_NAME, "_8bq7s4")[1]
        plus.click()
        sleep(3)
        plus.click()
        recherche=driver.find_element(By.CLASS_NAME, '_1mzhry13')
        recherche.click()