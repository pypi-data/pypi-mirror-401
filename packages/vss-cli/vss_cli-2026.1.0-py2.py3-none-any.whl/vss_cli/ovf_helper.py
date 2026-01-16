"""OVF/OVA parsing helpers used by VSS CLI (vss-cli)."""
import json
import logging
import tarfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import xmltodict

from vss_cli.exceptions import VssCliError

_LOGGING = logging.getLogger(__name__)


def get_namespaced_value(data: Dict, key: str, prefix: str = 'ovf') -> Any:
    """Get value from dict, trying namespaced key first then plain key.

    This abstracts the dual-key pattern commonly found in OVF XML where
    elements may appear as either 'ovf:ElementName' or 'ElementName'.

    Args:
        data: Dictionary to search in
        key: The key name without namespace prefix
        prefix: The namespace prefix to try first (default: 'ovf')

    Returns:
        The value if found, None otherwise
    """
    if data is None:
        return None

    namespaced_key = f'{prefix}:{key}'
    if namespaced_key in data:
        return data[namespaced_key]
    if key in data:
        return data[key]
    return None


def extract_ovf_content(file_path: Union[Path, str]) -> str:
    """Extract OVF content from file or archive.

    Handles different file formats:
    - .ovf: Read text content directly
    - .ova, .zip, .tar: Extract OVF member from archive

    Args:
        file_path: Path to the OVF file or archive containing OVF

    Returns:
        OVF content as string

    Raises:
        VssCliError: If file format is invalid or OVF cannot be extracted
    """
    file = Path(file_path)
    suffix = file.suffix.lower()

    if suffix == '.ovf':
        return file.read_text()

    if suffix in ['.ova', '.zip', '.tar']:
        return _extract_ovf_from_archive(file)

    raise VssCliError('Invalid OVA/OVF format.')


def _extract_ovf_from_archive(file: Path) -> str:
    """Extract OVF content from a tar-based archive.

    Args:
        file: Path to the archive file

    Returns:
        OVF content as string
    """
    tar = tarfile.open(str(file))
    ovf_members = [m for m in tar.getmembers() if '.ovf' in m.name.lower()]

    if ovf_members:
        f = tar.extractfile(ovf_members[0])
        ovf_str = f.read()
        tar.close()
        return ovf_str

    tar.close()
    return ''


def parse_ovf_strings(ovf_dict: Dict) -> Dict:
    """Parse OVF strings section for message ID lookups.

    Extracts the Strings/ovf:Strings section from the OVF envelope and
    builds a lookup dictionary mapping message IDs to their text values.
    This is used by other parsers to resolve @ovf:msgid references.

    Args:
        ovf_dict: The OVF envelope dictionary (Envelope/ovf:Envelope content)

    Returns:
        Dictionary mapping @ovf:msgid values to #text values.
        Returns empty dict if no strings section exists.
    """
    ovf_strings = {}
    strings_section = get_namespaced_value(ovf_dict, 'Strings')

    if not strings_section:
        return ovf_strings

    msgs = strings_section.get('Msg', [])
    for msg in msgs:
        msg_id = msg.get('@ovf:msgid')
        msg_text = msg.get('#text')
        ovf_strings[msg_id] = msg_text

    return ovf_strings


def parse_references(ovf_dict: Dict) -> List[Dict]:
    """Parse OVF references section for file information.

    Extracts file references from the References/ovf:References section.
    Each file entry contains href, id, and size attributes.

    Args:
        ovf_dict: The OVF envelope dictionary (Envelope/ovf:Envelope content)

    Returns:
        List of file dictionaries with keys: href, id, size.
        Returns empty list if no references section exists.
    """
    references_section = get_namespaced_value(ovf_dict, 'References')

    if not references_section:
        return []

    files_ref = get_namespaced_value(references_section, 'File')

    if not files_ref:
        return []

    # Normalize to list - handle both single dict and list inputs
    if isinstance(files_ref, dict):
        files_ref = [files_ref]

    files = [
        {
            'href': x.get('@ovf:href'),
            'id': x.get('@ovf:id'),
            'size': x.get('@ovf:size'),
        }
        for x in files_ref
    ]

    return files


