# QL Tracker - Collaboration Setup Guide

This guide will help you set up and use the `@track` decorator when you clone this project from GitHub in your collaborative environment.

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ql_tracker
```

### 2. Install Dependencies

```bash
# Install the package in development mode
pip install -e .

# Or install dependencies manually
pip install rich tomli requests
```

### 3. Basic Usage

```python
from ql_tracker import track

@track
def my_function(a, b):
    return a + b

# Use the function
result = my_function(5, 3)
```

## 📋 Complete Setup Instructions

### Step 1: Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ql_tracker
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

### Step 2: Configuration

Create a `trackconfig.toml` file in your project root:

```toml
[tracker]
enable_logging = true
pretty_print = true
log_to_file = false
log_file_path = "logs/tracker.log"
log_level = "INFO"

[queue]
max_batch_size = 10
flush_interval_secs = 5

[storage]
backend = "jsonl"
output_path = "logs/ql-tracker.jsonl"
```

### Step 3: Initialize Services

Before using the `@track` decorator, initialize the services:

```python
from ql_tracker import initialize, track

# Initialize with your API key and host (optional)
initialize(
    api_key="your-api-key-here",
    host="https://api.example.com",
    config_path="trackconfig.toml"
)

@track
def your_function():
    # Your code here
    pass
```

## 🔧 Usage Examples

### Basic Function Tracking

```python
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    return sum(numbers)

# Use the function
result = calculate_sum([1, 2, 3, 4, 5])
print(f"Sum: {result}")
```

### Async Function Tracking

```python
import asyncio
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
async def fetch_data(url):
    """Fetch data from a URL."""
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

### Class Method Tracking

```python
from ql_tracker import track, initialize

# Initialize services
initialize()

class DataProcessor:
    @track
    def process_data(self, data):
        """Process data and return results."""
        return [item * 2 for item in data]
    
    @track
    async def async_process(self, data):
        """Process data asynchronously."""
        import asyncio
        await asyncio.sleep(0.1)
        return [item.upper() for item in data]

# Use the class
processor = DataProcessor()
result = processor.process_data([1, 2, 3])
```

### Error Handling

```python
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
def divide_numbers(a, b):
    """Divide two numbers (may raise an exception)."""
    return a / b

# This will log the exception
try:
    result = divide_numbers(10, 0)
except ZeroDivisionError as e:
    print(f"Caught error: {e}")
```

## 🛠️ Advanced Configuration

### Custom Configuration

```python
from ql_tracker import initialize, get_config, load_config

# Load custom configuration
load_config("my_custom_config.toml")

# Initialize with custom settings
initialize(
    api_key="your-api-key",
    host="https://your-api-host.com",
    config_path="my_custom_config.toml"
)

# Check configuration
config = get_config()
print(f"Logging enabled: {config.enable_logging}")
print(f"Pretty print: {config.pretty_print}")
```

### Service Monitoring

```python
from ql_tracker import get_stats, get_initializer

# Get service statistics
stats = get_stats()
print(f"Services running: {stats['running']}")
print(f"Total events processed: {stats['services'][0]['total_events_processed']}")

# Get initializer instance
initializer = get_initializer()
print(f"API key configured: {initializer.get_api_key() is not None}")
print(f"Host configured: {initializer.get_host()}")
```

### Graceful Shutdown

```python
from ql_tracker import shutdown

# At the end of your program
shutdown()
```

## 📁 Project Structure for Collaboration

```
your_project/
├── ql_tracker/          # Cloned repository
│   ├── src/
│   ├── examples/
│   ├── trackconfig.toml
│   └── README.md
├── your_code.py         # Your code using @track
├── requirements.txt      # Your project dependencies
└── logs/               # Generated logs
    └── ql-tracker.jsonl
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Error:**
   ```python
   # Make sure you're importing from the correct package
   from ql_tracker import track  # Correct
   # from trackdecorator import track  # Wrong (old import)
   ```

2. **Services not initialized:**
   ```python
   # Always initialize before using @track
   from ql_tracker import initialize, track
   
   initialize()  # Initialize first
   
   @track
   def my_function():
       pass
   ```

3. **Configuration not loaded:**
   ```python
   # Load configuration explicitly
   from ql_tracker import load_config, initialize
   
   load_config("trackconfig.toml")
   initialize()
   ```

### Debug Mode

```python
from ql_tracker import initialize, get_config

# Enable debug logging
initialize()
config = get_config()
config.enable_logging = True
config.log_level = "DEBUG"
```

## 📊 Monitoring and Logs

### View Logs

```bash
# Check the JSONL log file
tail -f logs/ql-tracker.jsonl

# Or use Python to read logs
import json
with open("logs/ql-tracker.jsonl", "r") as f:
    for line in f:
        event = json.loads(line)
        print(f"Function: {event['func_name']}, Time: {event['execution_time']}")
```

### Service Statistics

```python
from ql_tracker import get_stats

stats = get_stats()
print("Service Statistics:")
for service in stats['services']:
    print(f"- {service['type']}: running={service['running']}")
    if 'total_events_processed' in service:
        print(f"  Events processed: {service['total_events_processed']}")
```

## 🚀 Integration Examples

### Flask Application

```python
from flask import Flask
from ql_tracker import track, initialize

# Initialize services
initialize()

app = Flask(__name__)

@app.route('/api/calculate')
@track
def calculate_endpoint():
    """API endpoint with tracking."""
    return {"result": "calculated"}

if __name__ == '__main__':
    app.run()
```

### Django Application

```python
from django.http import JsonResponse
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
def my_django_view(request):
    """Django view with tracking."""
    return JsonResponse({"status": "success"})
```

### Jupyter Notebook

```python
# In a Jupyter notebook cell
from ql_tracker import track, initialize

# Initialize services
initialize()

@track
def analyze_data(data):
    """Analyze data in notebook."""
    return {"mean": sum(data) / len(data), "count": len(data)}

# Use in notebook
result = analyze_data([1, 2, 3, 4, 5])
print(result)
```

## 📝 Best Practices

1. **Always initialize services** before using `@track`
2. **Use virtual environments** to avoid dependency conflicts
3. **Configure logging appropriately** for your environment
4. **Monitor service statistics** in production
5. **Handle exceptions gracefully** - the decorator will log them
6. **Use meaningful function names** for better tracking
7. **Consider performance impact** in high-frequency functions

## 🆘 Getting Help

- Check the `examples/` directory for working examples
- Review the main `README.md` for detailed documentation
- Check the `logs/ql-tracker.jsonl` file for debugging information
- Use `get_stats()` to monitor service health

## 🔄 Updates and Maintenance

When the repository is updated:

```bash
# Pull latest changes
git pull origin main

# Reinstall if needed
pip install -e .
```

This setup guide should help you and your collaborators use the `@track` decorator effectively in your collaborative environment! 