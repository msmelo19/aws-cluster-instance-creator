import sys
import json
from src.classes.instance import Instance
from src.classes.cluster_creator import ClusterCreator

if __name__ == '__main__':
    if(not len(sys.argv) >= 2):
        print('Configuration file is needed')

    conf_file = open(sys.argv[1])
    conf_json = json.load(conf_file)
    
    regions = conf_json['regions']
    num_checkpoints = conf_json['num_checkpoints']
    avg_time_checkpoint = conf_json['avg_time_checkpoint']

    num_nodes = conf_json.get('num_nodes', 1)
    instances_initial_data = []
    
    for instance_json in conf_json['instances']:
        if(not instance_json.get('name') or not instance_json.get('makespan')):
            print("Invalid instance datas: Instance name and makespan is required")
            exit()
        instance = Instance(name=instance_json['name'], makespan=instance_json['makespan'], num_nodes=instance_json.get('num_nodes', num_nodes))
        instances_initial_data.append(instance)
            
    cluster_creator  = ClusterCreator(regions, instances_initial_data, num_checkpoints, avg_time_checkpoint)
    instance = cluster_creator.select_best_instance()
    
    cluster_creator.create_log(instance)

