from dataclasses import dataclass
from environs import Env


@dataclass()
class DjangoConfig:
    secret_key: str
    domain: str


@dataclass()
class DB:
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str


@dataclass()
class Redis:
    redis_host: str
    redis_port: str
    redis_db: str
    redis_pass: str
    redis_key_list_size: int
    redis_key_ttl: int


@dataclass()
class Minio:
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_media_bucket: str



@dataclass()
class Config:
    django_config: DjangoConfig
    db: DB
    redis: Redis
    minio: Minio


def get_config(path: str):
    env = Env()
    env.read_env(path)

    return Config(

        django_config=DjangoConfig(
            secret_key=env.str("SECRET_KEY"),
            domain=env.str("DOMAIN"),
        ),

        db=DB(
            db_user=env.str("DB_USER"),
            db_pass=env.str("DB_PASS"),
            db_host=env.str("DB_HOST"),
            db_port=env.str("DB_PORT"),
            db_name=env.str("DB_NAME")
        ),

        redis=Redis(
            redis_host=env.str("REDIS_HOST"),
            redis_port=env.str("REDIS_PORT"),
            redis_db=env.str("REDIS_DB"),
            redis_pass=env.str("REDIS_PASS"),
            redis_key_list_size=env.int("REDIS_KEY_LIST_SIZE"),
            redis_key_ttl=env.int("REDIS_KEY_TTL")
        ),

        minio=Minio(
            minio_endpoint=env.str("MINIO_ENDPOINT"),
            minio_access_key=env.str("MINIO_ACCESS_KEY"),
            minio_secret_key=env.str("MINIO_SECRET_KEY"),
            minio_media_bucket=env.str("MINIO_MEDIA_BUCKET")
        ),
    )

config = get_config('.env')
