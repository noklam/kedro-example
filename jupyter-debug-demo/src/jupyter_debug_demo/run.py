import sys
from kedro.framework.session.session import KedroSession
from kedro.framework.project import configure_project
from pathlib import Path

package_name = Path(__file__).resolve().parent.name
configure_project(package_name)
print(str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "connectors"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "utilities"))

with KedroSession.create(package_name) as session:
    session.run()