# Instagram topic modeling endpoint

The following commands create an endpoint for model inference locally and in the azure cloud.

You need an azure subscription, a resource group, a machine learning workspace and the azure cli.

Login via the cli and configure it:

```
az account set --subscription <subscription ID>
az configure --defaults workspace=<Azure Machine Learning workspace name> group=<resource group>
```

# Local debugging

## Create a local endpoint

```
az ml online-endpoint create --local -n ig-classifier-endpoint -f endpoint.yml
```

## Create local deployment

```
az ml online-deployment create --local -n blue --endpoint ig-classifier-endpoint -f deployment.yml --debug
```

## Invoke local endpoint

```
az ml online-endpoint invoke --name ig-classifier-endpoint --request-file data/sample-request-classify.json --local
```

# Cloud deployment

## Register model

```
az ml model create -n ig-classifier -v 1 -f model.yml
```

## Register model environment

```
az ml environment create -n ig-classifier-env -v 1 -f environment.yml
```

## Register endpoint

```
az ml online-endpoint create --name ig-classifier-endpoint -f endpoint.yml
```

## Azure Deployment

```
az ml online-deployment create --name blue --endpoint ig-classifier-endpoint -f deployment_registered.yml --all-traffic
```

## Invoke azure online endpoint

```
az ml online-endpoint invoke --name ig-classifier-endpoint --request-file data/sample-request-classify.json
az ml online-endpoint invoke --name ig-classifier-endpoint --request-file data/sample-request-topics.json
```

## Show scoring URI  

```
az ml online-endpoint show -n ig-classifier-endpoint -o tsv --query scoring_uri
```

## Get credentials

```
az ml online-endpoint get-credentials -n ig-classifier-endpoint -o tsv --query primaryKey
```

## Test with curl

```
curl --request POST "<URI>" --header "Authorization: Bearer <KEY>" --header 'Content-Type: application/json' --data @data/sample-request-classify.json
```


