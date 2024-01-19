import unittest
from unittest.mock import patch
from nuvei.utils.nuvei_logger import NuveiLogger

class TestNuveiLogger(unittest.TestCase):
    def setUp(self):
        self.logger = NuveiLogger('/path/to/log/file.log')

    def test_log_error(self):
        service = 'service_name'
        method = 'method_name'
        transaction_id = 'transaction_id'
        message = 'This is an error message'

        with patch('nuvei.utils.nuvei_logger.logging.Logger.error') as mock_error:
            self.logger.log_error(service, method, transaction_id, message)
            mock_error.assert_called_once_with(message, extra={'service': service, 'method': method, 'transaction_id': transaction_id})

    def test_log_info(self):
        service = 'service_name'
        method = 'method_name'
        transaction_id = 'transaction_id'
        message = 'This is an info message'

        with patch('nuvei.utils.nuvei_logger.logging.Logger.info') as mock_info:
            self.logger.log_info(service, method, transaction_id, message)
            mock_info.assert_called_once_with(message, extra={'service': service, 'method': method, 'transaction_id': transaction_id})

if __name__ == '__main__':
    unittest.main()