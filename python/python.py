# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path
from ctypes import *
##
#@file python.py
#@author COUSAERT Flavien et CHARRONDIERE Romain
#@version 1.0
#@date 30 décembre 2021
def open_dll(name='libcreneau_valide.dll'):
    ##
	#@brief Cette fonction permet d'ouvrir l'algorithme en C
	#
	#@return le chemin d'accès à l'algorithme
    lib_path = Path().absolute().parent
    lib_path = lib_path / 'c' / 'creneau_valide' / 'bin' / 'Release' / name
    return CDLL(lib_path.as_posix())

def SaisirUE():
    ##
	#@brief Cette fonction permet de saisir toutes les informations d'une UE en appelant d'autres fonctions
	#@details Fonctions appelées : SaisirNomComplet() ; SaisirDesc() ; SaisirEffectif() ; SaisirCreneaux()
	#
	#@return UE avec son nom complet, sa description, son effectif et ses créneaux

    UE={'nomcomplet':0,'Description':0,'Effectif':0,'Creneaux':0}
    UE['nomcomplet']=SaisirNomComplet()
    UE['Description']=SaisirDesc()
    UE['Effectif']=SaisirEffectif()
    UE['Creneaux']=SaisirCreneaux()
    
    return UE

def SaisirNom(): 
    ##
	#@brief Cette fonction permet de saisir le nom d'une UE
	#@details Vérifie la contrainte sur le nom de l'UE (au moins deux lettres majuscules puis 2 chiffres)
	#
	#@return le nom de l'UE
    nomvalide=False
    while nomvalide==False:
        nomUE=input("Saisir le nom de d'UE : ")
        listnomUE=list(nomUE)
        i=0
        while listnomUE[i]<='Z' and listnomUE[i]>='A':
            i=i+1
            if listnomUE[i]<='9' and listnomUE[i]>='0' and listnomUE[i+1]>='0' and listnomUE[i+1]<='9' and len(listnomUE)==i+2:
                nomvalide=True
    return nomUE
def SaisirNomComplet():
    ##
	#@brief Cette fonction permet de saisir le nom complet d'une UE
	#@details Vérifie la contrainte sur le nom complet de l'UE (moins de 50 caractères)
	#
	#@return le nom complet de l'UE
    NomComplet=(input("Saisir le nom complet de l'UE : "))
    #Vérification des contraintes sur le nom complet de l'UE, qui doit comporter moins de 50 caractères
    correct=False
    while correct==False:
        if len(NomComplet)<=50:
            correct=True
        else:
            NomComplet=input("La saisie est mauvaise, resaisir le nom complet de l'UE (- de 50 caractères) : ")
    return NomComplet

def SaisirDesc():
    ##
	#@brief Cette fonction permet de saisir la description d'une UE
	#@details Vérifie la contrainte sur la description de l'UE (moins de 500 caractères)
	#
	#@return la description de l'UE
    Description=input("Saisir la description de l'UE : ")
    #Vérification des contraintes sur la description de l'UE, qui doit comporter moins de 500 caractères
    correct=False
    while correct==False:
        if len(Description)<=500:
            correct=True
        else:
            Description=input("La saisie est mauvaise, resaisir la description de l'UE (- de 500 caractères) : ")
    return Description

def SaisirEffectif():
    ##
	#@brief Cette fonction permet de saisir l'effectif d'une UE
	#@details Vérifie la contrainte sur l'effectif de l'UE (>= 1)
	#
	#@return le 'effectif de l'UE
    Effectif=int(input("Saisir l'effectif de l'UE : "))
    correct=False
    while correct==False:
        if Effectif >= 1:
            correct=True
        else:
            Effectif=int(input("La saisie est mauvaise, resaisir l'effectif (au moins 1) : "))
    return Effectif
def SaisirCreneaux():
    ##
	#@brief Cette fonction permet de saisir plusieurs créneaux en appelant plusieurs fois une autre fonction qui permet de saisir un créneau en vérifiant que ce dernier est compatible avec les autres
	#@details Fonctions appelées : SaisirCreneau() ; VerifCreneau() avec en paramètre d'entrée la liste des créneaux déjà saisis pour cette UE
	#
	#@return la liste des créneaux
    ListeCreneaux=[]
    creneauajout=input("Voulez vous ajouter un créneau ? (oui ou non) ")
    i=0
    while creneauajout == 'oui':
        if i<1:
            ListeCreneaux.append(SaisirCreneau())
        else:
            ListeCreneaux.append(VerifCreneau(ListeCreneaux))
        i=i+1
        creneauajout=input("Voulez vous ajouter un créneau ? ")
    return ListeCreneaux
