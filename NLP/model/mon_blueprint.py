import os
from .predict import prediction
import pickle
from flask import render_template, Blueprint, request, jsonify


def routes_fonction():
    #Le blueprint est un moule pour des futurs reproductions. On va pouvoir ensuite le mettre dans le fichier run.py
    blueprint_auteur=Blueprint('route',__name__)

    #Pour vérifier si la connexion est effective
    @blueprint_auteur.route('/', methods=['GET'])
    def health():
        return "Dear Agilytic Member (or not), \n Welcome to the Author Prediction API!!! \n Go to /upload to add your txt file"

    
    @blueprint_auteur.route('/upload', methods=['GET','POST'])
    def upload():
        #La fonction request de Flask permet d'utiliser une action différente selon le type de requête (GET ou POST ici)
        if request.method == 'GET':
            #La methode render_template de Flask permet d'appliquer le template html sans difficulté
            #Cette méthode va chercher PAR DEFAULT dans le dossier 'templates'!! C'est donc dans ce dossier qu'on met notre html
            return render_template('template.html')

        if request.method == 'POST':        
            #Lors d'un téléchargement, la fonction 'request.files' va récupérer le fichier (ici le txt file)
            f=request.files['txt']
            # On va ensuite la sauver au bon endroit
            FICHIER_UPLOAD =os.path.dirname(os.path.realpath(__file__)) + '/fichier_reception/'
            f.save(os.path.join(FICHIER_UPLOAD, f.filename))

            pred= prediction(f.filename)
            chemin = os.path.dirname(os.path.realpath(__file__)) + '/fichier_reception/{}'.format(f.filename)
            texte=[]
            with open(chemin, 'r') as fi:
                txt = fi.read()
                texte.append(txt)
                fi.close()

            return jsonify(Titre=pred[2],Auteur=pred[0], Genre=pred[1])
    #On retourne le blueprint pour mettre dans le fichier app.py        
    return blueprint_auteur







