import time
import threading

class database:
    count: int
    neighbors: dict
    interested: dict  # subset de vizinhos: interessados em ver o stream
    lock: threading.Lock
    interestedLock: threading.Lock

    def __init__(self):
        self.count = 0
        self.neighbors = dict()
        self.lock = threading.Lock()

    def addNeighbor(self, addr: tuple):
        self.lock.acquire()
        self.neighbors[addr[0]] = self.count
        self.count+=1
        self.lock.release()
    
    def removeNeighbor(self, addr: tuple):
        self.lock.acquire()
        self.neighbors.pop(addr[0])
        self.count-=1
        self.lock.release()
    
    def printNeighbors(self):
        self.lock.acquire()
        print(f"I have {self.count} neighbors")
        for key,value in self.neighbors.items():
            print(f"    My neighbor {key} is the number {value}")
            time.sleep(2)
        self.lock.release()
        print("")
        # Guarantee that the first print shows up from 4 to 4 seconds
        time.sleep(4)