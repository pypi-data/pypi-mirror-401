import os
# redefine to use local cache in /tmp
os.environ['XDG_CACHE_HOME'] = '/tmp/.cache'

import json
import boto3
from gen3.auth import Gen3Auth
from gen3.index import Gen3Index
from gen3.submission import Gen3Submission
import logging
from datetime import datetime
import jwt
from typing import Dict, List
import re
import pandas as pd
import uuid
from acdc_aws_etl_pipeline.validate.validate import write_parquet_to_db

logger = logging.getLogger(__name__)

def create_boto3_session(aws_profile: str = None):
    """
    Create and return a boto3 Session object using an optional AWS profile.

    Args:
        aws_profile (str, optional): The AWS CLI named profile to use for credentials. If None, uses default credentials.

    Returns:
        boto3.Session: The created session instance.
    """
    logger.debug(f"Creating boto3 session with aws_profile={aws_profile}")
    return boto3.Session(profile_name=aws_profile) if aws_profile else boto3.Session()

def is_s3_uri(s3_uri: str) -> bool:
    """
    Check if the provided URI is a valid S3 URI.

    Args:
        s3_uri (str): The string to check.

    Returns:
        bool: True if the string starts with 's3://', False otherwise.
    """
    logger.debug(f"Checking if {s3_uri} is an S3 URI.")
    return s3_uri.startswith("s3://")

def get_filename(file_path: str) -> str:
    """
    Extract the filename from a file path.

    Args:
        file_path (str): The full path to a file.

    Returns:
        str: The filename (with extension).
    """
    filename = file_path.split("/")[-1]
    logger.debug(f"Extracted filename '{filename}' from file_path '{file_path}'.")
    return filename

def get_node_from_file_path(file_path: str) -> str:
    """
    Extract the node name from a file path, assuming file is named as 'node.json'.

    Args:
        file_path (str): The file path.

    Returns:
        str: The base node name before the extension.
    """
    filename = get_filename(file_path)
    node = filename.split(".")[0]
    logger.debug(f"Extracted node '{node}' from filename '{filename}'.")
    return node

def list_metadata_jsons(metadata_dir: str) -> list:
    """
    List all .json files in a given directory.

    Args:
        metadata_dir (str): Directory containing metadata JSON files.

    Returns:
        list: List of absolute paths to all .json files in the directory.

    Raises:
        Exception: If there is an error reading the directory.
    """
    try:
        logger.info(f"Listing .json files in metadata directory: {metadata_dir}")
        files = os.listdir(metadata_dir)
        return [os.path.abspath(os.path.join(metadata_dir, f)) for f in files if f.endswith(".json")]
    except Exception as e:
        logger.error(f"Error listing metadata JSONs in {metadata_dir}: {e}")
        raise

def find_data_import_order_file(metadata_dir: str) -> str:
    """
    Find the DataImportOrder.txt file within a directory.

    Args:
        metadata_dir (str): Directory to search in.

    Returns:
        str: Full path to the DataImportOrder.txt file.

    Raises:
        FileNotFoundError: If no such file is found.
    """
    try:
        logger.info(f"Searching for DataImportOrder.txt in {metadata_dir}")
        files = [os.path.join(metadata_dir, f) for f in os.listdir(metadata_dir)]
        order_files = [f for f in files if "DataImportOrder.txt" in f]
        if not order_files:
            logger.error("No DataImportOrder.txt file found in the given directory.")
            raise FileNotFoundError("No DataImportOrder.txt file found in the given directory.")
        logger.debug(f"Found DataImportOrder.txt file: {order_files[0]}")
        return order_files[0]
    except Exception as e:
        logger.error(f"Error finding DataImportOrder.txt in {metadata_dir}: {e}")
        raise

