import os
import mimetypes
from datetime import datetime
from functools import lru_cache
from typing import Optional, Tuple
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()


class S3UploadResponse(BaseModel):
    success: bool
    key: str
    url: Optional[str] = None
    filename: str


def _bool_env(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


@lru_cache(maxsize=1)
def get_s3_settings() -> dict:
    return {
        "bucket": os.getenv("S3_BUCKET"),
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "prefix": os.getenv("S3_PREFIX", "").strip("/"),
        "public_read": _bool_env("S3_PUBLIC_READ", False),
        "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }


@lru_cache(maxsize=1)
def get_s3_client():
    settings = get_s3_settings()
    params = {}
    if settings["region"]:
        params["region_name"] = settings["region"]
    if settings["access_key"] and settings["secret_key"]:
        params["aws_access_key_id"] = settings["access_key"]
        params["aws_secret_access_key"] = settings["secret_key"]
    return boto3.client("s3", **params)


def build_s3_key(filename: str) -> str:
    settings = get_s3_settings()
    if not filename:
        raise ValueError("Filename cannot be empty")
    safe_name = filename.replace(" ", "_")
    key = f"{uuid4()}-{safe_name}"
    return f"{settings['prefix']}/{key}" if settings["prefix"] else key


def build_object_url(key: str) -> Optional[str]:
    settings = get_s3_settings()
    if not (settings["bucket"] and settings["region"]):
        return None
    return f"https://{settings['bucket']}.s3.{settings['region']}.amazonaws.com/{key}"


def upload_fileobj_to_s3(
    file_obj,
    filename: str,
    content_type: Optional[str] = None,
    acl_public_read: Optional[bool] = None,
) -> Tuple[str, Optional[str]]:
    """
    Uploads a file-like object to S3. Returns the object key and a direct URL if public.
    """
    settings = get_s3_settings()
    if not settings["bucket"]:
        raise RuntimeError("S3_BUCKET is not configured")

    key = build_s3_key(filename)
    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type
    else:
        guessed, _ = mimetypes.guess_type(filename)
        if guessed:
            extra_args["ContentType"] = guessed

    public_flag = settings["public_read"] if acl_public_read is None else acl_public_read
    if public_flag:
        extra_args["ACL"] = "public-read"

    s3 = get_s3_client()
    try:
        if extra_args:
            s3.upload_fileobj(file_obj, settings["bucket"], key, ExtraArgs=extra_args)
        else:
            s3.upload_fileobj(file_obj, settings["bucket"], key)
    except ClientError as exc:
        raise RuntimeError(f"S3 upload failed: {exc}")

    url = build_object_url(key) if public_flag else None
    return key, url


def generate_presigned_get_url(key: str, expires: int = 3600) -> str:
    settings = get_s3_settings()
    if not settings["bucket"]:
        raise RuntimeError("S3_BUCKET is not configured")

    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings["bucket"], "Key": key},
        ExpiresIn=expires,
    )


@router.post("/api/s3/upload", response_model=S3UploadResponse)
async def upload_photo(
    file: UploadFile = File(...),
):
    """
    Upload a file to S3 and return the key and URL.
    The photo database record should be created separately using POST /api/Photos
    """
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/heic"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Ensure file pointer is at the beginning
    file.file.seek(0)

    try:
        key, url = upload_fileobj_to_s3(
            file.file,
            filename=file.filename,
            content_type=file.content_type,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")

    return S3UploadResponse(
        success=True,
        key=key,
        url=url,
        filename=file.filename or key.split('/')[-1]
    )
