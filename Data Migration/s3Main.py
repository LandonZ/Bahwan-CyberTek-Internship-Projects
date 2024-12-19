#test to see how to upload into a S3 bucket

import s3Upload as s

file_path = "/Users/landonzheng/Documents/Intern/sample.json"
s.upload_file(file_path)