def list_metadata_jsons_s3(s3_uri: str, session) -> list:
    """
    List all .json files in an S3 "directory" (prefix).

    Args:
        s3_uri (str): S3 URI to the metadata directory (e.g. "s3://my-bucket/path/to/dir").
        session (boto3.Session): An active boto3 Session.

    Returns:
        list: List of S3 URIs for all .json files found under the prefix.
    """
    logger.info(f"Listing .json files in S3 metadata directory: {s3_uri}")
    s3 = session.client('s3')
    bucket = s3_uri.split("/")[2]
    prefix = "/".join(s3_uri.split("/")[3:])
    if prefix and not prefix.endswith("/"):
        prefix += "/"  # Ensure prefix ends with a slash for directories

    objects = s3.list_objects(Bucket=bucket, Prefix=prefix)
    result = [
        f"s3://{bucket}/{obj['Key']}"
        for obj in objects.get('Contents', [])
        if obj['Key'].endswith(".json")
    ]
    logger.debug(f"Found {len(result)} .json files in S3 at {s3_uri}")
    return result

def find_data_import_order_file_s3(s3_uri: str, session) -> str:
    """
    Search for the DataImportOrder.txt file in an S3 directory.

    Args:
        s3_uri (str): S3 URI specifying the directory/prefix to search.
        session (boto3.Session): An active boto3 Session.

    Returns:
        str: Full S3 URI of the found DataImportOrder.txt file.

    Raises:
        FileNotFoundError: If the file does not exist in the specified prefix.
    """
    logger.info(f"Searching for DataImportOrder.txt in S3 metadata directory: {s3_uri}")
    s3 = session.client('s3')
    bucket = s3_uri.split("/")[2]
    prefix = "/".join(s3_uri.split("/")[3:])
    objects = s3.list_objects(Bucket=bucket, Prefix=prefix)
    order_files = [obj['Key'] for obj in objects.get('Contents', []) if obj['Key'].endswith("DataImportOrder.txt")]
    if not order_files:
        logger.error("No DataImportOrder.txt file found in the given S3 directory.")
        raise FileNotFoundError("No DataImportOrder.txt file found in the given directory.")
    logger.debug(f"Found DataImportOrder.txt file in S3: s3://{bucket}/{order_files[0]}")
    return f"s3://{bucket}/{order_files[0]}"

def read_metadata_json(file_path: str) -> dict:
    """
    Read and return a JSON file from the local file system.

    Args:
        file_path (str): Path to the .json file.

    Returns:
        dict or list: Parsed contents of the JSON file.
    """
    logger.info(f"Reading metadata json from local file: {file_path}")
    with open(file_path, "r") as f:
        data = json.load(f)
    logger.debug(f"Read {len(data) if isinstance(data, list) else 'object'} objects from {file_path}")
    return data

def read_metadata_json_s3(s3_uri: str, session) -> dict:
    """
    Read and return JSON data from an S3 file.

    Args:
        s3_uri (str): Full S3 URI to the .json file.
        session (boto3.Session): Boto3 session.

    Returns:
        dict or list: Parsed JSON object from S3 file.
    """
    logger.info(f"Reading metadata json from S3 file: {s3_uri}")
    s3 = session.client('s3')
    obj = s3.get_object(Bucket=s3_uri.split("/")[2], Key="/".join(s3_uri.split("/")[3:]))
    data = json.loads(obj['Body'].read().decode('utf-8'))
    logger.debug(f"Read {len(data) if isinstance(data, list) else 'object'} objects from {s3_uri}")
    return data