def VerifCreneau(ListeCreneaux):
    ##
	#@brief Cette fonction permet de saisir un créneau en appelant la fonction SaisirCreneau()
	#@details Vérifie que le créneau saisi est compatible avec les autres créneaux déjà saisis pour cette UE
	#
    #@param La liste des créneaux déjà saisis
    #
	#@return le créneau ajouté
    NouveauCreneau = SaisirCreneau()
    valide = False
    while valide == False:
        valide = True
        for j in range(len(ListeCreneaux)):
            if NouveauCreneau['Jour'] == ListeCreneaux[j]['Jour'] and ((NouveauCreneau['Semaine'] == ListeCreneaux[j]['Semaine']) or NouveauCreneau['Semaine']== 'tout' or ListeCreneaux[j]['Semaine']== 'tout'):
                if (NouveauCreneau['HeureD'] >= ListeCreneaux[j]['HeureD'] and NouveauCreneau['HeureD'] < ListeCreneaux[j]['HeureF']) or (NouveauCreneau['HeureF'] > ListeCreneaux[j]['HeureD'] and NouveauCreneau['HeureF'] <= ListeCreneaux[j]['HeureF']) or (NouveauCreneau['HeureF'] > ListeCreneaux[j]['HeureF'] and NouveauCreneau['HeureD'] < ListeCreneaux[j]['HeureD']):
                    valide = False
        if valide == False : 
            print("l'Horaire de ce créneau n'est pas valide. Veuillez resaisir ce créneau : ")
            NouveauCreneau = SaisirCreneau()
    return NouveauCreneau       
        
    
def SaisirCreneau():
    ##
	#@brief Cette fonction permet de saisir toutes les informations d'un créneau
	#@details Vérifie que les informations du créneau correspondent aux contraintes de forme : Jour compris entre 1 et 7 ; Type de la forme TD, TP ou Cours ; HeureD et HeureF de la forme HH:mm avec HeureF > HeureD et compris entre 08:00 et 20:00 ; Semaine de la forme A, B ou tout.
    #
	#@return le créneau ajouté
    Creneau={'Type' : 0, 'Jour':0, 'HeureD':0, 'HeureF':0, 'Semaine':0 }
    c1=False
    Creneau["Type"]=input("Est-ce un Cours, un TD ou un TP ? ")
    while c1==False:
        if Creneau["Type"]=='Cours' or Creneau["Type"]=='TP' or Creneau["Type"]=='TD':
            c1=True
        else:
            Creneau["Type"]=input("Mauvaise saisie, veuillez entrer Cours ou TP ou TD : ")
    c2=False
    Creneau["Jour"]=input("Quel jour ce a lieu ? (1 à 7 pour lundi à dimanche) : ")
    while c2==False:
        if Creneau["Jour"]=='1' or Creneau["Jour"]=='2' or Creneau["Jour"]=='3' or Creneau["Jour"]=='4' or Creneau["Jour"]=='5' or Creneau["Jour"]=='6' or Creneau["Jour"]=='7':
            c2=True
        else:
            Creneau["Jour"]=input("Mauvaise saisie, un chiffre de 1 à 7: ")
    c3=False 
    Creneau["HeureD"]=str(input("Quelle est l'heure de début ? (au format HH:mm) : "))
    while c3==False:
        if len(Creneau["HeureD"])!=5:
            Creneau["HeureD"]=input("Mauvaise saisie, Quelle est l'heure de début ? (au format HH:mm) ")
        elif '08:00'<=Creneau['HeureD']<='20:00' and '0'<=Creneau["HeureD"][0]<='2' and '0'<=Creneau["HeureD"][1]<='9' and '0'<=Creneau["HeureD"][3]<='5' and '0'<=Creneau["HeureD"][4]<='9' and Creneau["HeureD"][2]==':' : 
            c3=True
        else:
            Creneau["HeureD"]=input("Mauvaise saisie, Quelle est l'heure de début ? (au format HH:mm) ")
    c4=False 
    Creneau["HeureF"]=str(input("Quelle est l'heure de fin ? (au format HH:mm) "))
    while c4==False:
        if len(Creneau["HeureF"])!=5:
            Creneau["HeureF"]=input("Mauvaise saisie, Quelle est l'heure de fin ? (au format HH:mm) ")
        elif '08:00'<=Creneau['HeureF']<='20:00' and Creneau["HeureF"] > Creneau["HeureD"] and '0'<=Creneau["HeureF"][0]<='2' and '0'<=Creneau["HeureF"][1]<='9' and '0'<=Creneau["HeureF"][3]<='5' and '0'<=Creneau["HeureF"][4]<='9' and Creneau["HeureF"][2]==':' :
            c4=True
        else:
            Creneau["HeureF"]=input("Mauvaise saisie, Quelle est l'heure de fin ? (au format HH:mm) ")
    c5=False
    Creneau["Semaine"]=input("Quand ce créneau est-il utilisé ? Semaine A, B ou tout ? ")
    while c5==False:
        if Creneau["Semaine"]=='A' or Creneau["Semaine"]=='B' or Creneau["Semaine"]=='tout':
            c5=True
        else:
            Creneau["Semaine"]=input("Mauvaise saisie, quand ce créneau est-il utilisé ? Semaine A, B ou tout ? ")
    return Creneau
