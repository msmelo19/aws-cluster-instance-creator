from typing import List
from src.classes.instance import Instance
from src.models.instance_market import InstanceMarket
from src.classes.pricing import Pricing

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
                    ondemand_data = Instance(instance.name, instance.makespan, ondemand_pricing, InstanceMarket.ONDEMAND, region, instance.num_nodes)
                    instances.append(ondemand_data)
                    
                spot_pricing = pricing.get_spot_instance_price()
                if spot_pricing:
                    spot_data = Instance(instance.name, instance.makespan, spot_pricing, InstanceMarket.SPOT, region, instance.num_nodes)
                    instances.append(spot_data)
        
        return instances
    
    def __calc_makespan_cost(self, cost: float, makespan: float, num_nodes: int = 1) -> float:
        return (cost * (makespan / 3600)) * num_nodes
          
    def select_best_instance(self) -> Instance:
        instances = self.__create_intance_list()
        
        print('Choosing the best instance...')
        vm_best = instances[0]
        min_cost = self.__calc_makespan_cost(vm_best.cost, vm_best.makespan, vm_best.num_nodes)

        for instance in instances:
            estimated_makespan = instance.makespan
            
            if instance.market == InstanceMarket.SPOT:
                time_checkpoints = self.num_checkpoints * self.avg_time_checkpoint
                estimated_makespan = time_checkpoints + estimated_makespan
                
            if min_cost > self.__calc_makespan_cost(instance.cost, estimated_makespan, instance.num_nodes):
                vm_best = instance
                min_cost = self.__calc_makespan_cost(instance.cost, estimated_makespan, instance.num_nodes)
                
        return vm_best
    
    def create_log(self, chosen_instance: Instance) -> None:
        print()
        print(f'Create a cluster in region: {chosen_instance.region}')
        print(f'Instance queue: {chosen_instance.name}')
        print(f'Use instance market: {chosen_instance.market}')
        
        if chosen_instance.market == InstanceMarket.SPOT:
            print()
            print(f'You will need to create more queues in your cluster')
            print(f'Instance in 2nd queue: {chosen_instance.name}')
            print(f'Use instance market: {InstanceMarket.ONDEMAND}')
