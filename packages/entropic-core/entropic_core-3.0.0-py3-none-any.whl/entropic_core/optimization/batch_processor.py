"""Batch processing for efficient bulk operations."""

import logging
import threading
import time
from collections import deque
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process items in batches for efficiency."""

    def __init__(
        self,
        batch_size: int = 100,
        flush_interval: float = 5.0,
        processor_func: Callable = None,
    ):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.processor_func = processor_func

        self.queue = deque()
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

        self.processed_count = 0
        self.batch_count = 0
        self.last_flush = time.time()

        self.pending_operations = self.queue

        self._processed_items = []

        if self.flush_interval > 0:
            self.start()

    def start(self):
        """Start background batch processor."""
        if self.running:
            logger.warning("Batch processor already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        logger.info("Batch processor started")

    def stop(self):
        """Stop batch processor and flush remaining items."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
        self._flush()
        logger.info("Batch processor stopped")

    def add(self, item: Any):
        """Add item to batch queue."""
        with self.lock:
            self.queue.append(item)

        # Flush if batch size reached
        if len(self.queue) >= self.batch_size:
            self._flush()

    def add_many(self, items: List[Any]):
        """Add multiple items to batch queue."""
        with self.lock:
            self.queue.extend(items)

        # Flush if batch size reached
        if len(self.queue) >= self.batch_size:
            self._flush()

    def _flush(self) -> List[Any]:
        """Process all queued items and return them."""
        if not self.queue:
            return []

        with self.lock:
            # Get batch from queue
            batch = []
            while self.queue and len(batch) < self.batch_size:
                batch.append(self.queue.popleft())

        if not batch:
            return []

        # Process batch
        try:
            if self.processor_func:
                self.processor_func(batch)

            self.processed_count += len(batch)
            self.batch_count += 1
            self.last_flush = time.time()

            self._processed_items.extend(batch)

            logger.debug(f"Processed batch of {len(batch)} items")

        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            # Re-queue items on error
            with self.lock:
                self.queue.extendleft(reversed(batch))
            return []

        return batch

    def _process_loop(self):
        """Background processing loop."""
        while self.running:
            time.sleep(0.1)

            # Flush if interval elapsed
            if time.time() - self.last_flush >= self.flush_interval:
                self._flush()

    def stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "queue_size": len(self.queue),
            "processed_count": self.processed_count,
            "batch_count": self.batch_count,
            "running": self.running,
        }

    def add_operation(self, operation: Any, data: Dict = None):
        """
        Add operation to batch (compatible with tests expecting 2 parameters).

        Args:
            operation: Operation identifier or data
            data: Optional additional data (combined with operation if provided)
        """
        if data is not None:
            item = {"operation": operation, "data": data}
        else:
            item = operation
        with self.lock:
            self.queue.append(item)

    def process_batch(self) -> List[Any]:
        """
        Process current batch and return results.

        Returns:
            List of processed items
        """
        was_running = self.running
        if was_running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=1)

        all_processed = []

        with self.lock:
            while self.queue:
                batch = []
                while self.queue and len(batch) < self.batch_size:
                    batch.append(self.queue.popleft())

                if batch:
                    if self.processor_func:
                        self.processor_func(batch)
                    self.processed_count += len(batch)
                    self.batch_count += 1
                    all_processed.extend(batch)

        if was_running:
            self.start()

        return all_processed

    def get_processed_items(self) -> List[Any]:
        """
        Retrieve all processed items.

        Returns:
            List of all processed items
        """
        return self._processed_items


class EntropyBatchProcessor(BatchProcessor):
    """Specialized batch processor for entropy measurements."""

    def __init__(self, brain, batch_size: int = 50):
        super().__init__(
            batch_size=batch_size,
            flush_interval=2.0,
            processor_func=self._process_measurements,
        )
        self.brain = brain

    def _process_measurements(self, batch: List[Dict[str, Any]]):
        """Process batch of entropy measurements."""
        # Aggregate measurements
        total_entropy = sum(item["entropy"] for item in batch)
        avg_entropy = total_entropy / len(batch)

        # Update brain state
        self.brain.current_entropy = avg_entropy

        # Check if regulation needed
        if avg_entropy > 0.8 or avg_entropy < 0.2:
            self.brain.regulate()

        # Log batch
        self.brain.memory.log_decision(
            entropy=avg_entropy,
            action=f"batch_processed_{len(batch)}",
            result="success",
        )

        logger.info(
            f"Processed {len(batch)} measurements, avg entropy: {avg_entropy:.3f}"
        )
