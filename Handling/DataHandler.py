import pandas as pd


class DB:

    def __init__(self):
        self.path = 'Handler/db.txt'
        self.table = {}
        self.load_table()
        
        self.code = 'Handler/code.txt'
        self.code = ""
        self.load_code()
    
    def load_table(self):
        lst = []
        with open(self.path, "r+") as f:
            lst = f.readlines()
        for i in range(len(lst)):
            # headers?
            self.table[i] = lst[i]
        return
    
    def load_code(self):
        with open(self.path, "r+") as f:
            self.code = "\n".join(f.readlines())
    
    def add_line(self, line):
        with open("Handler/code.txt", "a+") as f:
            f.write(line + "\n")

    def get_code(self):
        self.load_code()
        return self.code

    def delete_code(self):
        with open("Handler/code.txt", "a+") as f:
            pass

    


    def logMessage(self, row):
        with open(self.path, "a+") as f:
            f.write(", ".join(row) + "\n")
    
    def addMessage(self, message):
        idx = len(self.table)
        row = [message.author.name, message.content, message.created_at.strftime("%m/%d/%Y, %H:%M:%S")]
        self.table[idx] = row
        self.logMessage(row)
        print(self.table)
    
        
    