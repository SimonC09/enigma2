import streamlit as st
#Import du lemmatizer
import spacy_streamlit
from st_clickable_images import clickable_images
import time

st.set_page_config(layout="wide")

# @st.cache(allow_output_mutation=True)
###############################################
##########                           ##########
##########       LES SESSIONS        ##########
##########          STATES           ##########
##########                           ##########
###############################################

# if "modele_nlp" not in st.session_state:
#     st.session_state['modele_nlp'] = True
if "Machines" not in st.session_state: 
    st.session_state['Machine']=""

# # spacy.cli.download('en_core_web_sm')
# spacy.cli.download("fr_core_news_md")
# # nlpEn = spacy.load("en_core_web_sm")
# nlpFr = spacy.load("fr_core_news_md")
###############################################
##########                           ##########
##########       LES FONCTIONS       ##########
##########                           ##########
###############################################


###### MACHINE ENIGMA V1 ######

def enigma(chaine, posRotor1, posRotor2):

    ## Preparer la position des rotors ##    

    # Position initiale des rotors et reflecteur
    alpha=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    Rotor1 = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
    Rotor2 = ['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E']
    Reflecteur = ['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T']

    # on positionne les rotors convenablement 
    if posRotor1 != 0:
        ok=0
        while ok != posRotor1:
            lastLetter = Rotor1.pop()
            Rotor1.insert(0, lastLetter)
            ok+=1
    if posRotor2 != 0:
        ok=0
        while ok != posRotor2:
            lastLetter = Rotor2.pop()
            Rotor2.insert(0, lastLetter)
            ok+=1

            

    # Coder/decoder
    codeEnigma = ''
    for lettre in chaine:
        if lettre.isalpha():
            # On recupere l'index de la lettre a coder dans la liste alpha (exemple avec les positions initiales : Lettre B)
            indexAlpha = alpha.index(lettre.upper()) # Index = 1
            # On recupere le caractere dans le Rotor1 correspondant à l'index alpha (premier codage)
            codRot1 = Rotor1[indexAlpha] #codRot1 = K 
            # On retrouve l'index de cette lettre codé dans la liste alpha
            indexRot1 = alpha.index(codRot1.upper()) #indexRot1 = 10
            # On recupere le caractere dans le Rotor2 correspondant à l'index alpha de la lettre codé (deuxieme codage)
            codRot2 = Rotor2[indexRot1] # codRot2 = L
            # On retrouve l'index de cette lettre codé 2x dans la liste alpha
            indexRot2 = alpha.index(codRot2.upper()) # indexRot2= 11
            # On le passe dans le reflecteur
            codRefl = Reflecteur[indexRot2] # codeRefl = G

            # Et on fait le chemin inverse
            
            # Recuperation de l'index dans le Rotor2
            indexRot2 = Rotor2.index(codRefl.upper()) #indexRot2 = 17
            # Premier décodage dans l'alpha
            decod1 = alpha[indexRot2] # decod1 = R
            # On regarde l'index de ce caractere dans le rotor précedent
            indexRot1 = Rotor1.index(decod1.upper()) #indexRot1 = 23
            # On regarde la lettre correspondante dans l'alpha
            decod2 =  alpha[indexRot1] #decod2 = X

            # Normalement là on est bon on peux faire tourner nos rotors
            lastLetter = Rotor1.pop()
            Rotor1.insert(0, lastLetter)
            posRotor1+=1
            if posRotor1%5==0:
                lastLetter = Rotor2.pop()
                Rotor2.insert(0, lastLetter)
                posRotor2+=1

            # charger le code et passer à l'iteration suivante
            codeEnigma += decod2
        else:
            codeEnigma+= lettre
        # On peux afficher le code
    return codeEnigma


###### MACHINE CHRISTOPHER V1 ######


# La machine
def decodNigma(code):
    nlpFr = spacy_streamlit.load_model("fr_core_news_md")

    # Preparer la position des rotors    
    # Position initiale des rotors et reflecteur
    alpha=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    Rotor1 = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
    Rotor2 = ['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E']
    Reflecteur = ['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T']

    decode = False
    posRotor1 = 0
    posRotor2 = 0
    # Premiere boucle sur le deuxieme Rotor
    while posRotor2 <=25 and decode == False:
        # Deuxieme boucle sur le premier Rotor
        while posRotor1<=25 and decode == False:
            codeEnigma = ''
            # On copie les positions des rotors dans des variables test pour ne pas compromettre la variable qui sert a la boucle
            posRotorTest1 = posRotor1
            posRotorTest2 = posRotor2
            RotorTest1 = Rotor1.copy()
            RotorTest2 = Rotor2.copy()
            for lettre in code:
                if lettre.isalpha():
                    # On recupere l'index de la lettre a coder dans la liste alpha (exemple avec les positions initiales : Lettre B)
                    indexAlpha = alpha.index(lettre.upper()) # Index = 1
                    # On recupere le caractere dans le Rotor1 correspondant à l'index alpha (premier codage)
                    codRot1 = RotorTest1[indexAlpha] #codRot1 = K 
                    # On retrouve l'index de cette lettre codé dans la liste alpha
                    indexRot1 = alpha.index(codRot1.upper()) #indexRot1 = 10
                    # On recupere le caractere dans le Rotor2 correspondant à l'index alpha de la lettre codé (deuxieme codage)
                    codRot2 = RotorTest2[indexRot1] # codRot2 = L
                    # On retrouve l'index de cette lettre codé 2x dans la liste alpha
                    indexRot2 = alpha.index(codRot2.upper()) # indexRot2= 11
                    # On le passe dans le reflecteur
                    codRefl = Reflecteur[indexRot2] # codeRefl = G

                    # Et on fait le chemin inverse
                    
                    # Recuperation de l'index dans le Rotor2
                    indexRot2 = RotorTest2.index(codRefl.upper()) #indexRot2 = 17
                    # Premier décodage dans l'alpha
                    decod1 = alpha[indexRot2] # decod1 = R
                    # On regarde l'index de ce caractere dans le rotor précedent
                    indexRot1 = RotorTest1.index(decod1.upper()) #indexRot1 = 23
                    # On regarde la lettre correspondante dans l'alpha
                    decod2 =  alpha[indexRot1] #decod2 = X

                    # Normalement là on est bon on peux faire tourner nos rotors
                    lastLetter = RotorTest1.pop()
                    RotorTest1.insert(0, lastLetter)
                    posRotorTest1+=1
                    if posRotorTest1%5==0:
                        lastLetter = RotorTest2.pop()
                        RotorTest2.insert(0, lastLetter)
                        posRotorTest2+=1

                    # charger le code et passer à l'iteration suivante
                    codeEnigma += decod2
                else:
                    codeEnigma+= lettre
            
            # On verifie avec du nlp si le message est décodé
            tokenCode = nlpFr(codeEnigma.lower())
            for token in tokenCode:
                if token.is_oov:
                    decode = False
                    lastLetter = Rotor1.pop()
                    Rotor1.insert(0, lastLetter)
                    posRotor1+=1
                    break
                else:
                    decode = True
        lastLetter = Rotor2.pop()
        Rotor2.insert(0, lastLetter)
        posRotor2+=1
        posRotor1 = 0
    if decode == False:
        return "La b0mb à malheureusement échoué..."
    else:
        return codeEnigma

###############################################
##########                           ##########
##########       LE STREAMLIT        ##########
##########                           ##########
###############################################


############################# LES STYYYYYYYLES (BECAUSE ITS SWAAAAAAAAAAG )#################################
# Définir le contenu HTML avec l'image en arrière-plan
    
html_code = """
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://i.ibb.co/b20Tvw8/Design-sans-titre.png');
        background-size: cover;
        background-repeat: no-repeat;
        margin: 0;
        padding: 0;
        height: 100%;
        background-opacity : 0.75;
    }

</style>
"""

