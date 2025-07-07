import json
import os

class Database:
    def add_data(self, name, email, password):
        database = {}
        if os.path.exists('db.json'):
            with open('db.json', 'r') as rf:
                try:
                    database = json.load(rf)
                except json.JSONDecodeError:
                    database = {}

        if email in database:
            return 0
        else:
            database[email] = [name, password]
            with open('db.json', 'w') as wf:
                json.dump(database, wf, indent=4)
            return 1

    def search(self,email,password):

        with open('db.json','r') as rf:
            database = json.load(rf)
            if email in database:
                if database[email][1] == password:
                    return 1
                else:
                    return 0
            else:
                return 0