from nuvei.services.globalpay import GlobalPay
from nuvei.domain.transaction import Transaction
from nuvei.infrastructure.transaction_repository import TransactionRepository
import uuid
from nuvei.utils.nuvei_logger import NuveiLogger
import json


# Create an instance of the NuveiLogger class
logger = NuveiLogger('/Users/stefan/Work/Pyenvs/Yukinoaru/logs/file.log')
transaction_repository = TransactionRepository('HPPDB', logger)

# Create an instance of the GlobalPay class
global_pay = GlobalPay(logger, transaction_repository)

data = {
            "amount": 100,
            "currency": "CNY",
            "payment_method": "Alipay"
        }

json_string = json.dumps(data)
        

# Call the process_transaction method
global_pay.post_req(json_string)
