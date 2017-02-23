import random
from queue import PriorityQueue

from src.entity.flight import Flight

q = PriorityQueue()
q.put((2, "qwe", [Flight(), Flight(), Flight(), Flight(), Flight()]))
q.put((4, "asas", [Flight(), Flight(), Flight()]))
q.put((3, "awregds", [Flight(), Flight()]))
q.put((5, "asdfg", [Flight(), Flight(), Flight(), Flight()]))
q.put((0, "qwerqwe", [Flight(), Flight(), Flight()]))
