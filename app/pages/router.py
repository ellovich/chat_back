from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.utils import format_number_thousand_separator, get_month_days

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/chats", response_class=HTMLResponse)
async def get_chats_page(
    request: Request,
):
    token = "SnobZjCORyiNoPlgUmT-kwEw1ecXqu-Ns44KjsYAhHU"

    return templates.TemplateResponse(
        "chat/chats.html",
        {
            "request": request,
            "headers": {
                "Authorization": "Bearer ${token}"
            },
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )


@router.get("/chats/{id}", response_class=HTMLResponse)
async def get_chat_page(
    id: int,
    request: Request,
):
    token = "SnobZjCORyiNoPlgUmT-kwEw1ecXqu-Ns44KjsYAhHU"

    return templates.TemplateResponse(
        "chat/chat.html",
        {
            "request": request,
            "chat_id": id,
            "headers": {
                "Authorization": "Bearer ${token}"
            },
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
