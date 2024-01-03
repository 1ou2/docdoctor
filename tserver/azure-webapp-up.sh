source ../azure.env

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

az webapp up --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP --location $AZ_LOCATION --runtime PYTHON:3.12 --sku B1 --logs
