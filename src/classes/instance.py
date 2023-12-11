from src.models.instance_market import InstanceMarket

class Instance:
    def __init__(self, name: str, makespan: float, cost: float = None , market: InstanceMarket = None, region: str = None, num_nodes: int = 1):
        self.name = name
        self.makespan = makespan
        self.cost = cost
        self.market = market
        self.region = region
        self.num_nodes = num_nodes
