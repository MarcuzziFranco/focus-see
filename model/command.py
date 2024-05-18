class Command:
    def __init__(self,code,execute,description) :
        self.code = code
        self.execute = execute
        self.description = description
    
    def run(self):
        self.execute();
        