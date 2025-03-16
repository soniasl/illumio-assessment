from helper_functions import (
    parse_lookup_table,
    parse_flow_log_records,
    generate_output_file,
)

csv_file_name = "../lib/lookup-table.csv"
flow_log_records_file_name = "../lib/sample-flow-logs-v2.txt"


def runProgram(csv_file_name: str, flow_log_records_file_name: str) -> None:
    try:
        lookup_table = parse_lookup_table(csv_file_name)
    except:
        print("No values parsed from lookup table")
        return

    try:
        flow_log_records = parse_flow_log_records(flow_log_records_file_name)

    except:
        print("No valid flow log records")
        return

    generate_output_file(lookup_table, flow_log_records)
    print("Created output.txt file in project directory")


runProgram(csv_file_name, flow_log_records_file_name)
