import pathlib
import json
this_folder = pathlib.Path(__file__).parent.absolute()
parent_folder = this_folder.parent


# Rename this file a/c to latest backup
REGISTRATION_FILE = parent_folder / 'registrations-164730643373.json'


def unfucknames(name: str):
    if name.startswith(' '):
        name = name[1:]
    if name.endswith(' '):
        name = name[:-1]
    return name


def main(registration_file):
    REGISTRATIONS = {}
    with open(registration_file, 'r') as f:
        users = json.load(f)

    # registrations = [registration for registration in registrations if registration['transaction_status'] == 'PAID']

    for user_id, registrations in users.items():
        # print(user_id)
        # print(registrations)
        for event_code, registration in registrations.items():
            # print(event_code, registration)
            if event_code not in REGISTRATIONS:
                REGISTRATIONS[event_code] = []
            REGISTRATIONS[event_code].append(registration)
    for event, sorted_regis in REGISTRATIONS.items():
        with open(parent_folder / f'{event}.csv', 'w') as f:
            # f.write('\n'.join([','.join(registration.keys()) for registration in sorted_regis]))
            for regis in sorted_regis:
                f.write(unfucknames(regis['name']) + "," + regis['email'] + '\n')


if __name__ == "__main__":
    main(REGISTRATION_FILE)
