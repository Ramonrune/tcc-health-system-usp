import os
import boto3
import datetime


class S3:

    def __init__(self):
        self.s3 = boto3.resource(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=os.environ["ACCESS_KEY_AWS"],
            aws_secret_access_key=os.environ["SECRET_KEY_AWS"],
        )
        self.s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=os.environ["ACCESS_KEY_AWS"],
            aws_secret_access_key=os.environ["SECRET_KEY_AWS"],
            config=boto3.session.Config(
                s3={"addressing_style": "path"}, signature_version="s3v4"
            ),
        )

    def upload(self, bucket, key, file):
        s3Object = self.s3.Object(bucket, key)
        s3Object.put(Body=file)

    def get(self, bucket, key):
        return self.s3.Object(bucket, key).get()["Body"].read()

    def delete(self, bucket, key):
        self.s3.Object(bucket, key).delete()

    def create_presigned_post(self, bucket_name, object_name, expiration=3600):
        try:
            response = self.s3_client.generate_presigned_post(
                bucket_name, object_name, ExpiresIn=expiration
            )

            return response
        except Exception as e:
            return None

    def generate_presigned_url(self, bucket_name, object_name, expiration=86400):
        response = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

        return response
