import json
import os
from utils.fonctions_utiles import parse_custom_date, extract_full_name, clean_subject, extract_name, extract_timezone
from utils.email_config import NON_PERSONNE_EMAILS

input_file = os.path.join("src", "data", "input", "messages.json")

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transformer la liste de messages en liste de dictionnaires
message_table = []
for message in data['messages']:
    processed_message = {}
    
    # Traitement des données
    processed_message['indicatrice_previous_message'] = len(message['previous_messages']) > 0
    processed_message['full_name'] = extract_full_name(message['sender'])
    processed_message['date'] = parse_custom_date(message['date'])
    
    # Diviser la date en composants
    if processed_message['date']:
        date_components = processed_message['date'].split('-')
        processed_message['annee'], processed_message['mois'], processed_message['jour'], \
        processed_message['heure'], processed_message['minute'], processed_message['seconde'] = date_components
    
    processed_message['nb_recipients'] = len(message['recipients'])
    processed_message['prev_msg_count'] = len(message['previous_messages'])
    
    # Déterminer le type d'expéditeur
    processed_message['sender_type'] = 'non_personne' if message['sender'] in NON_PERSONNE_EMAILS else 'personne'
    
    # Nettoyer le sujet
    processed_message['subject'] = clean_subject(message['subject'])
    
    # Ajouter les champs originaux
    for key, value in message.items():
        if key not in processed_message:
            processed_message[key] = value
    
    # Filtrer les messages pour ne garder que ceux avec une date et un nom complet valides
    if processed_message['date'] and processed_message['full_name']:
        message_table.append(processed_message)

# Convertir en JSON et imprimer
print(json.dumps(message_table))
