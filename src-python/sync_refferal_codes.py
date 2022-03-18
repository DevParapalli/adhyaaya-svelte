from firebase_admin import firestore
import json
from dateutil.parser import parse
import firebase_admin
from firebase_admin import credentials
import pathlib
from time import time

this_folder = pathlib.Path(__file__).parent.absolute()
parent_folder = this_folder.parent

FIREBASE_SA_KEY = this_folder / 'serviceAccountKey.json'
FIREBASE_CA_SA_KEY = this_folder / 'serviceAccountKeyCA.json'

print('[INFO] Authenticating MAIN...')
main_cred = credentials.Certificate(FIREBASE_SA_KEY)
main_app = firebase_admin.initialize_app(main_cred, name='MAIN2')

print('[INFO] Authenticating CA...')
ca_cred = credentials.Certificate(FIREBASE_CA_SA_KEY)
ca_app = firebase_admin.initialize_app(ca_cred, name='CA2')

print('[INFO] Instantiating Client MAIN')
main_client = firestore.client(main_app)

print('[INFO] Instantiating Client CA')
ca_client = firestore.client(ca_app)

print('[INFO] Cloning Registrations...')


regs = {}
print('[INFO] Writing JSON Document...')
with open(parent_folder / f'main_registrations.json', 'w', encoding="utf-8") as f:
    print('[INFO] Fetching Registrations...')
    snapshots = list(main_client.collection('registrations').get())
    print('[INFO] Registraions Fetched')
    for snapshot in snapshots:
        regs[snapshot.id] = snapshot.to_dict()
        
    f.write(json.dumps(regs, indent=4))
    # f.write(json.dumps(k))
print('[INFO] Finished Writing JSON Document')

trans = {}
print('[INFO] Writing JSON Document...')
with open(parent_folder / f'main_transactions.json', 'w', encoding="utf-8") as f:
    print('[INFO] Fetching Transactions...')
    snapshots = list(main_client.collection('transactions').get())
    print('[INFO] Transactions Fetched')
    for snapshot in snapshots:
        trans[snapshot.id] = snapshot.to_dict()
        
    f.write(json.dumps(trans, indent=4))
    # f.write(json.dumps(k))
print('[INFO] Finished Writing JSON Document')


def is_free(code: str):
    if code == 'COV':
        return True
    if code == 'STGF':
        return True
    if code == 'TSI':
        return True
    if code == 'CSW':
        return True
    if code == 'UPG':
        return True
    if code == 'COS':
        return True
    return False


# At this point, k contains all the registrations.
# parse the json file and get all counts of ca_codes
ca_codes = {}
with open(parent_folder / f'ca_codes.json', 'w') as f:
    for user_id, user_registrations in regs.items():
            # print(key) # This is user_id,
            # print(value) # This is a dict of all the registrations
            for event_code, registration in user_registrations.items():
                # print('[INFO] CA CODE: ', registration['refferal_code'], registration['registration_id'])
                if len(registration['refferal_code']) == 0:
                    continue
                # update the count for that specific refferal code.
                # if the refferal code is not in the dict, add it.
                if registration['refferal_code'] not in ca_codes:
                    ca_codes[registration['refferal_code']] = 0 if is_free(event_code) else 1
                    continue
                else:
                    ca_codes[registration['refferal_code']] += 0 if is_free(event_code) else 1
    f.write(json.dumps(ca_codes, indent=4))

print('[INFO] WRITING TO DB')
batch = ca_client.batch()


for code, count in ca_codes.items():
    iter_ref = ca_client.collection('ca_code').document(code)
    batch.set(iter_ref, {'number_of_regis': count})
    # print(code, count)



batch.commit()


# TEST CONDITION FOR CA CODE
#ca_client.collection('ca_code').document('CA_CODE_1').set({'number_of_regis': 1})
# print(json.dumps(ca_codes, indent=4))