#Importation de toutes les dépendances
import pandas as pd
import os
import re
import spacy
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import pickle
from sklearn.pipeline import Pipeline

def DirectoryToDataFrame(NomDossier):
    '''Cette fonction va permettre de rajouter chaque fichier .txt dans le DataFrame df.
    le NomDossier est à mettre entre guillemet'''
    NomDossier = str(NomDossier)
    chemin = os.getcwd() + '\\{}\\'.format(NomDossier)
    chemin = str(chemin)
    datas = []
    file_dir = []
    file_name = []
    for file in os.listdir(chemin):
        file_name.append(file)
        file_dir = chemin + str(file)
        with open(file_dir, 'r') as f:
            data = f.read()
            datas.append(data)
            f.close()

    df["Texte"] = datas
    df["File_Name"] = file_name
    pattern = "[A-Z]{3}[.]+txt$"
    search = []
    for values in df["File_Name"]:
        search.append(re.search(r'[A-Z]{3}', values).group())
    df['Auteur'] = search

    return df

def FileToDataFrame(nom, df):
    '''Cette fonction va permettre de rajouter chaque fichier .txt dans le DataFrame df.
    le NomDossier est à mettre entre guillemet'''
    chemin = os.path.dirname(os.path.realpath(__file__)) + '/fichier_reception/{}'.format(nom)
    datas = []

    with open(chemin, 'r') as f:
        data = f.read()
        datas.append(data)
        f.close()

    df["Texte"] = datas
    df["File_Name"] = nom

    return df


def NlpCleaning(df):
    '''Cette fonction va permettre de tokeniser, de lemmatiser,
    d'enelver les stopwords et également de créer une colonne entité, sur base de Spacy.
    On créer ensuite un training et un test set pour renvoyer X-train, X_test, y_train et y_test'''
    nlp = spacy.load("en_core_web_sm")
    tokens = []
    lemma = []
    pos = []
    stop_words = []
    ent = []

    for doc in nlp.pipe(df['Texte'].astype('unicode').values, batch_size=50, n_threads=3):
        if doc.is_parsed:
            tokens.append([n.text for n in doc])
            lemma.append([n.lemma_ for n in doc])
            pos.append([n.pos_ for n in doc])
            stop_words.append([n.text for n in doc if not n.is_stop])
            ent.append([e.label_ for e in doc.ents])

        else:
            # Ajouter des blancs si erreur pour avoir le même nombre d'entrées
            lemma.append(None)
            pos.append(None)
            stop_words.append(None)
            ent.append(None)

    df['Tokens'] = tokens
    df['Tokens_NoStopW'] = stop_words
    df['lemma'] = lemma
    df['PartOfSpeech'] = pos
    df['ent'] = ent

    df['clean_text'] = str()
    for i, row in df.iterrows():
        row['clean_text'] = ' '.join(row['lemma'])

    df['clean_text'] = df.clean_text.replace("[PRON\s\W]", " ", regex=True)
    df['clean_text'] = df.clean_text.replace(' +', ' ', regex=True)
    df['clean_text'] = df.clean_text.replace('^ ', '', regex=True)
    try:
        df['Auteur_number'] = df['Auteur'].map({'EAP': 1, 'HPL': 2, 'MWS': 3})
    except:
        pass
    return df

def TfidFModelTrain(X_train, X_test, y_train, y_test):
    '''On transforme ensuite norme texte en vecteur basé sur Tfid.
    On passe ensuite dans données dans l'algo basé sur Naïve Bayes.
    On sauve ensuite notre modèle sous'tfif_model.sav pour pouvoir le récupérer'''
    auteurs = ['EAP', 'HPL', 'MWS']
    nb = Pipeline([('tfidf', TfidfVectorizer()), ('clf', MultinomialNB())])
    nb.fit(X_train, y_train)
    y_pred_NB = nb.predict(X_test)


    chemin = os.getcwd() + '\\model_save\\'
    chemin = str(chemin)
    with open(os.path.join(chemin, "nb.sav"), "wb") as f:
        pickle.dump(nb, f)
        f.close()

    print('accuracy %s' % accuracy_score(y_pred_NB, y_test))
    return classification_report(y_test, y_pred_NB, target_names=auteurs)

def CountModelTrain(df):
        ctv = CountVectorizer()
        X_ctv = ctv.fit_transform(X)
        X_train_ctv = ctv.transform(X_train)
        X_test_ctv = ctv.transform(X_test)

        nb1 = MultinomialNB()
        nb1.fit(X_train_ctv, y_train)
        y_pred_NB1 = nb1.predict(X_test_ctv)

        filename = 'count_model.sav'
        pickle.dump(nb1, open(filename, 'wb'))

        print(classification_report(y_test, y_pred_NB1, target_names=auteurs))
        return 'accuracy %s' % accuracy_score(y_pred_NB1, y_test)

#Si le modèle n'est pas encore créer, on le fait en lançant ce fichier
if __name__ == '__main__':
    df = pd.DataFrame()
    DirectoryToDataFrame('training_data')
    NlpCleaning(df)
    y = df['Auteur_number']
    X = df['clean_text']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    TfidFModelTrain(X_train, X_test, y_train, y_test)






