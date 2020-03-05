import sys
import os
from model.app import create_app

#Si j'ai bien compris, on va se mettre dans le dossier /model
#sys.path.append('/model')

server=create_app()

#Quand on lance le fichier, on créer un port et le server se lance
if __name__ =='__main__':
    port = os.environ.get('PORT', 5000)
    server.run(host='0.0.0.0', port=port, debug=False)
    