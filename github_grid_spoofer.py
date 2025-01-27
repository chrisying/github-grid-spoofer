"""Spoofs your GitHub contributions grid to show any message.

See README.md for how to run.
"""

from datetime import datetime, timedelta
import os
import pytz
import random
import subprocess

# These constants can be changed
GITHUB_REPO = "git@github.com:chrisying/github-grid-spoofer"
TIMEZONE = pytz.timezone("America/Los_Angeles")
MESSAGE = [
    # Best viewed on a wide monitor
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
]
SPOOFED_COMMIT = "Why are you looking at my commit messages?"

# Probably don't need to change these
DRYRUN = True
MAX_WIDTH = 52
MAX_HEIGHT = 7
MIN_COMMITS = 20
MAX_COMMITS = 30
NOW = datetime.now().astimezone(TIMEZONE)
REPO_NAME = GITHUB_REPO.split("/")[-1]


def validate_message() -> None:
    assert all([len(row) == len(MESSAGE[0]) for row in MESSAGE]), "All rows must have same width"
    assert len(MESSAGE) <= MAX_HEIGHT, f"Height = {len(MESSAGE)} > Max height = {MAX_HEIGHT}"
    assert len(MESSAGE[0]) <= MAX_WIDTH, f"Width = {len(MESSAGE[0])} > Max width = {MAX_WIDTH}"


def unsafe_run_command(cmd: str) -> None:
    if DRYRUN:
        print(cmd)
    else:
        # Runs a command directly, definitely not safe from malicious code!
        assert subprocess.call(cmd, shell=True) == 0


def unix_time_with_offset(dt: datetime) -> str:
    assert dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None, "datetime must be aware"
    timestamp = int(dt.timestamp())
    offset = dt.strftime("%z")
    return f"{timestamp} {offset}"


def reset_git_history() -> None:
    # Warning: this is destructive! Run at your own peril!
    cwd = os.getcwd()
    assert os.path.split(cwd)[-1] == REPO_NAME, f"Must run this script from {REPO_NAME}/"

    unsafe_run_command("rm -rf .git")
    unsafe_run_command("git init")
    unsafe_run_command(f"git remote add origin {GITHUB_REPO}")
    unsafe_run_command("git add -A")
    # Any time longer than 1 year should ensure that it is gone from the grid
    two_years_ago = unix_time_with_offset(NOW - timedelta(weeks=104))
    unsafe_run_command(f"git commit -am \"Squashed commit of all non-spoofed code\" --date \"{two_years_ago}\"")


def start_of_week(dt: datetime) -> datetime:
    # Returns noon on the Sunday of this week
    sunday = dt - timedelta(days=(dt.weekday() + 1) % 7)  # weekday() on Monday == 0
    sunday = sunday.replace(hour=12, minute=0, second=0, microsecond=0)
    return sunday


def add_n_commits(day: datetime, n: int) -> None:
    for i in range(n):
        day_iso = day.isoformat()
        message = f"{SPOOFED_COMMIT} ({day_iso} {i+1}/{n})"

        day_str = unix_time_with_offset(day)
        unsafe_run_command(f"git commit -m \"{message}\" --allow-empty --date \"{day_str}\"")


def main() -> None:
    validate_message()
    print("Today's date: ", NOW)

    q = input("This script will destroy your git history, run for real? [y/N] ")
    if q in {"y", "Y"}:
        print("WARNING: Running for real!")
        global DRYRUN
        DRYRUN = False
    else:
        print("Doing dryrun, commands are printed but not executed...")

    reset_git_history()

    week_start = start_of_week(NOW) - timedelta(weeks=1)
    width = len(MESSAGE[0])
    height = len(MESSAGE)
    commit_count = 1  # reset_git_history created 1 commit

    # Builds columns backwards in time
    for col in range(width):
        print(f"Progress: {col + 1} / {width}")
        for row in range(height):
            if MESSAGE[row][width - col - 1] == 1:
                day = week_start + timedelta(days=row)
                n = random.randint(MIN_COMMITS, MAX_COMMITS)
                add_n_commits(day, n)
                commit_count += n
        week_start -= timedelta(weeks=1)

    print(f"Created {commit_count} commits. Please run `git push -f origin HEAD` to push your spoofed commits.")


if __name__ == "__main__":
    main()
