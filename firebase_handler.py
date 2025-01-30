import firebase_admin
from firebase_admin import credentials, firestore, auth
import time

import services


def current_milli_time():
    return str(round(time.time() * 1000))


cred = credentials.Certificate("firebase_creds.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")
sessions_ref = db.collection("sessions")


def create_user(name, email, userid):
    for doc in users_ref.get():
        if userid == doc.id:
            return
    users_ref.document(userid).set({'name': name, 'email': email, 'sessions': []})


def create_group(userid):
    ssid = current_milli_time()
    a = users_ref.document(userid).get().to_dict()['sessions']
    a.append(ssid)
    users_ref.document(userid).update({'sessions': a})
    sessions_ref.document(ssid).set({'owner': userid})
    a = [userid]
    sessions_ref.document(ssid).update({'users': a})
    print("returning: ", ssid)
    return ssid


def add_message_to_first_chat(role, sessionid, message):
    sessions_ref.document(sessionid).collection("first chat").document(current_milli_time()).set(
        {'role': role, 'parts': [{'text': message}]})


def get_first_chat(sessionid):
    docs = sessions_ref.document(sessionid).collection("first chat").stream()
    arr = []
    for doc in docs:
        arr.append(doc.to_dict())
    return arr


def get_ai_chat(sessionid):
    docs = sessions_ref.document(sessionid).collection("ai chat").stream()
    arr = []
    for doc in docs:
        arr.append(doc.to_dict())
    return arr


def add_message_to_group_chat(username, sessionid, message):
    sessions_ref.document(sessionid).collection("group chat").document(current_milli_time()).set(
        {'message': message, 'user': username})


def add_message_to_ai_chat(role, sessionid, message):
    sessions_ref.document(sessionid).collection("ai chat").document(current_milli_time()).set(
        {'role': role, 'parts': [{'text': message}]})


def add_activities(sessionid, activities):
    for activity in activities:
        print("adding smth")
        sessions_ref.document(sessionid).collection("activities").document(current_milli_time()).set(activity)


def add_activity_to_itinerary(sessionid, activity):
    id=current_milli_time()
    sessions_ref.document(sessionid).collection("itinerary").document(id).set(activity)
    return id

def remove_activity_from_itinerary(sessionid, activity):
    sessions_ref.document(sessionid).collection("itinerary").document(activity).delete()

def update_activity(sessionid, activityid, fromdate, todate):
    sessions_ref.document(sessionid).collection("itinerary").document(activityid).update({'FromDate': fromdate, 'ToDate': todate})

def set_status(sessionid, status):
    sessions_ref.document(sessionid).update({'status': status})

def get_full_itinerary(sessionid):
    arr = []
    docs = sessions_ref.document(sessionid).collection("itinerary").stream()
    for doc in docs:
        arr.append(doc.to_dict())
    return arr


def get_name_by_userid(userid):
    return users_ref.document(userid).get().to_dict()['name']


def get_activity_by_id(sessionid, activityid):
    return sessions_ref.document(sessionid).collection("activities").document(activityid).get().to_dict()


def get_all_activities(sessionid):
    arr = []
    docs = sessions_ref.document(sessionid).collection("activities").stream()
    for doc in docs:
        arr.append([doc.id,doc.to_dict()])
    return arr


def add_summary(sessionid, summary):
    sessions_ref.document(sessionid).update({"summary": summary})


def get_summary(sessionid):
    return sessions_ref.document(sessionid).get().to_dict()['summary']


def verify_id_token(idToken):
    print(auth.verify_id_token(idToken))
    return auth.create_session_cookie(idToken, 60 * 60 * 24 * 5)


def verify_session_cookie(cookie):
    try:
        print(auth.verify_session_cookie(cookie))
        return True
    except:
        return False


def get_uid(idToken):
    return auth.verify_session_cookie(idToken)['uid']


def get_email(idToken):
    return auth.verify_session_cookie(idToken)['email']


def get_name_by_session_cookie(idToken):
    return auth.verify_session_cookie(idToken)['name']


def get_groups(userid):
    return users_ref.document(userid).get().to_dict()['sessions']


def get_group_name(groupId):
    return "temp name for now"


def get_group_member_count(groupId):
    a = sessions_ref.document(groupId).get().to_dict()['users']
    return len(a)


def group_leave(groupId, userid):
    arr = users_ref.document(userid).get().to_dict()['sessions']
    arr.remove(groupId)
    users_ref.document(userid).update({'sessions': arr})
    arr = sessions_ref.document(groupId).get().to_dict()['users']
    arr.remove(userid)
    sessions_ref.document(groupId).update({'users': arr})


def group_join(groupId, userid):
    a = users_ref.document(userid).get().to_dict()['sessions']
    a.append(groupId)
    users_ref.document(userid).update({'sessions': a})
    # Added to user now adding to group
    a = sessions_ref.document(groupId).get().to_dict()['users']
    a.append(userid)
    sessions_ref.document(groupId).update({'users': a})


def check_group_existance(groupId):
    return sessions_ref.document(groupId).get().exists
