from collections import defaultdict
from pathlib import Path
import csv


def parse_lookup_table(file_path: str) -> dict | None:
    """
    Parses CSV file with lookup table data, which has the columns dstport, protocol, and tag.

    :param file_path: relative file path to file with lookup table data

    :returns: lookup table dictionary with the different port names as keys and tuple (protocol, tag)
    as values or None if there is no valid data in the csv file; strings in tuple are uppercase

    :raises IsADirectoryError: raises exception if file path points to a directory
    :raises FileNotFoundError: raises exception if file at the given file path is not found
    :raises ValueError: raises exception if file is not a CSV file
    """
    LOOKUP_TABLE_HEADERS = {"DSTPORT", "PROTOCOL", "TAG"}
    LOOKUP_TABLE_NUM_COLS = 3

    if Path(file_path).is_dir():
        raise IsADirectoryError

    if not Path(file_path).is_file():
        raise FileNotFoundError

    if Path(file_path).suffix != ".csv":
        raise ValueError

    file_stream = open(file_path)
    csv_reader = csv.reader(file_stream)

    lookup_table = {}

    for row in csv_reader:
        row = [col.upper() for col in row]

        if set(row) == LOOKUP_TABLE_HEADERS or len(row) != LOOKUP_TABLE_NUM_COLS:
            continue

        dstport, protocol, tag = row
        lookup_table[dstport] = (protocol, tag)

    return lookup_table if lookup_table else None


def parse_flow_log_records(file_path: str) -> dict | None:
    """
    Parses text file with flow log record data.
    Only successfully parses flow log records in default format (version 2).

    :param file_path: relative file path to file with flow log records data

    :returns: flow log record dictionary with the different port names as keys and the
    count of matches for the port as values or None if there is no valid data in the text file;
    port names are uppercase strings

    :raises IsADirectoryError: raises exception if file path points to a directory
    :raises FileNotFoundError: raises exception if file at the given file path is not found
    :raises ValueError: raises exception if file is not a text file
    """
    FLOW_LOG_RECORDS_NUM_COLS = 14
    DSTPORT_COL = 6
    LOG_STATUS_COL = 13

    if Path(file_path).is_dir():
        raise IsADirectoryError

    if not Path(file_path).is_file():
        raise FileNotFoundError

    if not Path(file_path).suffix == ".txt":
        raise ValueError("File must be in .txt format")

    file_stream = open(file_path)
    file_lines = file_stream.readlines()

    records = defaultdict(int)

    for line in file_lines:
        columns = line.upper().strip("\n").split(" ")

        if len(columns) != FLOW_LOG_RECORDS_NUM_COLS:
            continue

        dstport = columns[DSTPORT_COL]
        log_status = columns[LOG_STATUS_COL]

        if log_status == "OK":
            records[dstport] += 1

    return records if records else None


def generate_output_file(lookup_table: dict, flow_log_records: dict) -> None:
    """
    Using a lookup table and flow log records, creates a text file with the
    count of matches for each tag and the count of matches for each port/protocol
    combination.

    :param lookup_table: dictionary created by the parse_lookup_table function
    :param flow_log_records: dictionary created by the parse_flow_log_records function

    :returns: None
    """
    NO_TAG = "UNTAGGED"

    tags = defaultdict(int)
    port_protocol_combinations = defaultdict(int)

    for port, count in flow_log_records.items():
        if port not in lookup_table:
            tags[NO_TAG] += count
            continue

        protocol, tag = lookup_table[port]

        tags[tag] += count
        port_protocol_combinations[(port, protocol)] += count

    tags_output = ["Tags Count:\n", "Tag,Count\n"]

    for tag, count in tags.items():
        if tag != NO_TAG:
            string = f"{tag},{str(count)}\n"
            tags_output.append(string)

    untagged_string = f"{NO_TAG},{str(tags[NO_TAG])}\n"
    tags_output.append(untagged_string)

    port_protocol_combinations_output = [
        "Port/Protocol Combinations Counts:\n",
        "Port,Protocol,Count\n",
    ]

    for combination, count in port_protocol_combinations.items():
        port, protocol = combination

        string = f"{port},{protocol},{str(count)}\n"
        port_protocol_combinations_output.append(string)

    with open("./output.txt", "w") as output:
        output.writelines(tags_output)
        output.write("\n")
        output.writelines(port_protocol_combinations_output)
