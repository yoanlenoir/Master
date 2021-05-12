#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour le module fonctions
"""
from fonctions import(
    genere_dico,
    genere_graph,
    trouve_chemins,
    genere_matrice_log,
    genere_gain_chemin,
    ajout_gain,
    ordonne,
    calcul_taxe_echange,
    ajout_final,
    liste_meilleur_chemin
)

rates=[
    [1,46.45,130.14],
    [0.020,1,2.66],
    [0.0077,0.357,1]
]

currencies=('EUR', 'ROU', 'YEN','FIN')
monnaie= 'EUR'
index_monnaie=currencies.index(monnaie)
montant=500

def test_genere_dico():
    attendu= {'EUR':0,'ROU':1,'YEN':2,'FIN':0}
    reel=genere_dico(currencies,index_monnaie)
    assert attendu==reel
    
def test_genere_graph():
    attendu={'EUR': ('EUR', 'ROU', 'YEN'),
 'ROU': ('EUR', 'ROU', 'YEN', 'FIN'),
 'YEN': ('EUR', 'ROU', 'YEN', 'FIN'),
 'FIN': ()}
    reel=genere_graph(currencies,index_monnaie)
    assert attendu==reel
    
def test_trouve_chemin():
    attendu=[['EUR', 'ROU', 'YEN', 'FIN'],
 ['EUR', 'ROU', 'FIN'],
 ['EUR', 'YEN', 'ROU', 'FIN'],
 ['EUR', 'YEN', 'FIN']]
    reel=trouve_chemins(genere_graph(currencies,index_monnaie),monnaie)
    assert attendu==reel
    
def test_genere_matrice_log():
    attendu=[[-0.0, -3.8383764652598478, -4.8686107940668375],
 [3.912023005428146, -0.0, -0.9783261227936078],
 [4.866534950122499, 1.030019497202498, -0.0]]
    reel=genere_matrice_log(rates)
    assert attendu==reel
    
def test_genere_gain_chemin():
    attendu=[525.5474391176937, 538.2131324004304, 538.0975196287217, 498.96315456481443]
    reel=genere_gain_chemin(rates,currencies,monnaie,index_monnaie,montant)
    assert attendu==reel

def test_ajout_gain():
    attendu=[['EUR', 'ROU', 'YEN', 'FIN', 525.5474391176937],
 ['EUR', 'ROU', 'FIN', 538.2131324004304],
 ['EUR', 'YEN', 'ROU', 'FIN', 538.0975196287217],
 ['EUR', 'YEN', 'FIN', 498.96315456481443]]
    reel=ajout_gain(rates,currencies,monnaie,index_monnaie,montant)
    assert attendu==reel
    
def test_ordonne():
    attendu=[['EUR', 'YEN', 'FIN', 498.96315456481443],
 ['EUR', 'ROU', 'YEN', 'FIN', 525.5474391176937],
 ['EUR', 'YEN', 'ROU', 'FIN', 538.0975196287217],
 ['EUR', 'ROU', 'FIN', 538.2131324004304]]
    reel=ordonne(rates,currencies,monnaie,index_monnaie,montant)
    assert attendu==reel

def test_calcul_taxe_echange():
    attendu=[497.9657272188394, 523.9723729171105, 536.4848408242968, 537.1372443487619]
    reel=calcul_taxe_echange(rates,currencies,monnaie,index_monnaie,montant)[0]
    assert attendu==reel

def test_ajout_final():
    attendu=[['EUR', 'YEN', 'FIN', 498.96315456481443, 497.9657272188394],
 ['EUR', 'ROU', 'YEN', 'FIN', 525.5474391176937, 523.9723729171105],
 ['EUR', 'YEN', 'ROU', 'FIN', 538.0975196287217, 536.4848408242968],
 ['EUR', 'ROU', 'FIN', 538.2131324004304, 537.1372443487619]]
    reel=ajout_final(rates,currencies,monnaie,index_monnaie,montant)
    assert attendu == reel

def test_liste_meilleur_chemin():
    attendu=(['EUR', 'ROU', 'EUR'], 538.21313, ['EUR', 'ROU', 'EUR'], 537.13724)
    reel=liste_meilleur_chemin(rates,currencies,monnaie,index_monnaie,montant)
    assert attendu == reel


    
    
    
    
    