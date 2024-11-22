# xtable-sync-lambda![Untitled Diagram drawio-2](https://github.com/user-attachments/assets/d196aa87-b2e2-4e45-b0dd-d1e4825a41d3)

# Deploy steps 
```
nano config.yaml
```

```
sourceFormat: HUDI

targetFormats:
  - ICEBERG
datasets:
  -
    tableBasePath: s3://<>/hudi/people
    tableName: people
    partitionSpec: city:VALUE
    namespace: icebergdb
```


##### Ship config file to S3
```
aws s3 cp <PATH>/config.yaml s3://XXXconfig/config.yaml
```


#### Test it 
```
docker build -t xtable-lambda .

docker run -p 9000:8080 \
    -v ~/.aws:/root/.aws:ro \
    xtable-lambda

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"path":"s3://datalake-demo-1995/config/config.yaml"}'
```
