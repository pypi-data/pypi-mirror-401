from .sdk_client import SDKClient
from .enums import TaskTypes
from .task_context import TaskContext
from typing import Any, Dict, Optional

class Run:
    def __init__(self, run_id: str, client: SDKClient) -> None:
        self.run_id: str = run_id
        self.client: SDKClient = client
        # will be set by Workflow.start_run
        # this is so that tasks can include the workflow linkage
        self.workflow_id: str | None = None
    
    def step(self, task_step_id: str, task_type: Optional[TaskTypes], metadata: Dict[Any, Any] = {}) -> TaskContext:
        return TaskContext(
            task_step_id=task_step_id,
            client=self.client,
            type=task_type,
            metadata=metadata
        )

    def end(self) -> None:
        pass
        # end here