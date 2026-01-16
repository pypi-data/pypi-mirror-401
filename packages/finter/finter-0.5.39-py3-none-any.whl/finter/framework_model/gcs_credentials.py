"""
GCS Credentials wrapper for accessing Google Cloud Storage.
Provides functions to load Avro files from prod-krx-avro bucket.
"""

import re
from io import BytesIO

import pandas as pd

from finter.api.gcs_credentials_api import GCSCredentialsApi
from finter.rest import ApiException
from finter.settings import get_api_client, logger


def get_gcs_credentials(bucket: str):
    """Retrieve GCS credentials from the backend API.

    Args:
        bucket: GCS bucket name to get credentials for

    Returns:
        GcsCredentialsResponse: Response containing access_token, expires_at, bucket, object_path
    """
    api_instance = GCSCredentialsApi(get_api_client())
    try:
        api_response = api_instance.gcs_credentials_retrieve(bucket=bucket)
        return api_response
    except ApiException as e:
        logger.error(
            "Exception when calling GCSCredentialsApi->gcs_credentials_retrieve: %s\n" % e
        )
        raise


def load_krx_avro(date: str, tr_code: str) -> pd.DataFrame:
    """
    Load KRX Avro file from GCS as a DataFrame.

    Args:
        date: Date string in YYYYMMDD format (e.g., "20260109")
        tr_code: TR code for the data (e.g., "Z6000")

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame
    """
    # Validate date format (YYYYMMDD)
    if not re.match(r'^\d{8}$', date):
        raise ValueError(
            f"Invalid date format: {date}. Expected YYYYMMDD format (e.g., '20260109')"
        )

    bucket_name = "prod-krx-avro"

    credentials_response = get_gcs_credentials(bucket=bucket_name)
    if not credentials_response:
        raise PermissionError(f"Failed to get GCS credentials for {date}/{tr_code}.avro")

    # Lazy imports to avoid import errors when dependencies are not installed
    import fastavro
    from google.cloud import storage
    from google.oauth2.credentials import Credentials

    # Create OAuth2 credentials from access token
    credentials = Credentials(token=credentials_response.access_token)

    # Create GCS client with credentials
    client = storage.Client(credentials=credentials, project=None)

    blob_path = f"{date}/{tr_code}.avro"

    logger.info(f"Loading Avro file: gs://{bucket_name}/{blob_path}")

    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        avro_bytes = blob.download_as_bytes()

        avro_buffer = BytesIO(avro_bytes)
        reader = fastavro.reader(avro_buffer)
        records = list(reader)

        df = pd.DataFrame(records)
        logger.info(f"Loaded {len(df)} rows from gs://{bucket_name}/{blob_path}")
        return df

    except Exception as e:
        if "Not Found" in str(e) or "404" in str(e):
            logger.error(f"Avro file not found: gs://{bucket_name}/{blob_path}")
            raise FileNotFoundError(f"Avro file not found: gs://{bucket_name}/{blob_path}")
        raise
