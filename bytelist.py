class ByteList:
    def __init__(self, *bytelist, value=None):
        self.value = value
        self.list = []
        for byte in bytelist:
            self.list.append(byte)

    def add(self, byte):
        self.list.append(byte)

    def __add__(self, byte):
        return ByteList(*self.list, byte, value=self.value)

    def setList(self, bytelist):
        self.list = bytelist

    def getList(self):
        return self.list

    def hasValue(self):
        return value != None

    def setValue(self, v):
        self.value = v

    def getValue(self):
        return self.value