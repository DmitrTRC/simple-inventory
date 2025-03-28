# Inventory Handler App

## Overview

The Simple Inventory App is designed to help users effectively manage and track various personal items such as vehicles and weapons. The app aims to simplify inventory management, enhance organization, and provide quick access to inventory data for personal use.

## Features

### Vehicle Inventory Management
- **Model Information:** Track vehicle models and their year of issue.
- **Maintenance Tracking:** Record details about last maintenance, next scheduled maintenance, and replaced parts.
- **Replacement Scheduling:** Specify parts to be replaced, including replacement schedules.
- **Financial Tracking:** Keep track of purchase prices, maintenance costs, and overall vehicle expenses.

### Weapon Inventory Management
- **Licensing:** Manage and track weapon licenses and renewals.
- **Safety Checks:** Record and schedule regular safety inspections.
- **Storage Management:** Keep detailed records of storage locations and security measures.

## Accessibility Levels

The app supports multiple user roles with varying access levels:
- **Admin:** Full access, including deep system configuration and fine-tuning.
- **Master User:** Full access to all data but restricted from deep configuration settings.
- **Regular User:** Access to most data but restricted from sensitive financial information, such as purchase prices.

## Architecture Overview

The app will follow a client-server architecture, consisting of:

- **Client:**
  - **Telegram Bot:** Provides a conversational interface using AIOgram for asynchronous interaction.
  - **Console Interface:** Supports command-line interaction via ArgsParse, Click, or preferably Typer.
  - **Text-based User Interface (TUI):** Rich library to provide an enhanced visual experience in terminal.

- **Server:**
  - API-based backend using FastAPI for handling business logic, database operations, and authentication.
  - SQLite: Lightweight database solution for persistent storage.

## Technologies

List the main technologies used:
- **Programming Languages:** Python
- **Frameworks and Libraries:** FastAPI, AIOgram, Typer, Rich
- **Tools and Platforms:** Docker, SQLite, GitHub
- **Additional:** Pytest for testing, Poetry for dependency management

## Dependencies

Specify key dependencies, prerequisites, or services required:
- Docker: For containerization
- SQLite: Database
- FastAPI: API framework for backend development
- Telegram Bot API via AIOgram
- Rich: For enhanced terminal interface
- Typer: Preferred for command-line interactions

## Installation and Setup

Detailed steps to set up the project locally:

```bash
# Clone repository
git clone git@github.com:DmitrTRC/simple-inventory.git

# Navigate to the project folder
cd <project_folder>

# Install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

TBD

## Deployment

TBD

## Project Structure

Outline the project’s file structure for clarity:

```
## Project Structure
simple-inventory/
├── .3.11_simple_inventory/
├── SQL/
│   ├── create_todos_db.sql
│   └── create_users_db.sql
├── data/
│   └── users
├── Documentation/
│   ├── Meeting-1.MD
│   ├── Meeting-2.MD
│   ├── Meeting-3.MD
│   ├── Meeting_4.MD
│   ├── Meeting_5.MD
│   ├── Meeting_6.MD
│   ├── Project.MD
│   └── README.md
├── lazy_orm/
│   ├── __init__.py
│   └── db_manager.py
├── model/
│   ├── __init__.py
│   ├── todo_model.py
│   └── user_model.py
├── models/
├── service/
│   ├── __init__.py
│   ├── todo_srv.py
│   └── user_srv.py
├── telegram_bot/
│   ├── .env
│   ├── handlers.py
│   ├── keyboards.py
│   ├── run.py
│   └── simple_inventory.log
├── tests/
│   ├── test_data/
│   │   └── test_db_sqlite
│   ├── tests/
│   │   └── test_data/
│   │       └── test_db_sqlite
│   └── test_db_manager.py
├── utils/
│   ├── __init__.py
│   ├── email.py
│   ├── logging_simp_inv.py
├── .gitignore
├── dc_temp.py
├── inv_cli.py
├── main.py
├── requirements.txt
└── simple_inventory.log
```

## Roadmap

- [ ] Barcode scanning for quick item addition
- [ ] Cloud synchronization and backup
- [ ] Notifications for important events (license renewals, maintenance)

## License

TBD

## Contributors

Dmitry
alekslk 
ArinaMdm 
markea_bg