import sys

from s3_package_manager import define_s3_bucket,S3Manager


def copy_package_from_development_bucket():
    package_name = "looqbox"
    package_version = sys.argv[2]

    bucket = define_s3_bucket(sys.argv)
    s3_client = S3Manager("looqbox-dynamic-packages-development")

    s3_client.copy_package(source_bucket_name="looqbox-dynamic-packages-development",
                           package_name=package_name,
                           version=package_version,
                           destination_bucket_name=bucket)


if __name__ == "__main__":
    copy_package_from_development_bucket()
