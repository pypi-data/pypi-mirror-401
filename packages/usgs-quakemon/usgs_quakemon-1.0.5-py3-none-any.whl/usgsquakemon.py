#!/usr/bin/python3

"""
This program displays a list of recent earthquakes.
Parses GeoJSON API Endpoint from https://earthquake.usgs.gov
and displays the result as optional color coded list in the terminal.
Color requires a terminal that supports 256 colors.

The PAGER status colors are taken from https://earthquake.usgs.gov/data/pager/background.php
The suggested levels of response are:
no response needed -> green,
local/regional     -> yellow,
national           -> orange,
international      -> red
"""

# native imports
import argparse
from dataclasses import dataclass
import errno
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

# third party imports
import requests
from tabulate import tabulate

# small performance optimization
tabulate.WIDE_CHARS_MODE = False

# constants
VERSION = "1.0.5"
DESCRIPTION = """
Monitor recent earthquakes reported by USGS at https://earthquake.usgs.gov.
If no arguments are specified, the significant earthquakes for the day (--day)
is output by default.

USGS has developed PAGER: an automated system for rapidly estimating impact,
exposure, fatalities, and losses. Color-coded alerting determines the
suggested levels of response: no response needed (green), local/regional (yellow),
national (orange), or international (red).

+-------------------------+----------------------+---------------------------+
| Alert Level and Color   | Estimated Fatalities | Estimated Losses (USD)    |
+-------------------------+----------------------+---------------------------+
| Red                     | 1,000+               | $1 billion+               |
| Orange                  | 100 - 999            | $100 million - $1 billion |
| Yellow                  | 1 - 99               | $1 million - $100 million |
| Green                   | 0                    | < $1 million              |
+-------------------------+----------------------+---------------------------+
"""
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_TIMEOUT = 10
DEFAULT_REFRESH = 300  # 5 minutes in seconds
MAGS = (45, 25, 10)
MAX_REFRESH = 86400  # 24 hours in seconds
MIN_REFRESH = 60
PAGERS = ("red", "orange", "yellow", "green")
QUAKECOLORS = {
    # pager
    "green": "\033[38;5;046m",
    "orange": "\033[38;5;208m",
    "red": "\033[38;5;009m",
    "reset": "\033[0m",
    "yellow": "\033[38;5;011m",
    # magnitude
    "mag8": "\033[38;5;201m",
    "mag7": "\033[38;5;001m",
    "mag6": "\033[38;5;196m",
    "mag5": "\033[38;5;202m",
    "mag4": "\033[38;5;226m",
    "mag3": "\033[38;5;216m",
    "mag2": "\033[38;5;033m",
    "mag1": "\033[38;5;006m",
}
RESULT_WARNING_THRESHOLD = 50
UNITS = ("hour", "day", "week", "month")


# classes
@dataclass
# this is a basic script, we can tolerate a few too many attributes
# pylint: disable=too-many-instance-attributes
class GlobalState:
    """use class to store global states"""

    progname: str
    acceptwarn: bool = False
    alerted: bool = False
    enablecolor: bool = True
    eventbase: str = ""
    geolink: bool = False
    localtime: bool = True
    runonce: bool = False
    usgslink: bool = True
    shortlink: bool = False


@dataclass
class GlobalConfig:
    """use class to store global config"""

    alarm: list
    pageralerts: list
    apitimeout: int = DEFAULT_TIMEOUT
    magalert: float = 666.666
    refresh: int = DEFAULT_REFRESH
    timeformat: str = DEFAULT_TIME_FORMAT


# functions
def clear_screen():
    """clear screen using subprocess"""
    try:
        if os.name == "nt":
            subprocess.run("cls", shell=True, check=True)
        else:
            subprocess.run(["clear"], check=True)
    except (subprocess.SubprocessError, OSError):
        # Fallback to ANSI escape
        sys.stdout.write("\033[H\033[J")
        handle_output("flush")


def colorize_string(color: str, enablecolor: bool, string: str) -> str:
    """conditionally colorize a string"""
    if enablecolor:
        return f"{QUAKECOLORS[color]}{string}{QUAKECOLORS['reset']}"
    return string


def confirmation_prompt(prompt: str) -> bool:
    """confirm yes/no prompt"""
    try:
        response = input(f"{prompt} (y/n): ").lower().strip()
    except KeyboardInterrupt:
        print()
        return False
    return response in ["y", "yes"]


