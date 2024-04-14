import os
import sys
from hatespeechclassification.configuration.mongodb import MongoDB
from mongourl import mongodb_url

econfig = {
    "mongo_uri": mongodb_url,
    "db_name": "nlp",
}
zip_file_name = "my_zip_file.zip"
destination_dir = r"C:\Users\subha\nlp_pipeline_creation\downloads"

MongoDB.extract_zip_from_mongodb(econfig, zip_file_name, destination_dir)




