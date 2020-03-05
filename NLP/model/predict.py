import pandas as pd
from model.Train_Fonctions import FileToDataFrame, NlpCleaning
import pickle
import os

def prediction(nom):
    # On donne le nom du fichier txt téléchargé
    nom = str(nom)
    df = pd.DataFrame()
    FileToDataFrame(nom, df)
    NlpCleaning(df)
    X = df['clean_text']
    DOSSIER_MODEL = os.path.dirname(os.path.realpath(__file__)) + '/model_save/nb.sav'

    model = pickle.load(open(DOSSIER_MODEL, 'rb'))
    pred = model.predict(X)
    pred_accuracy = model.predict_proba(X)

    if pred == 1:
        #prediction = "Il s'agit de l'auteur est EAP. Ca va dans la section 'HORROR'"
        prediction_author = "EAP"
        prediction_type = "Horror"
        prediction_accuracy = pred_accuracy[0][0]
        prediction_accuracy = str(prediction_accuracy)

    elif pred == 2:
        #prediction = "Il s'agit de l'auteur est HLP. Ca va dans la section 'FICTION'"
        prediction_author = "HLP"
        prediction_type = "Fiction"
        prediction_accuracy = pred_accuracy[0][1]
        prediction_accuracy = str(prediction_accuracy)
    else:
        #prediction = "Il s'agit de l'auteur est MWS. Ca va dans la section 'ROMANTICISM'"
        prediction_author = "MWS"
        prediction_type = "Romanticism"
        prediction_accuracy = pred_accuracy[0][2]
        prediction_accuracy = str(prediction_accuracy)

    return prediction_author, prediction_type, prediction_accuracy
