import json
from nuvei.domain.payment_method import PaymentMethod
from nuvei.domain.currency import Currency

class Transaction:
    def __init__(self, amount: int, currency: Currency, payment_method: PaymentMethod):
        self.id = None
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.status = 'Pending'

    def __str__(self):
        return json.dumps(self.__dict__)

    
    
