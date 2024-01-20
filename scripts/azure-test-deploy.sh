source azure.env

# prepare packages
FILES="requirements.txt tserver/server.py templates static .deployment startup.sh prebuild.sh postbuild.sh"
rm -rf dist
mkdir dist
cp -r $FILES dist
cd dist
rm -f ./src.zip 2> /dev/null && zip src.zip $FILES

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION
echo "****"

az webapp config connection-string list --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME > settings.json 
echo "***"
echo "set config SCM_DO_BUILD_DURING_DEPLOYMENT = true"
az webapp config appsettings set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --settings "@appsettings.json"

#az webapp config appsettings set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
#az webapp config appsettings set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --startup-file "startup.sh"
#echo "deploy"
#echo "webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path src.zip"
#az webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path "src.zip"
echo "set startup file"
az webapp config set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --startup-file "startup.sh"
#az webapp restart --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP

echo "list config appsettings"
az webapp config appsettings list --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME