import click
import pandas as pd
import json
from pathlib import Path
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

@click.command()
@click.option('-i', '--input', required=True, type=click.Path(exists=True, path_type=Path), help="Input directory path")
@click.option('-o', '--output', required=True, type=click.Path(path_type=Path), help="Output directory path")
@click.option('-u', '--unix', is_flag=True, help="Keep timestamps in UNIX format")
def process_files(input: str, output: str, unix: bool) -> None:
    """
    Process JSON files in the input directory and save each as a CSV file in the output directory.
    Replace empty strings with a specified value and identify the most frequent non-NaN string value in a specific column.

    Args:
        input (str): The path to the directory containing the JSON files.
        output (str): The path to the directory where the CSV files will be saved.
        unix (bool): If set, keep timestamps in UNIX format; otherwise, convert to human-readable format.
    """
    print(unix)
    input_path = Path(input)
    output_path = Path(output)


    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Iterate over all JSON files in the input directory
    for json_file in input_path.glob('*.json'):
        with open(json_file, "r", encoding="UTF-8") as f:
            data_on_file = [json.loads(line) for line in f]

        # Convert JSON objects to a DataFrame
        df = pd.DataFrame(data_on_file)

        
        # Create the CSV file path
        csv_file = output_path / (json_file.stem + '.csv')
        # Check if the file already exists, and delete it if it does
        if csv_file.exists():
            csv_file.unlink()  # This deletes the file
        

        # Process data to match required columns
        df_processed = pd.DataFrame({
            'web_browser': df['a'].apply(lambda x: extract_browser_and_os(x)[0]).ffill(),
            'operating_sys': df['a'].apply(lambda x: extract_browser_and_os(x)[1]).ffill(),
            'from_url': df['r'].apply(shorten_url).ffill(),
            'to_url': df['u'].apply(shorten_url).ffill(),
            'city': df['cy'].ffill(),
            'longitude': df['ll'].apply(lambda x: x[1] if isinstance(x, list) and len(x) == 2 else None).ffill(),
            'latitude': df['ll'].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 2 else None).ffill(),
            'time_zone': df['tz'],
            'time_in': df['t'].apply(lambda x: convert_timestamp(x, unix)).ffill(),
            'time_out': df['hc'].apply(lambda x: convert_timestamp(x, unix)).ffill(),
        })

        # get the most valuse in time_zone 
        most_tz = df_processed['time_zone'].mode().iloc[0]
        # get the most city
        most_c = df_processed['city'].mode().iloc[0]

        df_processed["time_zone"] = df_processed["time_zone"].str.strip().replace(to_replace='', value=most_tz)
        df_processed["city"] = df_processed["city"].replace(to_replace='', value=most_c)
        # Save the DataFrame to a CSV file
        df_processed.to_csv(csv_file, index=False)
        click.echo(f"Processed file saved to {csv_file}")

if __name__ == "__main__":
    process_files()
