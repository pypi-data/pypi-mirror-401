# MM (Micro Model) Template

This template provides the standard directory structure for building a **Micro Model (MM)** compliant with the LIM architecture.

## Directory Structure

```text
.
├── meta.json           # [REQUIRED] Project metadata and service configuration
├── mms/                # Source code for the Micro Model Service
│   ├── app/            # Application logic (agents, api, blueprints)
│   └── tests/          # Unit and integration tests
├── models/             # Storage for trained model artifacts
│   └── default/        # Default model location
├── data/               # Local datasets or persistent storage
├── run/                # Execution and deployment scripts
│   ├── start.py        # Service entry point
│   └── docker/         # Docker configuration (Dockerfile, compose)
└── requirements.txt    # Python dependencies
```

## Key Components

### 1. `meta.json`
The manifest file that defines your Micro Model. It includes:
- **Identity**: Name, version, description.
- **Interface**: Input/Output specifications.
- **LIM Integration**: Registration details for the Large Intelligent Model (LIM) system.

### 2. `mms/` (Micro Model Service)
Place your core application logic here.
- `app/`: Recommended structure for your business logic, API handlers, and agents.
- `tests/`: Place to write tests for your service.

### 3. `models/`
Use this directory to store your model files (weights, serialized objects, etc.). The `mm pull` command uses this target to download models.

### 4. `run/`
Contains scripts to run and build your service.
- `start.py`: The local entry point. Customize this to bootstrap your specific framework (Quart, FastAPI, Flask, etc.).
- `docker/`: Contains `Dockerfile` and `docker-compose.yml` for containerization via `mm build`.

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Locally**:
   ```bash
   mm run
   # OR directly:
   python run/start.py
   ```

3. **Validate Metadata**:
   ```bash
   mm validate
   ```
