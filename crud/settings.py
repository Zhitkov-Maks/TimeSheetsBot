from database.db_conf import MongoDB


async def create_settings(data: dict, user_id: int) -> None:
    """
    Create or update the user's settings.

    :param data: A dictionary with the entered data.
    :param user_id: The user's ID.
    """
    try:
        client = MongoDB()
        collection = client.get_collection("users_settings")
        collection.update_one(
            {"user_id": user_id}, {"$set": data}, upsert=True
        )
    finally:
        client.close()


async def get_settings_user_by_id(user_id: int) -> dict:
    """
    Get the user's settings.
    
    :param user_id: The telegram ID.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("users_settings")
        data: dict | None = collection.find_one({"user_id": user_id})

        if data is not None:
            return data
        return {}
    finally:
        client.close()    


async def delete_settings(user_id) -> None:
    """
    Delete the records from the database by user ID.

    :param user_id: The telegram ID.
    """
    try:
        client: MongoDB = MongoDB()
        collection = client.get_collection("users_settings")
        collection.delete_one({"user_id": user_id})
    finally:
        client.close()
