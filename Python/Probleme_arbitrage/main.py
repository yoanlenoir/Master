import tkinter as tk
from tkinter import ttk
from fonctions import liste_meilleur_chemin

"""
TOUS LES ELEMENTS SONT PLACES GRACE A UNE GRID : 
    
    grid (column = ** , row = **, sticky="ew")
    ** : n° de colonne ou de ligne 
    sticky="ew" : l'élément prend toute la largeur de la page , et est centré 
    
les FRAME (zoneWelcome,zoneEntryMoneyNumber ... )  permettent de créer des "blocks" indépendants (plus facile pour positionner les éléments)
    
"""


class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.childWindow = None
        self.master = master
        self.grid()
        self.create_page()

    def create_welcome_text(self):
        """
        Methode permettant d'afficher le texte de bienvenu
        :return:
        """
        zoneWelcome = tk.Frame(self)

        title = tk.Label(zoneWelcome)
        title["text"] = "Bienvenue sur cet outil !"
        title.config(font=("Arial", 20))
        title.grid(column=0, row=0, sticky="ew")

        text = tk.Label(zoneWelcome)
        text["text"] = "Laissez vous guider"
        text.grid(column=0, row=1, sticky="ew")

        zoneWelcome.grid(column=0, row=0, padx=100)

    def create_page(self):
        """
        Methode permettant d'affiche la premiere page :
        - entry permettant de renseigner le nombre de monnaie
        - button permettant de valider le nombre de monnaie et d'affciher les entry correspondant
        :return:
        """
        self.create_welcome_text()

        zoneEntryMoneyNumber = tk.Frame(self)
        self.label_money = tk.Label(zoneEntryMoneyNumber)
        self.label_money["text"] = "Nombre de monnaie"
        self.label_money.grid(column=0, row=0, sticky="ew")

        self.money_number = tk.Entry(zoneEntryMoneyNumber)
        self.money_number.grid(column=1, row=0, sticky="ew")

        self.valid = tk.Button(zoneEntryMoneyNumber)
        self.valid["text"] = "Valider le nombre de monnaie"

        """
        Appel de la fonction createList lors du clique sur le bouton
        """
        self.valid["command"] = self.createList
        self.valid.grid(column=0, row=1, columnspan=5, sticky="ew")
        zoneEntryMoneyNumber.grid(column=0, row=1, pady=20, padx=100, sticky="ew")

    def createList(self):
        """
        Affiche la liste d'entry pour renseigner toutes les monnaies
        :return:
        """
        zoneListMoney = tk.Frame(self)
        self.money_number['state'] = 'disabled'
        self.valid['state'] = "disabled"
        value = int(self.money_number.get())
        self.moneys = []
        for i in range(0, value):
            temp = tk.Entry(zoneListMoney)
            temp.grid(column=0, row=i, sticky="ew")
            self.moneys.append(temp)
        self.valid = tk.Button(zoneListMoney)
        self.valid["text"] = "Valider les monnaies"
        """
                Appel de la fonction createMatrix lors du clique sur le bouton
        """
        self.valid["command"] = self.createMatrix
        self.valid.grid(column=0, row=i + 1, sticky="ew")
        zoneListMoney.grid(column=0, row=2, pady=20, padx=100, sticky="ew")

    def createMatrix(self):
        """
        Prepare la liste de monnaie puis appelle la focniton createMatrixInWindow
        :return:
        """
        value = int(self.money_number.get())
        self.valid['state'] = "disabled"
        values = []
        for i in range(0, value):
            values.append(self.moneys[i].get())
            self.moneys[i]['state'] = 'disabled'

        """
           Creation d'une nouvelle fenetre
        """
        newWindow = tk.Toplevel(self)
        self.createMatrixInWindow(newWindow, values)

    def createMatrixInWindow(self, window, values):
        """
        Affiche la matrice permettant de rentrer les taux de change
        :param window: Nouvelle fenetre dans laquelle il faut créer la matrice
        :param values: Liste des monnaies
        :return:
        """
        self.childWindow = window
        zoneMatrix = tk.Frame(window)
        self.matrix = []
        for i in range(0, len(values)):
            self.matrix.append([])
            temp = tk.Label(zoneMatrix, width=5)
            temp["text"] = values[i]
            temp.grid(column=i + 1, row=0)
            for j in range(0, len(values)):
                if j == 0:
                    c = tk.Label(zoneMatrix, width=5)
                    c["text"] = values[i]
                    c.grid(column=0, row=i + 1)

                """
                    met la diagonale de la matrice à 1 et empeche l'utilisateur de modifier cette diagonale 
                """
                if i == j:
                    state = "disabled"
                    value = tk.StringVar(self, value="1")
                else:
                    state = "normal"
                    value = tk.StringVar(self, value="")

                temp = tk.Entry(zoneMatrix, textvariable=value, width=5)
                temp["state"] = state
                temp.grid(column=i + 1, row=j + 1)
                self.matrix[i].append(temp)

        zoneMatrix.grid(column=0, row=0, sticky="ew")

        """
            Creation du combobox permettant de renseigner la monnaie de départ + creation du boutton de validation
        """
        zoneValidation = tk.Frame(window)
        label = tk.Label(zoneValidation)
        label["text"] = "Selectionnez la monnaie de départ : "
        label.grid(column=0, row=0)

        self.combobox = ttk.Combobox(zoneValidation, values=values, state="readonly")
        self.combobox.grid(column=1, row=0)
        self.combobox.current(0)
        
        label=tk.Label(zoneValidation)
        label["text"] = "Sélectionnez le montant de l'échange : "
        label.grid(column=0, row=1)
        
        self.montant= tk.Entry(zoneValidation)
        self.montant.grid(column=1, row =1)

        """
            transforme le tableau de monnaie en tuple
        """
        self.currencies = tuple(values)
        valid = tk.Button(zoneValidation)
        valid["text"] = "Calculer"

        """
        Appel de la fonction calcul lors du clique sur le bouton 
        """
        valid["command"] = self.calcul
        valid.grid(column=1, row=2)
        zoneValidation.grid(column=0, row=2, sticky="ew")

    def calcul(self):
        """
        Calcul le chemin grace à toute les données rentrées par l'utilisteur :
            - taux de change
            - liste des monnaies
            - monnaie de départ
            - montant
        :return:
        """
        rates = []
        for i in range(0, len(self.matrix)):
            rates.append([])
            for j in range(0, len(self.matrix[i])):
                rates[i].append(float(self.matrix[j][i].get()))

        current = self.combobox.current()
        montant= int(self.montant.get())
        """
        Ajout de "FIN" dans le tuple de monnaie
        """
        self.currencies += ("FIN",)
        nameCurrent = self.combobox.get()
        taux = liste_meilleur_chemin(rates, self.currencies, nameCurrent, current, montant)
        """
            destruction du message de résultat s'il existe (permet de changer les taux de change et de recalculer le chemin)
        """
        if hasattr(self, 'result'):
            self.result.destroy()
        self.texte = tk.Label(self.childWindow)
        self.result = tk.Label(self.childWindow)
        self.chemin = tk.Label(self.childWindow)
        self.result_gain = tk.Label(self.childWindow)
        self.chemin_gain = tk.Label(self.childWindow)
        self.texte_gain = tk.Label(self.childWindow)
        if taux == "None":
            self.result[
                "text"] = "Pas d'échange possible ! (Le chemin fait perdre de l'argent)  :  0.0 " + nameCurrent + " pour "+ str(montant) +  nameCurrent
            self.chemin["text"] = ""
        else:
            self.texte["text"] = "Voici le meilleur chemin sans taxe à chaque échange"
            self.result["text"] = "Ce chemin rapporte " + str(taux[1]) + nameCurrent + " pour " + str(montant) + nameCurrent
            self.chemin["text"] = " --> ".join(taux[0])
        self.texte.grid(column=0, row=3, sticky="ew")
        self.result.grid(column=0, row=4, sticky="ew")
        self.chemin.grid(column=0, row=5, sticky="ew")
        
        if taux == "None":
            self.result_gain[
                "text"] = "Pas d'échange possible (Le chemin fait perdre de l'argent)  :  0.0 " + nameCurrent + " pour " + str (montant)+ nameCurrent
            self.chemin_gain["text"] = ""
        else:
            self.texte_gain["text"] = "Voici le meilleur chemin avec une taxe à chaque échange"
            self.result_gain["text"] = "Ce chemin rapporte " + str(taux[3]) + nameCurrent + " pour " + str(montant) + nameCurrent
            self.chemin_gain["text"] = " --> ".join(taux[2])
        self.texte_gain.grid(column=0, row=6, sticky="ew")
        self.result_gain.grid(column=0, row=7, sticky="ew")
        self.chemin_gain.grid(column=0, row=8, sticky="ew")


root = tk.Tk()
root.title("Problème d'arbitrage")
app = HomePage(master=root)
app.mainloop()
