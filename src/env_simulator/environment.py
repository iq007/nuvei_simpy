import simpy
import json
from env_simulator.utils.sim_logger import SimLogger
from dotenv import load_dotenv
import os
import nuvei.services.globalpay as globalpay
import nuvei.infrastructure.transaction_repository as transaction_repository
from nuvei.utils.nuvei_logger import NuveiLogger
from env_simulator.transaction_generator import TransactionGenerator
from env_simulator.resource_decorator import ResourceDecorator



load_dotenv()  # take environment variables from .env.


# Define the environment class
class Environment:
    def __init__(self, resources, simulation):
        self.resources = resources
        self.simulation = simulation
        self.env = simpy.Environment()
        self.nuvei_logger = NuveiLogger(os.getenv('NUVEI_LOG_PATH'))
        self.logger = SimLogger(os.getenv('SIM_LOG_PATH'))
        self.globalPay = globalpay.GlobalPay(self.nuvei_logger, transaction_repository.TransactionRepository('HPPDB', self.nuvei_logger))
        self.transaction_generator = TransactionGenerator(self.simulation['transactions']['provider_distribution'])

    def run_simulation(self):
        self.logger.log_info(f"{self.env.now:7.4f}: Starting simulation...")
        self.logger.log_info(f"{self.env.now:7.4f}: Warming up to process {self.simulation['transactions']['total_count']} transactions...")
        # Create transactions and prepare the process
        for _ in range(self.simulation['transactions']['total_count']):
            #generate a trx as per distribution
            transaction_payload = self.transaction_generator.generate_transaction_payload()
            self.logger.log_info(f"{self.env.now:7.4f} Preparing transaction processing from payload {transaction_payload}")
            self.env.process(self.globalPay.post_req(transaction_payload))

        # Run the simulation
        self.env.run()


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
            resources = [
                {
                    'name': resource.get('name'),
                    'entry_function': resource.get('entry_function'),
                    'failure_rate': resource.get('failure_rate'),
                    'latency_min': resource.get('latency_min'),
                    'latency_max': resource.get('latency_max'),
                    'dependencies': resource.get('dependencies'),
                    'max_threads': resource.get('max_threads'),
                    'faulty_methods': resource.get('faulty_methods'),
                    'latency_methods': resource.get('latency_methods')
                }
                for resource in data['environment']['resources']]
            

            simulation = data['environment']['simulation']
                    
            _env = Environment(resources, simulation)

            for resource in resources:
                #instantiate all resources needed - for now only GlobalPay
                if resource['name'] == 'GlobalApi':
                    ResourceDecorator(_env.globalPay,
                                  _env.env, 
                                  _env.nuvei_logger, 
                                  resource['entry_function'],
                                  resource['faulty_methods'],
                                  resource['latency_methods'],
                                  resource['failure_rate'],
                                  resource['latency_min'],
                                  resource['latency_max'])()
                else:
                    continue

            return _env




