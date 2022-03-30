import pymongo
client = pymongo.MongoClient("mongodb+srv://user:user1234@cluster0.7vyjt.mongodb.net/dbname?retryWrites=true&w=majority")
db = client.test
collection = db.test

def __inititalize_db():
    collection.create_index([('curse_name', pymongo.ASCENDING)],
                                  unique=True)
    collection.create_index([('curse_name', pymongo.TEXT)],name="full text searcher")

def __fill_collection():
    import csv

    with open(r"C:\Users\pasho\Desktop\old_staff.csv",encoding='utf8') as file_obj:
        # Create reader object by passing the file
        # object to reader method
        reader_obj = csv.reader(file_obj)
        c = 0
        for row in reader_obj:
            c+=1
            try:
                collection.insert_one({'curse_name':'%s' % row})
                print(c)
            except Exception as e:
                print(e)


def inserting(name:str):
    try:
        db.test.insert_one({'curse_name':'%s' % name})
    except Exception as e:
        print(e)

