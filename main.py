
# =============== PARTIE 1 =============
# =============== 1.1 : REDDIT ===============

import praw
import pandas as pd
from Classes import Document
import datetime



################ UTILISATION DU TP4 pour GENERATION corpus avec reddit et Arxiv ###
# Identification
reddit = praw.Reddit(client_id='G2Ud8d40E_RqAe8YnAe7kA', client_secret='eNtSKwVwRsF18e4U6iXoKF7lyqvQOA', user_agent='LawfulnessSalty5238')

# Requete
limit = 100
hot_posts = reddit.subreddit('pokemon').hot(limit=limit)#.top("all", limit=limit)#

# Recuperation du texte
docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):
    if i%10==0: print("Reddit:", i, "/", limit)
    if afficher_cles:  # Pour connaitre les differentes variables et leur contenu
        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)

    if post.selftext != "":  # posts sans texte non taits
        pass
        print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))

#print(docs)


# =============== 1.2 : ArXiv ===============
# Libraries
import urllib, urllib.request, _collections
import xmltodict

# Parametres
query_terms = ["pokemon"]
max_results = 50

# Requete
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('ISO-8859-1'))

#showDictStruct(data)


# Ajout  la liste
for i, entry in enumerate(data["feed"]["entry"]):
    if i%10==0: print("ArXiv:", i, "/", limit)
    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))
    print(docs_bruts)
    #showDictStruct(entry)

# =============== 1.3 : Exploitation ===============
print("# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print("# docs sans doublons : {len(docs)}")

for i, doc in enumerate(docs):
    print("Document {i}\t caracteres : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)
        
#print(docs)

longueChaineDeCaracteres = " ".join(docs)
collection = []


for nature, doc in docs_bruts:
    if nature == 'ArXiv':  
        titre = doc["title"].replace('\n', '')  # On enleve les retours  la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, separes par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enleve les retours  la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en annee/mois/jour avec librairie datetime
        doc_classe = Document(nature, titre, authors, date, doc["id"], summary)  # Creation du Document
        collection.append(doc_classe)  # Ajout du Document la liste.

    elif nature == 'Reddit':
        print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(nature, titre, auteur, date, url, texte)

        collection.append(doc_classe)

# Creation de l index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

# =============== 2.4, 2.5 : CLASSE AUTEURS ===============
from Classes import Author

# =============== 2.6 : DICT AUTEURS ===============
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Creation de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)


# =============== 2.7, 2.8 : CORPUS ===============
from Corpus import Corpus
corpus = Corpus("Mon corpus")

# Construction du corpus partir des documents
for doc in collection:
    Corpus.nettoyer_texte(doc, doc.texte)
    corpus.add(doc)
    

#print(repr(corpus))


# =============== 2.9 : SAUVEGARDE ===============

#avec valeurC on recupere les nature et les titre dans le corpus
nature=corpus.valeursC()[0]
titre=corpus.valeursC()[1]

#Avec le traitement precedent on genere une dataframe puis son csv
df = pd.DataFrame(zip(nature,titre), columns=['Nature','Titre'])
df.to_csv(r'corpus.csv',index=False,sep=':')
    

print("CSV crée avec le corpus pour Dash")


#Creation d un deuxieme csv avce toutes les valeurs de corpus

naturec=corpus.valeursComplet()[0]
titrec=corpus.valeursComplet()[1]
auteurc=corpus.valeursComplet()[2]
datec=corpus.valeursComplet()[3]
urlc=corpus.valeursComplet()[4]
textec=corpus.valeursComplet()[2]

dfc = pd.DataFrame(zip(naturec,titrec, auteurc, datec, urlc, textec), columns=['Nature','Titre','auteur','date','url','texte'])
dfc.to_csv(r'corpuscomplet.csv',index=False,sep=':')
     
print("CSV crée avec le corpus Complet")



########################## TESTS ###################


for doc in collection:
    Corpus.nettoyer_texte(doc, doc.texte)

#print(corpus.concorde('fire'))
#corpus.chaineRegex()
#print(corpus.chaineUnique)
#print(corpus.search('pokemon'))
#print(corpus.stats())





