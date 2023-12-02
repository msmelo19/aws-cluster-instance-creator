from typing import List
from classes.instance import Instance
from models.instance_market import InstanceMarket
from classes.pricing import Pricing

class ClusterCreator:
    def __init__(self, regions: List[str], instances_initial_data: List[Instance], num_checkpoints: int, avg_time_checkpoint: float) -> None:
        self.regions = regions
        self.instances_initial_data = instances_initial_data
        self.num_checkpoints = num_checkpoints
        self.avg_time_checkpoint = avg_time_checkpoint

    def __create_intance_list(self) -> List[Instance]:
        print('Creating instance list...')
        instances: List[Instance] = []

        for region in self.regions:
            for instance in self.instances_initial_data:
                pricing = Pricing(region, instance.name)
                
                ondemand_pricing = pricing.get_ondemand_instance_price()
                if ondemand_pricing:
                    ondemand_data = Instance(instance.name, instance.makespan, ondemand_pricing, InstanceMarket.ONDEMAND, region)
                    instances.append(ondemand_data)
                    
                spot_pricing = pricing.get_spot_instance_price()
                if spot_pricing:
                    spot_data = Instance(instance.name, instance.makespan, spot_pricing, InstanceMarket.SPOT, region)
                    instances.append(spot_data)
        
        return instances
          
    def select_best_instance(self) -> Instance:
        instances = self.__create_intance_list()
        
        print('Choosing the best instance...')
        vm_best = instances[0]
        min_cost = vm_best.cost * vm_best.makespan

        for instance in instances:
            makespan_line = instance.makespan
            
            if instance.type == InstanceMarket.SPOT:
                time_checkpoints = self.num_checkpoints * self.avg_time_checkpoint
                makespan_line = time_checkpoints + makespan_line
                
            if min_cost > (instance.cost * makespan_line):
                vm_best = instance
                min_cost = instance.cost * makespan_line
                
        return vm_best
