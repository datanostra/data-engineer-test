# Foodvisor - Data Engineer Technical Test

## Overview

This project implements a marketing data pipeline for processing AppLovin advertising performance data used by Foodvisor's marketing team.

It was developed as part of a technical assessment for a Data Engineer role, focusing on data ingestion, historical tracking, data curation, and analytical API development.

The objective is to:
- Ingest CSV produced by AppLovin API (d0, d7, d30)
- Maintain curated datasets containing the latest known values.
- Expose aggregated KPIs through a REST API.
- Demonstrate a production-oriented architecture suitable for AWS deployment.

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker Compose

## Project Structure
'''
foodvisor-data-engineer-test/
├── data/
|   ├── source/         # Input CSV files provided with the challenge
|   ├── raw_archive/    # Immutable copies of ingested files
├── app/
|   ├── models/
|   ├── services/
|   ├── api/
|   ├── commands/
├── foodvisor_ads/      # Django configuration
'''

## Development Setup

Create Virtual Environment
'''
python -m venv .venv
'''

Activate Environment (Windows)
'''
.venv\Scripts\activate
'''

Install Dependencies
'''
pip install -r requirements.txt
'''

Run Migrations
'''
python manage.py makemigrations
python manage.py migrate
'''

## Running the Project
Reset All Ingested Data
'''
python manage.py reset_data
'''
Deletes all ingestion metadata and raw performance records.

Ingest All Available Files
'''
python manage.py ingest_directory
'''
By default, files are loaded from:

../data/source

Ingest a Single File
'''
python manage.py ingest_file ../data/source/2022-06-01_day0_anon.csv
'''

## Idempotency

The pipeline computes a SHA-256 hash for each source file.

If a file with the same content has already been processed, ingestion is skipped automatically.

This guarantees that running the ingestion multiple times does not create duplicate records.

## Storage Layers
### FileIngestion

Stores ingestion metadata and lineage information.

### RawAdsRow

Stores the original AppLovin performance records exactly as received from the source files.

This layer is append-only and serves as the system of record for all ingested data.

# Author

Guillaume Blot

Data Engineer | Analytics | Data Products

This project was developed as part of a technical assessment for a Data Engineer position and demonstrates the implementation of a reproducible and auditable marketing data ingestion pipeline.

GitHub: https://github.com/datanostra