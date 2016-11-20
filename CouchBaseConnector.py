from couchbase.bucket import Bucket

class CouchBaseConnector():

    def __init__():
        pass

    def open_connection(self):
        self.db = Bucket('couchbase://localhost/default')

    def insert(self, reading):
        db.upsert(reading['time'], reading)