# acuity-cli

Python CLI for managing Acuity Scheduling appointments, clients, and availability.

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# Step 1: Get appointment types (ALWAYS FIRST)
acuity types list

# Step 2: Check availability
acuity availability dates --type 12345 --month 2025-01
acuity availability times --type 12345 --date 2025-01-15

# Step 3: Validate slot
acuity availability check --type 12345 --datetime "2025-01-15T14:00:00"

# Step 4: Book appointment
acuity appointments book --type 12345 --datetime "2025-01-15T14:00:00" \
  --first-name Jane --last-name Doe --email jane@example.com
```

## Configuration

Set credentials via environment variables or config file:

```bash
export ACUITY_USER_ID="your-user-id"
export ACUITY_API_KEY="your-api-key"
```

Or create `~/.config/acuity/config.json`:

```json
{
  "user_id": "your-user-id",
  "api_key": "your-api-key",
  "default_timezone": "America/Chicago",
  "output": "json"
}
```

## Development

```bash
# Type checking
mypy acuity_cli

# Linting & formatting
ruff check acuity_cli
ruff format acuity_cli

# Run tests
pytest
```
