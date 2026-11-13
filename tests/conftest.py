import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from pyspark.sql import SparkSession

# PySpark 3.5.0 supports Java 8, 11 and 17; the Jupyter image used by the stack runs Java 17.
SUPPORTED_JAVA = (11, 17)


def java_major() -> int | None:
    """Major version of the JVM PySpark will use (JAVA_HOME, else PATH), None when there is none."""
    home = os.environ.get("JAVA_HOME")  # the JVM that PySpark itself launches
    java = str(Path(home) / "bin" / "java") if home else "java"
    try:
        out = subprocess.run([java, "-version"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None
    found = re.search(r'version "(\d+)(?:\.(\d+))?', out.stderr + out.stdout)
    if not found:
        return None
    major = int(found.group(1))
    return int(found.group(2)) if major == 1 and found.group(2) else major


@pytest.fixture(scope="session")
def spark():
    """Local Spark session; no supported JVM = skip, or fail when REQUIRE_SPARK=1 (CI)."""
    major = java_major()
    if major not in SUPPORTED_JAVA:
        reason = f"Spark tests need Java {' or '.join(map(str, SUPPORTED_JAVA))}, found {major}"
        if os.environ.get("REQUIRE_SPARK") == "1":
            pytest.fail(reason)
        pytest.skip(reason)
    # Python workers must run the interpreter of this environment, not whatever `python` is on PATH.
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    session = (
        SparkSession.builder.appName("tests")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()
