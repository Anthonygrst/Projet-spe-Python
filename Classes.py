import datetime 

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self,nature="", titre="", auteur="", date="", url="", texte=""):
        self.nature = nature #On a ajoute nature qui représente la source du document pour pouvoir utiliser les code du tp4
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte a  afficher lorsquon tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte a afficher lorsqu on tape str classe
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    def gettexte(self):
       return self.texte
    
    def getSource(self):
        pass


# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
        
    def moyenneDoc(self):
        total = 0
        for i in self.production.values():
            total += len(i.texte)
        return total/len(self.production) #la taille moyenne de tout les docs

    def affichage(self):
        print("nom de l'auteur est : "+self.name)
        print("nb document = ",self.ndoc)
        cpt = 1
        for i in self.production.values():
            print("document n",cpt,i)
            cpt+=1
        print("________________")

    def __str__(self):
        return "nom de l'auteur est : "+self.name
    
    
    
    
#Heritage de document
 
        

class RedditDocument(Document): #Herite de document
    
    def __init__(self,nature, nb_Comments, title, author, text, url, date=datetime.datetime.now()):
        super().__init__(self,date,title, author, text, url)
        self.nb_Comments = nb_Comments
        self.nature = "Reddit"
    
  
    def getNbComments(self):
        return self.nb_Comments
    
    def getSource(self):
        return "reddit"
  
    def setNombreComments(self,nb_Comments):
        self.nb_Comments = nb_Comments
        
    def __str__(self):
        return "[Source: "+self.getSource() +"] "+super().__str__(self) + " [" + str(self.nb_Comments) + " commentaires]"




class ArxivDocument(Document): #Herite de Document
    
    def __init__(self, nature, coauteurs, title, author, text, url, date= datetime.datetime.now()):
        super().__init__(self, date, title, author, text, url)
        self.coauteurs = coauteurs
        self.nature = "Arxiv"
    
    def get_num_coauteurs(self):
        if self.coauteurs is None:
            return(0)
        return(len(self.coauteurs) - 1)

    def get_coauteurs(self):
        if self.coauteurs is None:
            return([])
        return(self.coauteurs)
        
    def getSource(self):
        return "arxiv"

    def __str__(self):
       s = super().__str__(self)
       if self.get_num_coauteurs() > 0:
           return "[Source: "+self.getSource() +"] "+s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
       else:
           return "[Source: "+self.getSource() +"] "+s