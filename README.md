# Cer2Cen Data Migration Tool

Cer2Cen is a Python-based tool designed for data migration between a local MariaDB database and a remote API. It transfers data in a structured sequence, ensuring that tables are migrated in the correct order while handling API authentication and communication seamlessly.

## Features

- **Automatic Data Migration**: Transfers data from local tables to a remote API, mapping database tables to API objects.
- **Configurable Settings**: Allows full edit mode through environment settings to reprocess all records.
- **Dependency-Aware Migration**: Migrates tables in a specific order to ensure data integrity across dependent tables.

## Installation

### System Requirements

- **Python 3.12+**
- **MariaDB**: The local database to connect to.
- **Debian-Based System**: Tested with Debian Bookworm.

### Dependencies

Install the following system dependencies on a Debian-based system:

```bash
sudo apt update
sudo apt install -y python3 python3-pip libmariadb3 libmariadb-dev
```

Install the Python dependencies using `poetry`:

```bash
pip install poetry
poetry install
```

## Configuration

Create a `.env` file with the following structure to set up the necessary environment variables:

```ini
# API Credentials
APP_USERNAME=vda
APP_PASSWORD=password

# Local Database Credentials
DB_USERNAME=db_user
DB_PASSWORD=db_user_pass
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=ARPA_VAL_V2

# Optional: Uncomment to enable full edit mode
# SETTING_EDIT=
```

Additionally, a `tables.json` file is required to map the local database tables to the corresponding API tables. Example:

```json
{
  "TBL_TIPO_TRATTA": "elf_tbl_tipo_tratta",
  "TBL_TIPO_TESTA_SOSTEGNO": "elf_tbl_tipo_testa_sostegno",
  "TBL_TIPO_BASE_SOSTEGNO": "elf_tbl_tipo_base_sostegno",
  "TBL_TIPO_SOSTEGNO": "elf_tbl_tipo_sostegno",
  "TBL_CONDUTTORI": "elf_tbl_conduttori",
  "TBL_SOGGETTI": "elf_tbl_soggetti",
  "TBL_TIPO_IMPIANTO": "elf_tbl_tipo_impianto",
  "TBL_IMPIANTI": "elf_tbl_impianti",
  "TBL_LINEE": "elf_tbl_linee",
  "TBL_PUNTI_SOSPENSIONE": "elf_tbl_punti_sospensione",
  "TBL_SOSTEGNI": "elf_tbl_sostegni",
  "TBL_TRONCHI": "elf_tbl_tronchi",
  "TBL_FASI": "elf_tbl_fasi",
  "TBL_SOST_AEREI": "elf_tbl_sost_aerei",
  "TBL_DENOM_SOSTEGNO": "elf_tbl_denom_sostegno",
  "TBL_TRATTE": "elf_tbl_tratte",
  "TBL_CORRENTI": "elf_tbl_correnti",
  "TBL_CAMPATE": "elf_tbl_campate"
}
```

## Running the Script

Once the environment is set up and dependencies are installed, you can run the migration tool using:

```bash
poetry run migrate
```

This will initiate the data migration process from the local database to the remote API.

## Docker (Optional)

For environments that require Docker, you can build and run the tool using the following commands:

```bash
docker build -t cer2cen .
docker run --env-file .env cer2cen
```

### Create container

```bash
docker run -d --name cer2cen --env-file .env cer2cen
```

### Start container from crontab

```bash
0 0 * * * docker start cer2cen
```

### Docker logs

```bash
docker logs cer2cen
```

## License

**Cer2Cen** is developed by [**Riccardo Bertelli**](mailto:riccardo@codetotime.com) and is distributed under the terms of the GNU General Public License v3 (GPLv3). For more information, please refer to the license file.
