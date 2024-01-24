import random
import json

class TransactionGenerator:
    def __init__(self, provider_distribution):
        self.provider_distribution = provider_distribution

    def generate_transaction_payload(self) -> str:
        transaction_types = list(self.provider_distribution.keys())
        probabilities = list(self.provider_distribution.values())
        transaction = {
            "amount": random.randint(1, 100),
            "currency": random.choices(["CNY", "USD", "EUR"])[0],
            "payment_method": random.choices(transaction_types, probabilities)[0]
        }
        
        return json.dumps(transaction)