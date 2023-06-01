import os
import logging
import argparse

from myaction import __name__ as name

logger = logging.getLogger(name)
parser = argparse.ArgumentParser(name)

parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("--ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-gr",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "-gi",
    "--github-instance",
    default=os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    help="GitHub Instance",
)
parser_github.add_argument(
    "-t",
    "-gt",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)


if __name__ == "__main__":
    arguments = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # My action workflow

