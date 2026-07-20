"""
Dashboard module for git-fishbowl.
Handles calculation logic and terminal-formatted reporting.
"""


class FishbowlDashboard:
    @staticmethod
    def calculate_health_metrics(raw_issues: list, raw_pulls: list) -> dict:
        """
        Processes raw GitHub API lists to aggregate telemetry health counters.
        """
        # Active issues exclude pull requests mixed into the issues payload
        actual_issues = [i for i in raw_issues if "pull_request" not in i]
        active_issues_count = len(actual_issues)

        # Filter critical unresolved issues by scanning labels
        critical_count = 0
        for issue in actual_issues:
            labels = [
                label.get("name", "").lower() for label in issue.get("labels", [])
            ]
            if any(name in labels for name in ["bug", "critical", "blocker"]):
                critical_count += 1

        # Process Pull Requests
        open_prs_count = 0
        draft_prs_count = 0

        for pr in raw_pulls:
            open_prs_count += 1
            if pr.get("draft") is True:
                draft_prs_count += 1

        return {
            "active_issues": active_issues_count,
            "critical_issues": critical_count,
            "open_prs": open_prs_count,
            "draft_prs": draft_prs_count,
        }

    @staticmethod
    def render(target_repo: str, metrics: dict) -> str:
        """
        Calculates status thresholds and returns the formatted telemetry report
        as a pure ASCII string to maintain cross-platform stream compatibility.
        """
        active_issues = metrics.get("active_issues", 0)
        critical_issues = metrics.get("critical_issues", 0)
        open_prs = metrics.get("open_prs", 0)
        draft_prs = metrics.get("draft_prs", 0)

        # State evaluation logic
        if critical_issues > 0:
            status = "ATTENTION_REQUIRED"
            header_flag = "[ ALERT ]"
        else:
            status = "HEALTHY"
            header_flag = "[ OK ]"

        # Safe ASCII layouts for robust terminal streaming
        output = [
            "=" * 60,
            f"GIT-FISHBOWL(1)       HEALTH SUMMARY       {header_flag}",
            "=" * 60,
            f"TARGET REPOSITORY : {target_repo}",
            "-" * 60,
            f"  - Active Issues          : {active_issues}",
            f"  - Critical Unresolved   : {critical_issues}",
            f"  - Open Pull Requests    : {open_prs}",
            f"  - Draft Pull Requests   : {draft_prs}",
            "-" * 60,
            f"SYSTEM METRIC STATUS  : {status}",
            "=" * 60,
        ]

        return "\n".join(output) + "\n"
