import requests

class telegram_notification:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message: str) -> None:
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.get(self.base_url, params=payload)
        response.raise_for_status()

    def new_properties_notification(self, new_properties: list, property_count: int) -> None:
        if not new_properties:
            message = (
                f"There are no new properties out of {property_count} properties "
                "on PropertyGuru matching your criteria since the last time we checked."
            )
            self.send_message(message)
            return

        count = len(new_properties)
        if count == 1:
            message = (
                f"There is 1 new property listed out of {property_count} properties "
                "on PropertyGuru matching your criteria since the last time we checked. "
                "The new property is:\n"
            )
        else:
            message = (
                f"There are {count} new properties listed out of {property_count} properties "
                "on PropertyGuru matching your criteria since the last time we checked. "
                "The new properties are:\n"
            )

        for prop_id in new_properties:
            message += f"\nhttps://www.propertyguru.com.sg/listing/{prop_id}"

        self.send_message(message)
