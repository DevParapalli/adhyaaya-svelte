from random import randint, random
from firebase_admin import firestore
import json
from dateutil.parser import parse
import firebase_admin
from firebase_admin import credentials
import pathlib
from time import time

from collections import OrderedDict
from operator import itemgetter


this_folder = pathlib.Path(__file__).parent.absolute()
parent_folder = this_folder.parent

# FIREBASE_SA_KEY = this_folder / 'serviceAccountKey.json'
FIREBASE_CA_SA_KEY = this_folder / 'serviceAccountKeyCA.json'


print('[INFO] Authenticating CA...')
ca_cred = credentials.Certificate(FIREBASE_CA_SA_KEY)
ca_app = firebase_admin.initialize_app(ca_cred, name='CA3')

print('[INFO] Instantiating Client CA')
ca_client = firestore.client(ca_app)

RANKS = []
CA_CODES = []
with open(parent_folder / f'ca_codes.json', 'r') as f:
    data = json.load(f)
    CA_CODES = data
    RANKS = sorted(data.items(), key=itemgetter(1), reverse=True)



CAS = {}
with open(parent_folder / f'cas.json', 'r') as f:
    CAS = json.load(f)

batch = ca_client.batch()

for user_id, details in CAS.items():
    iter_ref = ca_client.collection('users').document(user_id)
    code = user_id[:7]
    rank = 30 + randint(0, 120) 
    if code in CA_CODES:
        rank = RANKS.index((code, CA_CODES[code])) # We ignore the first rank, cuz its the default registration code.
    details['rank'] = rank
    batch.set(iter_ref, details, merge=True)
    # print(iter_ref, details, rank)
    
    # batch.update(iter_ref, {'rank': rank})

batch.commit()