def convert_magnitude(magnitude: float, magstr: str, enablecolor: bool) -> str:
    """convert magnitude into desired printable strings"""
    if magnitude >= 8.5:
        result = colorize_string("mag8", enablecolor, magstr)
    elif magnitude >= 7.5:
        result = colorize_string("mag7", enablecolor, magstr)
    elif magnitude >= 6.5:
        result = colorize_string("mag6", enablecolor, magstr)
    elif magnitude >= 5.5:
        result = colorize_string("mag5", enablecolor, magstr)
    elif magnitude >= 4.5:
        result = colorize_string("mag4", enablecolor, magstr)
    elif magnitude >= 3.5:
        result = colorize_string("mag3", enablecolor, magstr)
    elif magnitude >= 2.5:
        result = colorize_string("mag2", enablecolor, magstr)
    elif magnitude >= 1.5:
        result = colorize_string("mag1", enablecolor, magstr)
    else:
        result = magstr
    return result


def convert_seconds_to_human_readable(seconds: int) -> str:
    """convert seconds to human readable output"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or len(parts) == 0:
        parts.append(f"{secs}s")

    return " ".join(parts)


def get_earthquake(
    feature: dict, state: GlobalState, config: GlobalConfig
) -> list:
    """returns a list of properties for one earthquake"""
    properties = feature["properties"]

    # time is given in milliseconds since epoch
    utctime = datetime.fromtimestamp(properties["time"] / 1000, timezone.utc)
    localtime = utctime.astimezone()
    timestamp = localtime if state.localtime else utctime

    # colorize magnitude
    magnitude: float = properties["mag"]

    # send alarm based on magnitude
    if magnitude >= config.magalert and state.alerted is False:
        if len(config.alarm) >= 1:
            state.alerted = run_custom_alarm(state.progname, config.alarm)
        else:
            print("\a", end="")
        state.alerted = True  # page only once per refresh

    # alert property is the PAGER status
    alertprop = properties["alert"]
    if isinstance(alertprop, str) and alertprop.lower() in PAGERS:
        alert = colorize_string(alertprop, state.enablecolor, alertprop.upper())
        if alertprop.lower() in config.pageralerts and state.alerted is False:
            if len(config.alarm) >= 1:
                state.alerted = run_custom_alarm(state.progname, config.alarm)
            else:
                print("\a", end="")
            state.alerted = True
    else:
        alert = "-"

    results = [
        timestamp.strftime(config.timeformat),
        convert_magnitude(magnitude, f"{magnitude:.1f}", state.enablecolor),
        properties["place"],
        alert,
    ]

    [eventbase, eventid] = str(properties["url"]).rsplit("/", maxsplit=1)
    eventurl = f"{eventbase}/{eventid}"
    state.eventbase = eventbase

    if state.shortlink:
        eventurl = eventid

    if state.usgslink:
        results.append(eventurl)

    if state.geolink:
        coordinates = feature["geometry"]["coordinates"]
        results.append(
            f"geo:{coordinates[1]},{coordinates[0]},{coordinates[2]}"
        )

    return results


def get_request(
    progname: str, url: str, timeout: int
) -> requests.models.Response:
    """get request with retry"""
    result = None
    for attempt in range(3):
        try:
            result = requests.get(url, timeout=timeout)
            result.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                print(f"{progname}: error: {e}", file=sys.stderr)
                sys.exit(1)
            time.sleep(2**attempt)
    return result


def get_sites() -> str:
    """generate API site URLs"""
    base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary"
    url = {
        f"{unit}{mag}": f"{base_url}/{mag / 10}_{unit}.geojson"
        for unit in UNITS
        for mag in MAGS
    }
    url.update(
        {f"all_{unit}": f"{base_url}/all_{unit}.geojson" for unit in UNITS}
    )
    url.update(
        {
            f"significant_{unit}": f"{base_url}/significant_{unit}.geojson"
            for unit in UNITS
        }
    )
    return url


def handle_output(operation: str = "flush") -> bool:
    """simplify output flush/close"""
    try:
        if operation == "flush":
            sys.stdout.flush()
            sys.stderr.flush()
        elif operation == "close":
            sys.stdout.close()
            sys.stderr.close()
        elif operation == "line_buffer":
            sys.stdout.reconfigure(line_buffering=True)
            sys.stderr.reconfigure(line_buffering=True)
        return True
    except (OSError, AttributeError):
        return False


def init_args(
    parser: argparse.ArgumentParser, state: GlobalState
) -> argparse.Namespace:
    """initialize arguments"""
    parser.add_argument(
        "-a",
        "--alarm",
        help='set a custom alarm command, this disables the terminal bell alarm, for example using\
            the sox utility: "play -q ~/Audio/quake-alarm.wav"',
        type=str,
    )
    parser.add_argument(
        "-f",
        "--follow",
        help="enable follow mode like tail, (default: False)",
        action="store_true",
    )
    parser.add_argument(
        "-g",
        "--geo-link",
        help=f"enable geo: link column, (default: {state.geolink})",
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--magnitude",
        help="enable audible alarm (defaults to terminal bell) for specified magnitude threshold,\
            value >= mag will trigger the alarm",
        type=float,
    )
    parser.add_argument(
        "-l",
        "--localtime",
        help=f"display timestamps in local timezone, (default: {state.localtime})",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--pager",
        help=f"enable audible alarm (defaults to terminal bell) for desired pager, valid pagers are\
            {PAGERS}",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-n",
        "--no-usgs-link",
        help=f"disable the More Info column displaying USGS link, (default: {not state.usgslink})",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--usgs-short-link",
        help=f"display only the USGS eventpage ID instead of the entire link, (default:\
            {state.shortlink})",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--refresh",
        help=f'set the API request refresh rate in optional time unit, omitted unit presumes "s"\
            (seconds); minimum {convert_seconds_to_human_readable(MIN_REFRESH)}, maximum\
            {convert_seconds_to_human_readable(MAX_REFRESH)} (default:\
            {convert_seconds_to_human_readable(DEFAULT_REFRESH)})',
        type=str,
    )
    parser.add_argument(
        "-ro",
        "--run-once",
        help=f"disable watch and run a single loop (default: {state.runonce})",
        action="store_true",
        default=state.runonce,
    )
    parser.add_argument(
        "-t",
        "--time-format",
        help=f"set an strptime compatible string to customize the time format (default:\
            {DEFAULT_TIME_FORMAT.replace('%', '%%')})",
        type=str,
    )
    parser.add_argument(
        "--color",
        help=f"control color output (default: {state.enablecolor})",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--api-timeout",
        help=f"set the API request timeout value in seconds, minimum {DEFAULT_TIMEOUT} (default:\
            {DEFAULT_TIMEOUT})",
        type=int,
        nargs=1,
    )
    parser.add_argument(
        "--accept-warning",
        help=f"accept/suppress all warning prompts (default: {state.acceptwarn})",
        action="store_true",
        default=state.acceptwarn,
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {VERSION}"
    )

    group = parser.add_mutually_exclusive_group()
    for unit in UNITS:
        for mag in MAGS:
            group.add_argument(
                f"-{unit[0]}{mag}",
                f"--{unit}{mag}",
                help=f"show earthquakes >= M{mag / 10:.1f} for the last {unit}",
                action="store_true",
            )
        group.add_argument(
            f"-{unit[0]}s",
            f"--{unit}",
            help=f"show significant earthquakes for the {unit}",
            action="store_true",
        )
        group.add_argument(
            f"-{unit[0]}a",
            f"--{unit}-all",
            help=f"show all earthquakes for the last {unit}",
            action="store_true",
        )
    return parser.parse_args()


def is_executable(file):
    """check if a file exists and is executable"""
    path = Path(file)

    # handle relative or absolute
    if (
        path.is_absolute()
        or file.startswith(("./", "../", ".\\", "..\\"))
        or os.path.sep in file
        or (os.path.altsep and os.path.altsep in file)
    ):
        # handle symlinks
        followed = path.resolve()
        return followed.is_file() and os.access(followed, os.X_OK)

    # handle name only
    return shutil.which(path) is not None


def print_table(
    url: str, follow: bool, state: GlobalState, config: GlobalConfig
):
    """prints the table of all earthquakes"""
    req = get_request(state.progname, url, config.apitimeout)
    earthquakes = req.json()
    currenttime = (
        datetime.now() if state.localtime else datetime.now(timezone.utc)
    )
    quakelist = [
        get_earthquake(f, state, config) for f in earthquakes["features"]
    ]
    tz_name = (
        str(time.localtime().tm_zone)
        if state.localtime
        else str(currenttime.tzinfo)
    )
    quakeheaders = [
        f"Time ({tz_name})",
        "Mag",
        "Location",
        "PAGER",
    ]

    if state.usgslink:
        quakeheaders.append("More info")

    if state.geolink:
        quakeheaders.append("Geo link")

    events_found = len(quakelist)

    if events_found >= RESULT_WARNING_THRESHOLD and not state.acceptwarn:
        if confirmation_prompt(
            f"""Warning, {events_found} is greater than {RESULT_WARNING_THRESHOLD}.

