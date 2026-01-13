import json
import logging
from datetime import datetime

from dojo_sdk_core.tasks import RemoteTaskLoader

from dojo_sdk_client.dojo_eval_client import EvaluationResult

logger = logging.getLogger(__name__)


def load_tasks_from_hf_dataset(dataset_name: str, revision: str = "main") -> list[str]:
    """Load all tasks from HuggingFace dataset and return as dojo_name/task_id format."""
    loader = RemoteTaskLoader(dataset_name, revision=revision)
    all_tasks = loader._get_all_tasks()

    task_list = []
    for task in all_tasks:
        task_path = f"{task.spa}/{task.id}"
        task_list.append(task_path)

    logger.info(f"Loaded {len(task_list)} tasks from HF dataset {dataset_name}")
    return task_list


EXCLUDE_TASKS = ["weibo/music-posts-likes-and-follow-v2"]


def exclude_tasks(tasks: list[str]) -> list[str]:
    """Exclude tasks from a list of tasks."""
    logger.info(f"Excluding {len(EXCLUDE_TASKS)} tasks: {EXCLUDE_TASKS}")
    return [task for task in tasks if task not in EXCLUDE_TASKS]


def write_results_to_json(results: list[EvaluationResult], output_file: str = None, job_id: str = None) -> str:
    """Write evaluation results to a JSON file.

    Args:
        results: List of EvaluationResult objects
        output_file: Optional output file path. If not provided, generates a timestamped filename.
        job_id: Optional job ID to include in the output

    Returns:
        Path to the written JSON file
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"eval_results_{timestamp}.json"

    output_data = {
        "job_id": job_id,
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tasks": len(results),
            "successful": len([r for r in results if r.score == 1.0]),
            "failed": len([r for r in results if r.score == 0.0 and not r.error]),
            "errors": len([r for r in results if r.error]),
            "score_percentage": (sum(r.score for r in results) / len(results) * 100) if results else 0,
        },
        "results": [
            {
                "task_id": r.task_id,
                "task_name": r.task_name,
                "score": r.score,
                "reason": r.reason,
                "status": r.status.value,
                "total_steps": r.total_steps,
                "error": r.error,
            }
            for r in results
        ],
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    logger.info(f"Results written to {output_file}")
    return output_file
