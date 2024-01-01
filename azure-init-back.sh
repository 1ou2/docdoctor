source azure.env
echo "creating app service plan $AZ_SERVICE_PLAN"
az appservice plan create \
   --resource-group $AZ_RESOURCEGROUP \
   --name $AZ_SERVICE_PLAN \
   --is-linux

echo "creating webapp $AZ_WEBAPP"
az webapp create \
    --name $AZ_WEBAPP \
    --plan $AZ_SERVICE_PLAN \
    --resource-group $AZ_RESOURCEGROUP \
    --runtime "python|3.12"
