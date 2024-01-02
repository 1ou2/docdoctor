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

