import type { registrationDetails } from '$lib/types/registrationDetails';
import type { FirebaseApp } from '@firebase/app';
import type { Auth, UserInfo } from 'firebase/auth';
import type { Firestore } from 'firebase/firestore/lite';
import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore/lite';

export const event_name_mapping = {
    VPM: 'Virtual Placement',
    CADMS: 'Cadddction Mechanical Solo',
    CADMD: 'Cadddction Mechanical Duo',
    CADCS: 'Cadddction Civil Solo',
    CADCD: 'Cadddction Civil Duo',
    VAV: 'Vaad Vivad',
    RPNBS: 'Respawn BGMI Squad',
    RPNBT: 'Respawn BGMI TeamDeathMatch',
    RPNVS: 'Respawn Valorant Squad',
    RPNCI: 'Respawn Chess Individual',
    MUNA: 'Model United Nations DISEC',
    MUNU: 'Model United Nations Lok Sabha',
    COV: 'Code Venture',
    CSW: 'Spectrum',
    UPG: 'Campus Bridge',
    AVK: 'Avishkar',
    TSI: 'Jigyasa',
    COS: 'CAD-O-Shop',
    STG: 'StarGaze Offline',
    STGF: 'StarGaze Online',
    FOH: 'Foodoholics',
    CCB: 'Cricbash',
    BSYD: 'Bornpsycos Duo',
    BSYT: 'Bornpsycos Team',
};

export function get_event_cost(event_code) {
    switch (event_code) {
        case 'RPNBS':
            return 160;
        case 'RPNBT':
            return 80;
        case 'RPNVS':
            return 150;
        case 'RPNCI':
            return 50;
        case 'VPM':
            return 70;
        case 'CADMS':
            return 60;
        case 'CADMD':
            return 100;
        case 'CADCS':
            return 60;
        case 'CADCD':
            return 100;
        case 'MUNA':
            return 700;
        case 'MUNU':
            return 700;
        case 'VAV':
            return 50;
        case 'AVK':
            return 150;
        case 'BSYD':
            return 80;
        case 'BSYT':
            return 150;
        case 'COV':
            return 0;
        case 'FOH':
            return 200;
        case 'CCB':
            return 360;
        case 'STG':
            return 60;
        case 'STGF':
            return 0;
        case 'TSI':
            return 0;
        case 'CSW':
            // Spectrum
            return 0;
        case 'UPG':
            return 0;
        case 'COS':
            return 0;
        default:
            return 0;
    }
}

export const event_extra_members_mapping = {
    VPM: 0,
    CADMS: 0,
    CADMD: 1,
    CADCS: 0,
    CADCD: 1,
    VAV: 0,
    RPNBS: 3,
    RPNBT: 3,
    RPNVS: 4,
    RPNCI: 0,
    MUNA: 0,
    MUNU: 0,
    COV: 0,
    CSW: 0,
    UPG: 0,
    AVK: 4,
    TSI: 0,
    COS: 0,
    STG: 0,
    STGF: 0,
    FOH: 3,
    CCB: 5,
    BSYD: 1,
    BSYT: 3,
};

export async function get_user_registrations(app: FirebaseApp, auth: Auth, db: Firestore) {
    const user = auth.currentUser;
    const user_id = user.uid;
    const ref = doc(db, `registrations/${user_id}`);
    const user_doc = await getDoc(ref);
    if (user_doc.exists()) {
        return user_doc.data();
    } else {
        return {};
    }
}

export async function add_new_user_registration(
    app: FirebaseApp,
    auth: Auth,
    db: Firestore,
    event_code: string,
    registration: registrationDetails,
) {
    const user = auth.currentUser;
    const user_id = user.uid;
    const ref = doc(db, `registrations/${user_id}`);
    const user_doc = await getDoc(ref);
    const _data = user_doc.exists() ? user_doc.data() : {};
    _data[event_code] = registration;
    await setDoc(ref, _data);
}

export async function verify_transaction(app: FirebaseApp, db: Firestore, transaction_id: string) {
    // transaction_id is made up of user_id and event_code
    const [user_id, event_code, _] = transaction_id.split('-');
    //const user_id = _[0];
    //const event_code = _[1];
    const ref = doc(db, `registrations/${user_id}`);
    const user_doc = await getDoc(ref);
    const _data = user_doc.data();
    _data[event_code].transaction_status = 'PAID';
    await setDoc(ref, _data);
    const trans_ref = doc(db, `transactions/${user_id}-${event_code}`);
    const __data = _data[event_code];
    await setDoc(trans_ref, __data);
}

export function get_event_date(event_code) {
       switch (event_code) {
        case 'RPNBS':
            return '25-03-2022';
        case 'RPNBT':
            return '25-03-2022';
        case 'RPNVS':
            return '26-03-2022';
        case 'RPNCI':
            return '25-03-2022';
        case 'VPM':
            return '25/26-03-2022';
        case 'CADMS':
            return '26-03-2022';
        case 'CADMD':
            return '26-03-2022';
        case 'CADCS':
            return '26-03-2022';
        case 'CADCD':
            return '26-03-2022';
        case 'MUNA':
               //DISEC
            return '26/27-03-2022';
        case 'MUNU':
               //Lok Sabha
            return '26/27-03-2022';
        case 'VAV':
            return '26/27-03-2022';
        case 'AVK':
            return '25-03-2022';
        case 'BSYD':
            return '27-03-2022';
        case 'BSYT':
            return '27-03-2022';
        case 'COV':
            return '27-03-2022';
        case 'FOH':
            return '26-03-2022';
        case 'CCB':
            return '25/26-03-2022';
        case 'STG':
            return '25/26-03-2022';
        case 'STGF':
            return '25/26-03-2022';
        case 'TSI':
               //Jigyasa
            return '25-03-2022';
        case 'CSW':
            // Spectrum
            return '26-03-2022';
        case 'UPG':
               //Campus Bridge
            return 'Stay tuned';
        case 'COS':
            return '25-03-2022';
        default:
            return 0;
    }
}
