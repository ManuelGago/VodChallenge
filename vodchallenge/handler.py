import json
import boto3
import csv

print('Loading function')

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def main(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try: 
        s3_client.download_file(bucket, key, '/tmp/file.json')
        
        input_file = "/tmp/file.json"
        json_file = open(input_file)
        json_data = json_file.read()
        json_file.close()
        data = json.loads(json_data)

        output = open("/tmp/file.csv", "w")
        f = csv.writer(output)

        # Write CSV Header without response True
        f.writerow(["Title", "Year", "Rated", "Released", "Runtime","Genre", "Director",
        	"Writer","Plot","Language","Country","Awards","Poster","Ratings",
            	"Metascore","imdbRating", "imdbVotes", "imdbID", "Type", "DVD",
            	"BoxOffice", "Production", "Website"])

        f.writerow([data["Title"], data["Year"], data["Rated"], data["Released"], data["Runtime"], data["Genre"],
               	data["Director"], data["Writer"], data["Actors"], data["Language"], data["Country"], data["Awards"],
               	data["Poster"], data["Ratings"], data["Metascore"], data["imdbRating"], data["imdbVotes"],
               	data["imdbID"], data["Type"], data["DVD"], data["BoxOffice"], data["Production"], data["Website"]])
        
        output.close()
        s3_client.upload_file('/tmp/file.csv', bucket, 'csv/' + key[:-5] + '.csv')
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