def suppUE():
    ##
	#@brief Cette fonction permet de supprimer une UE du catalogue
	#@details Vérifie que l'UE est déjà dans le catalogue et la supprime si c'est le cas.
	#
	#@return La fonction ne retourne rien mais modifie le fichier .json du catalogue
    nomUE=input("Saisir le nom de l'UE à supprimer : ")
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    if nomUE in UEs:
        del UEs[nomUE]
    else:
        print("Cette Ue n'est pas dans le catalogue")
    with open("listeUEs.json", "w") as jsonFile:
        json.dump(UEs, jsonFile, indent=4)
def modifUE():
    ##
	#@brief Cette fonction permet de modifier une information au choix d'une UE
	#@details Vérifie que l'UE est déjà dans le catalogue et la modifie dans avec l'information choisie par l'utilisateur
	#
	#@return La fonction ne retourne rien mais modifie le fichier .json du catalogue
    modif_UE=input('Quelle UE voulez-vous modifier ? ' )
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    if modif_UE in UEs:

        Choixmodif=input("Que voulez-vous modifier ? nom, nom complet, description, effectif ou créneau : ")
        while Choixmodif != 'nom' and Choixmodif != 'nom complet' and Choixmodif != 'description' and Choixmodif != 'effectif' and Choixmodif != 'créneau':
            Choixmodif=input("Saisie nom valide, veuillez saisir l'und es choix suivants : nom, nom complet, description, effectif ou créneau : ")
        if Choixmodif =='nom' :    
            UEs[SaisirNom()]= UEs.pop(modif_UE)
            with open("listeUEs.json", "w") as jsonFile:
                json.dump(UEs, jsonFile, indent=4)
        elif Choixmodif == "nom complet":
            UEs[modif_UE]['nomcomplet']=SaisirNomComplet()
            with open("listeUEs.json", "w") as jsonFile:
                json.dump(UEs, jsonFile, indent=4)
        elif Choixmodif == "description":
            UEs[modif_UE]['Description']=SaisirDesc()
            with open("listeUEs.json", "w") as jsonFile:
                json.dump(UEs, jsonFile, indent=4)
        elif Choixmodif == "effectif":
            UEs[modif_UE]['Effectif']=SaisirEffectif()
            with open("listeUEs.json", "w") as jsonFile:
                json.dump(UEs, jsonFile, indent=4)
        elif Choixmodif == "créneau":
            print("Voici la liste des créneaux actuels pour ", modif_UE," : ")
            for i in range(len(UEs[modif_UE]['Creneaux'])):
                print("Créneau ", i+1," : ")
                print("Type :",UEs[modif_UE]['Creneaux'][i]["Type"])
                print("Jour :",UEs[modif_UE]['Creneaux'][i]["Jour"])
                print("Heure de début :",UEs[modif_UE]['Creneaux'][i]["HeureD"])
                print("Heure de fin :",UEs[modif_UE]['Creneaux'][i]["HeureF"])
                print("Semaine :",UEs[modif_UE]['Creneaux'][i]["Semaine"])
                print('\n')
            Choixmodifcre = input("Que voulez-vous faire ? Ajouter ou supprimer un créneau ? ")
            while Choixmodifcre != 'ajouter' and Choixmodifcre != 'supprimer':
                Choixmodifcre = ("Saisie incorrecte. Que voulez-vous faire ? Ajouter ou supprimer un créneau ? ")
            if Choixmodifcre == 'ajouter':
                if len(UEs[modif_UE]['Creneaux']) == 0:
                    UEs[modif_UE]['Creneaux'].append(SaisirCreneau())
                else :
                    UEs[modif_UE]['Creneaux'].append(VerifCreneau(UEs[modif_UE]['Creneaux']))
            elif Choixmodifcre == 'supprimer':
                numcre = input("Quel créneau voulez-vous supprimer ? ")
                while numcre < '1' or numcre > str(len(UEs[modif_UE]['Creneaux'])):
                    numcre = input("Ce créneau n'existe pas. Quel créneau voulez-vous supprimer ? ")
                del UEs[modif_UE]['Creneaux'][int(numcre)-1]
            with open("listeUEs.json", "w") as jsonFile:
                json.dump(UEs, jsonFile, indent=4)
    else :
        print("Cette UE n'est pas dans le catalogue")

