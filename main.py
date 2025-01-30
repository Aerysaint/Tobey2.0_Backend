from datetime import datetime
import threading

from fastapi import FastAPI, Cookie, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse
import sightseeing_llm_queries as llm
import services

import firebase_handler as fh
import geminiFunctions as gemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"]  # Explicitly expose the Set-Cookie header
)


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
    response = gemini.next_message_for_ai_chat(history)
    fh.add_message_to_ai_chat("model", sessionid, response)
    return "ok"


@app.get("/updateNextInitial")
async def updateNextInitial(sessionid: str):
    history = fh.get_first_chat(sessionid)
    if len(history) % 2 == 0:
        return -1
    response = gemini.next_message_for_initial_chat(history)
    if ("Received hihihiha" in response):
        realhist = history.copy()
        history.append({"role": "model", "parts": [{"text": response}]})
        history.append({"role": "user", "parts": [{"text": "Please give me a summary of my trip again as a json."}]})
        response = gemini.next_message_for_initial_chat(history)
        fh.add_summary(sessionid, response)
        realhist = realhist[0:-2]
        thread = threading.Thread(target=services.additinerary, args=(realhist, sessionid))
        thread.start()
        return "ok"
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
async def addActivityToItinerary(groupid: str, activityid: str, fromdate: str, todate: str):
    # TODO: custom events
    activity = fh.get_activity_by_id(groupid, activityid)
    activity = services.addTimeToActivity(activity, fromdate, todate)
    return fh.add_activity_to_itinerary(groupid, activity)

@app.get("/removeActivityFromItinerary")
async def addActivityToItinerary(groupid: str, activityid: str):
    fh.remove_activity_from_itinerary(groupid, activityid)

@app.get("/updateActivityInItinerary")
async def updateActivityInItinerary(groupid: str, activityid: str, fromdate: str, todate: str):
    fh.update_activity(groupid, activityid, fromdate, todate)


@app.get("/getAllActivities")
async def getAllActivities(groupid: str):
    return fh.get_all_activities(groupid)


@app.get("/createUser")
async def createUser(request: Request):
    idToken = request.cookies.get("session")
    print("token is", idToken)
    email = fh.get_email(idToken)
    userid = fh.get_uid(idToken)
    username = fh.get_name_by_session_cookie(idToken)
    fh.create_user(username, email, userid)
    return "ok"


@app.get("/createGroup")
async def createGroup(request: Request):
    idToken = request.cookies.get("session")
    userid = fh.get_uid(idToken)
    try:
        return {"groupId": fh.create_group(userid)}
    except:
        return {"groupId": None}


class AuthToken(BaseModel):
    idToken: str


@app.post("/authenticateUser")
async def authenticateUser(token: AuthToken):
    print("id token is", token.idToken)
    cookie = fh.verify_id_token(token.idToken)
    response = JSONResponse(content={"status": "ok"}, status_code=200)
    response.set_cookie(
        key="session",
        value=cookie,
        samesite="lax",
        secure=False,
        httponly=True,
        path="/"
    )
    return response


@app.get("/authenticateSession")
async def authenticateSession(request: Request):
    cookie = request.cookies.get("session")
    print("cookie is", cookie)
    return {"session": fh.verify_session_cookie(cookie)}


@app.get("/getGroups")
async def getGroups(request: Request):
    cookie = request.cookies.get("session")
    uid = fh.get_uid(cookie)
    return fh.get_groups(uid)


@app.get("/getGroupName")
async def getGroupName(groupId: str):
    return {"name": fh.get_group_name(groupId)}


@app.get("/getGroupMemberCount")
async def getGroupMemberCount(groupId: str):
    return {"count": fh.get_group_member_count(groupId)}


@app.get("/leaveGroup")
async def leaveGroup(groupId: str, request: Request):
    cookie = request.cookies.get("session")
    userid = fh.get_uid(cookie)
    fh.group_leave(groupId, userid)
    return {"status": "ok"}


@app.get("/joinGroup")
async def joinGroup(groupId: str, request: Request):
    if fh.check_group_existance(groupId) is False:
        return {"status": "Group does not exist"}
    cookie = request.cookies.get("session")
    userid = fh.get_uid(cookie)
    fh.group_join(groupId, userid)

    return {"status": "ok"}


@app.get("/signOut")
async def signOut():
    response = JSONResponse(content={"status": "ok"}, status_code=200)
    response.set_cookie(
        key="session",
        value="",
        samesite="lax",
        secure=False,
        httponly=True,
        path="/",
        max_age=0
    )
    return response
