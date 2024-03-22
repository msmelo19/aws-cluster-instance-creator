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
          
    def select_best_instances(self) -> List[Instance]:
        instances = self.__create_intance_list()
        
        print('Choosing the best instance...')
        vm_best = instances[0]
        vm_second_opt = None
        vm_third_opt = None
        min_cost = self.__calc_makespan_cost(vm_best.cost, vm_best.makespan, vm_best.num_nodes)

        for instance in instances:
            estimated_makespan = instance.makespan
            
            if instance.market == InstanceMarket.SPOT:
                time_checkpoints = self.num_checkpoints * self.avg_time_checkpoint
                estimated_makespan = time_checkpoints + estimated_makespan
                
            instance_cost = self.__calc_makespan_cost(instance.cost, estimated_makespan, instance.num_nodes)
                
            print(f'Instance: {instance.name}')
            print(f'Region: {instance.region}')
            print(f'Market: {instance.market}')
            print(f'Makespan: {estimated_makespan}')
            print(f'Instance Price (USD/H): {instance.cost}')
            print(f'Possible Cost: {instance_cost}')              
            print('\n')
                
            if min_cost > instance_cost:
                vm_third_opt = vm_second_opt
                vm_second_opt = vm_best
                vm_best = instance
                min_cost = instance_cost

        return [vm_best, vm_second_opt, vm_third_opt]
    
    def create_log(self, chosen_instance: Instance) -> None:
        if not chosen_instance:
            return

        print()
        print(f'Create a cluster in region: {chosen_instance.region}')
        print(f'Instance queue: {chosen_instance.name}')
        print(f'Use instance market: {chosen_instance.market}')