def visu_ensemble_UE():
    ##
	#@brief Cette fonction permet de visualiser toutes les UEs du catalogue en même temps.
	#
	#@return La fonction ne retourne rien mais affiche des informations
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    for noms in UEs:
        print(noms, ' : ')
        print("Nom complet : ", UEs[noms]['nomcomplet'])
        print("Description : ", UEs[noms]['Description'])
        print("Effectif : ", UEs[noms]['Effectif'])
        print("Créneaux : ")
        for i in range(len(UEs[noms]['Creneaux'])):
            print("Créneau ", i+1," : ")
            print("")
            print("Type :", UEs[noms]['Creneaux'][i]["Type"])
            print("Jour :",UEs[noms]['Creneaux'][i]["Jour"])
            print("Heure de début :",UEs[noms]['Creneaux'][i]["HeureD"])
            print("Heure de fin :",UEs[noms]['Creneaux'][i]["HeureF"])
            print("Semaine :",UEs[noms]['Creneaux'][i]["Semaine"])
            print('\n')
        print("\n ---------------------------------- \n")
def visu_une_UE():
    ##
	#@brief Cette fonction permet de visualiser les informations d'une UE du catalogue
	#@details Vérifie que l'UE est déjà dans le catalogue et l'affiche si c'est le cas.
	#
	#@return La fonction ne retourne rien mais affiche des informations
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    visu_UE=input('Quelle UE voulez-vous visualiser? ' )
    if visu_UE in UEs:
        print(visu_UE, ' : ')
        print("Nom complet : ", UEs[visu_UE]['nomcomplet'])
        print("Description : ", UEs[visu_UE]['Description'])
        print("Effectif : ", UEs[visu_UE]['Effectif'])
        print("Créneaux : ")
        for i in range(len(UEs[visu_UE]['Creneaux'])):
            print("Créneau ", i+1," : ")
            print("")
            print("Type :", UEs[visu_UE]['Creneaux'][i]["Type"])
            print("Jour :",UEs[visu_UE]['Creneaux'][i]["Jour"])
            print("Heure de début :",UEs[visu_UE]['Creneaux'][i]["HeureD"])
            print("Heure de fin :",UEs[visu_UE]['Creneaux'][i]["HeureF"])
            print("Semaine :",UEs[visu_UE]['Creneaux'][i]["Semaine"])
            print('\n')
    else:
        print("Cette UE n'est pas dans le catalogue")
        
