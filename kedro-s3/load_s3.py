import s3fs

client_kwargs = {"endpoint_url": "http://localhost:9000"}
fs = s3fs.S3FileSystem(
    key="minioadmin", secret="minioadmin", client_kwargs=client_kwargs
)


fs = s3fs.S3FileSystem(
    key="noknoknok", secret="noknoknok", client_kwargs=client_kwargs
)
print(fs.ls('nok/'))

# with fs.open("nok/data/01_raw/iris.csv/2022-09-16/iris.csv", "rb") as f:
#     print(f.read())


from kedro import io