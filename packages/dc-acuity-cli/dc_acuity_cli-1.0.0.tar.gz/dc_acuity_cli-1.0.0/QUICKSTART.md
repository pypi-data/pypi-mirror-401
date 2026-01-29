# Acuity CLI - Quick Start

Get up and running in 5 minutes.

## 1. Install

Requires Python 3.10 or higher.

```bash
pip install -e .
```

Verify installation:

```bash
acuity --version
```

## 2. Configure Credentials

Get your credentials from [Acuity Scheduling API settings](https://secure.acuityscheduling.com/app.php?key=api).

### Option A: Environment Variables (Recommended)

```bash
export ACUITY_USER_ID="your-user-id"
export ACUITY_API_KEY="your-api-key"
```

### Option B: Config File

Create `~/.config/acuity/config.json`:

```json
{
  "user_id": "your-user-id",
  "api_key": "your-api-key"
}
```

## 3. First Commands

### List appointment types (REQUIRED FIRST STEP)

You'll need the appointment type ID for booking:

```bash
acuity types list
```

This shows all available appointment types with their IDs.

### Check availability for next month

Replace `12345` with an actual type ID from the previous command:

```bash
acuity availability dates --type 12345 --month 2025-02
```

### See available time slots for a specific date

```bash
acuity availability times --type 12345 --date 2025-02-15
```

### Book an appointment

```bash
acuity appointments book \
  --type 12345 \
  --datetime "2025-02-15T10:00:00" \
  --first-name "John" \
  --last-name "Doe" \
  --email "john@example.com"
```

## Common Workflows

### Check upcoming appointments

```bash
acuity appointments list --min-date 2025-02-01
```

### Cancel an appointment

```bash
acuity appointments cancel 98765
```

### Search for a client

```bash
acuity clients list --search "john"
```

## Output Formats

Change output format with the `-o` flag:

```bash
# JSON (default, best for automation)
acuity types list -o json

# Human-readable table
acuity types list -o text

# Markdown table
acuity types list -o markdown
```

## Recommended Booking Flow

1. **Get appointment type ID**: `acuity types list`
2. **Find available dates**: `acuity availability dates --type ID --month YYYY-MM`
3. **Check time slots**: `acuity availability times --type ID --date YYYY-MM-DD`
4. **Validate slot** (optional): `acuity availability check --type ID --datetime "..."`
5. **Book**: `acuity appointments book --type ID --datetime "..." --first-name ... --last-name ... --email ...`

## Environment Variables Reference

```bash
export ACUITY_USER_ID="..."          # Required: Your Acuity user ID
export ACUITY_API_KEY="..."          # Required: Your Acuity API key
export ACUITY_TIMEZONE="..."         # Optional: Default timezone (default: America/Chicago)
export ACUITY_OUTPUT="json"          # Optional: Default output format (json|text|markdown)
```

## Next Steps

- See [README.md](./README.md) for complete command reference
- Check exit codes in README for automation integration
- Explore calendar filtering with `--calendar` option
- Use `--help` on any command for detailed options:
  ```bash
  acuity appointments book --help
  ```

## Troubleshooting

**Authentication failed (exit code 3)**

- Verify your `ACUITY_USER_ID` and `ACUITY_API_KEY` are correct
- Check credentials at https://secure.acuityscheduling.com/app.php?key=api

**Slot unavailable (exit code 5)**

- The time slot may have been booked by someone else
- Run `acuity availability check` before booking to validate

**Configuration error (exit code 2)**

- Ensure environment variables are exported or config file exists
- Verify JSON syntax if using config file

## License

MIT
