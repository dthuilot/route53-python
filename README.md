# Hudl DocumentDB route53 upserts

## What does this code

This code generate a batch file of type :

{
    "Comment": "UPSERT",
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "t-speedtest-docdb.app.thorhudl.com",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "speedtest.foo.com"
                    }
                ]
            }
        },
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "t-sportradar-docdb.app.thorhudl.com",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "sportradar.foo.com"
                    }
                ]
        }
    ]
}

from a source file of type :

[
    {"service_name":"speedtest","host":"speedtest.foo.com"},
    {"service_name":"sportradar","host":"sportradar.foo.com"}
]

and apply the batch file on the DNS Zone specified by the dnsZoneID.

It's used to update the CNAME when we refresh the documentDB databases in the Thor environment.

## Variables

* `sourceFile`

    Path to the source file of the format [{"service_name":"a","host":"b"}]
* `batchFile`

    Path to the batch file generated for the actions on the Route53 records (the file itself is not used but should be backuped with a timestamp to keep the history of the changes)

* `dnsZoneID`

    DNS Zone ID
