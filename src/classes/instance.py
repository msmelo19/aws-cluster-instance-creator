from models.instance_market import InstanceMarket

class Instance:
    def __init__(self, name: str, makespan: float, cost: float , type: InstanceMarket, region: str):
        self.name = name
        self.makespan = makespan
        self.cost = cost
        self.type = type
        self.region = region