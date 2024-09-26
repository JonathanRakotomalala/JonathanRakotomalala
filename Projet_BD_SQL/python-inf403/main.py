#!/usr/bin/python3

from utils import db

from tkinter import *
from tkinter import ttk
import tkinter as tk


def select_tous_les_donateurs(conn):
    """
    Affiche la liste de tous les donnateurs.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("""
                SELECT * 
                FROM Donateurs
                """)

    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)
        ecrit=ecrit+str(row)+"\n"
    return ecrit


        

def select_produit_non_donnee(conn):
    """Affiche la liste des produits non donnees"""
    cur = conn.cursor()
    cur.execute("""
                SELECT code_produit
                FROM Produits
                EXCEPT
                SELECT code_produit
                FROM ProduitsDons 
                """)
                
    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)
        ecrit=ecrit+str(row)
    return ecrit

def select_produit_transact(conn):
    """Affiche total produits"""
    cur = conn.cursor()
    cur.execute("""
                SELECT code_produit,designation,SUM(quantite_produit)
                FROM Produits JOIN Transactions USING (code_produit)
                GROUP BY code_produit,designation
                UNION 
                SELECT code_produit,designation,0
                FROM Produits
                WHERE code_produit NOT IN (
                                            SELECT code_produit
                                            FROM Transactions
                                            )
                """)
                
    rows = cur.fetchall()
    ecrit=""
    for row in rows:
           print(row)
           ecrit=ecrit+str(row)+"\n"
    return ecrit

def insere(conn,tabl,val):
    """Insertion dans une table"""
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO """+str(tabl)+""" VALUES """+str(val)
                )
    cur.execute("""SELECT * FROM """+str(tabl))
    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)  
        ecrit=ecrit+str(row)
def suppr(conn,tabl,val):
    """Suppression dans une table"""
    cur = conn.cursor()
    cur.execute("""
                DELETE FROM """+str(tabl)+""" WHERE """+str(val)
                )
    cur.execute("""SELECT * FROM """+str(tabl))                
    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)  
        ecrit=ecrit+str(row)
        
def maj(conn,tabl,val1,val2=""):
    """Mise a jour """
    cur = conn.cursor()
    if (val2==""):
        cur.execute("""
                    UPDATE """+str(tabl)+""" SET """+str(val1)
                    )
    elif (val2!=""):
        cur.execute("""
                    UPDATE """+str(tabl)+""" SET """+str(val1)+""" WHERE """+str(val2))
                    
    cur.execute("""SELECT * FROM """+str(tabl))
    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)  
        ecrit=ecrit+str(row)
    return ecrit
        
def vue(conn):
    """View des donnateurs et du beneficiaire qui a reçu les dons"""
    cur = conn.cursor()
    cur.execute("""
                CREATE VIEW Donations (id_donateur,nom,numero,produit,nom_produit,type,quantite,date_de_peremption,mois_restant) AS
               SELECT id_donateur,nom_donateur,id_don,code_produit,designation,type,quantite_produit,date_peremption, strftime('%m', 'now')-strftime('%m', date_peremption)+ (strftime('%Y', 'now')-strftime('%Y', date_peremption))*12 AS mois_restant
                FROM Donateurs JOIN Dons USING (id_donateur)
                JOIN ProduitsDons USING (id_don) 
                JOIN Produits USING (code_produit);		
                """)
    cur.execute("""
                SELECT *
                FROM Donations
                    """)


    rows = cur.fetchall()
    ecrit=""
    for row in rows:
        print(row)
        ecrit=ecrit+str(row)+"\n"
    cur.execute("""DROP VIEW "main"."Donations" """)
    return ecrit 

def nouveau_jeu(conn,jeu):
    """Importations d'un nouveau jeu de donnees"""
    try:
        db.mise_a_jour_bd(conn, "data/don_creation.sql")
        db.mise_a_jour_bd(conn,jeu)
        return "Jeu de donnees importé"
    except Exception:
        print("!!!!Erreur jeu de données!!!")
        return "!!!Erreur jeu de données!!!"
    

