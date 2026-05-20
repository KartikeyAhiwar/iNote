from fastapi import APIRouter, Request
from models.note import Note
from fastapi.responses import HTMLResponse
from config.db import conn
from schemas.note import noteEntity, noteEntities
from fastapi.templating import Jinja2Templates
from ichat import get_response
from fastapi.responses import JSONResponse

note = APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/")
async def read_item(request: Request):
    docs = conn.Notes.Notes.find({})

    newdocs = []
    for doc in docs:
        newdocs.append({
            "id":doc["_id"],
            "note": doc.get("note", "")})

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "newdocs": newdocs
        }
    )

@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.Notes.Notes.insert_one(formDict)
    return {"Success":True}


@note.post("/ichat")
async def ichat(request: Request):

    form = await request.form()

    user_message = form.get("chat")

    print(user_message)

    bot_reply = get_response(user_message)

    return JSONResponse({

        "reply": bot_reply

    })