# import khipu_tools

# khipu_tools.api_key = "your-secret-api-key"
# khipu_tools.log = "debug"
# banks = khipu_tools.Banks.getBanks()
# print(f"{banks = }")

# prediction = khipu_tools.Predict.get()
# print(f"{prediction = }")

import json
import os
import sys
import traceback
from collections import defaultdict

files = []
function_calls = defaultdict(lambda: defaultdict(int))


def trace_calls(frame, event, arg):
    if event == "call":
        # Get information about the function being called
        code = frame.f_code
        func_name = code.co_name
        file_name = code.co_filename

        allowed_directory = "/home/mariofix/proyectos/khipu-tools"

        # Only include files from the allowed directory
        if not file_name.startswith(allowed_directory):
            return

        if "site-packages" in file_name or "/usr/lib/python" in file_name:

            return

        # Print function name, file, and line number
        # print(f"Function: {func_name}, File: {file_name}, Line: {line_no}")
        function_calls[file_name][func_name] += 1

    return trace_calls


def main():
    import khipu_tools

    khipu_tools.api_key = "your-secret-api-key"
    khipu_tools.log = "debug"

    prediction = khipu_tools.Predict.get(
        payer_email="yo@mariofix.com",
        amount="500000",
        currency="CLP",
    )
    print(prediction)


def list_unused_files(tracked_files, project_directory):
    """
    Lists files in the project directory that were not used in the script.

    Args:
        tracked_files (list): List of file paths that were traced during execution.
        project_directory (str): Path to the root directory of the project.

    Returns:
        list: List of file paths that are in the project directory but were not used.
    """
    # Get all Python files in the project directory
    all_files = []
    for root, _, files in os.walk(project_directory):
        for file in files:
            if file.endswith(".py"):  # Only consider Python files
                all_files.append(os.path.join(root, file))

    # Normalize paths for comparison
    tracked_files_set = {os.path.normpath(file) for file in tracked_files}
    all_files_set = {os.path.normpath(file) for file in all_files}

    # Find unused files
    unused_files = all_files_set - tracked_files_set
    return sorted(unused_files)


if __name__ == "__main__":
    sys.settrace(trace_calls)  # Set the trace function
    try:
        main()  # Run your script
    except Exception:
        traceback.print_exc()
    finally:
        sys.settrace(None)  # Disable the trace function

        # Format the output as the required JSON structure
        output = []
        for file_name, functions in function_calls.items():
            modules = [
                {"function": func_name, "count": count}
                for func_name, count in functions.items()
            ]
            output.append({"file": file_name, "modules": modules})

        # Print the JSON string
        # print(json.dumps(output))

        project_directory = "/home/mariofix/proyectos/khipu-tools/khipu_tools"
        tracked_files = tracked_files = list(function_calls.keys())

        # Get unused files
        unused_files = list_unused_files(tracked_files, project_directory)

        print("Unused files:")
        for file in unused_files:
            print(file)
