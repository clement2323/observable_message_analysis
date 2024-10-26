import json
import pandas as pd
import os
from utils.fonctions_utiles import parse_custom_date, extract_full_name, clean_subject, extract_name, extract_timezone
from utils.email_config import NON_PERSONNE_EMAILS

input_file = os.path.join("input", "messages.json")

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transformer la liste de messages en DataFrame
message_table = pd.DataFrame(data['messages'])
# Process the data
message_table['indicatrice_previous_message'] = message_table['previous_messages'].apply(lambda x: len(x) > 0)
message_table['full_name'] = message_table.sender.apply(extract_full_name)
message_table['date'] = message_table['date'].apply(parse_custom_date)

# Split date into components
message_table[['annee', 'mois', 'jour', 'heure', 'minute', 'seconde']] = message_table['date'].str.split('-', expand=True)
message_table['nb_recipients'] = message_table['recipients'].apply(len)
message_table['prev_msg_count'] = message_table['previous_messages'].apply(len)

# Determine sender type
message_table['sender_type'] = message_table['sender'].apply(lambda x: 'non_personne' if x in NON_PERSONNE_EMAILS else 'personne')

# Clean subject
message_table['subject'] = message_table['subject'].apply(clean_subject)

# Filter messages if necessary
# Filtrer les messages pour ne garder que ceux avec une date et un nom complet valides
message_table = message_table[message_table['date'].notna() & message_table['full_name'].notna()]
print(message_table.to_json())
