#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup as BS
from parsing import Logement, logement, Debut, debut, Element, element, carac, final


@pytest.fixture
def annonces():
    path = "C:/Users/yoanl/MecenS3/Airbnb"
    with open(path + f"/voyageurs1/villeParis/page1.html", "r", encoding="utf8") as fichier:
        code = fichier.read()
    soupe = BS(code)
    test = soupe.find("div", {"class": "_fhph4u"})
    annonces = test.find_all("div", {"class": "_8ssblpx"})
    return annonces[:1]


liste = ["voyageur", "lit", "bain", "Wifi", "Cuisine", "Lave", "Chauffage", "Parking"]


def test_logement(annonces):
    attendu = [
        Logement(
            logement="Logement entier\xa0: appartement",
            vendeur="Professionnel",
            quartier="Commerce - Dupleix",
        )
    ]
    calculé = logement(annonces)
    assert attendu == calculé


def test_element(annonces):
    attendu = [Element(perle_rare=False, commentaire="vide", note="vide", prix="53€")]
    calculé = element(annonces)
    assert attendu == calculé


def test_carac(annonces):
    attendu = [
        [
            "2 voyageurs",
            "Studio",
            "1 lit",
            "1 salle de bain",
            "Wifi",
            "Cuisine",
            "Chauffage",
        ]
    ]
    calculé = carac(annonces)
    assert attendu == calculé


def test_final(annonces):
    attendu = [
        {
            "ville": "Paris",
            "logement": "Logement entier\xa0: appartement",
            "vendeur": "Professionnel",
            "quartier": "Commerce - Dupleix",
            "chambre": "Studio",
            "voyageur": ["2 voyageurs"],
            "lit": ["1 lit"],
            "bain": ["1 salle de bain"],
            "Wifi": ["Wifi"],
            "Cuisine": ["Cuisine"],
            "Lave": [],
            "Chauffage": ["Chauffage"],
            "Parking": [],
            "Perle": False,
            "Note": "vide",
            "Commentaire": "vide",
            "Prix": "53€",
        }
    ]
    calculé = final(annonces, "Paris", liste)
    assert attendu == calculé
