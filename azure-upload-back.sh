source azure.env

# prepare packages
ZIP_FILES="app/ requirements.txt .deployment chk.json"
APP_FILES="app/server.py app/embeddingDB.py"
ROOT_FILES="requirements.txt .deployment chk.json"
rm -rf dist
mkdir -p dist/app
cp $APP_FILES dist/app

cp $ROOT_FILES dist
cd dist
rm -f ./src.zip 2> /dev/null && zip src.zip $ROOT_FILES $APP_FILES

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

echo "****"
echo "webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path dist/src.zip"
echo "***"
az webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path "src.zip"