# modifier la police
custom_css = """
    <style>

        /* Appliquer une police personnalisée à tout le texte */
        h1 {
            font-family: "Tox Typewriter"; 
            color: black;
            text-align: center;            
            font-size: 96px;
        }
        .tache {
            font-family: "Tox Typewriter"; 
            color: black;
            text-align: center;
            -webkit-text-stroke: 2px black;
            font-size: 30px;
        }
        .titre2 {
            font-family: "Tox Typewriter"; 
            color: black;
            text-align: center;
            -webkit-text-stroke: 2px black;
            font-size: 42px;
        }
        input[type="text"] {
            background-color: #f1f1f1;
            color: black;
            font-family: "Tox Typewriter"; 
            border: 2px solid #ccc;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 16px;
        }
        .txt{
            font-family: atwriter; 
            color: black;
            text-align: center;
            font-size: 30px;
        }
    </style>
"""
# input_style = """
#     <style>

#     </style>
# """
# st.markdown(input_style, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(html_code, unsafe_allow_html=True)


######################## THE SIDE BAR ######################################
dictMachines = {0: "Enigma", 1: "Christopher"}
with st.sidebar:
    st.write("<p class=titre2> Que voulez vous faire ?</p>", unsafe_allow_html=True)

    st.write("<p class=tache> Utiliser Enigma ?</p>", unsafe_allow_html=True)

    dictMachines = {0: "Enigma", 1: "Christopher"}
    clicked = clickable_images(
        [
            'https://i.ibb.co/4YTZT3G/enigma2.png',
            "https://i.ibb.co/9VD8Y1C/bombe.png",
        ],
        titles=['Enigma','THE BOMB'],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap" }, 
        img_style={"height": "240px"},
    )
    if clicked > -1:
        st.write(clicked)
        st.session_state['Machine'] = dictMachines[clicked]

    st.write("<p class=tache> Ou utiliser THE BOMB ?</p>", unsafe_allow_html=True)

####################################################################
##################                                ##################
##################         THE MAIN GAME          ##################
##################                                ##################
####################################################################  
                               
st.write("<h1><strong>BIENVENUE DANS<br>LA HUTTE 8</strong></h1>", unsafe_allow_html=True)# Afficher le contenu HTML







###### UTILISER ENIGMA ######
if st.session_state['Machine'] == "Enigma":
    st.write("<div class = 'txt'>Veuillez entrer le message pour Enigma</div>", unsafe_allow_html=True)
    message = st.text_input(label= "message", label_visibility='hidden')
    if message:
        st.write("<div class = 'txt'>Entrez la position souhaitée pour le rotor 1 (entre 0 et 25)</div>", unsafe_allow_html=True)
        posRotor1 = st.text_input("R1", label_visibility='hidden')
        if posRotor1:
            st.write("<div class = 'txt'>Entrez la position souhaitée pour le rotor 2 (entre 0 et 25)</div>", unsafe_allow_html=True)
            posRotor2 = st.text_input("R2", label_visibility='hidden')
            if posRotor2:
                st.write("<div class = 'txt'>enigma va maintenant transformer votre message</div>", unsafe_allow_html=True)
                code = enigma(message,int(posRotor1),int(posRotor2))
                st.image("https://i.makeagif.com/media/2-21-2016/8-dmur.gif")
                # Faire une pause pendant 5 secondes
                time.sleep(2)
                st.write("<div class = 'txt'> voici votre message transformé par Enigma : {} </div>".format(code), unsafe_allow_html=True)
                message = ""


###### UTILISER CHRISTOPHER ######

if st.session_state['Machine'] == "Christopher":
    st.write("<div class = 'txt'>Veuillez entrer le message à decoder par THE BOMB</div>", unsafe_allow_html=True)
    code = st.text_input("code", label_visibility='hidden')
    if code:
        st.image("https://images.squarespace-cdn.com/content/v1/5f998d8e737bec64a3266c55/1604866357473-ZG7HP5S3VDIZV9HV7C3L/Bombe+ON2.gif")
        decode = decodNigma(code)
        st.write("<div class = 'txt'> voici votre message decodé par THE BOMB : {} </div>".format(decode), unsafe_allow_html=True)
        decode = ""
