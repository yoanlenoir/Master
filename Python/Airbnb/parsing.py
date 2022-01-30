""" 
Récupère les données des backup. 

Variables: 
- Liste des villes (Même que dans le fichier "Scraping")
- Liste des caractéristiques

Dataclass: 
- Logement
- Debut
- Element

Fonctions: 
- logement
- debut
- element
- final
- liste_annonces
"""

from typing import Optional, List
from bs4 import BeautifulSoup as BS
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
import json
import os
from dataclasses import dataclass


@dataclass
class Logement:
    logement: str
    vendeur: str
    quartier: str


def logement(annonces :str) -> List[Logement]:
    """ Récupère le type de logement, le type de vendeur et le quartier de l'annonce. 
    """
    type_logement = []
    for annonce in annonces:
        desc = annonce.find_all("div", {"class": "mjnkf15 dir dir-ltr"})
        for log in desc:
            coupe = log.get_text(strip=True)
            test = coupe.split("·")
            if len(test) == 3:
                logement = test[0]
                vendeur = test[1]
                quartier = test[2]
            else:
                logement = test
                vendeur = "vide"
                quartier = "vide"

        type_logement.append(Logement(logement, vendeur, quartier))
    return type_logement


@dataclass
class Debut:
    rare: Optional[str]
    com: Optional[str]
    etoile: Optional[str]
    prix: Optional[str]


def debut(annonces:str) -> List[Debut]:
    debut = []
    for annonce in annonces:
        rare = annonce.find("div", {"class": "ebaidbp dir dir-ltr"})
        com = annonce.find("span", {"class": "rapc1b3 dir dir-ltr"})
        etoile = annonce.find("span", {"class": "r1g2zmv6 dir dir-ltr"})
        prix = annonce.find("span", {"class": "_tyxjp1"})

        debut.append(Debut(rare, com, etoile, prix))
    return debut


@dataclass
class Element:
    perle_rare: bool
    commentaire: str
    note: str
    prix: str


def element(annonces: str) -> List[Element]:
    """Retourne les caractéristiques de chaque annonces.
    """
    liste_element = []
    for deb in debut(annonces):
        
        perle_rare = bool(deb.rare)

        if deb.com is not None:
            commentaire = deb.com.get_text(strip=True)
        else:
            commentaire = "vide"

        if deb.etoile is not None:
            note = deb.etoile.get_text(strip=True)
        else:
            note = "vide"

        if deb.prix is not None:
            prix_nuit = deb.prix.get_text(strip=True)
        else:
            prix_nuit = "vide"

        liste_element.append(Element(perle_rare, commentaire, note, prix_nuit))
    return liste_element


def carac(annonces:str) -> List[str]:
    liste1 = []
    for annonce in annonces:
        liste2 = []
        a = annonce.find_all("span", {"class": "mvk3iwl dir dir-ltr"})
        for j in a:
            liste2.append(j.get_text(strip=True))
        liste1.append(liste2)
    return liste1


def final(annonces: str, ville: str, liste: list) -> List:
    """ Créer le dictionnaire des annonces avec toutes les caractéristiques de chaque annonce. 
    """
    list_dict = []
    dictionnaire = {}
    log = logement(annonces)
    elem = element(annonces)
    for i in range(len(carac(annonces))):
        dictionnaire["ville"] = ville
        dictionnaire["logement"] = log[i].logement
        dictionnaire["vendeur"] = log[i].vendeur
        dictionnaire["quartier"] = log[i].quartier
        dictionnaire["chambre"] = carac(annonces)[i][1]
        for l in liste:
            caracteristiques = list(filter(lambda x: l in x, carac(annonces)[i]))
            dictionnaire[l] = caracteristiques
        dictionnaire["Perle"] = elem[i].perle_rare
        dictionnaire["Note"] = elem[i].note
        dictionnaire["Commentaire"] = elem[i].commentaire
        dictionnaire["Prix"] = elem[i].prix
        list_dict.append(dictionnaire)
        dictionnaire = {}
    return list_dict


def liste_annonces(liste_ville: List) -> List:
    """ Récupère le code html de chaque backup pour sortir un dictionnaire pour chaque annonce et de 
    leurs caractéristiques
    
    >>> liste_ville=["Marseille", "Paris"]
    >>> liste_annonce(liste_ville)
    [{"ville": "Marseille", "logement": "Logement entier: appartement", ..., "Prix" : "110€"}, ..., 
    {"ville": "Paris", ..., "Note": "4,93", "Prix": "93€"}]
    """
    for i in range(1, 6):
        for ville in liste_ville:
            dos1 = os.listdir(path + f"/voyageurs{i}/ville{ville}")
            if dos1[0] == ".ipynb_checkpoints":
                dos1 = dos1[1:]
            for page in dos1:
                with open(
                    path + f"/voyageurs{i}/ville{ville}/{page}", "r", encoding="utf8"
                ) as fichier:
                    code = fichier.read()
                    soupe = BS(code)
                    test = soupe.find("div", {"class": "_fhph4u"})
                    annonces = test.find_all("div", {"class": "_8ssblpx"})
                    fin = final(annonces, ville)
    return fin
