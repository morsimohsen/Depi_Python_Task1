from datetime import datetime
import re

def convert_timestamp(timestamp: int, keep_unix: bool):
    """
    Convert a UNIX timestamp to a human-readable format or retain it in UNIX format.

    Args:
        timestamp (int): The UNIX timestamp to convert.
        keep_unix (bool): If True, retain the UNIX timestamp format; otherwise, convert to a human-readable format.

    Returns:
        str: The timestamp in the specified format.
    """
    if keep_unix:
        return timestamp
    else:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def shorten_url(url: str):
    """
    Convert a long URL into a short format by extracting the domain.

    Args:
        url (str): The full URL to shorten.

    Returns:
        str: The shortened URL containing only the domain.
    """
    match = re.search(r'^(?:https?:\/\/)?(?:www\.)?([^\/]+)', url)
    return match.group(1) if match else url

def extract_browser_and_os(user_agent: str):
    """
    Extract the web browser and operating system from the user agent string.

    Args:
        user_agent (str): The user agent string from which to extract browser and OS information.

    Returns:
        tuple: A tuple containing the web browser and operating system as strings.

    """
    # Extract web browser and operating system using regex
    browser_match = re.search(r'([^\s]+)\/[\d\.]+', user_agent)
    os_match = re.search(r'\(([^)]+)\)', user_agent)
    
    browser = browser_match.group(1) if browser_match else 'Unknown'
    operating_system = os_match.group(1) if os_match else 'Unknown'

    return browser, operating_system