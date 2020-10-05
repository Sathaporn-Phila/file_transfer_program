class File:
    
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        f = open(self.filename, 'r')
        for line in f:
            print(line)
        f.close()
    
    def readbinary(self):
        f = open(self.filename, 'rb')
        r = f.read(1024)
        while r:
            print(r)
            r = f.read(1024)

    def copy(self, newfile):
        f1 = open(self.filename, 'r')
        f2 = open(newfile, 'w')
        for line in f1:
            f2.write(line)
        f1.close()
        f2.close()
    
    def copybinary(self, newfile):
        f1 = open(self.filename, 'rb')
        f2 = open(newfile, 'wb')
        r = f1.read(1024)
        while r:
            f2.write(r)
            r = f1.read(1024)
        f1.close()
        f2.close()