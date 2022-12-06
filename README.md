# Historical data fixes

## Implementation steps

### Create and activate a virtual environment, e.g.

  - `python3 -m venv venv/`
  - `source venv/bin/activate`

### Environment variable settings

#### Data query - file locations

- DIT_DATA_FOLDER=STRING
- TGB_DATA_FOLDER=STRING
- CDS_DATA_FOLDER=STRING

### Environment variable settings

- Install necessary Python modules via `pip3 install -r requirements.txt`

---

## Usage - searching for data

### Searching in EU-provided Taric files

- `python3 query.py m 3643189 tgb` (searches for measure with SID 3643189 in EU files)
- `python3 query.py c 2933199070 tgb` (searches for commodity with code 2933199070 in EU files)
- `python3 query.py mt 750 tgb` (searches for measures of type 750 in EU files)
- `python3 query.py g AL tgb` (searches for measures on geo area AL in EU files)

### Searching in DIT-provided Taric files (UK tariff)

- `python3 query.py m 20138293 dit` (searches for measure with SID 20138293 in UK files)
- `python3 query.py c 2933199070 dit` (searches for commodity with code 2933199070 in UK files)
- `python3 query.py mt 750 dit` (searches for measures of type 750 in UK files)
- `python3 query.py g AL dit` (searches for measures on geo area AL in UK files)

### Searching in CDS-provided files (UK tariff)

- `python3 query.py m 20138293 cds` (searches for measure with SID 20138293 in UK files)

## Usage - linting raw data

- `python3 linter.py`

# Alternatively

`./q`