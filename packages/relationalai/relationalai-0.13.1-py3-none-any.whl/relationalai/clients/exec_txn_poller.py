from __future__ import annotations

import time
from typing import Dict, Optional, TYPE_CHECKING

from relationalai import debugging
from relationalai.clients.util import poll_with_specified_overhead
from relationalai.tools.cli_controls import create_progress
from relationalai.util.format import format_duration

if TYPE_CHECKING:
    from relationalai.clients.resources.snowflake import Resources

# Polling behavior constants
POLL_OVERHEAD_RATE = 0.1  # Overhead rate for exponential backoff

# Text color constants
GREEN_COLOR = '\033[92m'
GRAY_COLOR = '\033[90m'
ENDC = '\033[0m'


class ExecTxnPoller:
    """
    Encapsulates the polling logic for exec_async transaction completion.
    """

    def __init__(
        self,
        resource: "Resources",
        txn_id: str,
        headers: Optional[Dict] = None,
        txn_start_time: Optional[float] = None,
    ):
        self.res = resource
        self.txn_id = txn_id
        self.headers = headers or {}
        self.txn_start_time = txn_start_time or time.time()

    def poll(self) -> bool:
        """
        Poll for transaction completion with interactive progress display.

        Returns:
            True if transaction completed successfully, False otherwise
        """

        # Don't show duration summary - we handle our own completion message
        with create_progress(
            description="Evaluating Query...",
            success_message="",  # We'll handle this ourselves
            leading_newline=False,
            trailing_newline=False,
            show_duration_summary=False,
        ) as progress:
            def check_status() -> bool:
                """Check if transaction is complete."""
                elapsed = time.time() - self.txn_start_time
                # Update the main status with elapsed time
                progress.update_main_status(
                    query_progress_message(self.txn_id, elapsed)
                )
                return self.res._check_exec_async_status(self.txn_id, headers=self.headers)

            with debugging.span("wait", txn_id=self.txn_id):
                poll_with_specified_overhead(check_status, overhead_rate=POLL_OVERHEAD_RATE)

            # Calculate final duration
            total_duration = time.time() - self.txn_start_time

            # Update to success message with duration
            progress.update_main_status(
                query_complete_message(self.txn_id, total_duration)
            )

        return True

def query_progress_message(id: str, duration: float) -> str:
    return (
        # Print with whitespace to align with the end of the transaction ID
        f"Evaluating Query... {format_duration(duration):>18}\n" +
        f"{GRAY_COLOR}Query: {id}{ENDC}"
    )

def query_complete_message(id: str, duration: float, status_header: bool = False) -> str:
    return (
        (f"{GREEN_COLOR}✅ " if status_header else "") +
        # Print with whitespace to align with the end of the transaction ID
        f"Query Complete: {format_duration(duration):>24}\n" +
        f"{GRAY_COLOR}Query: {id}{ENDC}"
    )
