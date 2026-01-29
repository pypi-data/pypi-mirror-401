"""
Koob-resume: A Python application to create a pdf resume.

Author: Philip Brown
Email: philip@koob.foo
"""

import argparse
import json
import os
import sys

from .resume import Resume


def get_output_filename(data, default="resume.pdf"):
    """
    Calculate the output filename based on applicant name and target role.

    Args:
    ----
        data (dict): The applicant data dictionary.
        default (str): The default filename if data is missing.

    Returns:
    -------
        str: The sanitized output filename (e.g., Name_Role.pdf).

    """
    try:
        p_info = data.get("p_info", {})
        name = p_info.get("name", "")

        # Use job_target['role'] (schema defaults)
        title = data.get("job_target", {}).get("role", "")

        if name and title:
            raw_name = f"{name}_{title}"
            return f"{raw_name.replace(' ', '_')}.pdf"
    except Exception:
        pass

    return default


def cli_runner(args=None):
    """
    Handle argument parsing, data loading (I/O), and document object instantiation.

    Args:
    ----
        args (list, optional): List of command line arguments. Defaults to None.

    """
    parser = argparse.ArgumentParser(
        description="Generate professional resume from a JSON data source."
    )
    parser.add_argument(
        "json_file",
        type=str,
        help="Path to the JSON file containing all applicant data.",
    )

    parsed_args = parser.parse_args(args)
    file_path = parsed_args.json_file

    if not os.path.exists(file_path):
        print(f"Error: Data file not found at '{file_path}'.")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            applicant_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Couldn't decode JSON from '{file_path}'. Check syntax.")
        sys.exit(1)

    try:
        document_object = Resume(data=applicant_data)

        output_file = get_output_filename(applicant_data)

        document_object.render(output_path=output_file)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
