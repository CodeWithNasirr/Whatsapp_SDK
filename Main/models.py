from django.db import models
import re
# Create your models here.

from django.db import models
import re

class Create_Template(models.Model):
    CHOICE_CATEGORY = [
        ('MARKETING', 'MARKETING'),
        ('UTILITY', 'UTILITY'),
        ('AUTHENTICATION', 'AUTHENTICATION')
    ]
    CHOICE_TYPE = [
        ('IMAGE', 'IMAGE'),
        ('TEXT', 'TEXT'),
        ('VIDEO', 'VIDEO'),
        ('FILE', 'FILE'),
        ("LOCATION", "LOCATION"),
    ]
    BUTTON_TYPE = [("QUICK-REPLIES", "QUICK-REPLIES"), ("CALLBACK", "CALLBACK")]

    template_name = models.CharField(max_length=255)
    template_language = models.CharField(max_length=10, default="en_US")
    template_category = models.CharField(max_length=50, choices=CHOICE_CATEGORY)
    
    header_type = models.CharField(max_length=50, choices=CHOICE_TYPE, null=True, blank=True)
    header_text = models.TextField(null=True, blank=True)  # For TEXT headers
    header_img_video_file_url = models.URLField(null=True, blank=True)  # For IMAGE, VIDEO, FILE

    body_text = models.TextField()
    footer_text = models.CharField(max_length=255, null=True, blank=True)

    button_type = models.CharField(max_length=50, choices=BUTTON_TYPE, null=True, blank=True)
    button_text = models.CharField(max_length=255, null=True, blank=True)  # For Quick Replies
    button_url = models.URLField(null=True, blank=True)  # For Callback Buttons
    button_number = models.IntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def extract_placeholders(self):
        """Extracts dynamic placeholders (e.g., {{1}}, {{2}}) from the body text."""
        return re.findall(r"{{\d+}}", self.body_text)

    def generate_payload(self, dynamic_values=None):
        """
        Generates a WhatsApp API-ready JSON payload.
        :param dynamic_values: Dictionary to replace placeholders, e.g., {"1": "John", "2": "#1234"}
        :return: JSON payload for API request
        """
        dynamic_values = dynamic_values or {}

        payload = {
            "name": self.template_name,
            "language": {"code": self.template_language},
            "category": self.template_category,
            "components": []
        }

        # 🟢 Add Header Component (TEXT, IMAGE, VIDEO, FILE)
        if self.header_type:
            header_component = {"type": "header", "format": self.header_type.upper()}
            
            if self.header_type.upper() == "TEXT" and self.header_text:
                header_component["text"] = self.header_text
            elif self.header_type.upper() in ["IMAGE", "DOCUMENT", "VIDEO", "FILE"] and self.header_img_video_file_url:
                header_component["parameters"] = [{
                    "type": self.header_type.lower(),
                    self.header_type.lower(): {"link": self.header_img_video_file_url}
                }]
            payload["components"].append(header_component)

        # 🟢 Add Body Component (With Dynamic Variables)
        body_component = {"type": "body", "text": self.body_text}
        placeholders = self.extract_placeholders()

        if placeholders:
            body_component["parameters"] = [
                {"type": "text", "text": dynamic_values.get(p.strip('{}'), f"Missing Value for {p.strip('{}')}")}
                for p in placeholders
            ]

        payload["components"].append(body_component)

        # 🟢 Add Footer Component (If Exists)
        if self.footer_text:
            payload["components"].append({"type": "footer", "text": self.footer_text})

        # 🟢 Add Buttons Component
        buttons = []
        if self.button_type:
            if self.button_type == "QUICK-REPLIES" and self.button_text:
                buttons.append({
                    "type": "button",
                    "sub_type": "QUICK_REPLY",
                    "text": self.button_text
                })
            elif self.button_type == "CALLBACK" and self.button_url:
                buttons.append({
                    "type": "button",
                    "sub_type": "URL",
                    "text": self.button_text,
                    "url": self.button_url
                })

        if buttons:
            payload["components"].append({"type": "buttons", "buttons": buttons})

        return payload

    def __str__(self):
        return self.template_name





class ReceivedMessage(models.Model):
    sender_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    message_text = models.TextField()
    message_id = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_name} ({self.phone_number})"

class MessageStatus(models.Model):
    message_id = models.CharField(max_length=255, unique=True)
    recipient_number = models.CharField(max_length=20)
    status = models.CharField(max_length=50)  # e.g., sent, delivered, read, failed
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status: {self.status} for {self.recipient_number}"