import sys
import os

from s3_package_manager import define_s3_bucket,S3Manager


def main():
    package_name = "looqbox"
    package_version = sys.argv[2]

    bucket = define_s3_bucket(sys.argv)

    dir_to_upload = os.getcwd() + f"/{package_name}"

    s3_client = S3Manager(bucket)

    s3_client.upload_dir(
        dir_name=dir_to_upload,
        s3_dir_name=f"{package_name}/{package_version}/{package_name}"
    )


if __name__ == "__main__":
    main()
