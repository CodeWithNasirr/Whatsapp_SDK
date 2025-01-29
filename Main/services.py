import requests

class WhatsAppSDK:
    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self, access_token, phone_number_id):
        self.access_token = access_token
        self.phone_number_id = phone_number_id


    def send_message(self, to, message_type, message_body):
        """
        Send a message via WhatsApp Cloud API.
        :param to: Recipient's phone number (e.g., +1234567890)
        :param message_type: Type of message ('text', 'template', etc.)
        :param message_body: Message body content as a dictionary
        """
        url = f"{self.BASE_URL}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": message_type,
            **message_body
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()



    def send_template_message(self, to, template_name, language_code="en_US"):
        """
        Send a template message.
        :param to: Recipient's phone number (e.g., +1234567890)
        :param template_name: Name of the pre-approved template
        :param language_code: Language of the template (default: 'en_US')
        """
        message_body = {
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": [
                    {
                        'type':'body',
                        'parameters':[
                            {'type':'text','text':'John Doe'},
                            {'type':'text','text':'50% OFF'}
                        ]
                    }
                ]
                
            }
        }
        return self.send_message(to, "template", message_body)
