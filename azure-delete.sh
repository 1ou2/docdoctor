source azure.env

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

# get json description of resource AZ_WEBAPP_NAME
# then parse output 
# load json object, and get "id" field
AZ_WEBAPP_ID=$(az resource list --name $AZ_WEBAPP_NAME | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
echo "deleting webapp $AZ_WEBAPP_NAME"
echo "webapp id = $AZ_WEBAPP_ID"
az resource delete --ids $AZ_WEBAPP_ID

AZ_SERVICE_PLAN_ID=$(az resource list --name $AZ_SERVICE_PLAN | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
echo "deleting app service plan $AZ_SERVICE_PLAN"
echo "service id = $AZ_SERVICE_PLAN_ID"
az resource delete --ids $AZ_SERVICE_PLAN_ID