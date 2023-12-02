import boto3
import json
from pkg_resources import resource_filename


class Pricing:
    def __init__(self, region: str, instance_name: str) -> None:
        self.region = region
        self.instance_name = instance_name

    def __get_region_name(self, region_code: str) -> str:
        default_region = 'US East (N. Virginia)'
        endpoint_file = resource_filename('botocore', 'data/endpoints.json')
        try:
            with open(endpoint_file, 'r') as f:
                data = json.load(f)
            # Botocore is using Europe while Pricing API using EU...sigh...
            return str(data['partitions'][0]['regions'][region_code]['description'].replace('Europe', 'EU'))
        except IOError:
            return default_region

    def get_ondemand_instance_price(self) -> float:
        pricing = boto3.client('pricing', region_name='us-east-1') # AWS Pricing API client

        response = pricing.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': self.__get_region_name(self.region)},
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': self.instance_name},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                { 'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used' },
                { 'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA' },
            ]
        )

        if not 'PriceList' in response:
            return None

        # Extract price information
        try:
            instance_data = json.loads(response['PriceList'][0])['terms']['OnDemand']
            id1 = list(instance_data)[0]
            id2 = list(instance_data[id1]['priceDimensions'])[0]
            return float(instance_data[id1]['priceDimensions'][id2]['pricePerUnit']['USD'])
        
        except IndexError:
            return None

    def get_spot_instance_price(self) -> float:
        ec2_client = boto3.client('ec2', region_name=self.region)
        response = ec2_client.describe_spot_price_history(
            InstanceTypes=[self.instance_name],
            MaxResults=1,
            ProductDescriptions=['Linux/UNIX']
        )
        
        if not 'SpotPriceHistory' in response:
            return None

        try:
            spot_price = response['SpotPriceHistory'][0]['SpotPrice']
            return float(spot_price)
        
        except IndexError:
            return None


        
    