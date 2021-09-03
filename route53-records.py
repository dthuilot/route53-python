from json import dump
import json
import boto3

## Variables
sourceFile = "values.json"                  # Source file of the format [{"service_name":"a","host":"b"}]
batchFile = "outputs/route53-batch.json"    # Path to the batch file used for the actions on the Route53 records
dnsZoneID = 'ZHOXMPZMS6ELK'                 # DNS Zone ID


## Read input data service name and host url by service
def services_list():
    print("Read JSON values\n")
    # Opening JSON file
    with open(sourceFile) as json_file:
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
    
    d = {"Comment": "UPSERT","Changes": changes}
    
    with open(batchFile, 'w') as f:
        dump(d, f)

    # Pretty Print JSON
    json_formatted_str = json.dumps(d, indent=4)

    # print changes
    print(json_formatted_str)

    return d

## Apply upsert on route53
def route53_upsert(batch):
    print("Route53 upserts\n")
    client = boto3.client('route53')

    response = client.change_resource_record_sets(
        # DNS host ID for thorhudl.com
        HostedZoneId= dnsZoneID,
        ChangeBatch= batch
    )

    print(response)


## Main function
def main():
    print("Welcome to main\n")
    route53_upsert(generate_json(services_list()))

if __name__ == "__main__":
    main()