The --accept-warning argument can be used to bypass this prompt.
Choosing yes here will suppress subsequent warnings.

Continue?"""
        ):
            state.acceptwarn = True
            print("Continuing...")
        else:
            print("Aborting...")
            sys.exit(1)

    if not follow and os.isatty(sys.stdout.fileno()):
        clear_screen()

    refreshstr = ""
    if not state.runonce:
        refreshstr = f", refreshing every {convert_seconds_to_human_readable(config.refresh)}"

    print(f"{earthquakes['metadata']['title']}{refreshstr}")
    print(
        f"Current Time ({tz_name}): {currenttime.strftime(config.timeformat)}"
    )
    if state.shortlink and state.eventbase != "":
        print(f"Event base URL: {state.eventbase}/")
    print(f"Events found: {events_found}")

    if not follow:
        print(tabulate(quakelist, headers=quakeheaders, floatfmt=".1f"))
    else:
        print(" | ".join(quakeheaders))
        for x in quakelist:
            print(" | ".join(x))


def parse_arg_to_seconds(arg: str) -> int:
    """parse argument time string to seconds"""

    if len(arg) < 2:
        raise ValueError(
            "invalid argument, {number} or {number}{unit} required"
        )

    # extract
    unit = "s"
    if not arg[-1].isdigit():
        unit = arg[-1]
        value = float(arg[:-1])
    else:
        value = float(arg)

    # convert
    if unit == "s":
        result = int(value)
    elif unit == "m":
        result = int(value * 60)
    elif unit == "h":
        result = int(value * 3600)
    else:
        raise ValueError(
            'invalid argument unit, use "s" for seconds, "m" for minutes, or "h" for hours'
        )

    # ensure minimum
    if result < MIN_REFRESH:
        raise ValueError(
            f'requires minimum value {MIN_REFRESH}, {MIN_REFRESH}s, or\
 {convert_seconds_to_human_readable(MIN_REFRESH)}" not: "{arg}"'
        )

    # ensure maximum
    if result > MAX_REFRESH:
        raise ValueError("invalid duration, greater than 24 hours")

    return result


def process_args(
    args: argparse.Namespace, state: GlobalState, config: GlobalConfig
):
    # we only process args once...
    # pylint: disable=too-many-branches
    """process arguments"""
    if isinstance(args.alarm, str):
        if args.alarm != "":
            try:
                config.alarm = shlex.split(args.alarm)
            except ValueError as e:
                print(
                    f"{state.progname}: error parsing argument -a/--alarm command: {e}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if not is_executable(config.alarm[0]):
                print(
                    f"{state.progname}: alarm error: command not found or is not\
 executable: {config.alarm[0]}",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            print(
                f"{state.progname}: error: argument -a/--alarm requires an input string",
                file=sys.stderr,
            )
            sys.exit(1)
    if isinstance(args.pager, list):
        for pager in args.pager:
            if pager not in PAGERS:
                print(
                    f'{state.progname}: error: argument -p/--pager: requires input of\
 {PAGERS} not: "{pager}"',
                    file=sys.stderr,
                )
                sys.exit(1)
        config.pageralerts = args.pager
    if args.refresh:
        if args.run_once:
            print(
                f"{state.progname}: error: arguments -r/--refresh and -ro/--run-once cannot\
 be used simultaneously",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            refresh = parse_arg_to_seconds(args.refresh)
            config.refresh = refresh
        except ValueError as e:
            print(
                f"{state.progname}: error: argument -r/--refresh: {e}",
                file=sys.stderr,
            )
            sys.exit(1)
    if args.api_timeout:
        if args.api_timeout[0] > config.apitimeout:
            config.apitimeout = args.api_timeout[0]
        elif not args.api_timeout[0] == config.apitimeout:
            print(
                f'{state.progname}: error: argument --api-timeout: requires minimum value\
 "{DEFAULT_TIMEOUT}" not: "{args.api_timeout[0]}"',
                file=sys.stderr,
            )
            sys.exit(1)
    if args.time_format:
        if validate_time_format(args.time_format):
            config.timeformat = args.time_format
        else:
            print(
                f'{state.progname}: error: argument -t/--time-format: requires strftime\
 format like "{DEFAULT_TIME_FORMAT}" not: "{args.time_format}"',
                file=sys.stderr,
            )
            sys.exit(1)


def select_site(args: argparse.Namespace, state: GlobalState) -> str:
    """parse args to select a site"""
    urls = get_sites()
    site = urls["significant_day"]
    for unit in UNITS:
        for mag in MAGS:
            if getattr(args, f"{unit}{mag}", True):
                if (
                    (unit == "day" and mag == 10)
                    or unit in ("week", "month")
                    and not state.acceptwarn
                ):
                    # warn about results
                    if confirmation_prompt(
                        f"""Warning, magnitude >= {mag} results for the {unit} can number in the\
 hundreds.

