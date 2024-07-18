from kedro.framework.startup import bootstrap_project
from pathlib import Path

# This is not needed when you do kedro run because the CLI does that behind the scene.
project_root = Path(__file__).parent
bootstrap_project(project_root)  # Load kedro settings etc.

from kedro.framework.session import KedroSession
with KedroSession.create() as session:
    result = session.run()

condition = result["some_condition"] # This is the name of the dataset
print(result)
print(condition)
if condition:
    # Or you don't need Kedro run, it could be calling external program
    with KedroSession.create() as session:
        session.run(pipeline_name="true")

else:
    # Or you don't need Kedro run, it could be calling external program
    with KedroSession.create() as session:
        session.run(pipeline_name="false")

