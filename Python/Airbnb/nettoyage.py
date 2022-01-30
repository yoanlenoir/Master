"""
Nettoie les données pour sortir une base de données prête à utiliser

Variables: 
- fichier .json 
- dataclass des annonces 

Fonction: 
- nettoyage
- caractéristiques
- chiffre_variable
- logement
- commentaire
- note 
- prix 
- doublons
- autre 
"""

from serde import deserialize, serialize
from serde.json import from_json
from typing import List
import pandas as pd
import re
import numpy as np
from dataclasses import dataclass

@serialize
@deserialize
@dataclass
class Annonce: 
    ville: str
    logement: str
    vendeur: str
    chambre: str
    voyageur: str
    lit : str
    bain: str
    Wifi : str
    Cuisine : str
    Lave : str
    Chauffage :str
    Parking: str
    Perle: str
    Note: float
    Commentaire: int
    Prix: int
    
def nettoyage(data, annonce : Annonce) :
    """Importe la base de données et regroupe toutes les fonctions du fichier. 
    """
    Airbnb = from_json (List[annonce],data)
    df=pd.DataFrame(Airbnb)
    df=caracteristiques(df)
    df=chiffre_variable(df)
    df=logement(df)
    df=commentaire(df)
    df=note(df)
    df=prix(df)
    df=doublons(df)
    df=autre(df)
    return df
    
def caracteristiques(df):
    """Permet de modfier les variables liées au caractéristiques du bien. 
    - Supprimer les éléments dans les listes
    - Règle les détails comme la virgule, les studios
    - Créer une variable 'salle de bain partagée'
    - Créer des booléens 
    """
    
    liste1=['voyageur','lit', 'bain','Wifi','Cuisine','Lave', 'Chauffage','Parking']
    for l in liste1 : 
        df[l]=df[l].str.get(0)
        df [l] = df [l]. replace (np.nan, 'vide')
        
    df['sdb_partage']= df['bain'].str.contains("partag")
    df.loc[df['chambre'].str.contains('Studio'), 'chambre'] = '0 chambre'
    df.loc[df['bain'].str.contains('Demi'), 'bain'] = '0.5 salle de bain'
    df.bain=df.bain.str.replace(",",".")
    
    liste2= ["Wifi","Cuisine","Lave","Chauffage","Parking"]
    for l in liste2: 
        df[l]=df[l].replace("vide",False)
        if l=="Lave": 
            df[l]=df[l].replace("Lave-linge",True)
        elif l=="Parking":
            df[l]=df[l].replace("Parking gratuit",True)
        else:
            df[l]=df[l].replace(l,True)
    return df

def chiffre_variable(df):
    """Modifie les variables qui renseignent un entier ou boolean. 
    - Conserve que les chiffres dans toutes les colonnes 
    
    Exemple: 
    entrée: ["2 chambres", 1.5 salle de bain]
    sortie: [2 , 1.5]
    """
    df.bain=df.bain.replace("vide","0")
    
    sdb=df.bain
    for i in range(df.bain.count()):
        for s in re.findall(r'-?\d+\.?\d*', sdb[i]):
            df.bain[i]=float(s)
    
        
    variables=['chambre','voyageur','lit']
    for variable in variables: 
        masque=(df[variable].str.replace(" ","").str.match(f"(.*){variable}") == False)
        df[variable].str.replace(" ","")[masque]
        masque = (df[variable].str.replace(" ","").str.match(f"^([0-9]+){variable}"))
        df = df[masque]
        df.reset_index(inplace=True)
        df.drop("index", axis=1, inplace=True)
        res = df[variable].str.replace(" ", "").str.extractall(f"([0-9]+){variable}")
        res.reset_index(inplace=True)
        df[variable] = res[0].astype(int)
    return df

def logement(df):
    """ Modifie la variable liée au logement
    - Supprime toutes les lignes où le vendeur n'est pas renseigné
    - Regroupe certaines classes.
    - Si le nombre de logement inférieure à 10, regroupement dans la classe 'autres'
    
    Ex: 
    entrée : ["logement entier - appartement", "chambre hôte" , "auberge de jeunesse"]
    sortie : ["appartement", "Hôtel/chambre d'hôte", "chambre partagée"]
    """
    df.drop(df.loc[df['vendeur']=='vide'].index, inplace=True)
    df.logement=df.logement.str.lower()
    
    df.loc[df['logement'].str.contains('appartement'), 'logement'] = 'appartement'
    df.loc[df['logement'].str.contains('entier'), 'logement'] = 'logement entier'
    df.loc[df['logement'].str.contains('hôte'), 'logement'] = 'Hôtel/chambre hôte'
    df.loc[df['logement'].str.contains('jeunesse'), 'logement'] = 'chambre partagée'
    df.loc[df['logement'].str.contains('péniche'), 'logement'] = 'bateau'
    
    tri = df.logement.value_counts().loc[lambda l : l<10]
    tri = tri.index.tolist()
    for t in tri: 
        df.loc[df.logement == t, "logement"] = "autres"
    return df

        
def commentaire(df):
    """ Nettoie la variable "Commentaire" pour ne garder que le nombre de commentaires. 
    """
    df.Commentaire=df.Commentaire.str.replace("commentaires","").str.replace("(","").str.replace(")","").str.replace("\u202f","")
    df.Commentaire=df.Commentaire.replace("vide","0")
    return df
    
def note(df):
    """ Nettoie la variable "Note", en modifiant la virgule par un point
    """
    df.Note=df.Note.replace("vide","0")
    df.Note=df.Note.str.replace(",",".")
    return df

def prix(df):
    """Nettoie la variable "Prix" pour ne conserver que le montant. 
    """
    df.Prix=df.Prix.str.replace("€","").str.replace("À partir de ","").str.replace("\u202f","")
    df.drop(df.loc[df['Prix']=='vide'].index, inplace=True)
    return df

def doublons(df):
    """ Supprime les doublons par rapport à quatres variables : "logement", "Note", "Commentaire", "Prix"
    """
    df=df.drop_duplicates(subset=['logement','Note','Commentaire','Prix'], keep='first')
    return df

def autre(df):
    df.Perle= df.Perle.replace("Oui", True).replace("Non", False)
    df[['Note','bain']]=df[['Note','bain']].astype(float)
    df[['Commentaire', 'lit', 'chambre', 'voyageur']]=df[['Commentaire', 'lit', 'chambre', 'voyageur']].astype(int)
    
    df=df*1
    df["lit/chambre"]=df.lit/df.chambre
    df["bain/voy"]=df.bain/df.voyageur
    df=df.replace([np.inf, -np.inf], 0)
    
    df=pd.get_dummies(df,columns=['vendeur','ville','logement'],drop_first=False)
    df.to_csv("base_Airbnb.csv",encoding="utf8")