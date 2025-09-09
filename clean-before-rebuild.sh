find ./slides -type d -name "*_cache" -exec rm -rf {} +
find ./slides -type d -name "*_files" -exec rm -rf {} +
rm -rf _site
rm -rf _freeze
