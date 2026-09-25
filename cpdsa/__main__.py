import os
import json
import logging
import argparse

from datetime import datetime, timezone

from ghastoolkit import Dependencies, GitHub, DependencyGraph

from cpdsa import __name__ as tool_name
from cpdsa.cocoapods import parseLockFile, findCocoaPods

logger = logging.getLogger(tool_name)
parser = argparse.ArgumentParser(tool_name)

parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
parser.add_argument("-l", "--cocoapods-lock", help="CocoaPods Lockfile location")

parser.add_argument("--sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("--ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-r",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "--github-instance",
    default=os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
    help="GitHub Instance",
)
parser_github.add_argument(
    "-t",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)


def exportSnapshot(
    dependencies: Dependencies, path: str, sha: str = "", ref: str = ""
) -> dict:
    """Export the dependency snapshot payload.

    ghastoolkit sets `scanned` to a naive local timestamp which the snapshots
    API rejects, so it is replaced with an RFC 3339 UTC timestamp.
    """
    bom = dependencies.exportBOM(tool_name, path, sha=sha, ref=ref)
    bom["scanned"] = (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    return bom


if __name__ == "__main__":
    arguments = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG
        if arguments.debug or os.environ.get("DEBUG")
        else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    lock_files = []

    GitHub.init(
        repository=arguments.github_repository,
        token=arguments.github_token,
        instance=arguments.github_instance,
    )
    if not GitHub.repository:
        raise Exception("Repository not set")

    depgraph = DependencyGraph(GitHub.repository)
    logger.debug(f"GitHub Instance :: {GitHub}")
    logger.debug(f"Repository :: {GitHub.repository}")

    if arguments.cocoapods_lock:
        logger.info(f"Lockfile provided :: {arguments.cocoapods_lock}")
        lock_files.append(arguments.cocoapods_lock)
    else:
        logger.info("Lockfile not provided, searching for lockfiles")
        lock_files = findCocoaPods(".")

    for lockfile in lock_files:
        logger.info(f"Lockfile found :: {lockfile}")

        dependencies = parseLockFile(lockfile)

        logger.info(f"Dependencies Count :: {len(dependencies)}")

        if not arguments.dry_run:
            depgraph.rest.postJson(
                "/repos/{owner}/{repo}/dependency-graph/snapshots",
                exportSnapshot(
                    dependencies, lockfile, sha=arguments.sha, ref=arguments.ref
                ),
                expected=201,
            )

            logger.info("Submitted BOM!")
        else:
            logger.info("Dry run mode, skipping submission")
            print(
                json.dumps(
                    exportSnapshot(
                        dependencies, lockfile, sha=arguments.sha, ref=arguments.ref
                    ),
                    indent=2,
                )
            )

            logger.info(f"Dependency Count :: {len(dependencies)}")

    logger.info("Done")
