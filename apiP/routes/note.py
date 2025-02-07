from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import conn
from bson import ObjectId

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    """Fetch all notes from MongoDB and render them in the template."""
    docs = conn.notes.notes.find({})
    newDocs = [{"id": str(doc["_id"]), "title": doc["title"], "desc": doc["desc"]} for doc in docs]
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


@note.post("/", response_class=HTMLResponse)
async def create_item(request: Request, title: str = Form(...), desc: str = Form(...)):
    """Handle form submission, save the note, and refresh the page with updated notes."""
    new_note = {"title": title, "desc": desc}
    conn.notes.notes.insert_one(new_note)

    # Fetch updated notes from database
    docs = conn.notes.notes.find({})
    newDocs = [{"id": str(doc["_id"]), "title": doc["title"], "desc": doc["desc"]} for doc in docs]

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs, "message": "Note added successfully!"})
