from fileinput import filename
import os
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from django.core.files.base import ContentFile

from SEBMS import settings
# Initialize Firebase (ensure you have the credentials file)
cred = credentials.Certificate('firebase_credentials/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Firestore database reference
db = firestore.client()

def fetch_meter_list():
    try:
        # Reference to the document in the 'meters' collection
        doc_ref = db.collection('meters').document('your_doc_id')
        doc = doc_ref.get()
        # Check if the document exists
        if doc.exists:
            data = doc.to_dict()
            # Assuming 'meter_list' is an array in the document
            meter_list = data.get('meter_list', [])
            # Extracting required fields from the meter list
            processed_meter_list = []
            for meter in meter_list:
                processed_meter_list.append({
                    'date': meter.get('date', ''),
                    'id': meter.get('id', ''),
                    'isActive': meter.get('isActive',''),
                    'meterImage': meter.get('meterImage',''),
                    'reading': meter.get('reading', ''),
                    'serial_no': meter.get('serial_no', ''),
                    
                })
            return processed_meter_list
        else:
            print("Document does not exist")
            return []
    except Exception as e:
        print(f"Error fetching meter list: {e}")
        return []


import os
import requests
from django.core.files.base import ContentFile
from uuid import uuid4
from django.conf import settings

def download_and_save_image(image_url):
    """
    Downloads an image from the provided URL and saves it to the media/meter_images folder.
    """
    print(image_url)
    try:
        response = requests.get(image_url)
        print(response)
        if response.status_code == 200:
            # Generate a unique filename for the image
            filename = f"{uuid4()}.jpg"
            # Define the path to save the image
            media_path = os.path.join(settings.MEDIA_ROOT, 'meter_images')
            os.makedirs(media_path, exist_ok=True)
            file_path = os.path.join(media_path, filename)
            # Save the image to the specified path
            with open(file_path, 'wb') as file:
                file.write(response.content)
            # Return the ContentFile for further use if needed
            with open(file_path, 'rb') as file:
                return ContentFile(file.read(), filename)
        else:
            print(image_url)
            print(f"Saving image to: {file_path}")
            print(f"Directory permissions: {oct(os.stat(media_path).st_mode)}")
            print(f"Failed to download image 123: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None