def parse_disk_section(ovf_dict: Dict) -> List[Dict]:
    """Parse OVF disk section for disk information.

    Extracts disk information from the DiskSection/ovf:DiskSection section.
    Each disk entry contains capacity, allocation units, disk ID, and file ref.

    Args:
        ovf_dict: The OVF envelope dictionary (Envelope/ovf:Envelope content)

    Returns:
        List of disk dictionaries with keys: capacity, capacityAllocationUnits,
        diskId, fileRef.
        Returns empty list if no disk section exists.
    """
    disk_section = get_namespaced_value(ovf_dict, 'DiskSection')

    if not disk_section:
        return []

    disks_ref = get_namespaced_value(disk_section, 'Disk')
    _LOGGING.debug(f'Found Disks: {disks_ref}: type: {type(disks_ref)}')

    if not disks_ref:
        return []

    # Normalize to list - handle both single dict and list inputs
    if isinstance(disks_ref, dict):
        disks_ref = [disks_ref]

    disks = [
        {
            'capacity': x.get('@ovf:capacity'),
            'capacityAllocationUnits': x.get('@ovf:capacityAllocationUnits'),
            'diskId': x.get('@ovf:diskId'),
            'fileRef': x.get('@ovf:fileRef'),
        }
        for x in disks_ref
    ]

    return disks


def parse_network_section(ovf_dict: Dict) -> List[Dict]:
    """Parse OVF network section for network information.

    Extracts network information from the NetworkSection/ovf:NetworkSection
    section. Each network entry contains name and description.

    Args:
        ovf_dict: The OVF envelope dictionary (Envelope/ovf:Envelope content)

    Returns:
        List of network dictionaries with keys: name, description.
        Returns empty list if no network section exists.
    """
    network_section = get_namespaced_value(ovf_dict, 'NetworkSection')

    if not network_section:
        return []

    nets = get_namespaced_value(network_section, 'Network')
    _LOGGING.debug(f'Found Networks: {nets}: type: {type(nets)}')

    if not nets:
        return []

    # Normalize to list - handle both single dict and list inputs
    if isinstance(nets, dict):
        nets = [nets]

    networks = [
        {
            'name': x.get('@ovf:name'),
            'description': get_namespaced_value(x, 'Description'),
        }
        for x in nets
    ]

    return networks


def _resolve_msgid(value: Any, ovf_strings: Dict) -> Optional[str]:
    """Resolve a value that may contain an @ovf:msgid reference.

    If the value is a dict with @ovf:msgid or msgid key, looks up
    the corresponding text in ovf_strings. Otherwise returns the
    value as-is (or None if value is a dict without msgid).

    Args:
        value: The value to resolve (string or dict with msgid)
        ovf_strings: Dictionary mapping msgid to text values

    Returns:
        Resolved string value or None
    """
    if value is None:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        msgid = value.get('@ovf:msgid') or value.get('msgid')
        if msgid:
            return ovf_strings.get(msgid)
        return None

    return None