def Inscrireetu():
    ##
    #@brief Cette fonction permet d'inscrire le numéro étudiant dans le .json.
    #@details Vérifie les contraintes:  -si le numéro d'étudiant est déjà utiliser (Mauvaise Saisie) et le numéro d'étudiant est au bon format ( 5 chiffres). 
    # 
    #
    #@return La fonction ne retourne rien, elle inscrit simplement le numéro étudiant dans le .json.
    num_etudiant=input("Entrer votre numéro étudiant: ")
    listnumetu=list(num_etudiant)
    with open("listeetus.json", "r+") as f:         
        numetus = json.load(f)
    numvalid=False
    while numvalid==False:
        if len(listnumetu)!=5:
            num_etudiant=input("Numero non valide, saisir votre numéro étudiant (5 chiffres) : ")
            listnumetu=list(num_etudiant)
        else:
            numvalid=True
            for i in range(5):
                if listnumetu[i]>'9' or listnumetu[i]<'0':
                    numvalid=False
            if numvalid==False:
                num_etudiant=input("Numero non valide, saisir votre numéro étudiant (5 chiffres) : ")
                listnumetu=list(num_etudiant)
    if num_etudiant in numetus :
         num_etudiant=input("Cet étudiant existe déjà.")
    else : 
        numetus[num_etudiant]=InscriptionsUE()
        with open("listeetus.json", "w") as f:
            json.dump(numetus, f, indent=4)
def InscriptionsUE():
    ##
    #@brief Cette fonction permet de choisir les UEs que l'étudiants va prendre. 
    #@details Vérifie les contraintes: l'étudiant peut choisir au maximum 7 UEs, les UEs doivent être compatibles entre elles au niveau des créneaux horaires, il doit rester de la place dans l'UE et UE saisie ne doit pas être déjà séléctionnée. 
    #
    #@return La fonction ne retourne rien, la liste d'UEs selectionnées est inscrite dans le .json.
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    with open("listeetus.json", "r+") as f:         
        numetus = json.load(f)
    nbUEs = 0
    listeUEs = []
    UEchoisie = input("Choisir une UE à ajouter, saisir stop pour arrêter la saisie des UEs. 7 UEs maximum : ")
    while (UEchoisie in UEs) == False and UEchoisie != 'stop':
        UEchoisie = input("Cette UE n'est pas dans le catalogue, saisir une autre UE ou stop pour arrêter : ")
    while nbUEs < 7 and UEchoisie != 'stop' :
        if (UEchoisie in listeUEs) == False:
            effectifactuel = 0
            for etu in numetus:
                if UEchoisie in numetus[etu]:
                    effectifactuel = effectifactuel+1
            if effectifactuel < UEs[UEchoisie]['Effectif']:     
                if nbUEs == 0:
                    listeUEs.append(UEchoisie)
                    nbUEs = nbUEs +1
                else:
                    CreneauxCompatibles = True  
                    ListeUEIncompatibles = []
                    for i in listeUEs: 
                        UEdejaincompatible = False
                        for j in range(len(UEs[i]['Creneaux'])): # ==> Comparaison avec tous les créneaux de toutes les UEs
                            for k in range(len(UEs[UEchoisie]['Creneaux'])): # ==> Comparaison de chaque créneau de l'UE choisie (avec du coup tous les créneaux de toutes les UEs déjà choisies)
                                #Appel de l'algorithme C, qui renvoie  True si les deux créneaux sont compatibles, False sinon.  
                                Jour1 = c_wchar(UEs[i]["Creneaux"][j]['Jour'])
                                HeureD1 = c_wchar_p(UEs[i]["Creneaux"][j]['HeureD'])
                                HeureF1 = c_wchar_p(UEs[i]["Creneaux"][j]['HeureF'])
                                Semaine1 = c_wchar(UEs[i]["Creneaux"][j]['Semaine'][0])
                                Jour2 = c_wchar(UEs[UEchoisie]["Creneaux"][k]['Jour'])
                                HeureD2 = c_wchar_p(UEs[UEchoisie]["Creneaux"][k]['HeureD'])
                                HeureF2 = c_wchar_p(UEs[UEchoisie]["Creneaux"][k]['HeureF'])
                                Semaine2 = c_wchar(UEs[UEchoisie]["Creneaux"][k]['Semaine'][0])          
                                Compatibilité = creneau_valide.CompatibiliteCreneaux(Jour1, HeureD1, HeureF1, Semaine1, Jour2, HeureD2, HeureF2, Semaine2)
                                #Fin de l'appel
                                if Compatibilité == False and UEdejaincompatible == False:
                                    UEdejaincompatible = True #Pour éviter que l'UE s'inscrive deux fois dans la liste
                                    CreneauxCompatibles = False
                                    ListeUEIncompatibles.append(i)
                    if CreneauxCompatibles == True :
                        listeUEs.append(UEchoisie)
                        nbUEs = nbUEs +1
                    else:
                        print("Les horaires de cette UE ne correspondent pas aux UEs suivantes choisies précédemment : ")
                        for i in range(len(ListeUEIncompatibles)):
                            print(ListeUEIncompatibles[i])
            else :
                print("Cette UE est complète")
            if nbUEs < 7:
                UEchoisie = input("Choisir une UE à ajouter, saisir stop pour arrêter la saisie des UEs. 7 UEs maximum : ")
                while (UEchoisie in UEs) == False and UEchoisie != 'stop':
                    UEchoisie = input("Cette UE n'est pas dans le catalogue, saisir une autre UE ou stop pour arrêter : ")
            else :
                print("Le nombre maximum d'UE a été choisi")
        else:
            print("Cette UE a déjà été choisie par l'étudiant")
            UEchoisie = input("Choisir une UE à ajouter, saisir stop pour arrêter la saisie des UEs. 7 UEs maximum : ")
            while (UEchoisie in UEs) == False and UEchoisie != 'stop':
                UEchoisie = input("Cette UE n'est pas dans le catalogue, saisir une autre UE ou stop pour arrêter : ")
    return listeUEs
