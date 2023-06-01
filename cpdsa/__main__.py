import os
import json
import logging
import argparse

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.dependencygraph import DependencyGraph

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
        lock_files.append(arguments.cocoapods_lock)
    else:
        lock_files = findCocoaPods(".")

    for lockfile in lock_files:
        logger.info(f"Lockfile found :: {lockfile}")

        dependencies = parseLockFile(lockfile)

        logger.info(f"Dependencies Count :: {len(dependencies)}")

        if not arguments.dry_run:
            depgraph.submitDependencies(
                dependencies, tool_name, lockfile, sha=arguments.sha, ref=arguments.ref
            )

            logger.info("Submitted BOM!")
        else:
            logger.info("Dry run mode, skipping submission")
            print(
                json.dumps(
                    dependencies.exportBOM(
                        tool_name, lockfile, sha=arguments.sha, ref=arguments.ref
                    ),
                    indent=2,
                )
            )

            logger.info(f"Dependency Count :: {len(dependencies)}")

    logger.info("Done")
