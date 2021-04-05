
class DataGenerator:

    def __init__(self):
        self.data = None

    def generate_data(self):
        self.data = [{
            f"planes:0":
                {
                    "kind": "tourist",
                    "num_seats": 200,
                    "category": "global",
                    "from": "Badajoz",
                    "to": "Barcelona",
                    "purchased_seats": "{}",  # We are going to use json.dumps
                    "days": "Tuesday",
                    "hour": "7:00"
                },
            f"planes:1":
                {
                    "kind": "tourist",
                    "num_seats": 200,
                    "category": "global",
                    "from": "Badajoz",
                    "to": "Barcelona",
                    "purchased_seats": "{}",  # We are going to use json.dumps
                    "days": "Thursday",
                    "hour": "7:00"
                }
        }]

    def get_data(self):
        return self.data
