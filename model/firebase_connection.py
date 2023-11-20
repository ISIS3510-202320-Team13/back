import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Use a service account.
cred = credentials.Certificate('parkez.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def get_collection(colection:str):
    docs = db.collection(colection).stream()
    return docs

def get_document(colection:str, uid:str):
    doc_ref = db.collection(colection).document(uid)
    doc = doc_ref.get()
    return doc

def get_documents_filtered(collection:str, atribute:str, compare:str, value):
    docs = db.collection(collection).where(filter=FieldFilter(atribute, compare, value)).stream()
    return docs

def add_document(colection:str, new_document:dict):
    uid = new_document.pop('uid')
    db.collection(colection).document(uid).set(new_document)
    return uid

def update_document(colection:str, updated_document:dict):
    uid = updated_document.pop('uid')
    db.collection(colection).document(uid).set(updated_document, merge=True)
    return True