def modifUEetu():
    ##
    #@brief Cette fonction permet de choisir le numéro étudiants dans le .json dont on souhaite modifier les UEs.
    #@details Vérifie si le numéro étudiants a déjà été saisie.
    num_etudiant=input("Entrer votre numéro étudiant: ")
    with open("listeetus.json", "r+") as f:         
        numetus = json.load(f)
    if num_etudiant in numetus :
        numetus[num_etudiant]=modifchoixUE(numetus[num_etudiant])
        with open("listeetus.json", "w") as f:
            json.dump(numetus, f, indent=4)
    else : 
        print("Cet étudiant n'est pas encore inscrit")
def modifchoixUE(listeUEs):
    ##
    #@brief Cette fonction permet de modifier les UEs selectionnées par un étudiant.
    #@details Vérifie les contraintes: l'étudiant peut choisir au maximum 7 UEs, les UEs doivent être compatibles entre elles au niveau des créneaux horaires, il doit rester de la place dans l'UE et UE saisie ne doit pas être déjà selectionner. 
    #
    #@param listeUEs est la liste des UEs choisit par l'étudiant.
    #
    #@return La fonction ne retourne rien, la liste modifiée d'UEs selectionnées est inscrite dans le .json.
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    with open("listeetus.json", "r+") as f:         
            numetus = json.load(f)
    nbUEs = len(listeUEs)
    Choixmodif = input("Que voulez vous faire ? supprimer une UE ou ajouter une UE ? Ou ne rien faire ? ")
    while Choixmodif != 'ajouter' and Choixmodif != 'supprimer' and Choixmodif != 'rien':
        Choixmodif = input("Choix non valide, veuillez choisir 'ajouter', 'supprimer' ou 'rien' : ")
    while Choixmodif != 'rien' :
        if Choixmodif == 'ajouter':
            if nbUEs < 7 :
                UEchoisie = input("Choisir une UE à ajouter, saisir stop pour arrêter la saisie des UEs. 7 UEs maximum : ")
                while (UEchoisie in UEs) == False and UEchoisie != 'stop':
                    UEchoisie = input("Cette UE n'est pas dans le catalogue, saisir une autre UE ou stop pour arrêter : ")
                if UEchoisie != 'stop' :
                    if (UEchoisie in listeUEs) == False:
                        effectifactuel = 0
                        for etu in numetus:
                            if UEchoisie in numetus[etu]:
                                effectifactuel = effectifactuel+1
                        if effectifactuel < UEs[UEchoisie]['Effectif']:        
                            if nbUEs == 0:
                                listeUEs.append(UEchoisie)
                                nbUEs = nbUEs +1
                            else:
                                CreneauxCompatibles = True
                                ListeUEIncompatibles = []
                                for i in listeUEs:
                                    UEdejaincompatible = False
                                    for j in range(len(UEs[i]['Creneaux'])):
                                        for k in range(len(UEs[UEchoisie]['Creneaux'])):
                                            Jour1 = c_wchar(UEs[i]["Creneaux"][j]['Jour'])
                                            HeureD1 = c_wchar_p(UEs[i]["Creneaux"][j]['HeureD'])
                                            HeureF1 = c_wchar_p(UEs[i]["Creneaux"][j]['HeureF'])
                                            Semaine1 = c_wchar(UEs[i]["Creneaux"][j]['Semaine'][0])
                                            Jour2 = c_wchar(UEs[UEchoisie]["Creneaux"][k]['Jour'])
                                            HeureD2 = c_wchar_p(UEs[UEchoisie]["Creneaux"][k]['HeureD'])
                                            HeureF2 = c_wchar_p(UEs[UEchoisie]["Creneaux"][k]['HeureF'])
                                            Semaine2 = c_wchar(UEs[UEchoisie]["Creneaux"][k]['Semaine'][0])          
                                            Compatibilité = creneau_valide.CompatibiliteCreneaux(Jour1, HeureD1, HeureF1, Semaine1, Jour2, HeureD2, HeureF2, Semaine2)
                                            if Compatibilité == False and UEdejaincompatible == False:
                                                UEdejaincompatible=True
                                                CreneauxCompatibles = False
                                                ListeUEIncompatibles.append(i)
                                if CreneauxCompatibles == True :
                                    listeUEs.append(UEchoisie)
                                    nbUEs = nbUEs +1
                                else:
                                    print("Les horaires de cette UE ne correspondent pas aux UEs suivantes choisies précédemment : ")
                                    for i in range(len(ListeUEIncompatibles)):
                                        print(ListeUEIncompatibles[i])
                        else:
                            print("Cette UE est complète.")
                    else:
                        print("Cette UE a déjà été choisie par l'étudiant.")
            else :
                print("Le nombre maximum d'UE a été choisi")
        elif Choixmodif == 'supprimer':
            UEchoisie = input("Choisir une UE à supprimer : ")
            if UEchoisie in listeUEs :
                for i in range (len(listeUEs)):
                    if listeUEs[i-1] == UEchoisie:
                        del listeUEs[i-1]
                        print("UE supprimée")
            else :
                print("Cette UE n'a pas été chosie par l'étudiant")
        Choixmodif = input("Que voulez vous faire ? supprimer une UE ou ajouter une UE ? Ou ne rien faire ? ")
        while Choixmodif != 'ajouter' and Choixmodif != 'supprimer' and Choixmodif != 'rien':
            Choixmodif = input("Choix non valide, veuillez choisir 'ajouter', 'supprimer' ou 'rien' : ")
    return listeUEs
