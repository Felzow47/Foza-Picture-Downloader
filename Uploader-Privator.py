
import keyboard
import time
import threading


import keyboard
import time
import threading

# Configuration
DELAY = 0.2  # Délai entre chaque touche
SEQUENCE_DELAY = 0.5  # Délai entre chaque bloc d'action
RUNNING = True

def killswitch():
    global RUNNING
    
    keyboard.wait('esc')
    RUNNING = False

def get_user_sequence():
    print("Choisissez la séquence à exécuter :")
    print("1 - Remove (ne plus partager)")
    print("2 - Upload (partager)")
    while True:
        choice = input("Votre choix (1 ou 2) : ").strip()
        if choice == '1':
            return 'remove'
        elif choice == '2':
            return 'upload'
        else:
            print("Choix invalide. Veuillez entrer 1 ou 2.")

# Séquences paramétrables

SEQUENCES = {
    'remove': [
        ['enter'],
        ['down'], ['enter'],
        ['down'], ['enter'],
        ['right'], ['enter'],
        ['down'], ['enter'],
        ['up'], ['enter'],
        ['down'], ['enter'],
        ['right'],
    ],
    'upload': [
        ['enter'],
        ['down'], ['enter'], ['enter'],
        'pause',
        ['down'], ['enter'],
        ['down'], ['enter'], ['enter'],
        'pause',
        ['right'], ['enter'],
        ['down'], ['enter'], ['enter'],
        'pause',
        ['up'], ['enter'],
        ['down'], ['enter'], ['enter'],
        'pause',
        ['right'],
    ]
}



threading.Thread(target=killswitch, daemon=True).start()

user_seq = get_user_sequence()
sequence = SEQUENCES[user_seq]
print("Choix de la séquence :", user_seq)
print("Vous avez 10 secondes pour vous préparer.")
time.sleep(10)
print(f"Lancement de la séquence : {user_seq} Appuyez sur 'esc' pour arrêter le script.")
while RUNNING:
    for action in sequence:
        if not RUNNING:
            break
        if action == 'pause':
            time.sleep(5)
            continue
        for key in action:
            if not RUNNING:
                break
            keyboard.press_and_release(key)
            time.sleep(DELAY)
        time.sleep(SEQUENCE_DELAY)
    # Boucle infinie jusqu'à killswitch

print("Script arrêté.")

while RUNNING:
    for action in sequence:
        for key in action:
            if not RUNNING:
                break
            keyboard.press_and_release(key)
            time.sleep(DELAY)
        time.sleep(SEQUENCE_DELAY)
        if not RUNNING:
            break
    # Boucle infinie jusqu'à killswitch

print("Script arrêté.")
