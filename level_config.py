# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# CONFIGURATION DES NIVEAUX DE BREAKOUT
# ----------------------------------------------------------------------------
#
# Chaque niveau est un dictionnaire avec les clés suivantes :
#   - "ball_speed": Vitesse initiale de la balle pour ce niveau.
#   - "paddle_size": Largeur de la raquette.
#   - "message": Un message ou nom de niveau à afficher (optionnel).
#   - "layout": Une liste de chaînes de caractères représentant le placement
#               des briques. Chaque caractère correspond à un type de brique.
#
# --- LÉGENDE DES CARACTÈRES ---
#   G: Vert (Classique, 1 coup)
#   K: Noir (Résistant, 3 coups)
#   R: Rouge (Accélérateur)
#   P: Violet (Multiplicateur)
#   W: Blanc (Ralentisseur)
#   Y: Gris (Réducteur de raquette)
#   B: Jaune (Bonus aléatoire)
#   L: Bleu clair (Élargisseur de raquette)
#   O: Orange (Inverseur de contrôles)
#   N: Brun (Invisible)
#   I: Indestructible
#   _: Espace vide
# ----------------------------------------------------------------------------

LEVELS = [
    # --- PHASE 1: INITIATION (Niveaux 1-10) ---
    {
        "ball_speed": 4,
        "paddle_size": 100,
        "message": "Niveau 1: L'échauffement",
        "layout": [
            "___________",
            "__GGGGGGG__",
            "__GGGGGGG__",
            "__GGGGGGG__",
        ]
    },
    {
        "ball_speed": 4,
        "paddle_size": 100,
        "message": "Niveau 2: Lignes",
        "layout": [
            "GGGGGGGGGGG",
            "___________",
            "GGGGGGGGGGG",
            "___________",
            "GGGGGGGGGGG",
        ]
    },
    {
        "ball_speed": 4.2,
        "paddle_size": 100,
        "message": "Niveau 3: Pyramide",
        "layout": [
            "_____G_____",
            "____GGG____",
            "___GGGGG___",
            "__GGGGGGG__",
            "_GGGGGGGGG_",
        ]
    },
    {
        "ball_speed": 4.2,
        "paddle_size": 100,
        "message": "Niveau 4: Murs",
        "layout": [
            "G_________G",
            "G_________G",
            "G__GGGGG__G",
            "G__GGGGG__G",
            "G_________G",
            "G_________G",
        ]
    },
    {
        "ball_speed": 4.4,
        "paddle_size": 95,
        "message": "Niveau 5: Un peu de challenge",
        "layout": [
            "GGGGGGGGGGG",
            "G_G_G_G_G_G",
            "GGGGGGGGGGG",
            "G_G_G_G_G_G",
            "GGGGGGGGGGG",
        ]
    },
    {
        "ball_speed": 4.5,
        "paddle_size": 95,
        "message": "Niveau 6: Blocs résistants !",
        "layout": [
            "___________",
            "___KKKKK___",
            "__GGGGGGG__",
            "___KKKKK___",
        ]
    },
    {
        "ball_speed": 4.5,
        "paddle_size": 95,
        "message": "Niveau 7: Armure",
        "layout": [
            "__KKKKKKK__",
            "_KGGGGGGGK_",
            "KGGKKKKKGGK",
            "_KGGGGGGGK_",
            "__KKKKKKK__",
        ]
    },
    {
        "ball_speed": 4.6,
        "paddle_size": 90,
        "message": "Niveau 8: Alternance",
        "layout": [
            "K_G_K_G_K_G",
            "G_K_G_K_G_K",
            "K_G_K_G_K_G",
            "G_K_G_K_G_K",
        ]
    },
    {
        "ball_speed": 4.7,
        "paddle_size": 90,
        "message": "Niveau 9: Le fort",
        "layout": [
            "__IIIII__",
            "_IKKKKKI_",
            "IKGGGGGIK",
            "_IKKKKKI_",
            "__IIIII__",
        ]
    },
    {
        "ball_speed": 4.8,
        "paddle_size": 90,
        "message": "Niveau 10: Le coeur",
        "layout": [
            "GGGG_K_GGGG",
            "GGGK_K_KGGG",
            "GGKK_K_KKGG",
            "GKKKKKKKKKG",
            "GGKK_K_KKGG",
            "GGGK_K_KGGG",
            "GGGG_K_GGGG",
        ]
    },

    # --- PHASE 2: POWER-UPS (Niveaux 11-20) ---
    {
        "ball_speed": 5,
        "paddle_size": 90,
        "message": "Niveau 11: Une aide bienvenue",
        "layout": [
            "_G_G_L_G_G_",
            "_G_GGGGG_G_",
            "_G_G_B_G_G_",
            "___GGGGG___",
            "____W____",
        ]
    },
    {
        "ball_speed": 5,
        "paddle_size": 90,
        "message": "Niveau 12: Zigzag",
        "layout": [
            "G_G_G_G_G_G",
            "_L_G_G_G_L_",
            "__G_G_G_G__",
            "___G_B_G___",
            "____GGG____",
        ]
    },
    {
        "ball_speed": 5,
        "paddle_size": 90,
        "message": "Niveau 13: Attention !",
        "layout": [
            "__Y_____Y__",
            "_K_GGGGG_K_",
            "_K_G_O_G_K_",
            "_K_GGGGG_K_",
            "__Y_____Y__",
        ]
    },
    {
        "ball_speed": 5.1,
        "paddle_size": 85,
        "message": "Niveau 14: Risque et récompense",
        "layout": [
            "Y_L_Y_L_Y_L",
            "_G_G_G_G_G_",
            "__K_K_K_K__",
            "___G_G_G___ ",
            "____B____",
        ]
    },
    {
        "ball_speed": 5.1,
        "paddle_size": 85,
        "message": "Niveau 15: Le piège",
        "layout": [
            "__OOOOO__",
            "_GKKKKKG_",
            "_G_L_B_G_",
            "_GKKKKKG_",
            "__WWWWW__",
        ]
    },
    {
        "ball_speed": 5.2,
        "paddle_size": 85,
        "message": "Niveau 16: Contrôle inversé",
        "layout": [
            "O_________O",
            "_G_G_G_G_G_",
            "__K_K_K_K__",
            "_G_G_G_G_G_",
            "O_________O",
        ]
    },
    {
        "ball_speed": 5.2,
        "paddle_size": 85,
        "message": "Niveau 17: Couloirs",
        "layout": [
            "IKI_IKI_IKI",
            "IGI_IGI_IGI",
            "I_I_I_I_I_I",
            "__L__B__W__",
        ]
    },
    {
        "ball_speed": 5.3,
        "paddle_size": 80,
        "message": "Niveau 18: Le sourire du diable",
        "layout": [
            "_Y_______Y_",
            "__O_____O__",
            "_________",
            "___G___G___",
            "__KKKKKKK__",
            "_K_K_K_K_K_",
        ]
    },
    {
        "ball_speed": 5.3,
        "paddle_size": 80,
        "message": "Niveau 19: Tout ou rien",
        "layout": [
            "L_B_W_Y_O_R",
            "I_I_I_I_I_I",
            "K_K_K_K_K_K",
            "G_G_G_G_G_G",
        ]
    },
    {
        "ball_speed": 5.4,
        "paddle_size": 80,
        "message": "Niveau 20: Calme avant la tempête",
        "layout": [
            "__IIIII__",
            "_I_L_W_I_",
            "I_G_B_G_I",
            "_I_K_K_I_",
            "__IIIII__",
        ]
    },

    # --- PHASE 3: CHAOS (Niveaux 21-30) ---
    {
        "ball_speed": 5.5,
        "paddle_size": 80,
        "message": "Niveau 21: Multi-Balles !",
        "layout": [
            "____P____",
            "___GGG___",
            "__KKKKK__",
            "_GGGGGGG_",
            "KKKKKKKKKKK",
        ]
    },
    {
        "ball_speed": 5.5,
        "paddle_size": 80,
        "message": "Niveau 22: Accélération !",
        "layout": [
            "R_R_R_R_R_R",
            "_G_G_G_G_G_",
            "__K_K_K_K__",
            "___L_W_L___ ",
        ]
    },
    {
        "ball_speed": 5.6,
        "paddle_size": 75,
        "message": "Niveau 23: Frénésie",
        "layout": [
            "R_P_R_P_R_P",
            "_K_K_K_K_K_",
            "__G_G_G_G__",
            "_Y_Y_Y_Y_Y_",
        ]
    },
    {
        "ball_speed": 5.6,
        "paddle_size": 75,
        "message": "Niveau 24: Briques invisibles",
        "layout": [
            "NNNNNNNNNNN",
            "N_________N",
            "N___GGG___N",
            "N___LWL___N",
            "N_________N",
            "NNNNNNNNNNN",
        ]
    },
    {
        "ball_speed": 5.7,
        "paddle_size": 75,
        "message": "Niveau 25: Le labyrinthe",
        "layout": [
            "IIIGIIIGIII",
            "I_G__G__G_I",
            "IGIKIGIKIGI",
            "I__G__G__GI",
            "IIIGIIIGIII",
            "____P_R____",
        ]
    },
    {
        "ball_speed": 5.8,
        "paddle_size": 70,
        "message": "Niveau 26: Pluie de bonus",
        "layout": [
            "L_B_W_Y_O_R",
            "B_W_Y_O_R_P",
            "W_Y_O_R_P_L",
            "Y_O_R_P_L_B",
        ]
    },
    {
        "ball_speed": 5.8,
        "paddle_size": 70,
        "message": "Niveau 27: Méfiez-vous",
        "layout": [
            "_NNNNNNNNN_",
            "_N_O_Y_O_N_",
            "_N_K_P_K_N_",
            "_N_L_B_L_N_",
            "_NNNNNNNNN_",
        ]
    },
    {
        "ball_speed": 5.9,
        "paddle_size": 70,
        "message": "Niveau 28: Vitesse lumière",
        "layout": [
            "R_R_R_R_R_R",
            "I_I_I_I_I_I",
            "K_P_K_P_K_P",
            "I_I_I_I_I_I",
            "W_W_W_W_W_W",
        ]
    },
    {
        "ball_speed": 6.0,
        "paddle_size": 65,
        "message": "Niveau 29: Précision chirurgicale",
        "layout": [
            "Y_Y_Y_Y_Y_Y",
            "I_I_I_I_I_I",
            "G_G_G_G_G_G",
            "_K_K_K_K_K_",
            "__P_____P__",
        ]
    },
    {
        "ball_speed": 6.0,
        "paddle_size": 65,
        "message": "Niveau 30: La totale",
        "layout": [
            "O_R_P_B_Y_L",
            "_I_I_I_I_I_",
            "_K_N_I_N_K_",
            "__G_I_I_G__",
            "___I_W_I___",
            "____III____",
        ]
    },

    # --- PHASE 4: THE ULTIMATE CHALLENGE (Levels 31-50) ---
    {
        "ball_speed": 6.1,
        "paddle_size": 65,
        "message": "Niveau 31: Tic-Tac",
        "layout": [
            "O_I_Y_I_R_I",
            "_G_I_K_I_G_",
            "__G_I_K_G__",
            "___G_I_G___",
            "____L_W____",
        ]
    },
    {
        "ball_speed": 6.2,
        "paddle_size": 60,
        "message": "Niveau 32: La fournaise",
        "layout": [
            "R_R_R_R_R_R",
            "_O_O_O_O_O_",
            "__Y_Y_Y_Y__",
            "___P_P_P___",
            "____B____",
        ]
    },
    {
        "ball_speed": 6.3,
        "paddle_size": 60,
        "message": "Niveau 33: Prison de verre",
        "layout": [
            "IIIIIIIIIII",
            "I_NNNNNNN_I",
            "I_N_K_K_N_I",
            "I_N_P_P_N_I",
            "I_NNNNNNN_I",
            "IIIIIIIIIII",
        ]
    },
    {
        "ball_speed": 6.4,
        "paddle_size": 60,
        "message": "Niveau 34: Double peine",
        "layout": [
            "O_Y_O_Y_O_Y",
            "_K_K_K_K_K_",
            "__P_P_P_P__",
            "_R_R_R_R_R_",
        ]
    },
    {
        "ball_speed": 6.5,
        "paddle_size": 55,
        "message": "Niveau 35: Le damier infernal",
        "layout": [
            "R_K_R_K_R_K",
            "K_O_K_O_K_O",
            "O_Y_O_Y_O_Y",
            "Y_P_Y_P_Y_P",
            "P_B_P_B_P_B",
        ]
    },
    {
        "ball_speed": 6.6,
        "paddle_size": 55,
        "message": "Niveau 36: La grande descente",
        "layout": [
            "B________B",
            "_L______L_",
            "__W____W__",
            "___Y__Y___",
            "____O_O____",
            "_____R_____",
        ]
    },
    {
        "ball_speed": 6.7,
        "paddle_size": 50,
        "message": "Niveau 37: Le mur de la peur",
        "layout": [
            "NNNNNNNNNNN",
            "KKKKKKKKKKK",
            "RRRRRRRRRRR",
            "OOOOOOOOOOO",
            "YYYYYYYYYYY",
        ]
    },
    {
        "ball_speed": 6.8,
        "paddle_size": 50,
        "message": "Niveau 38: Chaos contrôlé",
        "layout": [
            "P_I_P_I_P_I",
            "_R_I_R_I_R_",
            "__O_I_O_I__",
            "___Y_I_Y___",
            "____W_W____",
        ]
    },
    {
        "ball_speed": 6.9,
        "paddle_size": 50,
        "message": "Niveau 39: Labyrinthe invisible",
        "layout": [
            "IIINIIINIII",
            "I__N__N__GI",
            "INININININI",
            "I__N__N__NI",
            "IIINIIINIII",
            "____P_R____",
        ]
    },
    {
        "ball_speed": 7.0,
        "paddle_size": 50,
        "message": "Niveau 40: L'oeil du cyclone",
        "layout": [
            "__RRRRR__",
            "_R_Y_Y_R_",
            "R_Y_P_Y_R",
            "_R_Y_Y_R_",
            "__RRRRR__",
            "__WWWWW__",
        ]
    },
    {
        "ball_speed": 7.1,
        "paddle_size": 45,
        "message": "Niveau 41: Point de non-retour",
        "layout": [
            "O_R_Y_P_B_L",
            "R_Y_P_B_L_O",
            "Y_P_B_L_O_R",
            "P_B_L_O_R_Y",
            "B_L_O_R_Y_P",
        ]
    },
    {
        "ball_speed": 7.2,
        "paddle_size": 45,
        "message": "Niveau 42: La ruche",
        "layout": [
            "__K_K_K__",
            "_K_P_P_K_",
            "K_P_B_P_K",
            "_K_P_P_K_",
            "__K_K_K__",
            "_R_R_R_R_",
        ]
    },
    {
        "ball_speed": 7.3,
        "paddle_size": 40,
        "message": "Niveau 43: Pluie de météores",
        "layout": [
            "R_Y_O_P_B_L",
            "_Y_O_P_B_L_",
            "__O_P_B_L__",
            "___P_B_L___",
            "____B_L____",
            "_____L_____",
        ]
    },
    {
        "ball_speed": 7.4,
        "paddle_size": 40,
        "message": "Niveau 44: Le grand X",
        "layout": [
            "K_I_I_I_I_K",
            "_K_I_I_I_K_",
            "__K_I_I_K__",
            "___K_I_K___",
            "__K_I_I_K__",
            "_K_I_I_I_K_",
            "K_I_I_I_I_K",
        ]
    },
    {
        "ball_speed": 7.5,
        "paddle_size": 40,
        "message": "Niveau 45: Tout doit disparaître",
        "layout": [
            "RYPBLORYPBL",
            "YPBLORYPBLR",
            "PBLORYPBLRY",
            "BLORYPBLRYP",
            "LORYPBLRYPB",
        ]
    },
    {
        "ball_speed": 7.6,
        "paddle_size": 35,
        "message": "Niveau 46: Le couloir de la mort",
        "layout": [
            "I_R_O_Y_P_I",
            "I_K_K_K_K_I",
            "I_G_G_G_G_I",
            "I_L_B_W_L_I",
            "I_I_I_I_I_I",
        ]
    },
    {
        "ball_speed": 7.7,
        "paddle_size": 35,
        "message": "Niveau 47: La forteresse invisible",
        "layout": [
            "IIIIIIIIIII",
            "INNNNNNNNNI",
            "IN_K_P_K_NI",
            "IN_P_B_P_NI",
            "INNNNNNNNNI",
            "IIIIIIIIIII",
        ]
    },
    {
        "ball_speed": 7.8,
        "paddle_size": 35,
        "message": "Niveau 48: Apothéose",
        "layout": [
            "R_P_B_L_O_Y",
            "_P_B_L_O_Y_R",
            "__B_L_O_Y_R_P",
            "___L_O_Y_R_P_B",
            "____O_Y_R_P_B_L",
        ]
    },
    {
        "ball_speed": 8.0,
        "paddle_size": 30,
        "message": "Niveau 49: Presque la fin",
        "layout": [
            "I_K_I_K_I_K_I",
            "_K_I_K_I_K_I_K",
            "K_I_K_I_K_I_K_I",
            "_I_K_I_K_I_K_I_",
            "I_K_I_K_I_K_I_K",
        ]
    },
    {
        "ball_speed": 8.0,
        "paddle_size": 100,
        "message": "Niveau 50: BRAVO !",
        "layout": [
            "__L_L_L__B__Y_Y__R_R__",
            "_L_____L_B_Y___Y_R___R",
            "_L_____L_B_Y___Y_R___R",
            "__L_L_L__B__Y_Y__R_R__",
            "_____L___B_Y_Y___R___R",
            "_L_____L_B_Y__Y__R___R",
            "__L_L_L__B_Y___Y_R_R__",
        ]
    },
]
