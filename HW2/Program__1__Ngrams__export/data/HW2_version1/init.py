def init(modified_data): 
    DB = {}
    for x in modified_data:
        x= x.lower()
        if x in DB:
          DB[x] = DB[x]+1
        else:
          DB[x] = 1
    return DB 