def read_data_import_order_txt_s3(s3_uri: str, session, exclude_nodes: list = None) -> list:
    """
    Read a DataImportOrder.txt file from S3 and return node order as a list, optionally excluding some nodes.

    Args:
        s3_uri (str): S3 URI to the DataImportOrder.txt file.
        session (boto3.Session): Boto3 session.
        exclude_nodes (list, optional): Node names to exclude from result.

    Returns:
        list: Node names (order as listed in file), optionally excluding nodes in exclude_nodes.

    Raises:
        ValueError: If the provided S3 URI does not point to DataImportOrder.txt.
    """
    filename = s3_uri.split("/")[-1]
    if 'DataImportOrder.txt' not in filename:
        logger.error(f"File {filename} is not a DataImportOrder.txt file")
        raise ValueError(f"File {filename} is not a DataImportOrder.txt file")
    logger.info(f"Reading DataImportOrder.txt from S3 file: {s3_uri}")
    s3 = session.client('s3')
    obj = s3.get_object(Bucket=s3_uri.split("/")[2], Key="/".join(s3_uri.split("/")[3:]))
    content = obj['Body'].read().decode('utf-8')
    import_order = [line.rstrip() for line in content.splitlines() if line.strip()]
    logger.debug(f"Raw import order from S3 file: {import_order}")
    if exclude_nodes is not None:
        import_order = [node for node in import_order if node not in exclude_nodes]
        logger.debug(f"Import order after excluding nodes {exclude_nodes}: {import_order}")
    logger.debug(f"Final import order from S3 file {s3_uri}: {import_order}")
    return import_order

