# JSON to CSV Converter

This Python script processes JSON files and converts them into CSV files. The resulting CSV files are structured with specific columns, and the script allows for various options such as timestamp formatting, string replacement, and analyzing the most frequent values in a specified column.

## Features

- Converts JSON files to CSV format with predefined columns.
- Extracts web browser and operating system information from user agent strings.
- Shortens URLs by extracting the domain name.
- Converts UNIX timestamps to human-readable format (optional).
- Replaces empty string values with a user-specified value.
- Identifies the most frequent non-NaN value in a specified column.
- Automatically deletes existing CSV files if re-run with the same input.

## Requirements

- Python 3.x
- Required Python packages: `click`, `pandas`, `numpy`

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

   ```bash
   pip install click pandas
