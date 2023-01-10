# Correction de G. Poux-Médard, 2021-2022

import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords




from Classes import Author

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.collection = {}
        self.vocab = {}
        self.chaineUnique = ""
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        self.chaineUnique = ""
        self.chaineUniqueReddit = ""
        self.chaineUniqueArxiv = ""
        self.collection[self.ndoc] = doc
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        
        
        #creation de la chaineUnique pour le corpus - 
        
    def chaineRegex(self):
        liste = []
        for i in self.id2doc.values():
            texte = i.gettexte().replace("\n", " ")
            print(texte)
            liste.append(texte)
        self.chaineUnique = " ".join(liste)

    #recherche d'un motif dans le corpus
    def search(self, motif):
       if len(self.chaineUnique) == 0:
           self.chaineRegex()
       chaine = ', '.join([str(doc) for doc in self.chaineUnique ])
       return re.search(r"motif*", chaine)
   
    #Fonction concorde du TD demande
   
    def concorde(self,motif):
       motif=motif.lower()
       #transforme notre collection en chaine
       text_corpus=". ".join(str(doc) for doc in self.collection.values())
       #tokenize et supprime ponctuation
       text_corpus= self.nettoyer_texte(text_corpus)
       #reconversion en chaine
       text_corpus = " ".join(str(x) for x in text_corpus)
       #motif gauche
       gauche=re.findall(r"(.*?:^|\S+\s+\S+\s+\S+) {} ".format(motif), text_corpus)
       #motif droite
       droite=re.findall(r" {} (s*\S+\s+\S+\s+\S+|$)".format(motif), text_corpus)
       motif=[motif]*len(gauche)
       return pd.DataFrame(list(zip(gauche, motif,droite)),columns =['gauche', 'motif','droite'])
      
        
      #nettoyage du texte -nous avons pris exemple d ingenieurie des donnees
 
        
    def nettoyer_texte(self, chaine):
        chaine = re.sub(r'https?://\S+|www\S+', '', chaine) # enleve les liens (https,http, www etc...)
        chaine.split()
        #Ce tokenizer  de nltk supprime en meme temps les ponctuation, separe les apostrophes
        tokenizer = RegexpTokenizer(r'\w+')
        #mettre en minuscule et tokenize text
        chaine = tokenizer.tokenize(chaine.lower())
        #Supprime les tokens qui ne sont pas alphabetique
        chaine = [token for token in chaine if token.isalpha()]
        # suppression des mots peu informatifs
        stop_words = set(stopwords.words('english'))
        chaine = [token for token in chaine if not token in stop_words]
        # Supprimons les tokens de longueur egale  1 on supprime aussi les chiffres
        chaine = [token for token in chaine if len(token)>1]
        return chaine
        
    
    #petites statistiques

    def stats(self):
        print("mots differents dans le corpus: ",len(self.chaineUnique))


    ##fonction pour recuperer les valeurs dans le corpus que l on a cree
    ##facilite pour creation de la dataframe et le csv pour ensuite l'utiliser sur Dash
    
    def valeursC(self):
            natureC = []
            titreC = []
            for key in self.id2doc.keys():
                natureC.append(self.id2doc[key].nature)
                titreC.append(self.id2doc[key].titre)
            return natureC, titreC
    
     def valeursComplet(self):
            natureC = []
            titreC = []
            auteurC = []
            dateC = []
            urlC = []
            texteC = []
            for key in self.id2doc.keys():
                natureC.append(self.id2doc[key].nature)
                titreC.append(self.id2doc[key].titre)
                auteurC.append(self.id2doc[key].auteur)
                dateC.append(self.id2doc[key].date)
                urlC.append(self.id2doc[key].url)
                texteC.append(self.id2doc[key].texte)
            return natureC, titreC, auteurC, dateC, urlC, texteC
            
      
           

# =============== REPRESENTATION ===============


    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
