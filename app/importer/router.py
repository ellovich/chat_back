import codecs
import csv
from typing import Literal

from fastapi import APIRouter, Depends, UploadFile

from app.exceptions import CannotAddDataToDatabase, CannotProcessCSV
from app.importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format
from app.auth.auth import current_active_user

router = APIRouter(
    prefix="/import",
    tags=["DB Import"],
)


@router.post(
    "/{table_name}",
    status_code=201,
    dependencies=[Depends(current_active_user)],
)
async def import_data_to_table(
    file: UploadFile,
    table_name: Literal["doctors", "patients", "users", "chats"],
):
    ModelDAO = TABLE_MODEL_MAP[table_name]
    # Внутри переменной file хранятся атрибуты:
    # file - сам файл, filename - название файла, size - размер файла.
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=";")
    data = convert_csv_to_postgres_format(csvReader)
    file.file.close()
    if not data:
        raise CannotProcessCSV
    added_data = await ModelDAO.add_bulk(data)
    if not added_data:
        raise CannotAddDataToDatabase
