"""
Applique de nombreux modèles de machine learning pour prédire les prix des logement Airbnb

Modèles présent dans le fichier : 
- Forêts aléatoire
- Réseaux de neuronnes
- Boosting 
- K plus proche de voisins
- SVR

Compris également : 
- Tableau comparatif de tous les modèles
- Tableau valeur du meilleur modèle 
- Tableau des résultats des prédiction
"""

import pandas as pd
import numpy as np
import json

from rich.table import Table

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import  DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor

Airbnb=pd.read_csv('base_Airbnb.csv',index_col=0  )
y = Airbnb.Prix
X = Airbnb.drop('Prix', axis=1)

X_tr, X_te, y_tr, y_te = train_test_split(X,y,test_size=0.33)

resultats=dict()

rf = Pipeline(
    [
        ("Norm", MinMaxScaler()),
        ("Reg", RandomForestRegressor()),
    ]
)

RF = GridSearchCV(
    rf,
    {
        'Norm__feature_range': [(-1., 1.), (0., 1.), (1., 2.)],
        "Reg__n_estimators": [30, 40, 50, 60, 70],
    },
    n_jobs=-1,
)
RF.fit(X_tr, y_tr)
resultats["Random Forest"] = RF

p = Pipeline(
    [
        ("Norm", MinMaxScaler()),
        ("Reg", MLPRegressor()),
    ]
)

MLP = GridSearchCV(
    p,
    {
        'Norm__feature_range': [(-1., 1.), (0., 1.), (1., 2.)],
        'Reg__hidden_layer_sizes': [(25, 25, 25), (50, 75, 50), (75, 100, 75)],
        "Reg__max_iter": [10000],
    },
n_jobs=-1,)
MLP.fit(X_tr, y_tr)
resultats["MLP"] = MLP

p = Pipeline(
    [
        ("Norm", MinMaxScaler()),
        ("Reg", GradientBoostingRegressor()),
    ]
)

boost = GridSearchCV(
    p,
    {
        'Norm__feature_range': [(0., 1.), (-1., 1.), (1., 2.), (1.5, 2.)],
        "Reg__n_estimators": [400, 500, 600, 700],
    },
    n_jobs=-1,
)
boost.fit(X_tr, y_tr)
resultats["Boosting"] = boost

p = Pipeline(
    [
        ("Norm", MinMaxScaler()),
        ("Reg", KNeighborsRegressor()),
    ]
)
KN = GridSearchCV(
    p,
    {
        'Norm__feature_range': [(-2., 1.), (-1., 1.), (0., 1.), (1.5, 3.)],
        "Reg__n_neighbors": range(4, 14, 2),
    },
    n_jobs=-1,
)
KN.fit(X_tr, y_tr)
resultats["KNeighbors"] = KN

p = Pipeline(
    [
        ("Norm", MinMaxScaler()),
        ("Reg", SVR()),
    ]
)

svr = GridSearchCV(
    p,
    {
        'Norm__feature_range': [(-1., 1.), (0., 1.), (1., 2.)],
        "Reg__C": [0.1 * 10 ** j for j in range(5)],
        "Reg__epsilon": [00.1 * 10 ** j for j in range(6)],
    },
    n_jobs=-1,
)
svr.fit(X_tr, y_tr)
resultats["SVR"] = svr

tbl = Table(
    title="Résumé des résultats de crossvalidation.",
    show_header=True,
)
tbl.add_column("Nom")
tbl.add_column("Score Cross validation")
tbl.add_column("Score entrainement")
tbl.add_column("Choix Hyperparamètres")
for nom, modele in resultats.items():
    tbl.add_row(
        nom, 
        f"{modele.best_score_:.2f}", 
        f"{modele.score(X_tr, y_tr):.2f}",
        str(modele.best_params_),
    )


meilleur_modele=resultats["Random Forest"]

best_t=Table()
best_t.add_column("Meilleur score")
best_t.add_column("Entrainement")
best_t.add_column("Test")
best_t.add_row(f"{RF.best_score_:2f}",
               f"{RF.score(X_tr, y_tr):2f}",
               f"{RF.score(X_te, y_te):2f}",
              )

y_true, y_pred = y_te , meilleur_modele.predict(X_te)
true=np.array(y_true)
pred=np.array(y_pred)
pred=np.around(pred, decimals=1)

ecart=list()
for i in range(len(true)):
    ecart.append(((pred[i]-true[i])/true[i])*100)
ecart=np.around(ecart, decimals=2)

t=Table(
    title="Une partie des résulats de la prédiction",
    show_header=True,
)
t.add_column("Réalite")
t.add_column("Prédiction")
t.add_column("Ecart")
for i in range(20):
    t.add_row(
        f"{true[i]:.2f}",
        f"{pred[i]:.2f}",
        f"{ecart[i]:.2f} %",
    )