def read_data_import_order_txt(file_path: str, exclude_nodes: list) -> list:
    """
    Read DataImportOrder.txt from local file, optionally excluding some nodes.

    Args:
        file_path (str): Path to DataImportOrder.txt.
        exclude_nodes (list): Node names to exclude from result.

    Returns:
        list: Node names, excludes specified nodes, keeps listed order.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    try:
        logger.info(f"Reading DataImportOrder.txt from local file: {file_path}")
        with open(file_path, "r") as f:
            import_order = [line.rstrip() for line in f if line.strip()]
            logger.debug(f"Raw import order from file: {import_order}")
            if exclude_nodes is not None:
                import_order = [node for node in import_order if node not in exclude_nodes]
                logger.debug(f"Import order after excluding nodes {exclude_nodes}: {import_order}")
        logger.debug(f"Final import order from {file_path}: {import_order}")
        return import_order
    except FileNotFoundError:
        logger.error(f"Error: DataImportOrder.txt not found in {file_path}")
        return []

def split_json_objects(json_list, max_size_kb=50, print_results=False) -> list:
    """
    Split a list of JSON-serializable objects into size-limited chunks.

    Each chunk/list, when JSON-serialized, will not exceed max_size_kb kilobytes.

    Args:
        json_list (list): List of JSON serializable objects.
        max_size_kb (int, optional): Max chunk size in KB. Default: 50.
        print_results (bool, optional): If True, info log the size/count per chunk. Default: False.

    Returns:
        list: List of lists. Each sublist size (JSON-serialized) <= max_size_kb.
    """
    logger.info(f"Splitting JSON objects into max {max_size_kb} KB chunks. Total items: {len(json_list)}")
    def get_size_in_kb(obj):
        """
        Get the size in kilobytes of the JSON-serialized object.

        Args:
            obj: JSON-serializable object.

        Returns:
            float: Size of the object in kilobytes.
        """
        import sys
        size_kb = sys.getsizeof(json.dumps(obj)) / 1024
        logger.debug(f"Calculated size: {size_kb:.2f} KB")
        return size_kb

    def split_list(json_list):
        """
        Recursively split the list so each chunk fits within max_size_kb.

        Args:
            json_list (list): List to split.

        Returns:
            list: List of sublists.
        """
        if get_size_in_kb(json_list) <= max_size_kb:
            logger.debug(f"Split length {len(json_list)} is within max size {max_size_kb} KB.")
            return [json_list]
        mid = len(json_list) // 2
        left_list = json_list[:mid]
        right_list = json_list[mid:]
        logger.debug(f"Splitting list at index {mid}: left {len(left_list)}, right {len(right_list)}")
        return split_list(left_list) + split_list(right_list)

    split_lists = split_list(json_list)
    if print_results:
        for i, lst in enumerate(split_lists):
            logger.info(f"List {i+1} size: {get_size_in_kb(lst):.2f} KB, contains {len(lst)} objects")
    logger.debug(f"Total splits: {len(split_lists)}")
    return split_lists

def get_gen3_api_key_aws_secret(secret_name: str, region_name: str, session) -> dict:
    """
    Retrieve a Gen3 API key stored as a secret in AWS Secrets Manager and parse it as a dict.

    Args:
        secret_name (str): Name of the AWS secret.
        region_name (str): AWS region where the secret is located.
        session (boto3.Session): Boto3 session.

    Returns:
        dict: Parsed Gen3 API key.

    Raises:
        Exception: On failure to retrieve or parse the secret.
    """
    logger.info(f"Retrieving Gen3 API key from AWS Secrets Manager: secret_name={secret_name}, region={region_name}")
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        logger.error(f"Error getting secret value from AWS Secrets Manager: {e}")
        raise e

    secret = get_secret_value_response['SecretString']

    try:
        secret = json.loads(secret)
        api_key = secret
        logger.debug(f"Retrieved Gen3 API key from secret {secret_name}")
        return api_key
    except Exception as e:
        logger.error(f"Error parsing Gen3 API key from AWS Secrets Manager: {e}")
        raise e


def infer_api_endpoint_from_jwt(jwt_token: str, api_version: str = 'v0') -> str:
    """
    Extracts the URL from a JSON Web Token (JWT) credential.

    Args:
        jwt_string (string): The JSON Web Token (JWT) credential.

    Returns:
        str: The extracted URL.
    """
    logger.info("Decoding JWT to extract API URL.")
    url = jwt.decode(jwt_token, options={"verify_signature": False}).get('iss', '')
    if '/user' in url:
        url = url.split('/user')[0]
    url = f"{url}/api/{api_version}"
    logger.info(f"Extracted API URL from JWT: {url}")
    return url


def create_gen3_submission_class(api_key: dict):
    """
    Create and authenticate a Gen3Submission client using a temporary file for API key.

    Args:
        api_key (dict): The Gen3 API key as Python dict.
        api_endpoint (str): Gen3 endpoint (hostname/base API URL).

    Returns:
        Gen3Submission: An authenticated Gen3Submission object.
    """
    logger.debug("Extracting JWT token from API key dict.")
    jwt_token = api_key['api_key']
    logger.info("Inferring API endpoint from JWT token.")
    api_endpoint = infer_api_endpoint_from_jwt(jwt_token)
    logger.debug(f"Inferred API endpoint: {api_endpoint}")
    logger.info(f"Creating Gen3Submission class for endpoint: {api_endpoint}")
    auth = Gen3Auth(refresh_token=api_key)
    submit = Gen3Submission(endpoint=api_endpoint, auth_provider=auth)
    return submit


def submit_data_chunks(
    split_json_list: list,
    node: str,
    gen3_submitter,
    project_id: str,
    max_retries: int,
    file_path: str,
    program_id: str = "program1"
) -> List[Dict]:
    """
    Submit each chunk of data (in split_json_list) for a given node to Gen3, using retry logic and logging on failures.

    Args:
        split_json_list (list): List of JSON-serializable chunked data to submit.
        node (str): Name of the data node being submitted.
        gen3_submitter: A Gen3Submission instance for making submissions.
        project_id (str): The project identifier within Gen3.
        max_retries (int): Maximum number of retry attempts per chunk on failure.
        file_path (str): Path of the file that was submitted. Used only for data capture.
        program_id (str, optional): The Gen3 program id (default: "program1").

    Returns:
        List[Dict]: List of response dictionaries for each submitted chunk.

    Raises:
        Exception: If submission fails after all retry attempts for any chunk.
    """

    n_json_data = len(split_json_list)
    response_results = []

    for index, jsn in enumerate(split_json_list):
        progress_str = f"{index + 1}/{n_json_data}"

        submission_success = False
        last_exception = None

        attempt = 0
        while attempt <= max_retries:
            try:
                if attempt == 0:
                    log_msg = (
                        f"[SUBMIT]  | Project: {project_id:<10} | Node: {node:<12} | "
                        f"Split: {progress_str:<5}"
                    )
                    logger.info(log_msg)
                else:
                    log_msg = (
                        f"[RETRY]   | Project: {project_id:<10} | Node: {node:<12} | "
                        f"Split: {progress_str:<5} | Attempt: {attempt}/{max_retries}"
                    )
                    logger.warning(log_msg)

                res = gen3_submitter.submit_record(program_id, project_id, jsn)
                res.update({"file_path": file_path})
                response_results.append(res)
                submission_success = True
                logger.info(
                    f"\033[92m[SUCCESS]\033[0m | Project: {project_id:<10} | "
                    f"Node: {node:<12} | Split: {progress_str:<5}"
                )
                break  # Success

            except Exception as e:
                last_exception = e
                logger.error(
                    f"Error submitting chunk {progress_str} for node '{node}': {e}"
                )

                if attempt < max_retries:
                    import time
                    time.sleep(0.2)
                else:
                    logger.critical(
                        f"\033[91m[FAILED]\033[0m  | Project: {project_id:<10} | "
                        f"Node: {node:<12} | Split: {progress_str:<5} | Error: {e}"
                    )
            attempt += 1

        if not submission_success:
            # After retries, still failed
            raise Exception(
                f"Failed to submit chunk {progress_str} for node '{node}' after {max_retries + 1} attempts. "
                f"Last error: {last_exception}"
            )

    logger.info(f"Finished submitting node '{node}'.")
    return response_results


def flatten_submission_results(submission_results: List[Dict]) -> List[Dict]:
    """
    Flattens a list of Gen3 submission result dictionaries into a single list of entity dictionaries.

    For each submission result, this function processes its entities (if any),
    extracting the 'project_id' and 'submitter_id' from the 'unique_keys' field (if present)
    into the top-level entity dictionary for easy access.

    Any submission result that does not have a code of 200 or lacks entities is skipped, and a warning is logged.

    Args:
        submission_results (List[Dict]):
            A list of Gen3 submission result dictionaries, each containing at least a "code" and "entities" entry.

    Returns:
        List[Dict]:
            A flat list, where each element is an entity dictionary (with keys 'project_id' and 'submitter_id' added if available).
    """
    flat_list_dict = []
    total = len(submission_results)
    logger.info(f"Flattening {total} submission result(s)...")

    for idx, obj in enumerate(submission_results, 1):
        transaction_id = obj.get("transaction_id")
        code = obj.get("code")
        if code != 200:
            logger.warning(f"Skipping submission result at index {idx-1} (code={code})")
            continue

        entities = obj.get("entities")

        if entities is None:
            logger.warning(f"No entities found in submission result at index {idx-1}")
            continue

        logger.info(f"Processing submission result {idx} of {total}, {len(entities)} entities")

        for entity in entities:
            unique_keys = entity.get("unique_keys", [{}])
            if unique_keys and isinstance(unique_keys, list):
                keys = unique_keys[0]
                entity["project_id"] = keys.get("project_id")
                entity["submitter_id"] = keys.get("submitter_id")
                entity["transaction_id"] = transaction_id
                entity["file_path"] = obj.get("file_path", '')
            flat_list_dict.append(entity)

    # renaming cols
    for entity in flat_list_dict:
        entity["gen3_guid"] = entity.pop("id", None)
        entity["node"] = entity.pop("type", None)

    logger.info(f"Finished flattening. Total entities: {len(flat_list_dict)}")
    return flat_list_dict


def find_version_from_path(path):
    version_pattern = re.compile(r"^v?(\d+\.\d+\.\d+)$")
    found_versions = []

    for segment in path.split('/'):
        match = version_pattern.match(segment)
        if match:
            found_versions.append(match.group(1))

    if not found_versions:
        return None

    if len(found_versions) > 1:
        logger.warning("more than one match found in path for version string")

    return found_versions[-1]


def collect_versions_from_metadata_file_list(metadata_file_list):
    versions = []
    for file_path in metadata_file_list:
        version = find_version_from_path(file_path)
        if version:
            versions.append(version)
    versions = list(set(versions))
    if len(versions) > 1:
        logger.error(f"more than one version found in metadata file list: {metadata_file_list}")
        raise
    return versions[0]


class MetadataSubmitter:
    def __init__(
        self,
        metadata_file_list: list,
        api_key: dict,
        project_id: str,
        data_import_order_path: str,
        program_id: str = "program1",
        max_size_kb: int = 100,
        exclude_nodes: list = ["project", "program", "acknowledgement", "publication"],
        max_retries: int = 3,
        aws_profile: str = None
    ):
        """
        Initialises a MetadataSubmitter for submitting a set of metadata JSON files to a Gen3 data commons endpoint, in order.

        Args:
            metadata_file_list (list): List of local file paths or S3 URIs to metadata .json files, one per node type.
            api_key (dict): Gen3 API key as a parsed dictionary.
            project_id (str): Gen3 project ID to submit data to.
            data_import_order_path (str): Path or S3 URI to DataImportOrder.txt specifying node submission order.
            program_id (str, optional): Gen3 program ID (default: "program1").
            max_size_kb (int, optional): Maximum size per submission chunk, in KB (default: 100).
            exclude_nodes (list, optional): List of node names to skip during submission (default: ["project", "program", "acknowledgement", "publication"]).
            max_retries (int, optional): Maximum number of retry attempts per node chunk (default: 3).
            aws_profile (str, optional): AWS CLI named profile to use for boto3 session (default: None).
        """
        self.metadata_file_list = metadata_file_list
        self.api_key = api_key
        self.project_id = project_id
        self.data_import_order_path = data_import_order_path
        self.program_id = program_id
        self.max_size_kb = max_size_kb
        self.exclude_nodes = exclude_nodes
        self.max_retries = max_retries
        self.submission_results = []
        self.aws_profile = aws_profile
        self.boto3_session = self._create_boto3_session()
        logger.info("MetadataSubmitter initialised.")

    def _create_gen3_submission_class(self):
        return create_gen3_submission_class(self.api_key)
    
    def _create_boto3_session(self):
        return create_boto3_session(self.aws_profile)

    def _read_data_import_order(self, data_import_order_path: str, exclude_nodes: list[str], boto3_session = None):
        if is_s3_uri(data_import_order_path):
            session = boto3_session or self.boto3_session
            return read_data_import_order_txt_s3(data_import_order_path, session, exclude_nodes)  
        else:
            return read_data_import_order_txt(data_import_order_path, exclude_nodes)

    def _prepare_json_chunks(self, metadata_file_path: str, max_size_kb: int) -> List[List[Dict]]:
        """
        Read JSON data from a given file path and split it into chunks,
        each with a maximum size of ``max_size_kb`` kilobytes.

        Args:
            metadata_file_path (str): File path (local or S3 URI) to the JSON data.
            max_size_kb (int): Maximum allowed size (in kilobytes) for each chunk.

        Returns:
            list: A list of chunks, where each chunk is a list of dictionaries
                containing JSON data.
        """
        logger.info(f"Reading metadata json from {metadata_file_path}")
        if is_s3_uri(metadata_file_path):
            session = self.boto3_session
            data = read_metadata_json_s3(metadata_file_path, session)
        else:
            data = read_metadata_json(metadata_file_path)
        return split_json_objects(data, max_size_kb)

    def _create_file_map(self):
        """
        Generate a mapping from node names to metadata file paths.

        This method infers the node name for each file in `self.metadata_file_list`
        and returns a dictionary where the keys are node names and the values
        are the corresponding file paths.

        Returns:
            dict: Dictionary mapping node names (str) to their associated metadata file paths (str).
        """
        file_map = {
            get_node_from_file_path(file): file
            for file in self.metadata_file_list
        }
        return file_map

    def submit_metadata(self) -> List[Dict]:
        """
        Submits metadata for each node defined in the data import order, except those in the exclude list.

        For each node, this method retrieves the corresponding metadata file, splits the JSON data
        into size-constrained chunks, and submits each chunk to the Gen3 submission API. Responses
        from all submissions are gathered and returned as a list.

        Returns:
            List[Dict]: A list of response dictionaries returned from the Gen3 metadata submissions.
        """
        gen3_submitter = self._create_gen3_submission_class()
        data_import_order = self._read_data_import_order(self.data_import_order_path, self.exclude_nodes, self.boto3_session)
        file_map = self._create_file_map()
        output_response_list_dict = []

        logger.info("Starting metadata submission.")
        for node in data_import_order:

            if node in self.exclude_nodes:
                logger.info(f"Skipping node '{node}' (in exclude list).")
                continue
            file_path = file_map.get(node)
            if not file_path:
                logger.info(f"Skipping node '{node}' (not present in file list).")
                continue

            logger.info(f"Processing file '{file_path}' for node '{node}'.")
            logger.info("Splitting JSON data into chunks.")
            json_chunks = self._prepare_json_chunks(file_path, self.max_size_kb)

            logger.info("Submitting chunks to Gen3.")
            response_list = submit_data_chunks(
                split_json_list=json_chunks,
                node=node,
                file_path=file_path,
                gen3_submitter=gen3_submitter,
                project_id=self.project_id,
                max_retries=self.max_retries,
                program_id=self.program_id
            )
            output_response_list_dict.extend(response_list)

        self.submission_results = output_response_list_dict
        return output_response_list_dict

    def upload_metadata_submission_results(
        self,
        dataset_root: str,
        database: str,
        table: str,
        partition_cols: list = ["upload_datetime"],
    ):
        """
        Uploads the submission results to s3 and parquet table.

        Args:
            dataset_root (str): S3 path where the parquet files will be stored 
                (e.g., "s3://acdc-dataops-metadata/metadata_upload/").
            database (str): Database name for storing the metadata upload 
                (e.g., "acdc_dataops_metadata_db").
            table (str): Table name for storing the metadata upload 
                (e.g., "metadata_upload").
            partition_cols (list, optional): List of column names to partition the parquet table by. 
                Defaults to ["upload_datetime"].
        """
        logger.info("Collecting version from metadata file list.")
        version = collect_versions_from_metadata_file_list(self.metadata_file_list)
        logger.info(f"Extracted version: {version}")

        logger.info("Inferring API endpoint from JWT.")
        api_endpoint = infer_api_endpoint_from_jwt(self.api_key['api_key'])
        logger.info(f"Using API endpoint: {api_endpoint}")

        upload_datetime = datetime.now().isoformat()
        upload_id = str(uuid.uuid4())
        logger.info(f"Upload datetime: {upload_datetime}")
        logger.info(f"Generated upload ID: {upload_id}")

        logger.info("Flattening submission results for upload.")
        flattened_results = flatten_submission_results(self.submission_results)
        logger.info(f"Flattened {len(flattened_results)} submission result entries.")

        logger.info("Converting flattened results to DataFrame.")
        flattened_results_df = pd.DataFrame(flattened_results)
        flattened_results_df['upload_datetime'] = upload_datetime
        flattened_results_df['upload_id'] = upload_id
        flattened_results_df['api_endpoint'] = api_endpoint
        flattened_results_df['version'] = version

        logger.info(
            f"Writing DataFrame to parquet and S3/table: "
            f"dataset_root={dataset_root}, database={database}, table={table}, partition_cols={partition_cols}"
        )
        write_parquet_to_db(
            df=flattened_results_df,
            dataset_root=dataset_root,
            database=database,
            table=table,
            partition_cols=partition_cols
        )
        logger.info("Metadata submission results upload complete.")