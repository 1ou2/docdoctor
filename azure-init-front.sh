# deploy using azure cli
echo "loading environment variables"
source azure.env
echo "login using service principal"
az login --service-principal --username $AZ_SERVICEPRINCIPAL_APPID --password $AZ_SERVICEPRINCIPAL_PASSWORD --tenant $AZ_TENANTID
az account set --subscription $AZ_SUBSCRIPTION

# frontend server is static website stored in an azure blob storage
echo "creating account storage"
az storage account create --name $AZ_STORAGE_ACCOUNT --resource-group $AZ_RESOURCEGROUP --location $AZ_LOCATION --sku Standard_ZRS --encryption-services blob
echo "creating storage"
az storage container create \
    --account-name $AZ_STORAGE_ACCOUNT \
    --name gab-front \
    --auth-mode login
echo "updating storage properties to static-web-site"
az storage blob service-properties update --account-name $AZ_STORAGE_ACCOUNT --static-website --404-document error.html --index-document index.html