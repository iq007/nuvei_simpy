from nuvei.services.web_service import WebService
from nuvei.utils.nuvei_logger import NuveiLogger
from nuvei.utils.transaction_deserializer import TransactionDeserializer
from nuvei.domain.transaction import Transaction
from nuvei.infrastructure.transaction_repository import TransactionRepository
import uuid


class GlobalPay(WebService):
    def __init__(self, logger: NuveiLogger, transaction_repository: TransactionRepository):
        super().__init__('GlobalPay', logger)
        self.transaction_repository = transaction_repository

    def _validate_transaction(self, transaction: Transaction):
        self.logger.log_info(self.service_name, '_validate_transaction', 'N/A', 'Transaction validated')
        return self

    def _deserialize_transaction(self, json_data: str):
        transaction = TransactionDeserializer.from_json(json_data)
        self.logger.log_info(self.service_name, '_deserialize_transaction', 'N/A', f'Transaction deserialized: {transaction}',)
        return transaction

    def _save_transaction_to_db(self, transaction):
        self.transaction_repository.save_transaction(transaction)
        self.logger.log_info(self.service_name, '_save_transaction_to_db', transaction.id, 'Transaction saved in DB',)
        return self

    def _send_transaction_to_provider(self, provider, transaction: Transaction):
        self.logger.log_info(self.service_name, '_send_transaction_to_provider', transaction.id, f'Transaction sent to provider {provider}',)
        return self

    def _process_transaction(self, json_data: dict):
        transaction = self._deserialize_transaction(json_data)
        self._validate_transaction(transaction) \
        ._save_transaction_to_db(transaction) \
        ._send_transaction_to_provider(transaction.payment_method, transaction)

    def post_req(self, json_string):
        # Create a Transaction object (replace with your actual Transaction object
        self.logger.log_info(self.service_name, '_validate_transaction', 'N/A', f'Post recevied: {json_string}')
        self._process_transaction(json_string)