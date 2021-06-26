from storages.backends.s3boto3 import S3Boto3Storage


class S3(S3Boto3Storage):
	pass


s3_storage = S3()