def visuUE():
    ##
    #@brief Cette fonction permet de visualiser l'information de son choix parmi : Description, créneaux, effectifs actuels des UEs de son choix 
    #@details Vérifie que l'UE est dans le catalogue et si c'est le cas, affiche l'information demandée
    #
    #@return La fonction ne retourne rien, elle affiche des informations.
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    UEàvisu = input("Saisir les UEs à visualiser, stop pour arrêter : ")
    listeUEàvisu = []
    while UEàvisu != 'stop':
        if UEàvisu in UEs:
            listeUEàvisu.append(UEàvisu)
        else:
            print("Cette UE n'est pas dans le catalogue.")
        UEàvisu = input("Saisir une autre UE ou stop pour arrêter : ")
    Choixvisu = input("Que voulez-vous visualiser pour ces UEs : description, créneaux ou effectif : ")
    while Choixvisu != 'description' and Choixvisu != 'créneaux' and Choixvisu != 'effectif':
        Choixvisu = input("La saisie est incorrecte. Que voulez-vous visualiser pour ces UEs : description, créneaux ou effectif : ")
    if Choixvisu == 'description':
        print("Description des UEs selectionnées : ")
        for i in range(len(listeUEàvisu)):
            print(listeUEàvisu[i], " : ", UEs[listeUEàvisu[i]]['Description'])
    elif Choixvisu == 'créneaux':
        print("Créneaux des UEs sélectionnées : ")
        for i in range(len(listeUEàvisu)):
            print(listeUEàvisu[i], ' : ')
            for j in range(len(UEs[listeUEàvisu[i]]['Creneaux'])):
                print("Créneau ",j," : ")
                print(UEs[listeUEàvisu[i]]['Creneaux'][j])
    elif Choixvisu == 'effectif':
        print("Effectifs actuels des UEs sélectionnées : ")
        with open("listeetus.json", "r+") as f:         
            numetus = json.load(f)
        for i in range(len(listeUEàvisu)):
            effectifactuel = 0
            for etu in numetus:
                if listeUEàvisu[i] in numetus[etu]:
                    effectifactuel = effectifactuel+1
            print(listeUEàvisu[i], " : ", effectifactuel)

