# Setup CA Firebase Project, and then create a mapping of the codes to their profile details.
# Ideally we should only need the users thingy

from firebase_admin import firestore
import json
from dateutil.parser import parse
from time import time
import firebase_admin
from firebase_admin import credentials
import pathlib

this_folder = pathlib.Path(__file__).parent.absolute()
parent_folder = this_folder.parent

FIREBASE_CA_SA_KEY = this_folder / 'serviceAccountKeyCA.json'

print('[INFO] Authenticating CA...')
ca_cred = credentials.Certificate(FIREBASE_CA_SA_KEY)
ca_app = firebase_admin.initialize_app(ca_cred, name='CA')


ca_client = firestore.client(ca_app)


import re
REGEX = re.compile('[\n\r\t,]')
def escape(string):
    if isinstance(string, str):
        a = REGEX.sub('_', string)
    else:
        a = str(string)
    a = a.encode('ascii', 'ignore')
    a = a.decode()
    return a






cas = {}
print('[INFO] Writing JSON Document...')
with open(parent_folder / f'cas.json', 'w', encoding="utf-8") as f:
    print('[INFO] Fetching Registrations...')
    snapshots = list(ca_client.collection('users').get())
    print('[INFO] Registraions Fetched')
    for snapshot in snapshots:
        cas[snapshot.id] = snapshot.to_dict()
        
    f.write(json.dumps(cas, indent=4))
    # f.write(json.dumps(k))
print('[INFO] Finished Writing JSON Document')

cac = {}
with open(parent_folder / f'cas-registrations.json', 'w', encoding="utf-8") as f:
    snapshots = list(ca_client.collection('ca_code').get())
    for snapshot in snapshots:
        cac[snapshot.id] = snapshot.to_dict()
    f.write(json.dumps(cac, indent=4))


_LINE = "user_id, ca_code, first_name, last_name, phone, city, college_name, address, country, about, tasks_completed, registrations"

with open(parent_folder / f'cas.csv', 'w', encoding="utf-8") as f:
    f.write(_LINE + '\n')
    for [key, value] in cas.items():
        code = key[:7]
        if code in cac:
            registrations = cac[code]['number_of_regis']
        else: 
            registrations = 0
        count = 0
        for [_key, _value] in value['task_complition_data'].items():
            if _value:
                count += 1
        f.write(f"{key},{key[:7]}, {escape(value['first_name'])}, {escape(value['last_name'])}, {escape(value['phone'])}, {escape(value['city'])}, {escape(value['college_name'])}, {escape(value['address'])}, {value['country']}, {escape(value['about'])}, {count}, {registrations}\n")
    
# We can now convert this to a csv file.
# IDK if we should have the task thingy. I am going to just use the