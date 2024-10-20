import firebase_admin
from firebase_admin import credentials, firestore

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
                    'serial_no': meter.get('serial_no', ''),
                    'reading': meter.get('reading', '')
                })
            return processed_meter_list
        else:
            print("Document does not exist")
            return []
    except Exception as e:
        print(f"Error fetching meter list: {e}")
        return []