class App(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            
            

def main():
    # Nom de la BD à créer
    db_file = "data/plateforme_de_don.db"
    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)
    # Remplir la BD  
    print("1. On crée la bd et on l'initialise avec des premières valeurs.")
    db.mise_a_jour_bd(conn, "data/don_creation.sql")
    db.mise_a_jour_bd(conn, "data/don_inserts_ok.sql")
    #INTERFACE
    app=App()
    app.title("DB")
    #app.geometry('640x470')
    #Zone d'affichage
    zone=Label(app,width=100,height=36,text='Sortie',bg="lightcyan")
    zone.pack(side=LEFT)
    app.resizable(0,0)
    #Assignement des fonctions aux boutons de l'interface
    def changea():
        """bouton selection simple"""
        zone.config(text=select_tous_les_donateurs(conn))
    def changeb():
        """bouton selection avec operateur ensembliste"""
        zone.config(text=select_produit_non_donnee(conn))    
    def changec():
        """selection avec jointure"""
        zone.config(text=select_produit_transact(conn)) 
    def changee():
        """bouton creation insertion"""
        tabl=saisie1.get()
        val=saisie2.get()
        zone.config(text=insere(conn, tabl, val))
    def changef():
        """bouton suppression"""
        tabl=saisie3.get()
        val=saisie4.get()
        zone.config(text=suppr(conn, tabl, val))
    def changed():
        """bouton view"""
        zone.config(text=vue(conn))
    def changeg():
        """bouton update"""
        table=saisie5.get()
        val1=saisie6.get()
        val2=saisie7.get()
        zone.config(text=maj(conn,table,val1,val2))
    def changeh():
        """bouton importe jeu de donnees"""
        jeu=saisie8.get()
        jeu="data/"+jeu+".sql"
        zone.config(text=nouveau_jeu(conn,jeu))
    #Mise en place des boutons sur l'interface:
    #selection simple
    a=Button(app,width=23,height=1,text="a. Select. donateurs")
    a.pack(side=TOP)    
    a.config(command=changea)
    #selection avec opérateur ensembliste
    b=Button(app,width=23,height=1,text="b. Select. don non donnée")
    b.pack(side=TOP)
    b.config(command=changeb)
    #selection avec jointure
    c=Button(app,width=23,height=1,text="c. Select. produit transactionné")
    c.pack(side=TOP)
    c.config(command=changec)
    #vue
    d=Button(app,width=23,height=1,text="d. view")
    d.pack()
    d.config(command=changed)
    #insertion
    Label(app,text="table :",width=24,height=1,bg='powderblue').pack()
    saisie1=ttk.Entry(width=28)
    saisie1.insert(0,"")
    saisie1.pack()
    Label(app,text="valeurs à inserer:",width=24,height=1,bg='powderblue').pack()
    saisie2=ttk.Entry(width=28)
    saisie2.insert(0,"")
    saisie2.pack()
    e=Button(app,width=23,height=1,command=changee, text="e. insertion",bg='skyblue')
    e.pack()
    e.config(command = changee)
    #suppression
    saisie3=ttk.Entry(width=28)
    Label(app,text="table :",width=24,height=1,bg='lightsalmon').pack()
    saisie3.insert(0,"")
    saisie3.pack()
    saisie4=ttk.Entry(width=28)
    Label(app,text="valeurs à supprimer :",width=24,height=1,bg='lightsalmon').pack()
    saisie4.insert(0,"")
    saisie4.pack()
    f=Button(app,width=23,height=1, text="f. suppression",bg='lightsalmon3')
    f.pack()
    f.config(command = changef)
    #update d'une table
    saisie5=ttk.Entry(width=28)
    Label(app,text="table :",width=24,height=1,bg='seagreen').pack()
    saisie5.insert(0,"")
    saisie5.pack()
    saisie6=ttk.Entry(width=28)
    Label(app,text="attribut a modifier :",width=24,height=1,bg='seagreen').pack()
    saisie6.insert(0,"")
    saisie6.pack()
    saisie7=ttk.Entry(width=28)
    Label(app,text="condition :",width=24,height=1,bg='seagreen').pack()
    saisie7.insert(0,"")
    saisie7.pack()
    g=Button(app,width=23,height=1,text="g. Mise a jour",bg='palegreen4')
    g.pack()
    g.config(command=changeg)
    #importation jeu de donnees
    saisie8=ttk.Entry(width=28)
    Label(app,text="jeu de données :",width=24,height=1,bg='yellow2').pack()
    saisie8.insert(0,"")
    saisie8.pack()
    h=Button(app,width=23,height=1,text="h. Importe",bg='gold')
    h.pack()
    h.config(command=changeh)
    app.mainloop()


        

    
    
if __name__ == "__main__":
    main()
