source azure.env

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION


#echo "creating keyvault"
az keyvault create --resource-group $AZ_RESOURCEGROUP --location $AZ_LOCATION --name $AZ_KEYVAULT

AZ_PRINCIPAL_ID=$(az webapp identity assign --resource-group $AZ_RESOURCEGROUP  --name $AZ_WEBAPP_NAME | python3 -c "import sys, json; print(json.load(sys.stdin)['principalId'])")
az keyvault set-policy --secret-permissions get list --name $AZ_KEYVAULT --object-id $AZ_PRINCIPAL_ID