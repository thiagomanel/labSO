from .aging import Aging
from .fifo import FIFO
from .lru import LRU
from .nru import NRU
from .random_alg import Random
from .second_chance import SecondChance

algorithms = {
    "aging": Aging(),
    "fifo": FIFO(),
    "lru": LRU(),
    "nru": NRU(),
    "random": Random(),
    "second-chance": SecondChance()
}

def get_algorithm(algorithm_name):
    assert algorithm_name in algorithms.keys(), "ERROR: Algorithm %s not found"%algorithm_name
    return algorithms[algorithm_name]
