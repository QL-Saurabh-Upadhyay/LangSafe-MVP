# QL Tracker

A modern Python decorator for tracking function calls with rich logging capabilities and background event processing. The `@track` decorator provides detailed logging of function calls, including arguments, return values, exceptions, and execution time, with beautiful formatting using the `rich` library and automatic background processing of events.

## Features

- **Universal Decorator**: Works with both synchronous and asynchronous functions
- **Rich Logging**: Beautiful console output with syntax highlighting and panels
- **Comprehensive Tracking**: Logs function name, arguments, return values, exceptions, and execution time
- **Background Processing**: Automatic event queue processing with batch logging and storage
- **Configurable**: Easy configuration via `trackconfig.toml` file
- **File Logging**: Optional logging to file with plain text format
- **JSONL Storage**: Structured event storage in JSON Lines format
- **Thread-Safe**: Thread-safe event queue and background services
- **Type Hints**: Full type annotation support for better IDE integration
- **Modern Python**: Built with Python 3.8+ features and best practices

## Installation

### From Source

Clone the repository and install in development mode:

```bash
git clone <repository-url>
cd ql_tracker
pip install -e .
```

### Quick Setup for Collaboration

After cloning the repository, run the setup script for automatic configuration:

```bash
git clone <repository-url>
cd ql_tracker
python setup_collaboration.py
```

This will:
- Install all dependencies
- Create configuration files
- Test the installation
- Create example scripts

### Using pip (when published)

```bash
pip install ql_tracker
```

## Quick Start

```python
from ql_tracker import track, initialize

# Initialize services (required before using @track)
initialize()

@track
def add_numbers(a: int, b: int) -> int:
    return a + b

@track
async def async_multiply(x: float, y: float) -> float:
    import asyncio
    await asyncio.sleep(0.1)  # Simulate async work
    return x * y

# Use the functions
result = add_numbers(5, 3)
# Output: Beautiful rich panel showing function call details

# For async functions
import asyncio
async_result = await async_multiply(2.5, 4.0)
```

## Configuration

Create a `trackconfig.toml` file in your project root to customize the tracking behavior:

```toml
[tracker]
# Enable or disable logging entirely
enable_logging = true

# Enable pretty printing with rich formatting
pretty_print = true

# Log to file instead of console
log_to_file = false

# Path to log file (only used if log_to_file = true)
log_file_path = "tracker.log"

# Log level (INFO, DEBUG, WARNING, ERROR)
log_level = "INFO"

[queue]
# Maximum number of events to batch before flushing
max_batch_size = 10

# Time interval in seconds to flush events (even if batch is not full)
flush_interval_secs = 5

[storage]
# Storage backend type (jsonl, sqlite, etc.)
backend = "jsonl"

# Output path for storage files
output_path = "logs/ql-tracker.jsonl"
```

### Configuration Options

- **`enable_logging`**: Set to `false` to completely disable tracking
- **`pretty_print`**: Set to `false` for simple console output instead of rich panels
- **`log_to_file`**: Set to `true` to log to file instead of console
- **`log_file_path`**: Path to the log file (relative or absolute)
- **`log_level`**: Logging level (currently informational only)
- **`queue.max_batch_size`**: Maximum number of events to batch before flushing to storage
- **`queue.flush_interval_secs`**: Time interval in seconds to flush events to storage
- **`storage.backend`**: Storage backend type (currently supports "jsonl")
- **`storage.output_path`**: Path for storing events in JSONL format

## Usage Examples

### Basic Function Tracking

```python
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

# Call the function
result = calculate_fibonacci(5)
```

### Async Function Tracking

```python
import asyncio
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
async def fetch_data(url: str) -> dict:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Use in async context
async def main():
    data = await fetch_data("https://api.example.com/data")
    return data

# Run the async function
result = asyncio.run(main())
```

### Exception Handling

The decorator automatically tracks exceptions and provides detailed error information:

```python
@track
def divide_numbers(a: float, b: float) -> float:
    return a / b

# This will log the exception with full traceback
try:
    result = divide_numbers(10, 0)
except ZeroDivisionError:
    pass
```

## Background Processing

QL Tracker automatically processes events in the background using several services:

### Event Queue Service
- Thread-safe in-memory queue for storing function call events
- Events include function name, arguments, return values, exceptions, and timestamps
- Automatic batching and flushing to storage

### Storage Service
- Pluggable storage backends (currently JSONL)
- Structured event storage in JSON Lines format
- Configurable output paths

### Batch Logger Service
- Background service that monitors the event queue
- Flushes events based on batch size or time intervals
- Runs continuously in a background thread

### Background Executor Service
- Manages lifecycle of background services
- Ensures graceful shutdown on program exit
- Provides service statistics and monitoring

## Integration with Other Projects

### Adding to Existing Code

Simply import and apply the decorator to any function you want to track:

```python
from ql_tracker import track, initialize

# Initialize services first
initialize()

# Your existing function
def my_existing_function(param1, param2):
    # ... your code ...
    return result

# Add tracking
@track
def my_existing_function(param1, param2):
    # ... your code ...
    return result
```

### Monitoring Background Services

You can monitor the background services:

```python
from ql_tracker import get_stats, get_initializer

# Get service statistics
stats = get_stats()
print(f"Services running: {stats['running']}")
print(f"Total events processed: {stats['services'][0]['total_events_processed']}")

# Get initializer instance
initializer = get_initializer()
print(f"API key configured: {initializer.get_api_key() is not None}")
```

### Selective Tracking

You can enable/disable tracking globally by modifying the configuration:

```python
from ql_tracker import load_config, get_config

# Load custom configuration
load_config("my_trackconfig.toml")

# Check current configuration
config = get_config()
print(f"Logging enabled: {config.enable_logging}")
```

### Log File Output

When `log_to_file = true` is set, the decorator writes plain text logs to the specified file:

```
[2024-01-15 10:30:45.123] calculate_fibonacci(5)
Return: 5
Time: 0.0001s
--------------------------------------------------
[2024-01-15 10:30:45.124] divide_numbers(10, 0)
Exception: ZeroDivisionError: division by zero
Time: 0.0000s
--------------------------------------------------
```

## Project Structure

```
ql_tracker/
├── src/
│   └── ql_tracker/
│       ├── __init__.py
│       ├── config.py
│       ├── tracker.py
│       └── initialize.py
├── examples/
│   ├── example.py
│   ├── collaboration_example.py
│   └── initialization_example.py
├── setup_collaboration.py
├── COLLABORATION_SETUP.md
├── trackconfig.toml
├── pyproject.toml
└── README.md
```

## Dependencies

- **Python**: 3.8+
- **rich**: >=13.0.0 (for beautiful console output)
- **tomli**: >=2.0.0 (for Python < 3.11, for TOML parsing)

## Development

### Building the Package

```bash
# Install build dependencies
pip install hatch

# Build the package
hatch build
```

### Running Examples

```bash
# Run the basic example
python examples/example.py

# Run the collaboration setup example
python examples/collaboration_example.py

# Run the quick setup script
python setup_collaboration.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository. # demo_12