if __name__ == "__main__":
    ##
    #@brief Fonction principale, elle demande à l'utilisateur ce qu'il veut faire et vérifie que son choix existe.
    creneau_valide= open_dll()
    with open("listeUEs.json", "r") as jsonFile:
        UEs=json.load(jsonFile)
    Choix=input("Que voulez-vous faire : ajouter une UE (ajouter), supprimer une UE (supprimer), modifier une UE (modifier), valider le catalogue (valider),visualiser les UEs (visualiser) ou ne rien faire (rien) : ")
    while Choix != 'ajouter' and Choix != 'supprimer' and Choix != 'modifier' and Choix != 'valider' and Choix != 'rien' and Choix != 'visualiser':
        Choix=input("Choix non valide, veuillez saisir un des choix suivants : ajouter, supprimer, modifier, valider, rien : ")
    if Choix == 'rien':
        sys.exit()
    while Choix != 'rien':
        if Choix == 'ajouter':
            nomUE=SaisirNom()
            if nomUE in UEs:
                print("Cette UE est déjà dans le catalogue")
            else : 
                UEs[nomUE]=SaisirUE()
                with open("listeUEs.json", "w") as jsonFile:
                    json.dump(UEs, jsonFile, indent=4)
        elif Choix == 'supprimer':
            suppUE()
        elif Choix =='modifier':
            modifUE()
        elif Choix == 'visualiser':
            visu_UE='oui'
            while visu_UE=='oui':
                quelle_ue=input("Voulez-vous viualiser l'ensemble des UEs ? ")
                if quelle_ue=='oui':
                    visu_ensemble_UE()
                else:
                    visu_une_UE()
                visu_UE=input("Voulez-vous visualiser d'autres UE ? (oui ou non) : ")
        elif Choix =='valider':
            #Fin des modifications 
            valid_catalogue=input("Est-ce que le catalogue est fini? // Catalogue Valide? (oui ou non) : ")
            if valid_catalogue =='oui':
                Choix='rien'
        if Choix!='rien':
            Choix=input("Que voulez-vous faire : ajouter une UE (ajouter), supprimer une UE (supprimer), modifier une UE (modifier), valider le catalogue (valider), ou ne rien faire (rien) : ")
            while Choix != 'ajouter' and Choix != 'supprimer' and Choix != 'modifier' and Choix != 'valider' and Choix != 'rien' and Choix !='visualiser':
                Choix=input("Choix non valide, veuillez saisir un des choix suivants : ajouter, supprimer, modifier, valider, rien")
            if Choix == 'rien':
                sys.exit()
        
    Choixetu = input("Voulez vous inscrire les UEs d'un nouvel étudiant (inscrire), modifier les choix d'UE d'un étudiant (modifier), visualiser des UEs (visualiser) ou arrêter (arrêter) ? ")
    while Choixetu != 'inscrire' and Choixetu != 'modifier' and Choixetu != 'arrêter' and Choixetu != 'visualiser':
        Choixetu=input("Choix non valide, veuillez saisir un des choix suivants : inscrire, modifier, visualiser,  arrêter : ")
    while Choixetu != 'arrêter':
        if Choixetu == 'inscrire':
            Inscrireetu()
        elif Choixetu =='modifier':
            modifUEetu()
        elif Choixetu == 'visualiser':
            visuUE()
        Choixetu = input("Voulez vous inscrire les UEs d'un nouvel étudiant (inscrire), modifier les choix d'UE d'un étudiant (modifier), visualiser des UEs (visualiser) ou arrêter (arrêter) ? ")
        while Choixetu != 'inscrire' and Choixetu != 'modifier' and Choixetu != 'arrêter' and Choixetu != 'visualiser' :
            Choix=input("Choix non valide, veuillez saisir un des choix suivants : inscrire, modifier, visualiser, arrêter : ")
    if Choix == 'arrêter':
        sys.exit()
         
