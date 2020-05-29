#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import hashlib
import os
import urllib3
from minio import Minio
import io
from minio.error import (ResponseError)

scheme = '/minio'


def minio_init():
    httpClient = None
    if scheme != 'None':
        httpClient = urllib3.PoolManager(scheme=scheme)
    # Initialize minioClient with an endpoint and access/secret keys.
    minioClient = Minio(endpoint='host',
                        access_key='access_key',
                        secret_key='secret_key')
    return minioClient


def generator_bucket(user_id, image_type):
    bucket_name = hashlib.md5((str(datetime.datetime.utcnow()) + str(user_id)).encode()).hexdigest()
    object_name = bucket_name + str(user_id) + image_type + '.jpg'
    bucket_name = bucket_name[:3]
    if scheme != 'None':
        minioClient = minio_init()
        try:
            if minioClient.bucket_exists(bucket_name):
                return bucket_name, object_name
            else:
                minioClient.make_bucket(bucket_name=bucket_name, location='cn-north-1')
                return bucket_name, object_name
        except ResponseError as e:
            print(e)
    else:
        s3_bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
        return s3_bucket_name, bucket_name+'/'+object_name


def copy_picture_new_route(old_bucket, old_object):
    print(old_bucket, old_object)
    minio_client = minio_init()
    resp = minio_client.copy_object(bucket_name=old_bucket, object_name='picture'+'/'+old_object,
                                    object_source=old_bucket+'/'+old_object)


def get_object():
    minio_client = minio_init()
    buckets = minio_client.list_buckets()
    for bucket in buckets:
        if bucket.name != 'userinventory':
            continue
        bucket_name = bucket.name
        objects = minio_client.list_objects(bucket_name=bucket_name, recursive=True)
        for obj in objects:
            copy_picture_new_route(old_bucket=obj.bucket_name, old_object=obj.object_name)
            # print(obj.bucket_name, obj.object_name)
    print('move ok')


def upload_image(bucket_name, object_name, file):
    file.seek(0, 0)
    file_data = io.BytesIO(file.read())
    file_size = len(file_data.read())
    minioClient = minio_init()
    if file_size <= 0:
        return None
    file_data.seek(0, 0)
    # Put a file with default content-type, upon success prints the etag identifier computed by server.
    try:
        minioClient.put_object(bucket_name=bucket_name, object_name=object_name, data=file_data, length=file_size,
                               content_type='application/octet-stream')
        image_path = '/api/gp_user/get/{}/{}'.format(bucket_name, object_name)
        return image_path
    except ResponseError as err:
        # logger.error(err)
        return None


if __name__ == '__main__':
    get_object()
    # copy_picture_new_route(old_bucket='021', old_object='02104ca8a4e712dd471afa3706a314112feedback.jpg')
    # file = open('test.wav', 'rb')
    # bucket_name = 'audio'
    # object_name = 'sff/sffsfsg'
    # resp = upload_image(bucket_name=bucket_name, object_name=object_name, file=file)
    # print(resp)


