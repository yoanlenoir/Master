"""
Fichier de test pour la librairie "nettoyage"
"""
import pandas as pd
import numpy as np

from nettoyage import(
    Annonce, 
    caracteristiques,
    chiffre_variable,
    logement,
    commentaire,
    note,
    prix,
    doublons)

def test_caracteristiques():
    entrée=pd.DataFrame({'bain': [['1 salle de bain'],['0,5 salle de bain'], ['3,5 salles de bain partagée']],
                        'chambre': ['1 chambre', 'Studio', '2 chambres'],
                        'voyageur': [['1 voyageur'], ['3 voyageurs'] , ['4 voyageurs']],
                        'lit' : [['1 lit'], ['2 lit'], ['1 lit']],
                        'Wifi': [['Wifi'], ['Wifi'], [np.nan]], 
                        'Cuisine' : [[np.nan], ['Cuisine'], ['Cuisine']],
                        'Lave': [[np.nan], ['Lave-linge'], [np.nan]],
                        'Chauffage': [[np.nan], [np.nan], ['Chauffage']],
                        'Parking': [['Parking gratuit'],['Parking gratuit'],['Parking gratuit']]})
    calculé = caracteristiques(entrée)
    attendu = pd.DataFrame({'bain': ['1 salle de bain','0.5 salle de bain', '3.5 salles de bain partagée'],
                            'chambre': ['1 chambre', '0 chambre', '2 chambres'],
                            'voyageur': ['1 voyageur', '3 voyageurs' , '4 voyageurs'],
                            'lit' : ['1 lit', '2 lit', '1 lit'],
                            'Wifi': [True, True, False], 
                            'Cuisine' : [False, True, True],
                            'Lave': [False, True, False],
                            'Chauffage': [False, False, True],
                            'Parking': [True, True, True],
                            'sdb_partage': [False, False , True]
                           })
    assert all(calculé) == all(attendu)

def test_chiffre_variable():
    entrée=pd.DataFrame({'bain': ['vide','0.5 salle de bain', '3.5 salles de bain'],
                         'chambre': ['1 chambre', '5 chambres', '2 chambres'],
                         'voyageur': ['1 voyageur', '3 voyageurs' , '4 voyageurs'],
                         'lit' : ['1 lit', '4 lits', '3 lits']})
    calculé= chiffre_variable(entrée)
    attendu= pd.DataFrame({'bain': ['0.0','0.5', '3.5'],
                         'chambre': ['1', '5', '2'],
                         'voyageur': ['1', '3' , '4'],
                         'lit' : ['1', '4', '3']})
    assert all(calculé) == all(attendu)
    
def test_commentaire(): 
    entrée=pd.DataFrame({'Commentaire': ['(150 commentaires)','(10 commentaires)', 'vide']})
    calculé= commentaire(entrée)
    attendu=pd.DataFrame({'Commentaire': ['150','10', '0']})
    
def test_note():
    entrée= pd.DataFrame({'Note': ['4,5','2,9', 'vide']})
    calculé= note(entrée) 
    attendu= pd.DataFrame({'Note': ['4.5','2.9', '0']})
    
def test_prix():
    entrée= pd.DataFrame({'Prix': ['À partir de 150€','1\u202f 250€', 'vide']})
    calculé= prix(entrée)
    attendu= pd.DataFrame({'Prix': ['150','1 250€']})
    assert all(calculé) == all(attendu)
    
def test_doublons(): 
    entrée=pd.DataFrame({'logement' : ['appartement', 'appartement', 'bateau'],
                         'Note' : ['4.5', '4.5', '3.6'],
                         'Commentaire' : ['150', '150', '10'],
                         'Prix': ['69','69', '80']})
    calculé=doublons(entrée)
    attendu= pd.DataFrame({'logement' : ['appartement', 'bateau'],
                         'Note' : ['4.5', '3.6'],
                         'Commentaire' : ['150', '10'],
                         'Prix': ['69', '80']})
    calculé=calculé.reset_index()
    calculé=calculé.drop("index",axis=1)
    assert all(calculé.reset_index()) == all(attendu)