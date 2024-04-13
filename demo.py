import os
import sys
from hatespeechclassification.configuration.mongodb import MongoDB

econfig = {
    "mongo_uri": "mongodb+srv://subha:Sugan0510@cluster0.f05of.mongodb.net",
    "db_name": "nlp",
}
zip_file_name = "my_zip_file.zip"
destination_dir = r"C:\Users\subha\nlp_pipeline_creation\downloads"

MongoDB.extract_zip_from_mongodb(econfig, zip_file_name, destination_dir)




