source azure.env
# upload content of front directory
echo "uploading front"
az storage blob upload-batch -s front -d '$web' --account-name $AZ_STORAGE_ACCOUNT --overwrite
# display url of frontend server
echo "target URL :"
az storage account show -n $AZ_STORAGE_ACCOUNT -g $AZ_RESOURCEGROUP --query "primaryEndpoints.web" --output tsv