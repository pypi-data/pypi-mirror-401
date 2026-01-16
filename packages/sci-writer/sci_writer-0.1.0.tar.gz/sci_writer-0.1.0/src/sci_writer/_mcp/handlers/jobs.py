"""MCP handlers for background job management."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .compile import compile_handler


async def compile_async_handler(arguments: dict[str, Any]) -> str:
    """Handle compile_async tool - start compilation as background job.

    Returns immediately with job_id for tracking.
    """
    from sci_writer._jobs import job_manager

    project_dir = Path(arguments["project_dir"])

    if not project_dir.exists():
        return json.dumps(
            {"success": False, "error": f"Project not found: {project_dir}"}
        )

    # Create job
    job = job_manager.create_job("compile", arguments)

    # Start job in background
    job_manager.start_job(job, compile_handler)

    return json.dumps(
        {
            "success": True,
            "job_id": job.id,
            "status": job.status.value,
            "message": f"Compilation started. Use job_status with id '{job.id}' to check progress.",
        }
    )


async def job_status_handler(arguments: dict[str, Any]) -> str:
    """Handle job_status tool - get status of a background job."""
    from sci_writer._jobs import job_manager

    job_id = arguments["job_id"]
    job = job_manager.get_job(job_id)

    if not job:
        return json.dumps({"success": False, "error": f"Job not found: {job_id}"})

    return json.dumps({"success": True, **job.to_dict()})


async def job_list_handler(arguments: dict[str, Any]) -> str:
    """Handle job_list tool - list all background jobs."""
    from sci_writer._jobs import JobStatus, job_manager

    status_filter = arguments.get("status")
    limit = arguments.get("limit", 20)

    status = JobStatus(status_filter) if status_filter else None
    jobs = job_manager.list_jobs(status=status, limit=limit)

    return json.dumps(
        {"success": True, "jobs": [j.to_dict() for j in jobs], "count": len(jobs)}
    )


async def job_cancel_handler(arguments: dict[str, Any]) -> str:
    """Handle job_cancel tool - cancel a running job."""
    from sci_writer._jobs import job_manager

    job_id = arguments["job_id"]

    if job_manager.cancel_job(job_id):
        return json.dumps({"success": True, "message": f"Job {job_id} cancelled"})
    else:
        return json.dumps(
            {
                "success": False,
                "error": f"Cannot cancel job {job_id} (not running or not found)",
            }
        )


async def job_result_handler(arguments: dict[str, Any]) -> str:
    """Handle job_result tool - get result of completed job."""
    from sci_writer._jobs import JobStatus, job_manager

    job_id = arguments["job_id"]
    job = job_manager.get_job(job_id)

    if not job:
        return json.dumps({"success": False, "error": f"Job not found: {job_id}"})

    if job.status not in (JobStatus.COMPLETED, JobStatus.FAILED):
        return json.dumps(
            {
                "success": False,
                "error": f"Job {job_id} not finished yet (status: {job.status.value})",
                "status": job.status.value,
            }
        )

    return json.dumps(
        {
            "success": job.status == JobStatus.COMPLETED,
            "job_id": job_id,
            "status": job.status.value,
            "result": job.result,
            "error": job.error,
        }
    )


__all__ = [
    "compile_async_handler",
    "job_status_handler",
    "job_list_handler",
    "job_cancel_handler",
    "job_result_handler",
]
