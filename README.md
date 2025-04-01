# cocoapods-dependency-submission-action

This is the [CocoaPods Dependency Submission Action](https://github.com/advanced-security/cocoapods-dependency-submission-action) which parses CocoaPods Lock files and submits the dependencies to the [Dependency Graph Submission API](https://docs.github.com/en/enterprise-cloud@latest/code-security/supply-chain-security/understanding-your-software-supply-chain/using-the-dependency-submission-api).

> [!WARNING]
> Sadly, [GitHub's Security Advisory Database](https://github.com/advisories) does not contain CocoaPods security alert information which means no security vulnerabilities in your dependencies will be reported.
> This project is mainly to keep your Software Bill of Materials up to date and complete.

## Usage

```yaml
- name: CocoaPods Dependency Submission Action
  uses: advanced-security/cocoapods-dependency-submission-action@v1.2.0
```

### Action Inputs

```yaml
- name: CocoaPods Dependency Submission Action
  uses: advanced-security/cocoapods-dependency-submission-action@v1.2.0
  with:
    # [optonal] The path to the Podfile.lock file. Defaults to finding all 
    # Podfile.lock in the current working directory
    cocoapods-lock: "./Podfile.lock"
    # [optional] Token used to authenticate with the GitHub API. Defaults to the GITHUB_TOKEN secret.
    token: ${{ secrets.ACTIONS_TOKEN }}
```

### Workflow Example

```yaml
name: Brew Lockfile Dependency Submission Action
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions: 
  contents: write   # needed

jobs:
  gradle-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # ... generate CocoaPods Podfile.lock

      - name: CocoaPods Dependency Submission Action
        uses: advanced-security/cocoapods-dependency-submission-action@v1.2.0
```

## License

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE) for the full terms.

## Maintainers

Maintained by [@GeekMasher](https://github.com/GeekMasher).

## Support

Please [create GitHub issues](https://github.com/GeekMasher/cocoapods-dependency-submission-action) for any feature requests, bugs, or documentation problems.

## Acknowledgement

- @GeekMasher: Author and Maintainer
