"""Problème d'arbitrage

Variables: 
- rates
- currencies
- monnaie 
- index_monnaie
- montant

Fonctions:
- genere_dico
- genere_graph
- trouve_chemins
- genere_matrice_log
- genere_gain_chemin
- ajout_gain
- ordonne
- calcul_taxe_echange
- ajout_taxe
- liste_meilleur_chemin
- trouve_meilleur_gain
- trouve_meilleur_gain_taxe

"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from math import log

def genere_dico(currencies:List[str],index_monnaie:int)->dict:
    """Créer un dictionnaire de toutes les monnaies
    
    Exemple : 
     >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie = 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(genere_dico(currencies,index_monnaie))
    
    {'EUR': 0, 'ROU': 1, 'YEN': 2, 'FIN': 0}
    """
    dico={}
    for i in range(0,len(currencies)-1):
        dico[currencies[i]]= i
    dico[currencies[-1]]=index_monnaie
    return dico

def genere_graph(currencies:List[str],index_monnaie:int)->dict:
    """Genere un graph de tous les chemins possibles
    
    Exemple : 
    >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie = 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(genere_graph(currencies,index_monnaie))
    
    {'EUR': ('EUR', 'ROU', 'YEN'),
     'ROU': ('EUR', 'ROU', 'YEN', 'FIN'),
     'YEN': ('EUR', 'ROU', 'YEN', 'FIN'),
     'FIN': ()}
    """
    n=len(currencies)
    graph_tot=dict()
    for i in range(n): 
        graph_tot[currencies[i]]=currencies
    graph_tot[currencies[-1]]=()
    graph_tot[currencies[index_monnaie]]=currencies[:-1]
    return(graph_tot)

def trouve_chemins(graph:dict, depart: str,chemin=[])->List[List[str]]:
    """Trouve tous les chemins possible avec la monnaie de départ choisie
    
    Exemple : 
    >>> genere_graph(currencies,index_monnaie)=
    {'EUR': ('EUR', 'ROU', 'YEN'),
     'ROU': ('EUR', 'ROU', 'YEN', 'FIN'),
     'YEN': ('EUR', 'ROU', 'YEN', 'FIN'),
     'FIN': ()}
    >>> monnaie = 'EUR'
    >>> print (genere_graph(currencies,index_monnaie),monnaie)
    
    [['EUR', 'ROU', 'YEN', 'FIN'],
     ['EUR', 'ROU', 'FIN'],
     ['EUR', 'YEN', 'ROU', 'FIN'],
     ['EUR', 'YEN', 'FIN']]
    """
    chemin = chemin + [depart]
    if depart == 'FIN':
        return [chemin]
    if not depart in graph:
        return []
    chemins = []
    for node in graph[depart]:
        if node not in chemin:
            nvchemin = trouve_chemins(graph, node, chemin)
            for nouveau in nvchemin:
                chemins.append(nouveau)
    return chemins

def genere_matrice_log(rates: Tuple[Tuple[float]]) -> List[List[float]]:
    """Donne la matrice des taux de chance en logarithme
    """
    resultat = [[-log(noeud) for noeud in ligne] for ligne in rates]
    return resultat

def genere_gain_chemin(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int)->List[float]: 
    """Renvoie le gain de chaque chemin 
    """
    total=[]
    matrice=genere_matrice_log(rates)
    list_chemins=trouve_chemins(genere_graph(currencies,index_monnaie),depart)
    dico=genere_dico(currencies,index_monnaie)
    for chemin in list_chemins:
        ST=[]
        tot=[]
        taille=len(chemin)
        for i in range(taille-1):
            tot=matrice[dico[chemin[i]]][dico[chemin[i+1]]]
            i=i+1
            ST.append(tot)
        ST=sum(ST)
        ST=np.exp(ST)*montant
        total.append(ST)
    return(total)

def ajout_gain(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int):
    """Ajoute le gain pour chaque chemin
    
    Exemple : 
    >>> rates=[
    [1,46.45,130.14],
    [0.020,1,2.66],
    [0.0077,0.357,1]
]
    >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie= 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(ajout_gain(rates,currencies,monnaie,index_monnaie))
    
    [['EUR', 'ROU', 'YEN', 'FIN', 1.0510948782353873],
    ['EUR', 'ROU', 'FIN', 1.0764262648008607],
    ['EUR', 'YEN', 'ROU', 'FIN', 1.0761950392574433],
    ['EUR', 'YEN', 'FIN', 0.9979263091296289]]
    """
    chemins=trouve_chemins(genere_graph(currencies,index_monnaie),depart)
    gain=genere_gain_chemin(rates,currencies,depart,index_monnaie,montant)
    for n in range(len(gain)):
        chemins[n].append(gain[n])
    return chemins

def ordonne(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int):
    """ Ordonne les chemins par gain croissant
    """
    chemins_gain=ajout_gain(rates,currencies,depart,index_monnaie,montant)
    ordre=sorted(chemins_gain, key=lambda trajet: trajet[-1])
    return ordre

def calcul_taxe_echange(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int)->List[float]:
    """Renvoie les gains avec une taxe à chaque échange, pour chaque chemin
    """
    taxe=[]
    ordre=ordonne(rates,currencies,depart,index_monnaie,montant)
    if montant <200: 
        montant_taxe=0.008
    elif montant >499: 
        montant_taxe=0.001
    else: 
        montant_taxe=0.003
    for j in range(len(ordre)):
        taxe.append(ordre[j][-1]*(1-montant_taxe)**(len(ordre[j][:-1])-1))
    return taxe,montant_taxe


def ajout_final(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int):
    """ Ajoute le gain avec taxe pour chaque chemin 
    
    Exemple : 
    >>> rates=[
    [1,46.45,130.14],
    [0.020,1,2.66],
    [0.0077,0.357,1]
]
    >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie= 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(ajout_final(rates,currencies,monnaie,index_monnaie))
    
    [['EUR', 'YEN', 'FIN', 0.9979263091296289, 0.9919477326116333],
     ['EUR', 'ROU', 'YEN', 'FIN', 1.0510948782353873, 1.0416633755134195],
     ['EUR', 'YEN', 'ROU', 'FIN', 1.0761950392574433, 1.0665383121129202],
     ['EUR', 'ROU', 'FIN', 1.0764262648008607, 1.0699773950484388]]
    """
    ordre=ordonne(rates,currencies,depart,index_monnaie,montant)
    taxe=calcul_taxe_echange(rates,currencies,depart,index_monnaie,montant)[0]
    for n in range(len(ordre)):
        ordre[n].append(taxe[n])
    return ordre

def liste_meilleur_chemin(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant:int):
    final=ajout_final(rates,currencies,depart,index_monnaie,montant)
    taxe=calcul_taxe_echange(rates,currencies,depart,index_monnaie,montant)[0]
    MC_sansT=final[-1][:-2]
    MC_sansT[-1]=depart
    gain_MC_sansT=round(final[-1][-2],5)
    MC_avecT=final[taxe.index(max(taxe))][:-2]
    MC_avecT[-1]=depart
    gain_MC_avecT=round(max(taxe),5)
    return MC_sansT,gain_MC_sansT,MC_avecT,gain_MC_avecT

def trouve_meilleur_gain(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant)->List[str]:
    """ Resort le meilleur chemin sans taxe
    
    Exemple : 
    >>> rates=[
    [1,46.45,130.14],
    [0.020,1,2.66],
    [0.0077,0.357,1]
]
    >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie= 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(trouve_meilleur_gain(rates,currencies,monnaie,index_monnaie)[0])
    
    Ce chemin rapporte 1.07643 EUR pour 1 EUR
    ['EUR', 'ROU', 'EUR']
    """
    if liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[1]<montant:
        print("Pas d'échange possible ! Le meilleur chemin fait perdre  ", montant -
              liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[1], depart)
        return liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)
    else:
        print('Ce chemin rapporte', liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[1],depart,
              'pour', montant, depart)
        return liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)
        
def trouve_meilleur_gain_taxe(rates:Tuple[Tuple[float]],currencies:List[str],depart:str,index_monnaie:int,montant)->List[str]:
    """Resort le meilleur chemin avec une taxe
    
    Exemple : 
    >>> rates=[
    [1,46.45,130.14],
    [0.020,1,2.66],
    [0.0077,0.357,1]
]
    >>> currencies=('EUR', 'ROU', 'YEN','FIN')
    >>> monnaie= 'EUR'
    >>> index_monnaie=currencies.index(monnaie)
    >>> print(trouve_meilleur_gain_taxe(rates,currencies,monnaie,index_monnaie)[2])
    
    Ce chemin rapporte 1.06998 EUR pour 1 EUR
    ['EUR', 'ROU', 'EUR']
    """
    montant_taxe=calcul_taxe_echange(rates,currencies,depart,index_monnaie,montant)[1]
    if liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[3]<montant:
        print("Pas d'échange possible ! Le meilleur chemin fait perdre  ", round(montant - 
              liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[3],5) , depart, '\n Le montant de la taxe est de ' , montant_taxe*100,'%' )
        return liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)
    else:
        print('Ce chemin rapporte', liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)[3],depart,
              'pour', montant, depart, 'avec une taxe à ' ,montant_taxe*100, '%')

        return liste_meilleur_chemin(rates,currencies,depart,index_monnaie,montant)