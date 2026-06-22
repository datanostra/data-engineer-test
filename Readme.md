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

## Running the Project

Documentation will be completed as implementation progresses.