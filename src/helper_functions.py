from collections import defaultdict
from pathlib import Path
import csv


def parse_lookup_table(file_name: str) -> dict | None:
    """
    Parses CSV file with lookup table data

    :param file_name: string of relative file name
    :returns: lookup table dictionary with dstport as keys and tuple (protocol, tag) values or None if there is no valid data in the csv file
    :raises IsADirectoryError: raises exception when file_name is a directory
    :raises ValueError: raises exception if file is not in .csv format
    """
    LOOKUP_TABLE_HEADERS = {"dstport", "protocol", "tag"}
    LOOKUP_TABLE_NUM_COLS = 3

    if not Path(file_name).is_file():
        raise IsADirectoryError()

    if not Path(file_name).suffix == ".csv":
        raise ValueError("File must be in .csv format")

    file_stream = open(file_name)
    csv_reader = csv.reader(file_stream)

    lookup_table = {}

    for row in csv_reader:
        if set(row) == LOOKUP_TABLE_HEADERS or len(row) != LOOKUP_TABLE_NUM_COLS:
            continue

        dstport, protocol, tag = row
        lookup_table[dstport] = (protocol, tag.lower())

    return lookup_table if lookup_table else None


def parse_flow_log_records(file_name: str) -> dict | None:
    """
    Parses text file with flow log record data

    :param file_name: string of relative file name
    :returns: flow log record dictionary with
    :raises IsADirectoryError: raises exception if file_name points to a directory
    :raises ValueError: raises exception if file is not in .txt format
    """
    FLOW_LOG_RECORDS_NUM_COLS = 14
    DSTPORT_COL = 6
    LOG_STATUS_COL = 13

    if not Path(file_name).is_file():
        raise IsADirectoryError()

    if not Path(file_name).suffix == ".txt":
        raise ValueError("File must be in .txt format")

    file_stream = open(file_name)
    file_lines = file_stream.readlines()

    records = defaultdict(int)

    for line in file_lines:
        columns = line.strip("\n").split(" ")

        if len(columns) != FLOW_LOG_RECORDS_NUM_COLS:
            continue

        dstport = columns[DSTPORT_COL]
        log_status = columns[LOG_STATUS_COL]

        if log_status == "OK":
            records[dstport] += 1

    return records if records else None


def generate_output_file(lookup_table: dict, flow_log_records: dict) -> None:
    """
    Using a lookup table and flow log records, outputs a text file with the
    count of matches for each tag and the count of matches for each port/protocol
    combination

    :param lookup_table: dictionary created by the parse_lookup_table function
    :param flow_log_records: dictionary created by them parse_flow_log_records function
    :returns: None
    """
    tags = defaultdict(int)
    port_protocol_combinations = defaultdict(int)

    for port, count in flow_log_records.items():
        if port not in lookup_table:
            tags["Untagged"] += count
            continue

        protocol, tag = lookup_table[port]

        tags[tag] += count
        port_protocol_combinations[(port, protocol)] += count

    tags_output = ["Tags Count:\n", "Tag,Count\n"]

    for tag, count in tags.items():
        if tag != "Untagged":
            string = ",".join([tag, str(count)]) + "\n"
            tags_output.append(string)

    untagged_string = ",".join(["Untagged", str(tags["Untagged"])]) + "\n"
    tags_output.append(untagged_string)

    port_protocol_combinations_output = [
        "Port/Protocol Combinations Counts:\n",
        "Port,Protocol,Count\n",
    ]

    for combination, count in port_protocol_combinations.items():
        port, protocol = combination

        string = ",".join([port, protocol, str(count)]) + "\n"
        port_protocol_combinations_output.append(string)

    with open("../output.txt", "w") as output:
        output.writelines(tags_output)
        output.write("\n")
        output.writelines(port_protocol_combinations_output)
