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