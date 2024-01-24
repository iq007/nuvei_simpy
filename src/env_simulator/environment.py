import simpy
import random
import logging
import json
import random
import uuid
from env_simulator.utils.sim_logger import SimLogger
from dotenv import load_dotenv
import os
import nuvei.services.globalpay as globalpay
import nuvei.infrastructure.transaction_repository as transaction_repository
from nuvei.utils.nuvei_logger import NuveiLogger
from env_simulator.transaction_generator import TransactionGenerator


load_dotenv()  # take environment variables from .env.


# Define the environment class
class Environment:
    def __init__(self, resources, resource_types, simulation):
        self.resources = resources
        self.resource_types = resource_types
        self.simulation = simulation
        self.env = simpy.Environment()
        self.nuvei_logger = NuveiLogger(os.getenv('NUVEI_LOG_PATH'))
        self.logger = SimLogger(os.getenv('SIM_LOG_PATH'))
        self.globalPay = globalpay.GlobalPay(self.nuvei_logger, transaction_repository.TransactionRepository('HPPDB', self.nuvei_logger))
        self.transaction_generator = TransactionGenerator(self.simulation['transactions']['provider_distribution'])

    def run_simulation(self):
        self.logger.log_info(f"{self.env.now:7.4f}: Starting simulation...")
        self.logger.log_info(f"{self.env.now:7.4f}: Processign {self.simulation['transactions']['total_count']} transactions...")
        # Create transactions
        for _ in range(self.simulation['transactions']['total_count']):
            #generate a trx as per distribution
            transaction_payload = self.transaction_generator.generate_transaction_payload()
            self.logger.log_info(f"{self.env.now:7.4f} Init {transaction_payload}")
            self.env.process(self.init_transactions(transaction_payload))

        # Run the simulation
        self.env.run()

    
    def init_transactions(self, transaction_payload):
        # Get the resource dependencies for the transaction
        self.logger.log_info(f"{self.env.now:7.4f}: Processing transaction {transaction_payload}")
        yield self.env.process(self.globalPay.post_req(transaction_payload, self.env))
        #yield self.env.timeout(2000)
        

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
                    'latency_max': resource['latency_max'],
                    'dependencies': resource['dependencies'],
                    'max_threads': resource['max_threads'],
                }
                for resource in data['environment']['resources']
            }

            resource_types = {
                resource_type['type']: resource_type['exceptions']
                for resource_type in data['environment']['resource_types']
            }

            simulation = data['simulation']

            return Environment(resources, resource_types, simulation)




