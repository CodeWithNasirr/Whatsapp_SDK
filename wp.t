Webhook Event: {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "522798267590035",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551825634",
              "phone_number_id": "588918367638247"
            }, 
            "contacts": [
              {
                "profile": {
                  "name": "Anonymous"
                },
                "wa_id": "918093537813"
              }
            ],
            "messages": [
              {
                "from": "918093537813",
                "id": "wamid.HBgMOTE4MDkzNTM3ODEzFQIAEhggMjU5QUM3NzVCMTFFRTU2NDg5NzQzRDU2NEZDMzU3MEMA",
                "timestamp": "1738165844",
                "text": {
                  "body": "Hi"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

# this is sending a message to the user 
Webhook Event: {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "522798267590035",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551825634",
              "phone_number_id": "588918367638247"
            },
            "statuses": [
              {
                "id": "wamid.HBgMOTE4MDkzNTM3ODEzFQIAERgSOEFDNEQ3QkZCNkE0OTgxMEUwAA==",
                "status": "read",
                "timestamp": "1738166464",
                "recipient_id": "918093537813"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}



# tempalte strutuare
{
    "name": "xyzw",
    "category": "MARKETING",
    "language": "en_US",
    "components": [
        {
            "type": "HEADER",
            "format": "TEXT",
            "text": "Hello Dosto"
        },
        {
            "type": "BODY",
            "text": "Hello, this is a test message."
        },
        {
            "type": "FOOTER",
            "text": "This is a footer section"
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {
                    "type": "URL",
                    "text": "Visit Website",
                    "url": "https://ww19.0123movie.net/"
                }
            ]
        }
    ]
}
# image 
{
    "name": "xyzw",
    "category": "MARKETING",
    "language": "en_US",
    "components": [
        {
            "type": "HEADER",
            "format": "IMAGE",
            "image": {
                "link": "https://example.com/your-image.jpg"
            }
        },
        {
            "type": "BODY",
            "text": "Hello, this is a test message."
        },
        {
            "type": "FOOTER",
            "text": "This is a footer section"
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {
                    "type": "URL",
                    "text": "Visit Website",
                    "url": "https://ww19.0123movie.net/"
                }
            ]
        }
    ]
}




###

def send_template_message(request):
    recipient = "+918093537813"  # Replace with actual phone number
    template_name = "account_setup"

    # Fetch template from the database
    template = Create_Template.objects.filter(template_name=template_name).first()
    if not template:
        return JsonResponse({"error": "Template not found"}, status=404)

    # Extract placeholders from the template body
    placeholders = template.extract_placeholders()

    # Example dynamic values (replace with actual data)
    dynamic_values = {"1": "John Doe", "2": "50% OFF"}

    # Build WhatsApp parameters
    parameters = [{"type": "text", "text": dynamic_values.get(p.strip('{}'), p)} for p in placeholders]

    # Prepare the message payload
    message_body = {
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": parameters
                }
            ]
        }
    }

    # Send the message via WhatsApp API
    whatsapp = WhatsAppSDK(access_token=ACCESS_TOKEN, phone_number_id=PHONE_NUMBER_ID)
    response = whatsapp.send_message(recipient, "template", message_body)

    return JsonResponse(response)
