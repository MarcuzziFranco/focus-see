class Command:
    def __init__(self,code,execute) :
        self.code = code
        self.execute = execute
    
    def run(self):
        print(f"Running command:{self.code}")
        self.execute();
        