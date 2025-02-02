from django.core.management.base import BaseCommand
import requests
from Main.models import Create_Template
from Main.views import ACCESS_TOKEN, WHATSAPP_BUSINESS_ACCOUNT_ID  # Import your model

class Command(BaseCommand):
    help = "Sync WhatsApp Templates from Meta API to Database"

    def handle(self, *args, **kwargs):
        url = f"https://graph.facebook.com/v18.0/{WHATSAPP_BUSINESS_ACCOUNT_ID}/message_templates"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            templates = response.json().get("data", [])
            # first we need to print or check the data and then fix it
            for meta_template in templates:
                name = meta_template["name"]
                category = meta_template["category"]
                status = meta_template["status"]
                language = meta_template["language"]
                components = meta_template.get("components", [])

                # Extract Header, Body, Footer, and Buttons
                header_type = None
                header_text = None
                header_img_video_file_url = None
                body_text = None
                footer_text = None
                button_type = None
                button_text = None
                button_url = None

                for component in components:
                    if component["type"] == "HEADER":
                        header_type = component["format"]
                        if header_type == "TEXT":
                            header_text = component.get("text")
                        else:
                            if header_type == "IMAGE":
                                header_type["image"] = {"link": header_img_video_file_url}
                            elif header_type == "VIDEO":
                                header_type["video"] = {"link": header_img_video_file_url}
                            elif header_type == "DOCUMENT":
                                header_type["document"] = {"link": header_img_video_file_url}
                    
                    elif component["type"] == "BODY":
                        body_text = component["text"]
                    
                    elif component["type"] == "FOOTER":
                        footer_text = component["text"]
                    
                    elif component["type"] == "BUTTONS":
                        for button in component["buttons"]:
                            if button["type"] == "QUICK_REPLY":
                                button_type = "QUICK-REPLIES"
                                button_text = button["text"]
                            elif button["type"] == "URL":
                                button_type = "CALLBACK"
                                button_text = button["text"]
                                button_url = button["url"]

                # Save or update in database
                template_obj, created = Create_Template.objects.update_or_create(
                    template_name=name,
                    defaults={
                        "template_language": language["code"],
                        "template_category": category,
                        "status": status,  # Update the status
                        "header_type": header_type,
                        "header_text": header_text,
                        "header_img_video_file_url": header_img_video_file_url,
                        "body_text": body_text,
                        "footer_text": footer_text,
                        "button_type": button_type,
                        "button_text": button_text,
                        "button_url": button_url,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created new template: {name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated template: {name}"))
        else:
            self.stderr.write(self.style.ERROR("Failed to fetch templates from Meta"))
