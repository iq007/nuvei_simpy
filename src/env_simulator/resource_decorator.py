import functools
import json
import random
from simpy import Environment
from nuvei.utils.nuvei_logger import NuveiLogger
import types

class ResourceDecorator:
    def __init__(self, resource, env: Environment, logger: NuveiLogger, entry_function: str, faulty_methods: list, latency_methods: list, failure_rate: float, latency_min: float, latency_max: float):
        self.failure_rate = failure_rate
        self.latency_min = latency_min
        self.latency_max = latency_max
        self.faulty_methods = faulty_methods
        self.latency_methods = latency_methods
        self.entry_function = entry_function
        self.logger = logger
        self.env = env
        self.resource = resource  # the decorated resource

        
    def _add_exceptions(self, func, exception):
        @functools.wraps(func) 
        def wrapper(*args, **kwargs):
            if random.random() <= self.failure_rate:
                self.logger.log_error(self.resource.service_name, func.__name__, 'N/A', f'{exception.get("type")}: {exception.get("description")}')
                #yield self.env.timeout(1)
                return False
            else:
                self.logger.log_info(self.resource.service_name, func.__name__, 'N/A', 'No errors')  
                #yield self.env.timeout(1)
                return func(*args, **kwargs)
        return wrapper

    
    def _yeild_timeout(self, func):
        @functools.wraps(func) 
        def wrapper(*args, **kwargs):
            self.logger.log_info(self.resource.service_name, func.__name__, 'N/A', 'Entry function called')
            return func(*args, **kwargs)
            yield self.env.timeout(1000)
        return wrapper
    
    def decorate(self):
        for method in self.faulty_methods:
            method_name = method.get('name')
            exception = method.get('exception')
            decorated_method = self._add_exceptions(getattr(self.resource, method_name), exception)
            setattr(self.resource, method_name, decorated_method)
        
        method_name = self.entry_function
        decorated_method = self._yeild_timeout(getattr(self.resource, method_name))
        setattr(self.resource, method_name, decorated_method)

    def __call__(self):
        self.decorate()
