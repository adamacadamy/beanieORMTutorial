````markdown
# Python Logging: A Beginner's Guide

This guide covers everything you need to know to get started with Python's built-in logging module, including a class-based Pydantic-style configuration for easy reuse.

---

## 1. Why Use Logging?

- **Visibility into your code’s behavior.** Unlike `print()`, logging lets you control which messages appear and when.
- **Different severity levels.** You can emit detailed debug messages during development and suppress them in production.
- **Flexible destinations.** Send logs to the console, files, remote servers, or rotate them automatically.

---

## 2. Log Levels

| Level     | Numeric Value | When to Use                         |
|-----------|---------------|-------------------------------------|
| `DEBUG`   | 10            | Detailed diagnostic information     |
| `INFO`    | 20            | Routine events (startup, shutdown)  |
| `WARNING` | 30            | Unexpected situations, non-fatal    |
| `ERROR`   | 40            | Serious problems that need attention|
| `CRITICAL`| 50            | Very severe errors, system shutdown |

By default, the logging system handles messages at level `WARNING` and above.

---

## 3. Basic Configuration

The simplest way to get started:

```python
import logging

logging.basicConfig(level=logging.DEBUG)  # capture DEBUG and above
logging.debug("This is a debug message")
logging.info("Starting the process...")
logging.warning("This is a warning")
logging.error("An error occurred")
logging.critical("Critical failure!")
````

* **`level=`** sets the minimum severity to handle.
* By default, logs go to **stdout** in a simple format:

  ```
  WARNING:root:This is a warning
  ```

---

## 4. Formatting Logs

Customize the appearance of each log message:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("myapp")
logger.info("Application started")
```

* **`%(asctime)s`**: Timestamp
* **`%(levelname)s`**: Severity name
* **`%(name)s`**: Logger’s name
* **`%(message)s`**: The log message

---

## 5. Handlers: Sending Logs to Multiple Destinations

Use **handlers** to route logs to different outputs:

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("file_logger")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Rotating file handler (1 MB max, 3 backups)
fh = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=3)
fh.setLevel(logging.DEBUG)

# Shared formatter
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Attach handlers
logger.addHandler(ch)
logger.addHandler(fh)

# Usage
logger.debug("Debug details go to file only")
logger.info("This shows in console and file")
```

---

## 6. Logger Hierarchy & Best Practices

* **Module-specific loggers:** Use `getLogger(__name__)` in each module:

  ```python
  # module_a.py
  import logging
  logger = logging.getLogger(__name__)
  logger.info("Message from module A")
  ```
* **Single configuration point:** Call `basicConfig` (or your custom setup) once in your application entrypoint.
* **Avoid `print()` for errors:** Use `logger.exception()` inside `except` blocks to include stack traces:

  ```python
  try:
      1 / 0
  except ZeroDivisionError:
      logger.exception("Division failed")
  ```

---

## 7. Pydantic-Style Class-Based Configuration

Wrap your logging setup in a reusable Pydantic `BaseSettings` class:

```python
from pydantic import BaseSettings
import logging
from logging.handlers import RotatingFileHandler

class LoggingSettings(BaseSettings):
    """Define all your logger settings here—override via env vars prefixed LOG_."""
    level: str = "INFO"
    fmt: str = "%(asctime)s %(levelname)s [%(filename)s] %(message)s"  # use filename as source identifier
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    # File handler settings
    log_file: str = "app.log"
    max_bytes: int = 1_000_000
    backup_count: int = 3

    class Config:
        env_prefix = "LOG_"
        env_file = Path(__file__).parent.parent.parent / ".env"
        case_sensitive = (False,)
        extra = "allow"

    def configure_logger(self, name: str = None) -> logging.Logger:
        """
        Create or reconfigure a logger with both console and rotating-file handlers.
        Pass `name` to get a child logger (or None for the root logger).
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        # shared formatter
        formatter = logging.Formatter(self.fmt, datefmt=self.datefmt)

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(formatter)

        # rotating file handler
        fh = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        fh.setLevel(self.level)
        fh.setFormatter(formatter)

        # remove existing handlers to avoid duplicates
        logger.handlers.clear()
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger

log_cfg = LoggingSettings()
logger = log_cfg.configure_logger()
```

### Usage Example

```python
# main.py
from settings import LoggingSettings

# Load settings (reads env vars LOG_LEVEL, LOG_LOG_FILE, etc.)
log_cfg = LoggingSettings()

# Configure the root logger
logger = log_cfg.configure_logger()
logger.info("Application starting…")

# In other modules, just get the module logger
# module_a.py
import logging\ nlogger = logging.getLogger(__name__)

def do_work():
    logger.debug("Doing some work…")
```

**Override via Environment Variables**:

```bash
export LOG_LEVEL=DEBUG
export LOG_LOG_FILE="/var/log/myapp.log"
python main.py
```

---

With this complete setup, you have:

1. Centralized, environment-driven configuration.
2. Automatic validation of settings.
3. A single `configure_logger()` call usable across scripts, services, and tests.
 

```
```
