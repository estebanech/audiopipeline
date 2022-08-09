# pg_audiopipeline

events clustering.ipynb: note book that takes the content of an S3 bucket where there are audio files representing the events that are going to be clustered, and then use the DBSCAN algorithm to cluster them

readS3Bucket.py: script to read an S3 bucket with audio files and then create create another bucket representing the events to store the extracted events from those files
