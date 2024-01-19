from nuvei.utils.nuvei_logger import NuveiLogger

class WebService():
    def __init__(self, service_name: str, logger: NuveiLogger):
        self.logger = logger
        self.service_name = service_name

    def post_req(self):
        self.logger.log_info(self.service_name, '_validate_transaction', 'N/A', 'Post recevied')
        pass
