from app.chat.model import Chat, Message
from app.doctor.model import Doctor
from app.patient.model import Patient
from app.user.model import AccessToken, User
from sqladmin import ModelView


class UsersAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.access_tokens]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class AccessTokenAdmin(ModelView, model=AccessToken):
    column_list = [AccessToken.id, AccessToken.user, AccessToken.token, AccessToken.created_at]
    name = "Токен"
    name_plural = "Токены"
    icon = "fa-solid fa-key"


class PatientsAdmin(ModelView, model=Patient):
    column_list = [c.name for c in Patient.__table__.c]  + [Patient.user]
    can_delete = False
    name = "Пациент"
    name_plural = "Пациенты"
    icon = "fa-solid fa-hospital-user"


class DoctorsAdmin(ModelView, model=Doctor):
    column_list = [c.name for c in Doctor.__table__.c] + [Doctor.user]
    can_delete = False
    name = "Врач"
    name_plural = "Врачи"
    icon = "fa-solid fa-user-doctor"


class ChatsAdmin(ModelView, model=Chat):
    column_list = [Chat.id, Chat.doctor, Chat.patient, Chat.messages]
    name = "Чат"
    name_plural = "Чаты"
    icon = "fa-solid fa-comments"


class MessagesAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.chat, Message.sender, Message.content, Message.is_read, Message.timestamp]
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-comment"
