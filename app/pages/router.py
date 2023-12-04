from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.chat.router import router as chat_router
from app.utils import format_number_thousand_separator, get_month_days

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


# @router.get("/hotels/{location}", response_class=HTMLResponse)
# async def get_hotels_page(
#     request: Request,
#     location: str,
#     date_to: date,
#     date_from: date,
#     hotels=Depends(get_hotels_by_location_and_time),
# ):
#     dates = get_month_days()
#     if date_from > date_to:
#         date_to, date_from = date_from, date_to
#     # Автоматически ставим дату заезда позже текущей даты
#     date_from = max(datetime.today().date(), date_from)
#     # Автоматически ставим дату выезда не позже, чем через 180 дней
#     date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)
#     return templates.TemplateResponse(
#         "hotels_and_rooms/hotels.html",
#         {
#             "request": request,
#             "hotels": hotels,
#             "location": location,
#             "date_to": date_to.strftime("%Y-%m-%d"),
#             "date_from": date_from.strftime("%Y-%m-%d"),
#             "dates": dates,
#         },
#     )


# @router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
# async def get_rooms_page(
#     request: Request,
#     date_from: date,
#     date_to: date,
#     rooms=Depends(get_rooms_by_time),
#     hotel=Depends(get_hotel_by_id),
# ):
#     date_from_formatted = date_from.strftime("%d.%m.%Y")
#     date_to_formatted = date_to.strftime("%d.%m.%Y")
#     chat_length = (date_to - date_from).days
#     return templates.TemplateResponse(
#         "hotels_and_rooms/rooms.html",
#         {
#             "request": request,
#             "hotel": hotel,
#             "rooms": rooms,
#             "date_from": date_from,
#             "date_to": date_to,
#             "chat_length": chat_length,
#             "date_from_formatted": date_from_formatted,
#             "date_to_formatted": date_to_formatted,
#         },
#     )


# @router.post("/successful_chat", response_class=HTMLResponse)
# async def get_successful_chat_page(
#     request: Request,
#     _=Depends(add_chat),
# ):
#     return templates.TemplateResponse(
#         "chat/chat_successful.html", {"request": request}
#     )


@router.get("/chat", response_class=HTMLResponse)
async def get_chats_page(
    request: Request,
    #chat=Depends(get_chats),
):
    return templates.TemplateResponse(
        "chat/chat.html",
        {
            "request": request,
         #   "chat": chat,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
