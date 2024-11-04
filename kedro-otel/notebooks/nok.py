import mlflow

# Create a features.txt artifact file
import pandas as pd

data = pd.DataFrame([[0,0],[1,1]], columns=["a","b"])
data.to_csv("nok.csv", index=False)

import tempfile
# With artifact_path=None write features.txt under
# root artifact_uri/artifacts directory
with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
    data.to_csv(tmp)
    with mlflow.start_run():

        mlflow.log_artifact(tmp.name)
    # data.to_csv(artifact_file)



data.to_csv("abc.csv")
with open ("a.pkl")

# Clean up
try:
    os.remove(f)
except OSError:
    pass