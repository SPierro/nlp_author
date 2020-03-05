# Author Classification / NLP Project

If the app is launch you can have the prediction of the Author by uploading the book title you want inside a txt file to :
https://nlpagilytic.herokuapp.com/upload

## General info
This NLP Project has been realized in order to dertermine which Author it is.
To do it, I first import each txt files into a Pandas DataFrame
Then I cleaned the corpus as follow:
  * Tokenization
  * Lemmatization 
  * Removing Stop words

The model is based on the Naive Baive Algorithms after having transforming the text with TfidF


## Prerequisites
You need to have a Python distrubution installed. In this case I used Python 3.7

## Files Information

* The folder "Test_modèle" contains the text visualisation, the text exploration and the test of few algorithms
* The fodler "Model" contains the blueprint for the Flask API, the script to train the model and the prediction model
* The script ro un the app: run.py

## How to use it

### Installation & Building of the Model
Every Librairies (except one) needed are listed in the requirements.txr files.
Thus, just run in your terminal the following line:
  $ pip install -r requirements.txt

You will then have to install the Spacy dependeny "en_core_web_sm":
  $ python -m spacy download en_core_web_sm
  
If the model in not created then run:
  $ python Train_Fonctions.py

To launch the Flask API, just run:
  $ python run.py

### Flask API
Once the API launch, check if it's running by going to port:
http://http://localhost:5000/

If yes, go to http://http://localhost:5000/upload/ and upload a TEXT FILE.
You should be returned a JSON file with the prediction and the accuracy relative to it.


## Production 

A Docker File has been chose as the easiest solution to deploy the model.

### Prerequisites
For the Windows user, you need to install Docker Toolbox ( https://docs.docker.com/toolbox/toolbox_install_windows/ )

### Building the Docker Image
You will then have to build an image of our app inside the Docker Terminal:
  $ docker build -t NlP_project C:/.../FOLDER_NAME/NLP

Then, run the image:
  $ docker run -p 8888:5000 NLP_project
  
You can then go to your localhost:8888/ and use the App.
For information for the Windows user you can find your localhost with:
  $ docker-machine ip default

To push your image to the Docker Hub:
  $ docker tag NLP_project:latest pierrosmn/test_agilytic:latest
	$ docker push pierrosmn/test_agilytic:latest

### Deploy the image to Heroku
* Install Heroku CLI
* Create a new app in the Heroku Website
* Push the Docker Image to Heroku
* Crete a release
