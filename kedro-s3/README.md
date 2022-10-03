# kedro_s3
See https://docs.min.io/docs/minio-quickstart-guide.html

# Setup for MinIO Server
On Mac:
```
brew install minio/stable/minio
minio server ~/data

# Go to localhost:9000 to manually paste the file
```

# Setup for MC Admin tool (a.k.a mc CLI)
```
brew install minio/stable/mc
mc --help
mc admin user add myminio
Enter Access Key: console
Enter Secret Key: minioadmin

mc admin policy add myminio/ consoleAdmin admin.json

mc admin policy set myminio/ consoleAdmin user=console


```
# UI Admin
```
docker pull minio/console
```