source azure.env

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

echo "creating app service plan $AZ_SERVICE_PLAN"
az appservice plan create \
   --resource-group $AZ_RESOURCEGROUP \
   --name $AZ_SERVICE_PLAN \
   --is-linux

echo "creating webapp $AZ_WEBAPP_NAME"
az webapp create \
    --name $AZ_WEBAPP_NAME \
    --plan $AZ_SERVICE_PLAN \
    --resource-group $AZ_RESOURCEGROUP \
    --runtime "PYTHON|3.8"

echo "setting python 3.12"
az webapp config set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --linux-fx-version "PYTHON|3.12"
az webapp config appsettings set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
az webapp config set --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP --startup-file "python -m uvicorn app.server:app --host 0.0.0.0"


#az webapp restart --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP

#echo "creating keyvault"
#az keyvault create --resource-group $AZ_RESOURCEGROUP --location $AZ_LOCATION --name $AZ_KEYVAULT
#az webapp identity assign --resource-group $AZ_RESOURCEGROUP  --name $AZ_WEBAPP_NAME