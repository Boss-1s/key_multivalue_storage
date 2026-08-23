"""
[Automation. Do not use in production or as a tool for yourself. CI/CD integration only.]

Module that takes pylint JSON report and creates GitHub issues for severity error and above.
"""

import json
import subprocess
import warnings

try:
    import rich
except ImportError:
    rich = None
    warnings.warn("Rich library not found. Output will be less formatted.")

def open_issues():
    """
    Part 1: Issue creation for Pylint errors.

    ## Logic
    Issues are created for each Pylint **error** found in the JSON report.
    If an issue already exists for a specific error, it will not be created again.
    Note that only issues for a severity level of "error" or higher are created.
    """
    with open('pylint_report.json', 'r') as f:
        errors = json.load(f)

    subprocess.run('gh issue list --limit 10000 --json number,title,body > _issues.json',
                   shell=True,
                   check=True)

    with open('_issues.json', 'r') as f:
        existing_issues = json.load(f)

    for i in range(len(errors['messages'])):
        error = errors['messages'][i]
        if error['type'] != 'error':
            continue  # Skip non-error messages

        msg_id: str = error['messageId']
        line: int = error['line']
        path: str = error['path']
        message: str = error['message']

        title = f"fatal: pylint: pylint error {msg_id} at {path}:{line}"
        body = f"""
## Quick Glance

**File:** [{path}](https://github.com/Boss-1s/key_multivalue_storage/blob/semver1.4.x/{path})
**Line:** {line}
**Error ID:** {msg_id}

## Details

### Full JSON Message
```json
{json.dumps(error, indent=4)}
```

### Information

**Type:** `{error['type']}`
**Symbol**: `{error['symbol']}`
**Path:** `{error['path']}`
**Line:** {error['line']}
**Column:** {error['column']}
**Object:** `{error['obj']}`
**Module:** `{error['module']}`
**Pylint Message ID:** `{error['messageId']}`
**Confidence:** `{error['confidence']}`

**Error Message:**
```txt
{message}
```
"""

        # Check if the issue already exists
        issue_exists = False
        issue_id = None
        for issue in existing_issues:
            issue_exists = title in issue['title']
            if issue_exists:
                issue_id = issue['number']
                break

        if issue_exists:
            print(f"[yellow]Issue already exists for \"{title}\", with id {issue_id}![/]")
            continue

        # 3. Use the `gh` CLI to create the issue
        subprocess.run([
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', 'bug,pylint,Priority: CRITICAL'
            ], check=True)

    print("[b green]Successfully processed all Pylint errors into GitHub issues![/]")

def close_issues():
    """
    Part 2: Issue closure for resolved Pylint errors.

    ## Logic
    Issues are closed if they do not appear within the new Pylint report.
    Issues that do not begin with `fatal: pylint: pylint error ` are ignored,
    as they are not related to Pylint errors.
    """
    # 1. Load the Pylint JSON report
    with open('pylint_report.json', 'r') as f:
        report = json.load(f)
        errors = [error for error in report['messages'] if error['type'] == 'error']

    error_titles = []

    for error in errors:
        msg_id: str = error['messageId']
        line: int = error['line']
        path: str = error['path']
        error_titles.append(f"fatal: pylint: pylint error {msg_id} at {path}:{line}")

    subprocess.run('gh issue list --limit 10000 --json number,title,body > _issues.json',
                   shell=True,
                   check=True)

    with open('_issues.json', 'r') as f:
        existing_issues = json.load(f)

    # 2. Iterate through existing issues and close those that are resolved
    for issue in existing_issues:
        title = issue['title']
        issue_id = issue['number']

        if not title.startswith("fatal: pylint: pylint error "):
            continue  # Skip issues that are not related to Pylint errors

        if title not in error_titles:
            print(f"[green]Closing resolved issue \"{title}\" with id {issue_id}...[/green]")
            subprocess.run(['gh', 'issue', 'close', str(issue_id)], check=True)
            return

        print(f"[yellow]Issue \"{title}\" with id {issue_id} is still unresolved; skipping.[/]")

    print("[bold green]Successfully closed all resolved GitHub issues![/bold green]")

def main():
    """
    main.
    """
    print("[b green]Beginning to process Pylint errors and create GitHub issues...[/]")
    open_issues()
    print("[b green]Beginning to close GitHub issues that have been resolved in the codebase...[/]")
    close_issues()
    print("[b green]Finished processing Pylint errors and GitHub issues.[/]")


if __name__ == "__main__":
    if rich:
        from rich.console import Console
        from rich.traceback import install
        install(show_locals=True)
        console = Console()
        print = console.print #pylint: disable=redefined-builtin
    main()
