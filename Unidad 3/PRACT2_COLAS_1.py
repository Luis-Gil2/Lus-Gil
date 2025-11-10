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

class QueueInterface:
    def size(self):
        """returns the number of elements in Queue"""
        raise NotImplementedError

    def isEmpty(self):
        """verifies if the Queue is empty"""
        raise NotImplementedError

    def front(self):
        """returns the first element in Queue (without removing it)"""
        raise NotImplementedError

    def enqueue(self, info):
        """adds a new element to the Queue"""
        raise NotImplementedError

    def dequeue(self):
        """returns and removes the first element in Queue"""
        raise NotImplementedError


# =====================================================
# Node.py
# =====================================================
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



class Queue(QueueInterface):
    def __init__(self):
        self.top = None     #inicio
        self.last = None    #   Final
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

    # método adicional para imprimir toda la cola
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

        # Crear pedidos
        o1 = Order(20, "cust1")
        o2 = Order(30, "cust2")
        o3 = Order(40, "cust3")
        o4 = Order(50, "cust4")

        print("Enqueue o1, o2, o3")
        q.enqueue(o1)
        q.enqueue(o2)
        q.enqueue(o3)
        q.printInfo()

        print("Consultar front (sin remover):")
        f = q.front()
        if f is not None:
            f.print()
        else:
            print("Front: None\n")

        print("Enqueue o4 y mostrar estado:")
        q.enqueue(o4)
        q.printInfo()

        print("Dequeue (extraer un elemento) y mostrar estado:")
        removed = q.dequeue()
        print("Removed element:")
        if removed is not None:
            removed.print()
        else:
            print("None")
        q.printInfo()

        print("Extraer todos los elementos uno por uno:")
        while not q.isEmpty():
            r = q.dequeue()
            print("Dequeued:")
            r.print()
            q.printInfo()

        print("Cola vacía? ->", q.isEmpty())

if __name__ == "__main__":
    TestQueue.main()
