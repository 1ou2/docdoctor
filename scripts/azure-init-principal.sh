source azure.env
echo "app name: $AZ_APP_NAME"
az ad sp create-for-rbac --name $AZ_APP_NAME \
                         --role $AZ_CONTRIBUTOR \
                         --scopes /subscriptions/$AZ_SUBSCRIPTION/resourceGroups/$AZ_RESOURCEGROUP
