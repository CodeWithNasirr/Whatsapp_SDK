ACCESS_TOKEN = "EAANspVj8RlsBO03vjlwxuJNH4cbCb6mUZB0oD9yqGdfP6FCiTfCc5VinaGZC3UvbiZBwQ8BuT2wUfMHcbITUCvbyZB9bfyeTOZAQJ3v1sUvZAx4txKJQHQeuGWx65FhoIc3hkXmns1X4DaBeLR5ZBgReUFMZBPgo3onZC56tm42Oz7npOMh5BrUllR4IlZBnSa9ySsAVN7KBat"
# PHONE_NUMBER_ID = "561182647071541"
PHONE_NUMBER_ID = "588918367638247"#test number
import requests
import os

WHATSAPP_API_URL = "https://graph.facebook.com/v21.0"


def upload_image_to_whatsapp(image_path):
    """Uploads an image to WhatsApp and returns the MEDIA_ID"""
    
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    files = {
        "file": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg"),
        "messaging_product": (None, "whatsapp")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        media_id = response.json().get("id")
        print(f"✅ Image uploaded successfully! MEDIA_ID: {media_id}")
        return media_id
    else:
        print(f"❌ Error uploading image: {response.json()}")
        return None
# media_id = upload_image_to_whatsapp("Screenshot 2024-12-16 115751.png")

def check_uploaded_media(media_id):
    """Check if a WhatsApp media ID is valid and get its URL."""
    url = f"{WHATSAPP_API_URL}/{media_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    if "url" in data:
        print(f"✅ Image URL: {data['url']}")
    else:
        print(f"❌ Error: {data}")

# Check media
# check_uploaded_media(1334741300857600)