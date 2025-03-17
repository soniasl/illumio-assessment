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
- The lookup table only has exactly 3 columns in the order dstport, protocol, and tag

## Prerequistes to Run Program
- `python3`

## Instructions
1. Create a python virtual environment with `python3 -m venv venv`
2. `python3 program.py`

## Testing
1. Uncomment line 90
2. Comment out line 93
3. `python3 program.py`
