source azure.env

# prepare packages
ZIP_FILES="app/ requirements.txt .deployment db2.json"
CACHE_FILES="app/__pycache__ app/util/__pycache__  app/routers/__pycache__"
ROOT_FILES="requirements.txt .deployment db2.json"

rm -rf dist
mkdir -p dist
cp -r app dist/app
cp $ROOT_FILES dist

cd dist
rm -rf $CACHE_FILES
rm -f ./src.zip 2> /dev/null && zip src.zip -r $ZIP_FILES

echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

echo "****"
echo "webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path dist/src.zip"
echo "***"
az webapp deploy --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --src-path "src.zip"