def parse_deployment_options(ovf_dict: Dict, ovf_strings: Dict) -> List[Dict]:
    """Parse OVF deployment options section for configuration parameters.

    Extracts deployment configuration options from the
    DeploymentOptionSection/ovf:DeploymentOptionSection section.
    Each configuration item contains id, description, and label.

    Description and label values may be either direct strings or dicts
    containing @ovf:msgid references that need to be resolved from
    ovf_strings.

    Args:
        ovf_dict: The OVF envelope dictionary (Envelope/ovf:Envelope content)
        ovf_strings: Dictionary mapping @ovf:msgid to text values

    Returns:
        List of deployment option dictionaries with keys:
        id, description, label.
        Returns empty list if no deployment options section exists.
    """
    deploy_section = get_namespaced_value(ovf_dict, 'DeploymentOptionSection')

    if not deploy_section:
        return []

    config_items = get_namespaced_value(deploy_section, 'Configuration')

    if not config_items:
        return []

    # Normalize to list - handle both single dict and list inputs
    if isinstance(config_items, dict):
        config_items = [config_items]

    dparams = []
    for item in config_items:
        raw_desc = get_namespaced_value(item, 'Description')
        raw_label = get_namespaced_value(item, 'Label')

        description = _resolve_msgid(raw_desc, ovf_strings)
        label = _resolve_msgid(raw_label, ovf_strings) or ''

        obj = {
            'id': item.get('@ovf:id'),
            'description': description,
            'label': label,
        }
        dparams.append(obj)

    return dparams


def _extract_property_description(prop: Dict) -> Optional[str]:
    """Extract description from a property element.

    Checks multiple possible sources for the description value:
    Description, ovf:Description, Label, ovf:Label.

    Args:
        prop: Property dictionary from OVF

    Returns:
        Description string or None if not found
    """
    description = get_namespaced_value(prop, 'Description')
    if description is not None:
        return description

    return get_namespaced_value(prop, 'Label')


def _parse_user_configurable_properties(properties: List[Dict]) -> List[Dict]:
    """Parse user-configurable properties from a list of property elements.

    Filters properties to only those with @ovf:userConfigurable == 'true'
    and extracts key, type, description, and default values.

    Args:
        properties: List of property dictionaries from OVF

    Returns:
        List of user-configurable property dictionaries with keys:
        key, type, description, default
    """
    pparams = []
    for prop in properties:
        if prop.get('@ovf:userConfigurable', None) != 'true':
            continue

        param = {
            'key': prop.get('@ovf:key'),
            'type': prop.get('@ovf:type'),
            'description': _extract_property_description(prop),
            'default': prop.get('@ovf:value'),
        }
        pparams.append(param)

    return pparams


def _extract_properties_from_product_section(
    prod_sect: Any, prod_props: List[Dict]
) -> List[Dict]:
    """Extract properties from ProductSection, handling list or dict format.

    Args:
        prod_sect: ProductSection content (can be list, dict, or None)
        prod_props: Already collected properties from list iteration

    Returns:
        List of property dictionaries to process
    """
    if prod_props:
        return prod_props

    if isinstance(prod_sect, dict):
        props = get_namespaced_value(prod_sect, 'Property')
        if props is not None:
            if isinstance(props, dict):
                return [props]
            return props

    return []


def parse_virtual_system(value: Dict, ovf_strings: Dict) -> Dict:
    """Parse OVF VirtualSystem section for VM metadata and properties.

    Extracts virtual system information including name, product info,
    vendor, and user-configurable property parameters.

    Handles ProductSection in both list and dict formats:
    - List: Iterates items to find Product, Vendor, and Property elements
    - Dict: Extracts Product (or ovf:FullVersion), Version (or ovf:Version)

    Args:
        value: The VirtualSystem dictionary from OVF
        ovf_strings: Dictionary mapping @ovf:msgid to text values
            (unused but kept for API consistency)

    Returns:
        Dictionary with keys: Name, Product, Version, Vendor, PropertyParams
        Keys are only present if corresponding data exists in OVF
    """
    output = {}

    # Extract Name
    output['Name'] = get_namespaced_value(value, 'Name')

    # Extract ProductSection
    prod_sect = get_namespaced_value(value, 'ProductSection')
    if prod_sect is None:
        return output

    prod_props = []

    if isinstance(prod_sect, list):
        output.update(_parse_product_section_list(prod_sect, prod_props))
    elif isinstance(prod_sect, dict):
        output.update(_parse_product_section_dict(prod_sect))

    # Extract PropertyParams from list-collected props or dict section
    properties = _extract_properties_from_product_section(
        prod_sect, prod_props
    )
    if properties:
        pparams = _parse_user_configurable_properties(properties)
        if pparams:
            output['PropertyParams'] = pparams

    return output


