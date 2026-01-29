"""
Utility functions for EDC integration.
"""

import requests
import json
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def get_edc_url() -> Optional[str]:
    """Get EDC URL from settings."""
    return getattr(settings, 'EDC_URL', None)


def get_edc_participant_id() -> Optional[str]:
    """Get EDC participant ID from settings."""
    return getattr(settings, 'EDC_PARTICIPANT_ID', None)


def get_edc_api_key() -> Optional[str]:
    """Get EDC API key from settings."""
    return getattr(settings, 'EDC_API_KEY', None)


def get_asset_id_from_request(request, strategy: str = None) -> str:
    """
    Generate asset ID from the request URL.

    Strategy can be configured via EDC_ASSET_ID_STRATEGY setting:
    - 'slugify' (default): Slugify the URL without resource ID
    - 'path': Use the URL path (e.g., '/objects/trial6')
    - 'full_url': Use the complete URL
    - 'container': Use only the container path

    Args:
        request: Django request object
        strategy: Override for asset ID generation strategy

    Returns:
        str: Asset identifier
    """
    if strategy is None:
        strategy = getattr(settings, 'EDC_ASSET_ID_STRATEGY', 'slugify')

    url = request.build_absolute_uri()
    parsed_url = urlparse(url)

    if strategy == 'path':
        # Return just the path, removing resource IDs
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts and path_parts[-1].isdigit():
            path_parts = path_parts[:-1]
        return '/' + '/'.join(path_parts)

    elif strategy == 'container':
        # Return only the container/collection name
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts and path_parts[-1].isdigit():
            path_parts = path_parts[:-1]
        return path_parts[-1] if path_parts else ''

    elif strategy == 'full_url':
        # Return the full URL without resource ID
        path_parts = parsed_url.path.strip('/').split('/')
        if path_parts and path_parts[-1].isdigit():
            path_parts = path_parts[:-1]
        clean_path = '/'.join(path_parts)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/{clean_path}"

    else:  # 'slugify' (default)
        # Slugify the URL (backward compatible with existing implementation)
        netloc = parsed_url.hostname
        path_parts = parsed_url.path.strip('/').split('/')

        # Remove the resource ID if the last part is a digit
        if path_parts and path_parts[-1].isdigit():
            path_parts = path_parts[:-1]

        clean_path = '/'.join(path_parts)
        port = f":{parsed_url.port}" if parsed_url.port else ""
        clean_url = f"{parsed_url.scheme}{port}//{netloc}/{clean_path}"

        return slugify(clean_url)


