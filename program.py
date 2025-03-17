from src.helper_functions import (
    parse_lookup_table,
    parse_flow_log_records,
    generate_output_file,
)

TEST_CSV_FILE_PATH = "./lib/lookup_table.csv"
TEST_TXT_FILE_PATH = "./lib/sample_flow_log_records.txt"


def countTagAndPortProtocolCombinations(
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


def getFilePaths():
    csv_file_path = input("Enter relative file path to lookup table csv file: ")

    if not csv_file_path:
        print("⚠️ No csv file path entered")
        return

    txt_file_path = input("Enter relative file path to flow log records txt file: ")

    if not txt_file_path:
        print("⚠️ No txt file path entered")
        return

    countTagAndPortProtocolCombinations(csv_file_path, txt_file_path)


# TEST
# countTagAndPortProtocolCombinations(TEST_CSV_FILE_PATH, TEST_TXT_FILE_PATH)

getFilePaths()
