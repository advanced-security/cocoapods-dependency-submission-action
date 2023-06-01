
import os
import yaml
from typing import Any, Optional, Union

from ghastoolkit.octokit.dependencygraph import Dependencies, Dependency

def findCocoaPods(path: str) -> list[str]:
    """Find all the CocoaPods Lock files"""
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file == "Podfile.lock":
                results.append(os.path.join(root, file))
    return results

def parsePod(pod: str) -> Dependency:
    namespace = None
    version = None

    if " " in pod:
        name, version = pod.split(" ", 1)
        # process `(`, `)`
        version = version.replace("(", "").replace(")", "")
        # process `= `, `~> `
        if " " in version:
            _, version = version.split(" ", 1)
        if "/" in name:
            namespace, name = name.split("/", 1)
    else:
        name = pod

    dep = Dependency(
        name,
        namespace=namespace,
        version=version,
        manager="cocoapods"
    )
    return dep

def createPod(deps: Dependencies, pods: Union[str, dict[str, Optional[list]]]) -> Dependencies:
    if isinstance(pods, str):
        deps.append(parsePod(pods))
    else:
        for pod, subpods in pods.items():
            deps.append(parsePod(pod))

            if subpods:
                for spod in subpods:
                    createPod(deps, spod)

    return deps

def parseLockFile(path: str) -> Dependencies:
    deps = Dependencies()
    with open(path, "r") as handle:
        data = yaml.safe_load(handle)
    
    for dep in data.get("PODS", []):
        createPod(deps, dep)

    return deps