source ../azure.env

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

az webapp config set --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP --startup-file "python -m uvicorn app.server:app --host 0.0.0.0"
az webapp restart --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP