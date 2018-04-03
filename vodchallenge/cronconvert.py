from subprocess import call
import json
import boto3
import csv

print('Loading function')

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def main(event, context):

    try:

        resp = s3_client.list_objects_v2(Bucket='moviesmetadata')

        for obj in resp['Contents']:
                key = obj['Key']
                if key.endswith('.json'):
                        s3_client.download_file('moviesmetadata', key, '/tmp/file.json')
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
                        s3_client.upload_file('/tmp/file.csv', 'moviesmetadata', 'csv/' + key.strip('.json') + '.csv')
                        call('rm -rf /tmp/*', shell=True)
    except Exception as e:
        print(e)
        print('Error running cron from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format('moviesmetadata'))
        raise e
