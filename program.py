from src.helper_functions import (
    parse_lookup_table,
    parse_flow_log_records,
    generate_output_file,
)

TEST_CSV_FILE_PATH = "./lib/lookup_table.csv"
TEST_TXT_FILE_PATH = "./lib/sample_flow_log_records.txt"


def count_tag_and_port_protocol_combinations(
    lookup_table_file_path: str, flow_log_records_file_path: str
) -> None:
    """
    Creates a text file with tag and port/protocol combinations count by using
    the helper functions parse_look_table, parse_flow_log_records, and generate_output_file.
    Prints error messages if errors occur while extracting data.

    :params lookup_table_file_path: relative file path to file with lookup table data
    :params flow_log_records_file_name: relative file path to file with flow log records data
    :returns: None
    """
    try:
        lookup_table = parse_lookup_table(lookup_table_file_path)
    except IsADirectoryError:
        print("⚠️ Lookup table file path is a directory")
        return
    except FileNotFoundError:
        print("⚠️ No file found at lookup table file path")
        return
    except ValueError:
        print("⚠️ Lookup table file is not a CSV file")
        return
    except OSError:
        print("⚠️ Error occurred while reading lookup table file")
    except Exception:
        print("⚠️ Unexpected error occurred while parsing lookup table file")
        return

    if not lookup_table:
        print("⚠️ No or invalid lookup table data")
        return

    try:
        flow_log_records = parse_flow_log_records(flow_log_records_file_path)
    except IsADirectoryError:
        print("⚠️ Flow log records file path is a directory")
        return
    except FileNotFoundError:
        print("⚠️ No file found at flow log records file path")
        return
    except ValueError:
        print("⚠️ Flow log records file is not a CSV file")
        return
    except OSError:
        print("⚠️ Error occurred while reading flow log records file")
    except Exception:
        print("⚠️ Unexpected error occurred while parsing flow log records file")
        return

    if not flow_log_records:
        print("⚠️ No or invalid flow log records data")
        return

    generate_output_file(lookup_table, flow_log_records)
    print("✅ Created output.txt in program directory")


def get_file_paths():
    """
    Prompts the user for the relative file paths of the lookup table CSV file and flow log records text file.
    Uses user-entered file paths to call count_tag_and_port_protocol_combinations function.
    """
    csv_file_path = input("Enter relative file path to lookup table CSV file: ")

    if not csv_file_path:
        print("⚠️ No csv file path entered")
        return

    txt_file_path = input("Enter relative file path to flow log records text file: ")

    if not txt_file_path:
        print("⚠️ No txt file path entered")
        return

    count_tag_and_port_protocol_combinations(csv_file_path, txt_file_path)


# TESTING
# count_tag_and_port_protocol_combinations(TEST_CSV_FILE_PATH, TEST_TXT_FILE_PATH)

# FILE PATHS FROM USER
get_file_paths()
