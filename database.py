from pymongo import MongoClient


class Database:
    def __init__(self):
        self.MONGODB_URI = "mongodb://ninad:ratedrko.123@ds115729.mlab.com:15729/faceoff"
        self.client = MongoClient(self.MONGODB_URI, connectTimeoutMS=30000)
        self.db = self.client.get_database("faceoff")
        self.face = self.db.faces

    def getAll(self):
        records = self.face.find({})
        return records

    def pushRECORD(self, record):
        self.face.insert_one(record)

    def pushEntryLog(self, log):
        self.db.entrylog.insert_one(log)

    def pushdatelog(self, d):
        self.db.entrylog.insert_one(d)

    def getlogbydate(self, d):
        return self.db.entrylog.find_one({'_id': d})

    def updatelog(self, id, data, name):

        self.db.entrylog.update_one({'_id': id}, {'$set': {'logs': data}},  upsert=True)
        print(name+' updated')



db = Database()
