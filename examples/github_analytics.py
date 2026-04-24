#!/usr/bin/env python3
"""
GitHub Project Analytics — ADR-152

Demonstrates how to use the Trix Python SDK to access code intelligence
and delivery analytics for GitHub-connected projects.

Prerequisites:
  1. A Trix project with a linked GitHub repository
  2. Your TRIX_API_KEY and TRIX_PROJECT_ID in environment

Usage:
  export TRIX_API_KEY=your_api_key
  export TRIX_PROJECT_ID=your_project_id
  python examples/github_analytics.py
"""

import os
import sys

from trix import Trix


def print_section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


def show_velocity(client: Trix, project_id: str) -> None:
    print_section("PR Velocity")
    result = client.github.get_velocity(project_id)
    print(f"  Merged last 7 days:   {result.merged_last_7_days}")
    print(f"  Merged last 30 days:  {result.merged_last_30_days}")
    if result.avg_cycle_time_days is not None:
        print(f"  Avg cycle time:       {result.avg_cycle_time_days:.1f} days")
    else:
        print("  Avg cycle time:       no data yet")


def show_flagged_prs(client: Trix, project_id: str) -> None:
    print_section("Risk-Flagged PRs")
    result = client.github.get_flagged_prs(project_id)
    if not result.prs:
        print("  No risk-flagged PRs found.")
        return
    for pr in result.prs:
        print(f"\n  {pr.summary[:80]}")
        for flag in pr.flags:
            label = flag.removeprefix("pr:")
            print(f"    ⚠  {label}")


def show_cycle_time(client: Trix, project_id: str) -> None:
    print_section("Issue Cycle Time")
    result = client.github.get_cycle_time(project_id)
    trend = {"improving": "↓ faster", "worsening": "↑ slower"}.get(result.trend, "→ stable")
    print(f"  Trend: {trend}")
    if result.avg_cycle_days_last_30 is not None:
        print(f"  Avg close time (last 30d):  {result.avg_cycle_days_last_30:.1f} days")
    if result.avg_cycle_days_30_60 is not None:
        print(f"  Avg close time (prev 30d):  {result.avg_cycle_days_30_60:.1f} days")
    print(f"  Open issues:                {result.open_issue_count}")
    print(f"  Closed last 30 days:        {result.closed_last_30}")


def show_agent_attribution(client: Trix, project_id: str) -> None:
    print_section("AI vs Human Contributions")
    result = client.github.get_agent_attribution(project_id)
    total = result.agent_total + result.human_total
    if total == 0:
        print("  No commit or PR data synced yet.")
        return
    ai_pct = int(result.agent_ratio * 100)
    print(f"  Total commits:  {result.total_commits}")
    print(f"  Total PRs:      {result.total_prs}")
    print(f"  AI-assisted:    {ai_pct}%  ({result.agent_total}/{total})")
    print(f"  Human:          {100 - ai_pct}%  ({result.human_total}/{total})")
    if result.agent_breakdown:
        print("\n  By agent:")
        for agent, count in result.agent_breakdown.items():
            pct = int(count / total * 100) if total else 0
            bar = "█" * (pct // 5)
            print(f"    {agent:<12} {pct:>3}%  {bar}  ({count})")


def show_goal_progress(client: Trix, project_id: str) -> None:
    print_section("GitHub-Driven Goal Progress")
    result = client.github.get_goal_progress(project_id)
    if not result.goals:
        print("  No goals linked to GitHub issues.")
        return
    for g in result.goals:
        # progress is stored as 0.0–1.0; multiply by 100 for display
        progress = int(g.progress * 100)
        bar_len = progress // 10
        bar = "█" * bar_len + "░" * (10 - bar_len)
        print(f"  [{bar}] {progress:>3}%  {g.title}")


def show_file_complexity(client: Trix, project_id: str) -> None:
    print_section("File Complexity (top hotspots)")
    result = client.github.get_file_complexity(project_id)
    if not result.files:
        print("  No complexity data yet — run a repo scan first.")
        return
    for f in result.files[:10]:
        level = (f.complexity_level or "ok").upper()
        score = f"{f.hotspot_score:.2f}" if f.hotspot_score is not None else "—"
        cyc = f.cyclomatic_complexity or "—"
        print(f"  [{level:<8}] score={score}  cyc={cyc:<4}  {f.file_path}")


def generate_narrative(client: Trix, project_id: str, window_days: int = 7) -> None:
    print_section(f"Delivery Narrative (last {window_days} days)")
    print("  Generating…")
    result = client.github.generate_narrative(project_id, window_days=window_days)
    stored = "stored" if result.stored else "not stored"
    print(f"  [{stored}, {result.window_days}d window]\n")
    for line in result.narrative.split("\n"):
        if line.strip():
            print(f"  {line}")


def main() -> None:
    api_key = os.getenv("TRIX_API_KEY")
    project_id = os.getenv("TRIX_PROJECT_ID")

    if not api_key or not project_id:
        print("Error: set TRIX_API_KEY and TRIX_PROJECT_ID environment variables.")
        sys.exit(1)

    client = Trix(api_key=api_key)

    print("Trix GitHub Analytics — ADR-152")
    print(f"Project: {project_id}")

    show_velocity(client, project_id)
    show_flagged_prs(client, project_id)
    show_cycle_time(client, project_id)
    show_agent_attribution(client, project_id)
    show_goal_progress(client, project_id)
    show_file_complexity(client, project_id)

    # Uncomment to generate a new narrative (costs an LLM call):
    # generate_narrative(client, project_id, window_days=7)

    # Uncomment to backfill a repo connection (requires connection_id):
    # connection_id = os.environ.get("TRIX_CONNECTION_ID", "")
    # if connection_id:
    #     result = client.github.scan_repo(project_id, connection_id)
    #     print(f"\n  Scan: {result.commits} commits, {result.prs} PRs, {result.files} files")

    print("\nDone.")


if __name__ == "__main__":
    main()
