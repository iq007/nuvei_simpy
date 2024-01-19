import uuid
from nuvei.utils.nuvei_logger import NuveiLogger
from nuvei.domain.transaction import Transaction

class TransactionRepository():
    def __init__(self, name: str, logger: NuveiLogger):
        self._name = name
        self._logger = logger
    
    def save_transaction(self, transaction: Transaction):
        #simulates saving trx to a DB
        transaction.id = uuid.uuid4()
        self._logger.log_info(self._name, '_save_transaction_to_db', transaction.id, f'Transaction {transaction.id} saved in {self._name} DB',)
        return transaction
