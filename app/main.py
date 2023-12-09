import json
import time
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk

from app.admin.views import AttachmentsAdmin, ChatsAdmin, DoctorsAdmin, MessagesAdmin, PatientsAdmin, UsersAdmin, AccessTokenAdmin
from app.config import settings
from app.database import engine

from app.images.router import router as router_images
from app.chat.router import router as router_chats
from app.importer.router import router as router_import
from app.doctor.routes import router as router_doctor
from app.patient.routes import router as router_patient
from app.logger import logger
from app.pages.router import router as router_pages
from app.prometheus.router import router as router_prometheus
from app.auth.routes import add_auth_routes


app = FastAPI(
    title="МойДоктор",
    version="0.1.0",
    root_path="/",
    summary="API для мобильного чата пациент-врач"
)


if settings.MODE != "TEST":
    # Подключение Sentry для мониторинга ошибок. Лучше выключать на период локального тестирования
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )


# Основные роутеры
add_auth_routes(app)
app.include_router(router_doctor)
app.include_router(router_patient)
app.include_router(router_chats)
#app.add_websocket_route("/chat", router_ws_chats)

# Дополнительные роутеры
app.include_router(router_images)
app.include_router(router_prometheus)
app.include_router(router_import)

# Подключение CORS, чтобы запросы к API могли приходить из браузера 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(router_pages)

if settings.MODE == "TEST":
    # При тестировании через pytest, необходимо подключать Redis, чтобы кэширование работало.
    # Иначе декоратор @cache из библиотеки fastapi-cache ломает выполнение кэшируемых эндпоинтов.
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


# Подключение эндпоинта для отображения метрик для их дальнейшего сбора Прометеусом
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


# Подключение админки
admin = Admin(app, engine)#, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(AccessTokenAdmin)
admin.add_view(PatientsAdmin)
admin.add_view(DoctorsAdmin)
admin.add_view(ChatsAdmin)
admin.add_view(MessagesAdmin)
admin.add_view(AttachmentsAdmin)


app.mount("/static", StaticFiles(directory="app/static"), "static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response



from app.chat.ws_router import ws_manager

@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await ws_manager.connect(websocket, client_id=chat_id)
    try:
        while True:
            message_text = await websocket.receive_text()
            message_data = json.loads(message_text)
            await ws_manager.broadcast(chat_id= chat_id, 
                                       message_data=message_data, 
                                       add_to_db=True)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast(chat_id= chat_id,  
                                   message_data={},
                                   add_to_db=False)
