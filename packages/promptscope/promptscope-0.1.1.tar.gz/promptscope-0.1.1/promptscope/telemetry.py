import asyncio
import atexit
import gzip
import json
import logging
import uuid
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from promptscope.config import settings

logger = logging.getLogger(__name__)


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class PromptScopeTelemetry:
    """
    PromptScope Telemetry System.
    Features: Async Batching, Level Filtering, and Auto-Compression.
    """

    def __init__(self):
        self.log_dir = Path(settings.TELEMETRY_LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.min_level = LogLevel.INFO  # Or make this configurable
        self.batch_size = settings.TELEMETRY_BATCH_SIZE
        self.flush_interval = settings.TELEMETRY_FLUSH_INTERVAL

        # Queue is lazily created when a running event loop is available to avoid RuntimeError
        self.queue: Optional[asyncio.Queue] = None
        self._is_running = False
        self.worker_task: Optional[asyncio.Task] = None

    def _get_filename(self) -> Path:
        """Generates filename based on current date."""
        return self.log_dir / f"telemetry_{datetime.now().strftime('%Y%m%d')}.jsonl"

    async def log(self, level: LogLevel, event_type: str, details: Dict[str, Any]):
        """The main entry point for logging events."""
        if not self._is_running:
            self.start()
        
        if not self._is_running or level < self.min_level or self.queue is None:
            return

        event = {
            "id": str(uuid.uuid4()),
            "level": level.name,
            "level_val": int(level),
            "type": event_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        await self.queue.put(event)

    # Shorthand methods
    async def debug(self, event: str, details: dict): await self.log(LogLevel.DEBUG, event, details)
    async def info(self, event: str, details: dict): await self.log(LogLevel.INFO, event, details)
    async def warn(self, event: str, details: dict): await self.log(LogLevel.WARNING, event, details)
    async def error(self, event: str, details: dict): await self.log(LogLevel.ERROR, event, details)
    async def critical(self, event: str, details: dict): await self.log(LogLevel.CRITICAL, event, details)

    async def _write_batch_to_disk(self, batch: List[Dict]):
        """Writes a batch of events to a file."""
        if not batch:
            return
        
        target_file = self._get_filename()
        lines = [json.dumps(e) + "\n" for e in batch]

        def sync_write():
            with open(target_file, "a", encoding="utf-8") as f:
                f.writelines(lines)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, sync_write)

    async def _worker(self):
        """Background loop to process the queue."""
        if self.queue is None:
            return
        batch = []
        while self._is_running or not self.queue.empty():
            try:
                timeout = self.flush_interval if self._is_running else 0.1
                event = await asyncio.wait_for(self.queue.get(), timeout=timeout)
                batch.append(event)

                if len(batch) >= self.batch_size:
                    await self._write_batch_to_disk(batch)
                    batch = []
                self.queue.task_done()

            except asyncio.TimeoutError:
                if batch:
                    await self._write_batch_to_disk(batch)
                    batch = []
            except asyncio.CancelledError:
                break
            except Exception:
                logger.error("Telemetry worker encountered an error", exc_info=True)
        
        # Final flush before exiting
        if batch:
            await self._write_batch_to_disk(batch)
            batch = []

    def start(self):
        """Starts the background worker task."""
        if self._is_running:
            return

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop; skip starting to avoid crashing. Telemetry becomes a no-op.
            return

        if self.queue is None:
            self.queue = asyncio.Queue()

        self._is_running = True
        self.worker_task = loop.create_task(self._worker())

    async def _rotate_and_compress(self):
        """Maintenance: Compresses all logs except for today's active log."""
        today_file = self._get_filename().name
        loop = asyncio.get_event_loop()

        def sync_compress():
            for file in self.log_dir.glob("*.jsonl"):
                if file.name != today_file:
                    try:
                        with open(file, 'rb') as f_in:
                            with gzip.open(f"{file}.gz", 'wb') as f_out:
                                f_out.writelines(f_in)
                        file.unlink()
                    except Exception:
                        logger.error(f"Failed to compress telemetry file: {file}", exc_info=True)

        await loop.run_in_executor(None, sync_compress)

    async def shutdown(self):
        """Gracefully flushes remaining logs and stops the worker."""
        if not self._is_running:
            return

        self._is_running = False
        # Give the worker a moment to process remaining items
        if self.worker_task:
            try:
                await asyncio.wait_for(self.worker_task, timeout=self.flush_interval * 2)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass

        await self._rotate_and_compress()


class _NoOpTelemetry:
    """A telemetry client that does nothing."""
    async def log(self, *args, **kwargs): pass
    async def debug(self, *args, **kwargs): pass
    async def info(self, *args, **kwargs): pass
    async def warn(self, *args, **kwargs): pass
    async def error(self, *args, **kwargs): pass
    async def critical(self, *args, **kwargs): pass
    def start(self): pass
    async def shutdown(self): pass

NoOpTelemetry = _NoOpTelemetry()

# --- Global Telemetry Client Management ---
_telemetry_client: Union[PromptScopeTelemetry, _NoOpTelemetry, None] = None

def initialize():
    """Initializes and starts the global telemetry client."""
    global _telemetry_client
    if _telemetry_client is not None:
        return _telemetry_client

    if not settings.TELEMETRY_ENABLED:
        _telemetry_client = NoOpTelemetry
    else:
        _telemetry_client = PromptScopeTelemetry()
    
    return _telemetry_client

def shutdown_telemetry():
    """Gracefully shuts down the global telemetry client."""
    if _telemetry_client and hasattr(_telemetry_client, 'shutdown'):
        # This function is registered with atexit, which is synchronous.
        # We need to run the async shutdown logic in a new event loop.
        try:
            asyncio.run(_telemetry_client.shutdown())
        except RuntimeError:
            # If an event loop is already running, create a new one
            loop = asyncio.new_event_loop()
            loop.run_until_complete(_telemetry_client.shutdown())
            loop.close()

# The active telemetry client. Initialize on first access.
telemetry: Union[PromptScopeTelemetry, _NoOpTelemetry] = initialize()

# Ensure graceful shutdown on application exit
atexit.register(shutdown_telemetry)
