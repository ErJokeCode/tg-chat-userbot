from database.orm.core_orm import CoreOrm
from database.postgres_core import PostgresCore
from database.core_s3 import CoreS3
from database.orm.base_schemes import ResponseStatus, ListDTO

from config import settings


core_pg_orm = CoreOrm()

core_postgres = PostgresCore()

core_s3 = CoreS3(
    user=settings.MINIO_ROOT_USER,
    password=settings.MINIO_ROOT_PASSWORD,
    endpoint_url=settings.MINIO_URL,
    bucket_name=settings.MINIO_BUCKET_NAME,
)

__all__ = ["core_pg_orm", "core_postgres",
           "core_s3", "ResponseStatus", "ListDTO"]
