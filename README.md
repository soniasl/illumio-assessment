# Illumio Coding Assessment

## Assumptions
- Only supports default log format, specifically version 2
- Lookup table is a CSV file
  - Description states "lookup table is defined as a csv file", but then the requirement details states "Input file as well as the file containing tag mappings are plain text (ascii) files"
  - Decided to follow instruction that was stated first
- When reading the flow log records file, flow logs with a logging status of `NODATA` or `SKIPDATA` have no data for the fields:
  - `srcaddr`
  - `dstaddr`
  - `scrport`
  - `dstport`
  - `protocol`
  - `packets`
  - `bytes`
- The lookup table only has 3 columns (dstport, protocol, and tag)

## Prerequistes to Run Program
- `python3`

## Instructions
1. Create a python virtual environment: `python3 -m venv venv`
2. Activate python virtual environment: `source venv/bin/activate`
3. Run `python3 program.py`

## Testing
To verify that the output of the program is correct, the contents of `output.txt` is compared to `expected_output.txt` using the python `filecmp` module.
1. Uncomment line 96 and 97
2. Comment out line 100
3. `python3 program.py`
