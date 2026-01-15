import json
import os
import sys
from s3_package_manager import define_s3_bucket,S3Manager


def download_dependencies():
    with open("../looq_dependencies.json", "r") as dependencies_file:
        packages = json.load(dependencies_file)
        dependencies_file.close()

    bucket = define_s3_bucket(sys.argv)
    s3_client = S3Manager(bucket)
    s3_client.install_test_dependencies(bucket, packages, download_package_path=os.getenv("LOOQ_DEPENDENCIES_PATH",
                                                                                          "/home/looq_dependencies")
                                        )

if __name__ == "__main__":
    download_dependencies()