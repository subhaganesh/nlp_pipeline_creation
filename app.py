from hatespeechclassification.pipeline.train_pipeline import TrainPipeline
from mongourl import mongodb_url

mongo_uri=mongodb_url
db_name='nlp'

obj=TrainPipeline(mongo_uri,db_name)
obj.run_pipeline()
