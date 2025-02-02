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
    CHOICE_LANGUAGE = [
    ('en_US', 'English (US)'),
    ('en_IN', 'English (INDIA)'),
    ('es_ES', 'Spanish (Spain)'),
    ('fr_FR', 'French (France)'),
    ('de_DE', 'German (Germany)'),
    ('hi_IN', 'Hindi (India)'),
    # Add other supported languages
]
    template_name = models.CharField(max_length=255)
    template_language = models.CharField(max_length=100, default="en_US",choices=CHOICE_LANGUAGE)
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
        return re.findall(r"{{\d+}}", self.body_text)

    def generate_payload(self):
        payload = {
            "name": self.template_name,
            "language": {"code": self.template_language},
            "category": self.template_category,
            "components": []
        }

        # 🟢 Add Header Component (TEXT, IMAGE, VIDEO, FILE)
        if self.header_type:
            header_type_upper = self.header_type.upper()
            if header_type_upper not in ["TEXT", "IMAGE", "DOCUMENT", "VIDEO", "FILE"]:
                return  # or log an error

            header_component = {"type": "HEADER", "format": header_type_upper}

            if header_type_upper == "TEXT" and self.header_text:
                header_component["text"] = self.header_text
            elif self.header_img_video_file_url:
                # Create a dictionary mapping each header type to its corresponding key
                component_key = header_type_upper.lower()  # 'image', 'document', 'video', or 'file'
                header_component[component_key] = {
                    "link": self.header_img_video_file_url
                }

            payload["components"].append(header_component)

        # 🟢 Add Body Component (With or Without Dynamic Variables)
        body_component = {"type": "BODY"}
        body_component["text"] = self.body_text

        payload["components"].append(body_component)

        # 🟢 Add Footer Component (If Exists)
        if self.footer_text:
            payload["components"].append({"type": "FOOTER", "text": self.footer_text})

        # 🟢 Add Buttons Component
        buttons = []
        if self.button_type:
            if self.button_type == "QUICK-REPLIES" and self.button_text:
                buttons.append({
                    "type": "TEXT",
                    "text": self.button_text
                })
            elif self.button_type == "CALLBACK" and self.button_url:
                buttons.append({
                    "type": "URL",
                    "text": self.button_text,
                    "url": self.button_url
                })

        if buttons:
            payload["components"].append({"type": "BUTTONS", "buttons": buttons})

        return payload

    def __str__(self):
        return self.template_name
    # so basically here we are creating a model for the template that we are going to create and we are also creating a function that will extract the placeholders from the body text and then we are creating a function that will generate the payload for the whatsapp api request and then we are returning the template name as the string representation of the object. 





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