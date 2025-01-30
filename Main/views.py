from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from Main.services import WhatsAppSDK
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import json
import requests
# Replace these with your actual credentials
ACCESS_TOKEN = "EAANspVj8RlsBO03vjlwxuJNH4cbCb6mUZB0oD9yqGdfP6FCiTfCc5VinaGZC3UvbiZBwQ8BuT2wUfMHcbITUCvbyZB9bfyeTOZAQJ3v1sUvZAx4txKJQHQeuGWx65FhoIc3hkXmns1X4DaBeLR5ZBgReUFMZBPgo3onZC56tm42Oz7npOMh5BrUllR4IlZBnSa9ySsAVN7KBat"
# PHONE_NUMBER_ID = "561182647071541"
PHONE_NUMBER_ID = "588918367638247"
WHATSAPP_BUSINESS_ACCOUNT_ID='560756830446737' #7873445018



def send_template_message(request):
    # Initialize the WhatsApp SDK
    whatsapp = WhatsAppSDK(access_token=ACCESS_TOKEN, phone_number_id=PHONE_NUMBER_ID)
    
    # Example of sending a template message

    recipient = "+918093537813"  # Replace with the recipient's phone number
    template_name = "account_setup"
    
    response = whatsapp.send_template_message(to=recipient, template_name=template_name)
    
    return JsonResponse(response)


@api_view(["GET"])
def check_template_status(request, template_name):
    """
    Check the status of a WhatsApp template via Meta API.
    """
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_BUSINESS_ACCOUNT_ID}/message_templates"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract the template details based on the name
    for template in data.get("data", []):
        if template["name"] == template_name:
            return Response({
                "name": template["name"],
                "status": template["status"],  # Can be "APPROVED", "PENDING", or "REJECTED"
                "category": template["category"],
                "language": template["language"],
                "components": template["components"],
                "last_modified": template.get("last_modified"),
            })

    return Response({"error": "Template not found"}, status=404)

@api_view(['POST'])
def create_template(request):
    ''''
    Create a Whatsapp Template via meta api
    '''
    """
    Create a WhatsApp template via Meta API.
    """
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_BUSINESS_ACCOUNT_ID}/message_templates"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Extract template details from request body
    data = request.data

    payload = {
        "name": data.get("name"),
        "category": data.get("category", "UTILITY"),
        "language": data.get("language", "en_US"),
        "components": data.get("components", [])
    }
    response = requests.post(url, json=payload, headers=headers)

    return Response(response.json())


VERIFY_TOKEN = "XYZX_WEIRD"
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        # 🟢 Process incoming messages from WhatsApp
        data = json.loads(request.body)

        entry=data.get('entry',[])[0]
        changes=entry.get('changes',[])[0]
        value=changes.get('value',{})
        if 'contacts' in value and value['contacts']:
            contact=value.get('contacts',[])[0]
            username=contact.get('profile',{}).get('name','Unknown')
            phone_number=contact.get('wa_id','Null')
        if 'messages' in value and value['messages']:
            messages=value.get('messages',[])[0]
            message_text=messages.get('text',{}).get('body','No Message Found')
            message_id=messages.get('id','Null')
             # ✅ Store Message in Database
            print(f"📩 New Message from {username} ({phone_number}): {message_text}")

        if 'statuses' in value and value['statuses']:
            statuses=value.get('statuses',[])[0]
            status=statuses.get('status','message not send')
            timestamp=statuses.get('timestamp','Null')
            user_number=statuses.get('recipient_id','Null')
            message_id=statuses.get('id','Null')
            # ✅ Store Status in Database
            
            print(f"The Status is {status} TimeStamp {timestamp} and the Number {user_number}")
        # print("Webhook Event:", json.dumps(data, indent=2))
        return JsonResponse({"status": "success"})

    elif request.method == "GET":
        # 🟢 Handle Meta's webhook verification
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print(f"✅ Webhook Verified Successfully! Mode: {mode}, Token: {token}")
            return HttpResponse(challenge)
        else:
            print("❌ Verification Failed! Invalid token.")
            return JsonResponse({"error": "Invalid verification token"}, status=403)
