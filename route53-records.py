from json import dump
import json
# import boto3

## Read input data service name and host url by service
def services_list():
    print("Read JSON values\n")
    # Opening JSON file
    with open('values.json') as json_file:
        data = json.load(json_file)
  
    # Count the number of service to update
    print(str(len(data)) + " records need to be updated\n")

    return data

## Create JSON files for upsert
def generate_json(servicesList):
    print("Generate Route53 JSON Files\n")
    # Write changes for the batch file
    changes =[]
    for i in servicesList:
        changes.append({"Action": "UPSERT", "ResourceRecordSet": { "Name": "t-"+i['service_name']+"-docdb.app.thorhudl.com", "Type": "CNAME", "TTL": 300, "ResourceRecords": [{"Value": i['host']}]}})
    
    print(changes)
    
    
    d = {"Comment": "UPSERT","Changes": [changes]}
    
    with open('outputs/route53-batch.json', 'w') as f:
        dump(d, f)


## Apply upsert on route53
def route53_upsert():
    print("Route53 upserts\n")
    # client = boto3.client('route53')

## Main function
def main():
    print("Welcome to main\n")
    input = services_list()
    generate_json(input)
    route53_upsert()

if __name__ == "__main__":
    main()