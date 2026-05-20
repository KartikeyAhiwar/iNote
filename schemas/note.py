def noteEntity(item) -> dict :
    return{
        "id":str(item["_id"]),
        "title":item["title"],
        "desc":item["desc"],
        "important":item["important"],
    }
def noteEntities(items) -> list :
    return [noteEntity(item) for item in items]