def _parse_product_section_list(
    prod_sect: List[Dict], prod_props: List[Dict]
) -> Dict:
    """Parse ProductSection when it is a list of items.

    Args:
        prod_sect: List of ProductSection items
        prod_props: List to accumulate Property elements (modified in place)

    Returns:
        Dictionary with Product and Vendor if found
    """
    result = {}
    for item in prod_sect:
        if 'Product' in item:
            result['Product'] = item.get('Product')
        if 'Vendor' in item:
            result['Vendor'] = item.get('Vendor')
        if 'Property' in item:
            props = item.get('Property', [])
            if isinstance(props, dict):
                prod_props.append(props)
            elif isinstance(props, list):
                prod_props.extend(props)

    return result


def _parse_product_section_dict(prod_sect: Dict) -> Dict:
    """Parse ProductSection when it is a dictionary.

    Args:
        prod_sect: ProductSection dictionary

    Returns:
        Dictionary with Product and Version if found
    """
    result = {}
    product = prod_sect.get('Product') or prod_sect.get('ovf:FullVersion')
    if product is not None:
        result['Product'] = product

    version = prod_sect.get('Version') or prod_sect.get('ovf:Version')
    if version is not None:
        result['Version'] = version

    return result


def parse_ovf(file_path: Union[Path, str]) -> Dict:
    """Parse OVA or OVF file and extract VM deployment information.

    This is the main orchestrator function that coordinates the parsing
    of all OVF sections. It extracts file content, parses XML, and
    delegates to specialized section parsers.

    Args:
        file_path: Path to the OVF file or OVA/TAR/ZIP archive

    Returns:
        Dictionary with the following possible keys:
        - Files: List of file references (href, id, size)
        - Disks: List of disk info (capacity, capacityAllocationUnits,
                 diskId, fileRef)
        - Networks: List of network info (name, description)
        - DeploymentOptionParams: List of deployment options (id,
                                   description, label)
        - Name: Virtual system name
        - Product: Product name or version
        - Version: Product version
        - Vendor: Vendor name
        - PropertyParams: List of user-configurable properties (key, type,
                          description, default)

    Raises:
        VssCliError: If file format is invalid or OVF structure is malformed
    """
    # Extract OVF content from file or archive
    ovf_str = extract_ovf_content(file_path)

    # Parse XML and convert to dict via JSON round-trip
    xpars = xmltodict.parse(ovf_str)
    data = json.dumps(xpars)
    data_dict = json.loads(data)
    _LOGGING.debug(f'Parsed OVF and found keys: {data_dict.keys()}')

    # Validate envelope exists
    if 'Envelope' not in data_dict and 'ovf:Envelope' not in data_dict:
        raise VssCliError('Invalid OVF format: missing ovf:Envelope')

    ovf_dict = data_dict.get('Envelope') or data_dict.get('ovf:Envelope')
    output = {}

    # Build strings lookup for msgid resolution
    ovf_strings = parse_ovf_strings(ovf_dict)

    # Parse each section and add to output
    files = parse_references(ovf_dict)
    if files:
        output['Files'] = files

    disks = parse_disk_section(ovf_dict)
    if disks:
        output['Disks'] = disks

    networks = parse_network_section(ovf_dict)
    if networks:
        output['Networks'] = networks

    dparams = parse_deployment_options(ovf_dict, ovf_strings)
    if dparams:
        output['DeploymentOptionParams'] = dparams

    # Parse VirtualSystem section
    virtual_system = get_namespaced_value(ovf_dict, 'VirtualSystem')
    if virtual_system:
        vs_output = parse_virtual_system(virtual_system, ovf_strings)
        output.update(vs_output)

    return output
