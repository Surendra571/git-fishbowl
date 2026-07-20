"""
Orchestration script for git-fishbowl.
Executes the asynchronous telemetry stream pipeline.
"""

import asyncio
import os
import sys

from src.client import FishbowlClient
from src.dashboard import FishbowlDashboard


async def main():
    # Attempt to pull from environment or default to a target repo
    target_repo = os.getenv("GITHUB_REPOSITORY", "python/cpython")

    # If an argument is passed via command line, prioritize it
    if len(sys.argv) > 1:
        target_repo = sys.argv[1]

    # Initialize the client with the required target_repo argument
    client = FishbowlClient(target_repo=target_repo)

    # Concurrently fetch telemetry payloads
    raw_issues, raw_pulls = await client.fetch_data()

    # Process metrics and stream the text report to stdout
    metrics = FishbowlDashboard.calculate_health_metrics(raw_issues, raw_pulls)
    report = FishbowlDashboard.render(target_repo, metrics)
    sys.stdout.write(report)


if __name__ == "__main__":
    asyncio.run(main())
