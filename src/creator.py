from classes.instance import Instance
from classes.cluster_creator import ClusterCreator

if __name__ == '__main__':
      regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
      instances_initial_data = [
          Instance(name='c6a.12xlarge', makespan=779.6),
          Instance(name='c6in.12xlarge', makespan=826.1),
          Instance(name='r5n.12xlarge', makespan=1199.8),
      ]
      num_checkpoints = 24
      avg_time_checkpoint = 3.88
            
      cluster_creator  = ClusterCreator(regions, instances_initial_data, num_checkpoints, avg_time_checkpoint)
      instance = cluster_creator.select_best_instance()
      
      print(instance.name)
      print(instance.cost)
      print(instance.region)
      print(instance.type)
      print()

