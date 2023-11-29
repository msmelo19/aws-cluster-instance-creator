from models.instance_market import InstanceMarket

class Instance:
    def __init__(self, name: str, makespan: float, cost: float = None , type: InstanceMarket = None, region: str = None):
        self.name = name
        self.makespan = makespan
        self.cost = cost
        self.type = type
        self.region = region
