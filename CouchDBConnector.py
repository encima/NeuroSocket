import couchdb

class CouchDBConnector():
    
    def __init__(self, db_name, user, pwd):
        self.dbname = db_name
        self.server = couchdb.Server()
        self.server.resource.credentials = (user, pwd)

        def open_connection(self):
            try:
                self.db = server[self.dbname]
            except:
                self.db = server.create(self.dbname)


        def insert(self, reading);
            return db.save(reading)

        
