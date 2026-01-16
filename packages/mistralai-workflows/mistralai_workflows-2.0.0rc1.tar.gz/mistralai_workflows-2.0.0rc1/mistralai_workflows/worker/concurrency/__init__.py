"""
Concurrency utilities for parallel activity execution.

This module provides three execution patterns:

1. **Batch Executor** - Process a known list of items
   ```python
   await execute_activities_in_parallel(my_activity, items=[item1, item2, item3])
   ```

2. **Stream Executor** - Process items sequentially from a stream/queue
   ```python
   await execute_activities_in_parallel(my_activity, get_item_from_prev_item_activity=get_next)
   ```

3. **Paginated Executor** - Process items by fetching pages/chunks by index
   ```python
   await execute_activities_in_parallel(my_activity, get_item_from_index_activity=get_page)
   ```
"""

from mistralai_workflows.worker.concurrency.concurrency_workflow import InternalConcurrencyWorkflow
from mistralai_workflows.worker.concurrency.execute_activities_in_parallel import execute_activities_in_parallel
from mistralai_workflows.worker.concurrency.types import (
    DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    ExtraItemParams,
    GetItemFromIndexParams,
)

# Export public API
__all__ = [
    "execute_activities_in_parallel",
    "GetItemFromIndexParams",
    "ExtraItemParams",
    "DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS",
    "InternalConcurrencyWorkflow",
]
