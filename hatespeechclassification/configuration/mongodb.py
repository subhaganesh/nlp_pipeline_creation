import pymongo
from gridfs import GridFS
import os
import tempfile
import zipfile

class MongoDB:    
    @staticmethod
    def push_zip_to_mongodb(config, zip_file_path):
        client = pymongo.MongoClient(config['mongo_uri'])
        db = client[config["db_name"]]
        fs = GridFS(db)

        with open(zip_file_path, 'rb') as f:
            fs.put(f, filename="my_zip_file.zip")

        print("Zip file pushed to MongoDB GridFS.")

    
    @staticmethod
    def extract_zip_from_mongodb(econfig, zip_file_name, destination_dir):
        # Connect to MongoDB
        client = pymongo.MongoClient(econfig['mongo_uri'])
        db = client[econfig['db_name']]
        fs = GridFS(db)

        # Find the zip file in GridFS
        zip_file = fs.find_one({"filename": zip_file_name})

        if zip_file:
            # Create a temporary directory to extract the zip file
            temp_dir = tempfile.mkdtemp()

            # Save the zip file to the temporary directory
            temp_zip_path = os.path.join(temp_dir, zip_file_name)
            with open(temp_zip_path, 'wb') as f:
                f.write(zip_file.read())

            # Extract the contents of the zip file
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Move the extracted files to the destination directory
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                if os.path.isfile(file_path):
                    os.rename(file_path, os.path.join(destination_dir, file_name))

            # Clean up the temporary directory
            os.rmdir(temp_dir)

            print("Zip file extracted and files moved to destination directory.")
        else:
            print("Zip file not found in MongoDB GridFS.")
