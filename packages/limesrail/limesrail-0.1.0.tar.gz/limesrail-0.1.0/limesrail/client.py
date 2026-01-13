import asyncio
import aiohttp
import time
import uuid
import threading
from collections import deque
from threading import Lock
from contextlib import contextmanager
from datetime import datetime, timezone

class TraceBatcher:
    def __init__(self, api_key, api_url, batch_size=50, flush_interval=5):
        self.api_key = api_key
        self.api_url = api_url
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.queue = deque()
        self.lock = Lock()
        self._background_task = None
        self._loop = None
        
    def start(self):
        """Start background flush task"""
        # Create a new loop for the background thread
        def run_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._flush_loop())
        
        self._background_task = threading.Thread(target=run_loop, daemon=True)
        self._background_task.start()
    
    async def _flush_loop(self):
        """Periodically flush the queue"""
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()
    
    def add(self, payload: dict):
        """Add trace to batch"""
        with self.lock:
            self.queue.append(payload)
            if len(self.queue) >= self.batch_size:
                # Trigger immediate flush in background
                if self._loop:
                    asyncio.run_coroutine_threadsafe(self.flush(), self._loop)
    
    async def flush(self):
        """Send all batched traces"""
        with self.lock:
            if not self.queue:
                return
            batch = list(self.queue)
            self.queue.clear()
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                # Send as batch
                async with session.post(
                    f"{self.api_url}/batch",
                    json={"traces": batch},
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status not in [200, 201]:
                        print(f"⚠️ Limesrail: Batch upload failed: {response.status}")
        except Exception as e:
            print(f"❌ Limesrail: Batch upload error: {e}")

class Limesrail:
    def __init__(self, api_key: str, api_url: str = "http://localhost:8000"):
        """
        Initialize the Limesrail Client.
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/") + "/api" # Ensure correct API path
        
        # Initialize and start the batcher
        self.batcher = TraceBatcher(self.api_key, self.api_url)
        self.batcher.start()
        print(f"🚀 Limesrail initialized (URL: {self.api_url})")

    @contextmanager
    def trace(self, user_id=None, session_id=None, model=None, **kwargs):
        """
        Context manager to trace a block of code.
        """
        trace_id = str(uuid.uuid4())
        start_time = time.time()
        error_occurred = False
        error_message = None

        try:
            yield
        except Exception as e:
            error_occurred = True
            error_message = str(e)
            raise e
        finally:
            end_time = time.time()
            latency = (end_time - start_time) * 1000 # ms
            
            # Construct the trace payload
            payload = {
                "id": trace_id,
                "user_id": user_id,
                "session_id": session_id,
                "model": model,
                "latency_ms": latency,
                "status": "error" if error_occurred else "success",
                "error_message": error_message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": kwargs
            }
            
            # Add to batcher
            self.batcher.add(payload)