from typing import Dict

import pathlib
from argparse import ArgumentParser

import argparse

import loggr


SQLITE_CACHE = "sqlite"
IN_MEMORY_CACHE = "in-memory"


def construct_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser("pyebasy")

    # the logging arguments
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Outputs no informative messages")

    parser.add_argument("--normal", "-l", action="store_true", default="true",
                        help="Sets the logging to normal, overall, logging (enabled by default)")

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Outputs more verbose messages")

    parser.add_argument("--tracing", "-t", action="store_true",
                        help="Outputs detailed tracing informations")

    # caches
    parser.add_argument("--source-cache-format", type=str, choices=[IN_MEMORY_CACHE, SQLITE_CACHE],
                        default=SQLITE_CACHE, metavar="source_cache_format",
                        help="Specifies the format of the source cache (in-memory or sqlite)")

    parser.add_argument("--destination-cache-format", type=str, choices=[IN_MEMORY_CACHE, SQLITE_CACHE],
                        default=SQLITE_CACHE, metavar="destination_cache_format",
                        help="Specifies the format of the destination cache (in-memory or sqlite)")

    parser.add_argument("--update-source-cache", action=argparse.BooleanOptionalAction, default="true",
                        metavar="update_source_cache",
                        help="Enables/skips the source cache update (enabled by default)")

    parser.add_argument("--update-destination-cache", action=argparse.BooleanOptionalAction, default="true",
                        metavar="update_destination_cache",
                        help="Enables/skips the destination cache update (enabled by default)")

    parser.add_argument("SOURCE_PATH", type=str, action="store",
                        help="The path to the directory which to synchronize (the source)")

    parser.add_argument("DESTINATION_PATH", type=str, action="store",
                    help="The path to the directory which to synchronize to (the destination)")

    return parser


def configure_logging(parsed):
    verbocity = None
    if parsed.quiet:
        verbocity = loggr.QUIET_VERBOCITY
    if parsed.normal:
        verbocity = loggr.NORMAL_VERBOCITY
    if parsed.verbose:
        verbocity = loggr.VERBOSE_VERBOCITY
    if parsed.tracing:
        verbocity = loggr.TRACING_VERBOCITY

    loggr.set_verbocity(verbocity)


def parse_args() -> argparse.Namespace:
    parser = construct_parser()
    parsed = parser.parse_args()
    configure_logging(parsed)

    return parsed

