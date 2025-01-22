from fastapi import FastAPI
import firebase_handler as fh
import geminiFunctions as gemini

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/updateNextAi")
async def updateNextAi(sessionid: str):
    history = fh.get_ai_chat(sessionid)
    if len(history) % 2 == 0:
        return -1
    # TODO: get the actual AI response using this(for ai chat)
    response = "temp"
    fh.add_message_to_ai_chat("model", sessionid, response)
    return "ok"


@app.get("/updateNextInitial")
async def updateNextInitial(sessionid: str):
    history = fh.get_first_chat(sessionid)
    if len(history) % 2 == 0:
        return -1
    response = gemini.next_message_for_initial_chat(history)
    if(response.__contains__("Received hihihiha")):
        fh.add_summary(sessionid,response)
        return "information gathered"
    fh.add_message_to_first_chat("model", sessionid, response)
    return "ok"


@app.get("/addAiMessage")
async def addAiMessage(sessionid: str, message: str):
    history = fh.get_ai_chat(sessionid)
    if len(history) % 2 == 1:
        return -1
    fh.add_message_to_ai_chat("user", sessionid, message)
    return "ok"


@app.get("/addInitialMessage")
async def addInitialMessage(sessionid: str, message: str):
    history = fh.get_first_chat(sessionid)
    if len(history) % 2 == 1:
        return -1
    fh.add_message_to_first_chat("user", sessionid, message)
    return "ok"


@app.get("/addGroupMessage")
async def addGroupMessage(sessionid: str, message: str, userid: str):
    username = fh.get_name_by_userid(userid)
    fh.add_message_to_group_chat(username, sessionid, message)
    return "ok"


@app.get("/addActivityToItinerary")
async def addActivityToItinerary(sessionid: str, activityid: str, tim):
    # TODO: custom events
    activity = fh.get_activity_by_id(sessionid, activityid)
    fh.add_activity_to_itinerary(sessionid, activity, tim)


@app.get("/getAllActivities")
async def getAllActivities(sessionid: str):
    return fh.get_all_activities(sessionid)

@app.get("/createUser")
async def createUser(username: str, email: str, userid: str):
    fh.create_user(username, email,userid)
    return "ok"

@app.get("/createSession")
async def createSession(userid: str):
    try:
        fh.create_session(userid)
    except:
        return -1
    return "ok"
