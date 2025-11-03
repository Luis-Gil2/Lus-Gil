"""
MYLINKEDLIST
IMPLEMENTACIÓN DE UNA LINKED LIST SIMPLE EN PYTHON.
AUTOR: LUIS GIL
"""

class NODE:
    def __init__(self, DATA):
        self.DATA = DATA
        self.NEXT = None

class LINKEDLIST:
    def __init__(self):
        self.HEAD = None

    def APPEND(self, DATA):
        NEW_NODE = NODE(DATA)
        if not self.HEAD:
            self.HEAD = NEW_NODE
            return
        LAST = self.HEAD
        while LAST.NEXT:
            LAST = LAST.NEXT
        LAST.NEXT = NEW_NODE

    def PREPEND(self, DATA):
        NEW_NODE = NODE(DATA)
        NEW_NODE.NEXT = self.HEAD
        self.HEAD = NEW_NODE

    def DELETE(self, DATA):
        CURRENT = self.HEAD
        if not CURRENT:
            return False
        if CURRENT.DATA == DATA:
            self.HEAD = CURRENT.NEXT
            return True
        while CURRENT.NEXT:
            if CURRENT.NEXT.DATA == DATA:
                CURRENT.NEXT = CURRENT.NEXT.NEXT
                return True
            CURRENT = CURRENT.NEXT
        return False

    def FIND(self, DATA):
        CURRENT = self.HEAD
        while CURRENT:
            if CURRENT.DATA == DATA:
                return True
            CURRENT = CURRENT.NEXT
        return False

    def TO_LIST(self):
        RESULT = []
        CURRENT = self.HEAD
        while CURRENT:
            RESULT.append(CURRENT.DATA)
            CURRENT = CURRENT.NEXT
        return RESULT

    def __STR__(self):
        return " -> ".join(str(X) for X in self.TO_LIST())