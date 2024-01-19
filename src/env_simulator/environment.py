import simpy
import random
import logging
import json
import random
import uuid
from env_simulator.utils.sim_logger import SimLogger
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


# Define the environment class
class Environment:
    def __init__(self, resources, resource_types, simulation):
        self.resources = resources
        self.resource_types = resource_types
        self.simulation = simulation
        self.env = simpy.Environment()
        self.logger = SimLogger(os.getenv('SIM_LOG_PATH'))

    def _generate_transaction(self, provider_distribution):
        transaction_types = list(provider_distribution.keys())
        probabilities = list(provider_distribution.values())
        random_guid = uuid.uuid4()
        return random.choices(transaction_types, probabilities)[0], random_guid

    def run_simulation(self):
        self.logger.log_info(f"{self.env.now:7.4f}: Starting simulation...")
        self.logger.log_info(f"{self.env.now:7.4f}: Processign {self.simulation['transactions']['total_count']} transactions...")
        # Create transactions
        for transaction_no in range(self.simulation['transactions']['total_count']):
            #generate a trx as per distribution
            transaction, guid = self._generate_transaction(self.simulation['transactions']['provider_distribution'])
            self.logger.log_info(f"{self.env.now:7.4f} Init {transaction} - {guid}")
            self.env.process(self.init_transactions(transaction, guid))

        # Run the simulation
        self.env.run()

    
    def init_transactions(self, transaction, guid):
        # Get the resource dependencies for the transaction
        self.logger.log_info(f"{self.env.now:7.4f}: Init trx...")
        dependencies = self.get_dependencies(transaction)
        yield self.env.timeout(2000)
        # Check if any of the dependencies have failed
        if any(resource['name'] in self.resources and not self.resources[resource['name']]['status'] for resource in dependencies):
            # Log the failure event
            self.logger.log_info(f"{self.env.now:7.4f} Transaction {transaction} - {guid} failed due to dependency failure")
        else:
            # Process the transaction
            self.logger.log_info(f"{self.env.now:7.4f} Transaction {transaction} - {guid} processed")
        

    def get_dependencies(self, resource_name):
        # Get the dependencies for a given resource
        dependencies = []
        #for resource in self.resources:
        #    if resource['name'] == resource_name:
        #        dependencies = resource['dependencies']
        #        break
        return dependencies



class EnvironmentFactory:
    @staticmethod
    def create_environment(json_file_path: str) -> Environment:
        with open(json_file_path) as file:
            data = json.load(file)
            resources = {
                resource['name']: {
                    'status': True,
                    'failure_rate': resource['failure_rate'],
                    'failure_min_duration': resource['failure_min_duration'],
                    'failure_max_duration': resource['failure_max_duration'],
                    'latency_min': resource['latency_min'],
                    'latency_max': resource['latency_max']
                }
                for resource in data['environment']['resources']
            }

            resource_types = {
                resource_type['type']: resource_type['exceptions']
                for resource_type in data['environment']['resource_types']
            }

            simulation = data['simulation']

            return Environment(resources, resource_types, simulation)




