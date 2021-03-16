import argparse
import sys
from collections import namedtuple

Time = namedtuple("Time", ["hour", "minute"])
Cron = namedtuple("Cron", ["minute", "hour", "command"])

ALL = "*"


def parse_time(value):
    """Parse a string for an HH:MM format."""
    parts = value.split(":")
    assert len(parts) == 2
    hour = int(parts[0])
    assert 0 <= hour < 24
    minute = int(parts[1])
    assert 0 <= minute < 60
    return Time(hour=hour, minute=minute)


def parse_hour(value):
    """Parse a string to detect the cron hour specifier."""
    if value == "*":
        return ALL
    number = int(value)
    assert 0 <= number < 24
    return number


def parse_minute(value):
    """Parse a string to detect the cron minute specifier."""
    if value == "*":
        return ALL
    number = int(value)
    assert 0 <= number < 60
    return number


def parse_line(line):
    """Parse a line to detect a crontab entry: minute hour command."""
    parts = line.split()
    assert len(parts) == 3
    minute = parse_minute(parts[0])
    hour = parse_hour(parts[1])
    command = parts[2]
    return Cron(minute, hour, command)


def determine_next_runtime(cron, ref_time):
    """Calculate the next run time for a cron entry including whether it should be run today or tomorrow."""
    if cron.minute == ALL:
        minute = ref_time.minute
    else:
        minute = cron.minute
    if cron.hour == ALL:
        hour = ref_time.hour
        if ref_time.minute > minute:
            hour += 1
    else:
        hour = cron.hour
    diff = (hour * 60 + minute) - (ref_time.hour * 60 + ref_time.minute)
    runtime = Time(hour=hour, minute=minute)
    tomorrow = diff < 0
    return runtime, tomorrow


parser = argparse.ArgumentParser(description="Cron command line interface.")
parser.add_argument("ref_time", type=str, nargs=1, help="Reference Time, eg 14:25")
args = parser.parse_args()

# Read the reference time as parsed on the command line.
ref_time = parse_time(args.ref_time[0])

# Go through each of the lines passed through stdin
for line in sys.stdin.readlines():
    # Parse each of the crontab lines.
    cron = parse_line(line)
    # Calculate its next run time.
    runtime, tomorrow = determine_next_runtime(cron, ref_time)
    # Output the next run time including whether its today or tomorrow along with the command to be run
    print(
        f"{runtime.hour}:{runtime.minute:02d} {'tomorrow'if tomorrow else 'today'} - {cron.command}"
    )
