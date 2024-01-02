source azure.env

# prepare packages
FILES="requirements.txt app/server.py app/embeddingDB.py .deployment"
rm -rf dist
mkdir dist
cp $FILES dist
cd dist
rm -f ./src.zip 2> /dev/null && zip src.zip $FILES

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

az webapp deployment source config-zip --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src "src.zip"
az webapp restart --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP