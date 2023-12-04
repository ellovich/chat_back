from fastapi import FastAPI, UploadFile, File
from sqlalchemy.orm import Session

# class PatientDAO(BaseDAO[Patient, SPatientCreate, SPatientUpdate]):
#     model = Patient

# # Серверные эндпоинты
# @app.post("/upload-media/")
# async def upload_media(file: UploadFile = File(...), user_id: int = Form(...), db: Session = Depends(get_db)):
#     contents = await file.read()
#     media = Media(file_name=file.filename, file_data=contents, user_id=user_id)
#     db.add(media)
#     db.commit()
#     db.refresh(media)
#     return {"filename": file.filename}

# # Клиентский эндпоинт для получения файла
# @app.get("/get-media/{media_id}")
# async def get_media(media_id: int, db: Session = Depends(get_db)):
#     media = db.query(Media).filter(Media.id == media_id).first()
#     return JSONResponse(content=media.file_data, media_type="image/jpeg")