The --accept-warning argument can be used to bypass this prompt.
Choosing yes here will suppress subsequent warnings.

Continue?"""
                    ):
                        state.acceptwarn = True
                        print("Continuing...")
                    else:
                        print("Aborting...")
                        sys.exit(1)
                site = urls[f"{unit}{mag}"]
        if getattr(args, f"{unit}", True):
            site = urls[f"significant_{unit}"]
        if getattr(args, f"{unit}_all", True):
            if unit in ("day", "week", "month") and not state.acceptwarn:
                # warn about results
                if confirmation_prompt(
                    f"""Warning, all results for the {unit} can number in the hundreds.

The --accept-warning argument can be used to bypass this prompt.
Choosing yes here will suppress subsequent warnings.

Continue?"""
                ):
                    state.acceptwarn = True
                    print("Continuing...")
                else:
                    print("Aborting...")
                    sys.exit(1)
            site = urls[f"all_{unit}"]
    return site


def run_custom_alarm(progname: str, alarm: list) -> bool:
    """execute custom subprocess triggered by alerts"""
    try:
        # we want this to be non-blocking
        # pylint: disable=consider-using-with
        subprocess.Popen(alarm, shell=False)
    except subprocess.TimeoutExpired:
        print(
            f"{progname}: alarm error: command timed out",
            file=sys.stderr,
        )
        return False
    # broad except is the intention here
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(
            f"{progname}: alarm error: command unexpected error: {e}",
            file=sys.stderr,
        )
        return False
    return True


def validate_time_format(timefmt: str) -> bool:
    """test a strptime string format"""
    if "%" not in timefmt:
        return False
    try:
        timestr = datetime.now().strftime(timefmt)
        datetime.strptime(timestr, timefmt)
        return True
    except ValueError:
        return False


def main():
    """main function to parse arguments and watch for earthquakes"""
    if not os.isatty(sys.stdout.fileno()):
        handle_output("line_buffer")  # pipe compatibility

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    state = GlobalState(
        progname=parser.prog, enablecolor=os.isatty(sys.stdout.fileno())
    )
    config = GlobalConfig(
        pageralerts=[],
        alarm=[],
        apitimeout=DEFAULT_TIMEOUT,
        refresh=DEFAULT_REFRESH,
        timeformat=DEFAULT_TIME_FORMAT,
    )

    args = init_args(parser, state)
    state.acceptwarn = args.accept_warning
    site = select_site(args, state)
    process_args(args, state, config)

    if isinstance(args.color, bool):
        state.enablecolor = args.color
    state.geolink = args.geo_link
    state.localtime = args.localtime
    if args.no_usgs_link:
        state.usgslink = False
    state.shortlink = args.usgs_short_link
    state.runonce = args.run_once
    if isinstance(args.magnitude, float):
        config.magalert = args.magnitude

    while True:
        try:
            print_table(site, args.follow, state, config)
            if args.follow and not args.run_once:
                print()
            state.alerted = False
            if state.runonce:
                break
            time.sleep(config.refresh)
        except KeyboardInterrupt:
            handle_output("close")
            break
        except BrokenPipeError:
            handle_output("close")
            break


if __name__ == "__main__":
    try:
        main()
    except IOError as e:
        if e.errno == errno.EPIPE:
            # ignore pipe error trace
            pass
