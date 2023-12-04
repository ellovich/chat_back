from datetime import datetime

import pytest

from app.chat.dao import ChatDAO


@pytest.mark.parametrize("user_id, room_id", [
    (2,2),
    (2,3),
    (1,4),
    (1,4),
])
async def test_chat_crud(user_id, room_id):
    # Добавление брони
    new_chat = await ChatDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_chat["user_id"] == user_id
    assert new_chat["room_id"] == room_id

    # Проверка добавления брони
    new_chat = await ChatDAO.find_one_or_none(id=new_chat.id)

    assert new_chat is not None

    # Удаление брони
    await ChatDAO.delete(
        id=new_chat["id"],
        user_id=user_id,
    )

    # Проверка удаления брони
    deleted_chat = await ChatDAO.find_one_or_none(id=new_chat["id"])
    assert deleted_chat is None
    