def fetch_agreement(agreement_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch contract agreement details from EDC Management API v3.

    Uses the GET /v3/contractagreements/{id} endpoint.

    Args:
        agreement_id: Contract agreement identifier

    Returns:
        Dict containing agreement details, or None if not found/error
    """
    edc_url = get_edc_url()
    if not edc_url:
        logger.error("EDC_URL not configured")
        return None

    edc_participant_id = get_edc_participant_id()
    if not edc_participant_id:
        logger.error("EDC_PARTICIPANT_ID not configured")
        return None

    # Construct the v3 API endpoint
    url = f"{edc_url}/management/v3/contractagreements/{agreement_id}"

    headers = {
        'Content-Type': 'application/json',
    }

    # Add API key if configured (for provider-side validation)
    edc_api_key = get_edc_api_key()
    if edc_api_key:
        headers['X-Api-Key'] = edc_api_key
        print(f"[EDC UTILS] Using API key: {edc_api_key[:10]}...")

    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"[EDC UTILS] Response status: {response.status_code}")

        if response.status_code == 404:
            print(f"[EDC UTILS] Agreement {agreement_id} not found (404)")
            logger.info(f"Agreement {agreement_id} not found")
            return None

        response.raise_for_status()
        result = response.json()
        print(f"[EDC UTILS] Agreement data: {result}")
        return result

    except requests.exceptions.Timeout:
        print(f"[EDC UTILS] TIMEOUT fetching agreement")
        logger.error(f"Timeout fetching agreement {agreement_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[EDC UTILS] REQUEST ERROR: {str(e)}")
        logger.error(f"Error fetching agreement {agreement_id}: {str(e)}")
        return None


def fetch_catalog_entry(asset_id: str, resource_url: str = None) -> Optional[Dict[str, Any]]:
    """
    Fetch local asset and its policy from provider's EDC.

    Uses EDC Management API v3 to query LOCAL assets (not remote catalog).
    First tries exact ID match, then falls back to searching by baseUrl.

    Args:
        asset_id: The asset ID to search for
        resource_url: Optional resource URL to match against asset baseUrl
    """
    print(f"[EDC UTILS] fetch_catalog_entry:")
    print(f"[EDC UTILS]   - asset_id: {asset_id}")
    print(f"[EDC UTILS]   - resource_url: {resource_url}")

    edc_url = get_edc_url()
    if not edc_url:
        logger.error("EDC_URL not configured")
        return None

    headers = {
        'Content-Type': 'application/json',
    }

    edc_api_key = get_edc_api_key()
    if edc_api_key:
        headers['X-Api-Key'] = edc_api_key
    else:
        logger.warning("EDC_API_KEY not configured - asset fetch may fail")

    # First, try exact ID match using local assets endpoint
    try:
        print(f"[EDC UTILS] Querying local asset by ID: {asset_id}")
        asset_url = f"{edc_url}/management/v3/assets/{asset_id}"
        response = requests.get(asset_url, headers=headers, timeout=10)

        if response.status_code == 200:
            asset_data = response.json()
            print(f"[EDC UTILS] Found asset by ID match: {asset_id}")
            # Get policies for this asset
            return _build_catalog_entry_from_asset(asset_data, headers, edc_url)

        print(f"[EDC UTILS] Asset not found by ID (status {response.status_code}), trying URL match...")

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching asset {asset_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching asset: {str(e)}")

    # If no exact match and resource_url provided, search by baseUrl
    if resource_url:
        return fetch_catalog_entry_by_url(resource_url)

    return None


def _build_catalog_entry_from_asset(asset_data: Dict[str, Any], headers: Dict[str, str], edc_url: str) -> Optional[Dict[str, Any]]:
    """
    Build a catalog-like entry from asset data by fetching its offers from the DSP catalog.

    IMPORTANT: We must query the DSP protocol catalog endpoint to get proper offer IDs.
    The Management API only returns policy definitions, not the offer IDs needed for negotiation.
    """
    # EDC v3 may use different field names for asset ID
    asset_id = (
        asset_data.get('@id') or
        asset_data.get('id') or
        asset_data.get('edc:id') or
        asset_data.get('https://w3id.org/edc/v0.0.1/ns/id')
    )
    print(f"[EDC UTILS] Building catalog entry for asset: {asset_id}")
    print(f"[EDC UTILS] Asset data keys: {list(asset_data.keys())}")

    # Query the DSP catalog to get proper offer IDs
    # The provider queries its own catalog via DSP protocol
    try:
        catalog_entry = _fetch_catalog_offers_for_asset(asset_id, edc_url, headers)
        if catalog_entry:
            return catalog_entry

        print(f"[EDC UTILS] No offers found in catalog for asset {asset_id}")
        return None

    except Exception as e:
        print(f"[EDC UTILS] Error building catalog entry: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _fetch_catalog_offers_for_asset(asset_id: str, edc_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Fetch catalog offers for a specific asset via DSP protocol.

    This queries the provider's own catalog to get the real offer IDs
    that consumers need for contract negotiation.
    """
    # Derive the protocol endpoint from management URL
    # e.g., https://provider.connector/management -> https://provider.connector/protocol
    protocol_url = edc_url.replace('/management', '') + '/protocol'
    catalog_url = f"{edc_url}/management/v3/catalog/request"

    print(f"[EDC UTILS] Querying catalog for asset {asset_id}")
    print(f"[EDC UTILS] Protocol URL: {protocol_url}")

    # Query the catalog via Management API (provider querying its own catalog)
    catalog_request = {
        "@context": {
            "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
        },
        "@type": "CatalogRequest",
        "counterPartyAddress": protocol_url,
        "protocol": "dataspace-protocol-http",
        "querySpec": {
            "filterExpression": [
                {
                    "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
                    "operator": "=",
                    "operandRight": asset_id
                }
            ]
        }
    }

    try:
        response = requests.post(catalog_url, headers=headers, json=catalog_request, timeout=15)
        print(f"[EDC UTILS] Catalog response status: {response.status_code}")

        if response.status_code != 200:
            print(f"[EDC UTILS] Catalog request failed: {response.text}")
            # Try without filter as fallback
            return _fetch_full_catalog_and_find_asset(asset_id, catalog_url, protocol_url, headers)

        catalog = response.json()
        print(f"[EDC UTILS] Catalog response keys: {list(catalog.keys())}")

        # Extract dataset for our asset
        datasets = catalog.get('dcat:dataset', [])
        if isinstance(datasets, dict):
            datasets = [datasets]

        print(f"[EDC UTILS] Found {len(datasets)} datasets in catalog")

        for dataset in datasets:
            dataset_id = dataset.get('@id') or dataset.get('id')
            print(f"[EDC UTILS] Checking dataset: {dataset_id}")

            if dataset_id == asset_id:
                print(f"[EDC UTILS] Found matching dataset with offers!")
                # Return the dataset which contains proper offer IDs in odrl:hasPolicy
                return dataset

        # If no exact match, try partial match or return first dataset
        if datasets:
            print(f"[EDC UTILS] No exact match, using first dataset")
            return datasets[0]

        return None

    except Exception as e:
        print(f"[EDC UTILS] Error fetching catalog: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _fetch_full_catalog_and_find_asset(asset_id: str, catalog_url: str, protocol_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Fetch full catalog and find the asset (fallback when filtered query fails).
    """
    print(f"[EDC UTILS] Fetching full catalog as fallback")

    catalog_request = {
        "@context": {
            "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
        },
        "@type": "CatalogRequest",
        "counterPartyAddress": protocol_url,
        "protocol": "dataspace-protocol-http"
    }

    try:
        response = requests.post(catalog_url, headers=headers, json=catalog_request, timeout=15)

        if response.status_code != 200:
            print(f"[EDC UTILS] Full catalog request failed: {response.text}")
            return None

        catalog = response.json()
        datasets = catalog.get('dcat:dataset', [])
        if isinstance(datasets, dict):
            datasets = [datasets]

        print(f"[EDC UTILS] Full catalog has {len(datasets)} datasets")

        for dataset in datasets:
            dataset_id = dataset.get('@id') or dataset.get('id')
            if dataset_id == asset_id:
                print(f"[EDC UTILS] Found asset {asset_id} in full catalog")
                return dataset

        print(f"[EDC UTILS] Asset {asset_id} not found in catalog")
        return None

    except Exception as e:
        print(f"[EDC UTILS] Error fetching full catalog: {str(e)}")
        return None


def _fetch_policy_definition(policy_id: str, headers: Dict[str, str], edc_url: str) -> Optional[Dict[str, Any]]:
    """Fetch a policy definition by ID."""
    try:
        url = f"{edc_url}/management/v3/policydefinitions/{policy_id}"
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            policy_def = response.json()
            # Extract the actual policy
            policy = policy_def.get('policy', policy_def)
            policy['@id'] = policy_id
            return policy
    except Exception as e:
        print(f"[EDC UTILS] Error fetching policy {policy_id}: {str(e)}")
    return None


def fetch_catalog_entry_by_url(resource_url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch local asset that matches the given resource URL.

    Fetches all local assets and finds one whose baseUrl covers the resource.
    """
    print(f"[EDC UTILS] fetch_catalog_entry_by_url: {resource_url}")

    edc_url = get_edc_url()
    if not edc_url:
        return None

    headers = {
        'Content-Type': 'application/json',
    }

    edc_api_key = get_edc_api_key()
    if edc_api_key:
        headers['X-Api-Key'] = edc_api_key

    # Fetch all local assets using the assets query endpoint
    try:
        assets_url = f"{edc_url}/management/v3/assets/request"
        payload = {
            "@context": {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"},
            "@type": "QuerySpec"
        }
        response = requests.post(assets_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        assets = response.json()

        print(f"[EDC UTILS] Found {len(assets)} local assets")

        # Extract base URL from resource URL (remove trailing ID)
        parsed = urlparse(resource_url)
        path_parts = parsed.path.strip('/').split('/')
        if path_parts and path_parts[-1].isdigit():
            path_parts = path_parts[:-1]
        resource_base = f"{parsed.scheme}://{parsed.netloc}/{'/'.join(path_parts)}"
        print(f"[EDC UTILS] Resource base URL: {resource_base}")

        for asset in assets:
            # EDC v3 may use different field names for asset ID
            asset_id = (
                asset.get('@id') or
                asset.get('id') or
                asset.get('edc:id') or
                asset.get('https://w3id.org/edc/v0.0.1/ns/id') or
                'unknown'
            )
            print(f"[EDC UTILS] Checking asset: {asset_id}, keys: {list(asset.keys())}")

            # Skip index assets (they have 'index' in the name/id)
            if 'index' in asset_id.lower():
                print(f"[EDC UTILS] Skipping index asset: {asset_id}")
                continue

            # Check the asset's baseUrl from dataAddress
            data_address = asset.get('dataAddress', {}) or asset.get('edc:dataAddress', {})
            asset_base_url = (
                data_address.get('baseUrl') or
                data_address.get('edc:baseUrl') or
                data_address.get('baseurl') or
                ''
            )

            if asset_base_url:
                asset_base_stripped = asset_base_url.rstrip('/').rsplit('/index', 1)[0]
                print(f"[EDC UTILS] Checking asset {asset_id}: baseUrl={asset_base_stripped}")

                if resource_base.startswith(asset_base_stripped) or asset_base_stripped.startswith(resource_base):
                    print(f"[EDC UTILS] URL match found! Asset: {asset_id}")
                    # Build catalog entry with policies
                    return _build_catalog_entry_from_asset(asset, headers, edc_url)

        print(f"[EDC UTILS] No matching asset found for URL: {resource_url}")
        return None

    except Exception as e:
        print(f"[EDC UTILS] Error fetching assets by URL: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def extract_all_datasets_from_catalog(catalog: Any) -> List[Dict[str, Any]]:
    """Extract all datasets from a catalog response."""
    datasets = []

    if isinstance(catalog, list):
        for cat in catalog:
            datasets.extend(extract_all_datasets_from_catalog(cat))
    elif isinstance(catalog, dict):
        for ds in catalog.get('dcat:dataset', []):
            if ds.get('@type') == 'dcat:Catalog' and 'dcat:dataset' in ds:
                datasets.extend(extract_all_datasets_from_catalog(ds))
            else:
                datasets.append(ds)

    return datasets


def get_asset_base_url(asset_id: str) -> Optional[str]:
    """Fetch asset details and extract baseUrl from dataAddress."""
    edc_url = get_edc_url()
    if not edc_url:
        return None

    headers = {'Content-Type': 'application/json'}
    edc_api_key = get_edc_api_key()
    if edc_api_key:
        headers['X-Api-Key'] = edc_api_key

    try:
        asset_url = f"{edc_url}/management/v3/assets/{asset_id}"
        response = requests.get(asset_url, headers=headers, timeout=5)
        if response.status_code == 200:
            asset_data = response.json()
            data_address = asset_data.get('dataAddress', {}) or asset_data.get('edc:dataAddress', {})
            return (
                data_address.get('baseUrl') or
                data_address.get('edc:baseUrl') or
                data_address.get('baseurl') or
                ''
            )
    except Exception as e:
        logger.debug(f"Error fetching asset {asset_id}: {str(e)}")

    return None


def extract_dataset_from_catalog(catalog: Any, asset_id: str) -> Optional[Dict[str, Any]]:
    """
    Extract the dataset/asset from catalog response.

    Handles both flat and nested catalog structures.
    """
    # If catalog is a list, iterate through catalogs
    if isinstance(catalog, list):
        for cat in catalog:
            result = extract_dataset_from_catalog(cat, asset_id)
            if result:
                return result
        return None

    # If catalog is a dict, look for datasets
    if isinstance(catalog, dict):
        datasets = catalog.get('dcat:dataset', [])

        for dataset in datasets:
            # Check if this is the asset we're looking for
            dataset_id = dataset.get('id') or dataset.get('@id')
            if dataset_id == asset_id:
                return dataset

            # Check if this is a nested catalog
            if dataset.get('@type') == 'dcat:Catalog' and 'dcat:dataset' in dataset:
                inner_result = extract_dataset_from_catalog(dataset, asset_id)
                if inner_result:
                    return inner_result

    return None


def calculate_policy_openness(policy: Dict[str, Any]) -> float:
    """
    Calculate an "openness" score for a policy.

    Higher score = more open policy (fewer restrictions).

    Scoring:
    - Start with 100 points
    - -30 for each prohibition
    - -20 for each obligation
    - -10 for each constraint in permissions
    - -5 for each constraint in obligations

    Returns:
        float: Openness score (0-100, higher is more open)
    """
    score = 100.0

    # Check prohibitions
    prohibitions = policy.get('odrl:prohibition', [])
    if isinstance(prohibitions, dict):
        prohibitions = [prohibitions]
    score -= len(prohibitions) * 30

    # Check obligations
    obligations = policy.get('odrl:obligation', [])
    if isinstance(obligations, dict):
        obligations = [obligations]

    for obligation in obligations:
        score -= 20
        # Count constraints in obligations
        constraints = obligation.get('odrl:constraint', [])
        if isinstance(constraints, dict):
            constraints = [constraints]
        score -= len(constraints) * 5

    # Check permission constraints
    permissions = policy.get('odrl:permission', [])
    if isinstance(permissions, dict):
        permissions = [permissions]

    for permission in permissions:
        constraints = permission.get('odrl:constraint', [])
        if isinstance(constraints, dict):
            constraints = [constraints]
        score -= len(constraints) * 10

    return max(0, score)  # Never go below 0


def describe_policy(policy: Dict[str, Any]) -> str:
    """Generate human-readable policy description."""
    parts = []

    # Check prohibitions
    prohibitions = policy.get('odrl:prohibition', [])
    if prohibitions:
        if isinstance(prohibitions, dict):
            prohibitions = [prohibitions]
        parts.append(f"{len(prohibitions)} prohibition(s)")

    # Check obligations
    obligations = policy.get('odrl:obligation', [])
    if obligations:
        if isinstance(obligations, dict):
            obligations = [obligations]
        parts.append(f"{len(obligations)} obligation(s)")

    # Check permission constraints
    permissions = policy.get('odrl:permission', [])
    if permissions:
        if isinstance(permissions, dict):
            permissions = [permissions]

        constraint_count = sum(
            len(p.get('odrl:constraint', []) if isinstance(p.get('odrl:constraint', []), list) else [p.get('odrl:constraint')])
            for p in permissions if p.get('odrl:constraint')
        )
        if constraint_count > 0:
            parts.append(f"{constraint_count} constraint(s)")

    if not parts:
        return "Open access policy with no restrictions"

    return "Policy with " + ", ".join(parts)


def is_contract_valid(contract_data: Dict[str, Any]) -> bool:
    """
    Check if the contract agreement is valid (not expired, properly signed, etc.).

    Args:
        contract_data: The contract data from EDC API

    Returns:
        bool: True if the contract is valid
    """
    # Try different field names that EDC might use for state
    contract_state = (
        contract_data.get('state') or
        contract_data.get('edc:state') or
        contract_data.get('contractAgreement', {}).get('state') or
        contract_data.get('contractAgreement', {}).get('edc:state')
    )

    logger.info(f"Contract state found: {contract_state}")

    # If we can't find a state field, assume the contract exists and is valid
    # (the fact that we got it from the API means it exists)
    if contract_state is None:
        logger.warning("No state field found in contract data, assuming valid")
        return True

    # Check contract state - should be FINALIZED or VERIFIED
    valid_states = ['FINALIZED', 'VERIFIED', 'CONFIRMED', 'AGREED']
    if contract_state not in valid_states:
        logger.warning(f"Contract state '{contract_state}' is not in valid states: {valid_states}")
        return False

    return True


def is_resource_covered_by_contract(contract_data: Dict[str, Any], requested_url: str) -> bool:
    """
    Check if the requested resource URL is covered by the contract agreement.

    Args:
        contract_data: The contract data from EDC API
        requested_url: The URL being requested

    Returns:
        bool: True if the resource is covered by the contract
    """
    # Try different field names that EDC might use for asset ID
    asset_id = (
        contract_data.get('assetId') or
        contract_data.get('edc:assetId') or
        contract_data.get('@id') or
        contract_data.get('contractAgreement', {}).get('assetId') or
        ''
    )

    logger.info(f"Asset ID found: {asset_id}")
    logger.info(f"Requested URL: {requested_url}")

    # If no assetId, check policy.target as fallback
    if not asset_id:
        policy_target = (
            contract_data.get('policy', {}).get('target') or
            contract_data.get('edc:policy', {}).get('target') or
            contract_data.get('edc:policy', {}).get('edc:target')
        )
        if policy_target:
            logger.info(f"No assetId, using policy target: {policy_target}")
            asset_id = policy_target
        else:
            logger.warning("No assetId or policy target found in contract, denying access")
            return False

    # If asset_id looks like a URL (starts with http:// or https://), do direct matching
    if asset_id.startswith('http://') or asset_id.startswith('https://'):
        logger.info(f"Asset ID is a URL, doing direct matching")
        # Exact match
        if requested_url == asset_id:
            logger.info(f"Exact match: {requested_url} == {asset_id}")
            return True
        # Subresource match (remove /index suffix and check if it's a parent)
        asset_base = asset_id.rsplit('/index', 1)[0] if '/index' in asset_id else asset_id
        if requested_url.startswith(asset_base + '/'):
            logger.info(f"Subresource match: {requested_url} starts with {asset_base}/")
            return True
        logger.warning(f"URL mismatch. Asset: {asset_id}, Requested: {requested_url}")
        return False

    # Otherwise, asset_id is just an ID - need to fetch the asset details from EDC
    logger.info(f"Asset ID is not a URL, fetching asset details from EDC")

    edc_url = get_edc_url()
    if not edc_url:
        logger.error("EDC_URL not configured")
        return False

    asset_url = f"{edc_url}/management/v3/assets/{asset_id}"

    try:
        logger.info(f"Fetching asset from: {asset_url}")
        headers = {'Content-Type': 'application/json'}
        edc_api_key = get_edc_api_key()
        if edc_api_key:
            headers['X-Api-Key'] = edc_api_key

        asset_response = requests.get(asset_url, headers=headers, timeout=5)
        asset_response.raise_for_status()
        asset_data = asset_response.json()
        logger.info(f"Asset data: {asset_data}")

        # Extract dataAddress.baseUrl from the asset
        data_address = asset_data.get('dataAddress', {}) or asset_data.get('edc:dataAddress', {})
        base_url = (
            data_address.get('baseUrl') or
            data_address.get('edc:baseUrl') or
            data_address.get('baseurl') or
            data_address.get('edc:baseurl') or
            ''
        )

        logger.info(f"Base URL from asset: {base_url}")

        if not base_url:
            logger.warning("No baseUrl found in asset dataAddress, denying access")
            return False

        # Check if requested URL matches or is a subresource of base URL
        if requested_url == base_url:
            logger.info(f"Exact match with base URL")
            return True

        # Subresource match (remove /index suffix and check if it's a parent)
        base_url_stripped = base_url.rsplit('/index', 1)[0] if '/index' in base_url else base_url
        base_url_stripped = base_url_stripped.rstrip('/')
        print(f"[EDC UTILS]   - Base URL stripped: {base_url_stripped}")

        if requested_url.startswith(base_url_stripped + '/'):
            logger.info(f"Subresource match: {requested_url} starts with {base_url_stripped}/")
            return True

        logger.warning(f"Requested URL does not match base URL. Base: {base_url}, Requested: {requested_url}")
        return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching asset {asset_id}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking asset coverage: {str(e)}")
        return False
