import pymongo

from database.db_conf import MongoDB


async def add_many_shifts(shifts: list[dict]) -> None:
    """
    Add a shift group to the databas.

    :param shifts: A dictionary list with data to be added to the database.
    """
    client: MongoDB = MongoDB()
    collection = client.get_collection("salaries")

    collection.create_index(
        [("user_id", 1), ("date", 1)],
        unique=True,
        name="unique_user_date"
    )
    
    try:
        collection.insert_many(shifts)
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        client.close()
