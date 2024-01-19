import json
from nuvei.domain.transaction import Transaction

class TransactionDeserializer:
    @staticmethod
    def from_json(json_data):
        try:
            transaction_data = json.loads(json_data)
            transaction = Transaction(**transaction_data)
            return transaction
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
