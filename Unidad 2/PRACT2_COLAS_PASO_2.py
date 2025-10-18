class Order:
    def __init__(self, qty, customer):
        self.customer = customer
        self.qty = qty

    def print(self):
        print("   Customer: " + self.getCustomer())
        print("   Quantity: " + str(self.getQty()))
        print("   -----------")

    def getQty(self):
        return self.qty

    def getCustomer(self):
        return self.customer

class Node:
    def __init__(self, info=None, next_node=None):
        self.info = info
        self.next = next_node

    def getNext(self):
        return self.next

    def setNext(self, node):
        self.next = node

    def getInfo(self):
        return self.info

class QueueInterface:
    def size(self):
        raise NotImplementedError

    def isEmpty(self):
        raise NotImplementedError

    def front(self):
        raise NotImplementedError

    def enqueue(self, info):
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError
     
class Queue(QueueInterface):
    def __init__(self):
        self.top = None
        self.last = None
        self._size = 0

    def size(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    def front(self):
        if self.top is None:
            return None
        return self.top.getInfo()

    def enqueue(self, info):
        node = Node(info)
        if self.top is None:
            self.top = self.last = node
        else:
            self.last.setNext(node)
            self.last = node
        self._size += 1

    def dequeue(self):
        if self.top is None:
            return None
        info = self.top.getInfo()
        self.top = self.top.getNext()
        if self.top is None:
            self.last = None
        self._size -= 1
        return info

    
    def getNth(self, pos):
        if pos < 1 or pos > self._size:
            return None
        current = self.top
        count = 1
        while current is not None:
            if count == pos:
                return current.getInfo()
            current = current.getNext()
            count += 1
        return None

    def printInfo(self):
        print("********** QUEUE DUMP **********")
        print("Size:", self.size())
        node = self.top
        index = 1
        while node is not None:
            print("** Element", index)
            info = node.getInfo()
            if hasattr(info, "print"):
                info.print()
            else:
                print("   ", info)
                print("   -----------")
            node = node.getNext()
            index += 1
        print("*******************************\n")
        
class TestQueue:
    @staticmethod
    def main():
        q = Queue()

        o1 = Order(20, "cust1")
        o2 = Order(30, "cust2")
        o3 = Order(40, "cust3")
        o4 = Order(50, "cust4")

        print("Añadiendo 4 elementos a la cola...\n")
        q.enqueue(o1)
        q.enqueue(o2)
        q.enqueue(o3)
        q.enqueue(o4)

        q.printInfo()

        print("Obteniendo el tercer elemento con getNth(3):")
        nth = q.getNth(3)
        if nth is not None:
            nth.print()
        else:
            print("Posición no válida.")
        print("\n")

        print("Intentando obtener el elemento 10 (inexistente):")
        invalid = q.getNth(10)
        if invalid is None:
            print("Resultado: None (posición inválida)")
        print("\n")

if __name__ == "__main__":
    TestQueue.main()
