from classes.instance_initial_data import InstanceInitialData
from classes.cluster_creator import ClusterCreator

if __name__ == '__main__':
      regions = ['us-east-1', 'us-east-2']
      instances_initial_data = [
          InstanceInitialData('c6a.12xlarge', 779.6),
          InstanceInitialData('c6in.12xlarge', 826.1),
          InstanceInitialData('r5n.12xlarge', 1199.8),
      ]
            
      cluster_creator  = ClusterCreator(regions, instances_initial_data)
      instance = cluster_creator.select_best_instance()
      
      print(instance.name)
      print(instance.makespan)
      print(instance.cost)
      print(instance.region)
      print(instance.type)
      print()

