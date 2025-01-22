import firebase_admin
from firebase_admin import credentials, firestore
import time


def current_milli_time():
    return str(round(time.time() * 1000))


cred = credentials.Certificate("firebase_creds.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")
sessions_ref = db.collection("sessions")


def user_exists(userid):
    doc = users_ref.document(userid).get()
    return doc.exists


def get_or_create_user(name, email, userid):
    user_doc = users_ref.document(userid)
    if not user_doc.get().exists:
        user_doc.set({"name": name, "email": email, "sessions": []})
    return user_doc.get().to_dict()


def create_session(userid):
    ssid = current_milli_time()
    user_doc = users_ref.document(userid).get()
    if not user_doc.exists:
        raise Exception("User does not exist")

    sessions = user_doc.to_dict().get("sessions", [])
    sessions.append(ssid)
    users_ref.document(userid).update({"sessions": sessions})
    sessions_ref.document(ssid).set({"owner": userid})
    return ssid


def add_message_to_first_chat(role, sessionid, message):
    sessions_ref.document(sessionid).collection("first chat").document(
        current_milli_time()
    ).set({"role": role, "parts": [{"text": message}]})


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
    sessions_ref.document(sessionid).collection("group chat").document(
        current_milli_time()
    ).set({"message": message, "user": username})


def add_message_to_ai_chat(role, sessionid, message):
    sessions_ref.document(sessionid).collection("ai chat").document(
        current_milli_time()
    ).set({"role": role, "parts": [{"text": message}]})


def add_activities(sessionid, activities):
    for activity in activities:
        sessions_ref.document(sessionid).collection("activities").document(
            current_milli_time()
        ).set(activity)


def add_activity_to_itinerary(sessionid, activity, time):
    sessions_ref.document(sessionid).collection("itinerary").document(time).set(
        activity
    )


def get_full_itinerary(sessionid):
    arr = []
    docs = sessions_ref.document(sessionid).collection("itinerary").stream()
    for doc in docs:
        arr.append([doc.id, doc.to_dict()])
    return arr


def get_name_by_userid(userid):
    return users_ref.document(userid).get().to_dict()["name"]


def get_activity_by_id(sessionid, activityid):
    return (
        sessions_ref.document(sessionid)
        .collection("activities")
        .document(activityid)
        .get()
        .to_dict()
    )


def get_all_activities(sessionid):
    arr = []
    docs = sessions_ref.document(sessionid).collection("activities").stream()
    for doc in docs:
        arr.append([doc.id, doc.to_dict()])
    return arr


def add_summary(sessionid, summary):
    sessions_ref.document(sessionid).update({"summary": summary})
