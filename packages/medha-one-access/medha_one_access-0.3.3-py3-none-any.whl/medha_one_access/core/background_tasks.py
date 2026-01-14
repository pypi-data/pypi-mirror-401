"""
MedhaOne Access Control - Background Task Manager

Handles background processing for auto-recalculation and other async tasks.
Allows CRUD operations to return immediately while processing happens in background.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timezone
from asyncio import Queue, Task
from enum import Enum
import traceback

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels for queue processing."""
    HIGH = 1    # Critical updates (e.g., permission changes)
    MEDIUM = 2  # Normal recalculations
    LOW = 3     # Batch operations, maintenance


class TaskStatus(Enum):
    """Status of background tasks."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BackgroundTask:
    """Represents a background task to be processed."""
    
    def __init__(
        self,
        task_id: str,
        task_type: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        callback: Optional[Callable] = None
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload
        self.priority = priority
        self.callback = callback
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now(timezone.utc)
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
        self.result: Optional[Any] = None
        
    def __lt__(self, other):
        """Enable priority queue sorting."""
        return self.priority.value < other.priority.value


class AsyncBackgroundTaskManager:
    """
    Manages background tasks for async processing.
    
    Features:
    - Priority queue for task processing
    - Multiple worker support
    - Task status tracking
    - Error handling and retry logic
    - Graceful shutdown
    """
    
    def __init__(self, num_workers: int = 5, max_queue_size: int = 10000):
        """
        Initialize the background task manager.
        
        Args:
            num_workers: Number of concurrent workers
            max_queue_size: Maximum tasks in queue
        """
        self.num_workers = num_workers
        self.max_queue_size = max_queue_size
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_queue_size)
        self.workers: List[Task] = []
        self.running = False
        self.tasks: Dict[str, BackgroundTask] = {}  # Track all tasks
        self.task_handlers: Dict[str, Callable] = {}  # Task type handlers
        self._task_counter = 0
        self._lock = asyncio.Lock()
        
        # Statistics
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "cancelled_tasks": 0,
            "average_processing_time": 0,
        }
    
    def register_handler(self, task_type: str, handler: Callable):
        """Register a handler for a specific task type."""
        self.task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")
    
    async def start(self):
        """Start the background task manager and workers."""
        if self.running:
            logger.warning("Background task manager already running")
            return
            
        self.running = True
        logger.info(f"Starting background task manager with {self.num_workers} workers")
        
        # Start worker tasks
        for i in range(self.num_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
        
        logger.info("Background task manager started successfully")
    
    async def stop(self, timeout: float = 30.0):
        """
        Stop the background task manager gracefully.
        
        Args:
            timeout: Maximum time to wait for workers to finish
        """
        if not self.running:
            return
            
        logger.info("Stopping background task manager...")
        self.running = False
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for workers to finish with timeout
        try:
            await asyncio.wait_for(
                asyncio.gather(*self.workers, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.warning(f"Workers did not finish within {timeout} seconds")
        
        self.workers.clear()
        logger.info("Background task manager stopped")
    
    async def submit_task(
        self,
        task_type: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        callback: Optional[Callable] = None
    ) -> str:
        """
        Submit a task for background processing.
        
        Args:
            task_type: Type of task to process
            payload: Task data
            priority: Task priority
            callback: Optional callback when task completes
            
        Returns:
            Task ID for tracking
        """
        async with self._lock:
            self._task_counter += 1
            task_id = f"{task_type}_{self._task_counter}_{datetime.now(timezone.utc).timestamp()}"
        
        task = BackgroundTask(
            task_id=task_id,
            task_type=task_type,
            payload=payload,
            priority=priority,
            callback=callback
        )
        
        # Store task for tracking
        self.tasks[task_id] = task
        self.stats["total_tasks"] += 1
        
        # Add to queue (non-blocking)
        try:
            self.queue.put_nowait((priority.value, task))
            logger.debug(f"Task {task_id} submitted with priority {priority.name}")
        except asyncio.QueueFull:
            task.status = TaskStatus.FAILED
            task.error = "Queue is full"
            self.stats["failed_tasks"] += 1
            logger.error(f"Failed to submit task {task_id}: Queue is full")
            raise Exception("Background task queue is full")
        
        return task_id
    
    async def submit_recalculation_task(
        self,
        user_ids: List[str],
        application: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> str:
        """
        Submit a user access recalculation task.
        
        Args:
            user_ids: List of user IDs to recalculate
            application: Application context
            priority: Task priority
            
        Returns:
            Task ID for tracking
        """
        payload = {
            "user_ids": user_ids,
            "application": application,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return await self.submit_task(
            task_type="recalculate_access",
            payload=payload,
            priority=priority
        )
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific task."""
        task = self.tasks.get(task_id)
        if not task:
            return None
            
        return {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "error": task.error,
            "result": task.result
        }
    
    async def get_queue_stats(self) -> Dict[str, Any]:
        """Get current queue statistics."""
        return {
            "queue_size": self.queue.qsize(),
            "max_queue_size": self.max_queue_size,
            "num_workers": self.num_workers,
            "active_workers": len([w for w in self.workers if not w.done()]),
            "total_tasks": self.stats["total_tasks"],
            "completed_tasks": self.stats["completed_tasks"],
            "failed_tasks": self.stats["failed_tasks"],
            "cancelled_tasks": self.stats["cancelled_tasks"],
            "average_processing_time": self.stats["average_processing_time"],
            "pending_tasks": self.queue.qsize(),
        }
    
    async def _worker(self, worker_name: str):
        """
        Worker coroutine that processes tasks from the queue.
        
        Args:
            worker_name: Name of the worker for logging
        """
        logger.info(f"{worker_name} started")
        
        while self.running:
            try:
                # Wait for task with timeout to allow checking running status
                priority, task = await asyncio.wait_for(
                    self.queue.get(),
                    timeout=1.0
                )
                
                # Process the task
                await self._process_task(task, worker_name)
                
            except asyncio.TimeoutError:
                # No task available, continue
                continue
            except asyncio.CancelledError:
                logger.info(f"{worker_name} cancelled")
                break
            except Exception as e:
                logger.error(f"{worker_name} error: {str(e)}\n{traceback.format_exc()}")
        
        logger.info(f"{worker_name} stopped")
    
    async def _process_task(self, task: BackgroundTask, worker_name: str):
        """
        Process a single task.
        
        Args:
            task: Task to process
            worker_name: Name of the worker processing the task
        """
        logger.debug(f"{worker_name} processing task {task.task_id}")
        
        task.status = TaskStatus.PROCESSING
        task.started_at = datetime.now(timezone.utc)
        
        try:
            # Get handler for task type
            handler = self.task_handlers.get(task.task_type)
            if not handler:
                raise Exception(f"No handler registered for task type: {task.task_type}")
            
            # Execute handler
            result = await handler(task.payload)
            
            # Mark as completed
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now(timezone.utc)
            task.result = result
            self.stats["completed_tasks"] += 1
            
            # Execute callback if provided
            if task.callback:
                try:
                    await task.callback(task.task_id, result)
                except Exception as e:
                    logger.error(f"Callback error for task {task.task_id}: {str(e)}")
            
            # Update average processing time
            processing_time = (task.completed_at - task.started_at).total_seconds()
            self._update_average_processing_time(processing_time)
            
            logger.debug(f"{worker_name} completed task {task.task_id} in {processing_time:.2f}s")
            
        except asyncio.CancelledError:
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now(timezone.utc)
            self.stats["cancelled_tasks"] += 1
            logger.info(f"Task {task.task_id} cancelled")
            raise
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now(timezone.utc)
            task.error = str(e)
            self.stats["failed_tasks"] += 1
            logger.error(f"Task {task.task_id} failed: {str(e)}\n{traceback.format_exc()}")
            
            # Execute error callback if provided
            if task.callback:
                try:
                    await task.callback(task.task_id, None, error=str(e))
                except Exception as callback_error:
                    logger.error(f"Error callback failed for task {task.task_id}: {str(callback_error)}")
    
    def _update_average_processing_time(self, new_time: float):
        """Update the average processing time statistic."""
        completed = self.stats["completed_tasks"]
        if completed == 0:
            self.stats["average_processing_time"] = new_time
        else:
            current_avg = self.stats["average_processing_time"]
            self.stats["average_processing_time"] = (current_avg * (completed - 1) + new_time) / completed
    
    async def cleanup_old_tasks(self, max_age_hours: int = 24):
        """
        Clean up old completed/failed tasks from memory.
        
        Args:
            max_age_hours: Maximum age of tasks to keep in memory
        """
        current_time = datetime.now(timezone.utc)
        tasks_to_remove = []
        
        for task_id, task in self.tasks.items():
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                if task.completed_at:
                    age_hours = (current_time - task.completed_at).total_seconds() / 3600
                    if age_hours > max_age_hours:
                        tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
        
        if tasks_to_remove:
            logger.info(f"Cleaned up {len(tasks_to_remove)} old tasks")


# Global instance for singleton pattern (optional)
_global_task_manager: Optional[AsyncBackgroundTaskManager] = None


def get_background_task_manager() -> AsyncBackgroundTaskManager:
    """Get the global background task manager instance."""
    global _global_task_manager
    if _global_task_manager is None:
        _global_task_manager = AsyncBackgroundTaskManager()
    return _global_task_manager


# Export classes and functions
__all__ = [
    "AsyncBackgroundTaskManager",
    "BackgroundTask",
    "TaskPriority",
    "TaskStatus",
    "get_background_task_manager",
]