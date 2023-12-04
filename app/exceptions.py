from fastapi import HTTPException, status

class ChatException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(ChatException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"
        
class IncorrectEmailOrPasswordException(ChatException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"
        
class TokenExpiredException(ChatException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"
        
class TokenAbsentException(ChatException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"
        
class IncorrectTokenFormatException(ChatException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"
        
class UserIsNotPresentException(ChatException):
    status_code=status.HTTP_401_UNAUTHORIZED

class CannotAddDataToDatabase(ChatException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить запись"

class CannotProcessCSV(ChatException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось обработать CSV файл"
