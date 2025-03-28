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
- **Tools and Platforms:** Docker, SQLite, GitHub Actions
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
git clone <repository_url>

# Navigate to the project folder
cd <project_folder>

# Install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

Provide instructions or examples demonstrating how to run the project:

```bash
uvicorn main:app --reload
```

## Deployment

Describe steps and considerations for deploying the project to production or staging environments, including Docker deployment strategies.

## Project Structure

Outline the project’s file structure for clarity:

```
project
│─── app/
│    ├── routers/
│    ├── schemas/
│    └── models/
│─── tests/
│─── Dockerfile
│─── requirements.txt
└─── README.md
```

## Roadmap

- [ ] Barcode scanning for quick item addition
- [ ] Cloud synchronization and backup
- [ ] Notifications for important events (license renewals, maintenance)

## License

Specify the project's license here.

## Contributors

List key contributors or your contact information.

---

Feel free to add, remove, or modify sections as needed to better fit your project specifics.

