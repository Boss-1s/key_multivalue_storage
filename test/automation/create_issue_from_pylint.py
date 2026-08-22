import json
import subprocess

def main():
    # 1. Load the Pylint JSON report
    with open('pylint_report.json', 'r') as f:
        errors = json.load(f)

    subprocess.run('gh issue list --json number,title,body > issues.json',
                   shell=True,
                   check=True,
                   capture_output=True)

    with open('issues.json', 'r') as f:
        existing_issues = json.load(f)

    # 2. Iterate through errors and create issues
    for i in range(len(errors['messages'])):
        error = errors['messages'][i]
        if error['type'] != 'error':
            continue  # Skip non-error messages

        msg_id: str = error['messageId']
        line: int = error['line']
        path: str = error['path']
        message: str = error['message']

        # Construct the GitHub Issue title and body
        title = f"fatal: pylint error {msg_id}"
        body = f"""
**File:** [{path}](https://github.com/Boss-1s/key_multivalue_storage/blob/semver1.4.x/{path})
**Line:** {line}
**Error ID:** {msg_id}

**Description:**
{message}
"""

        # Check if the issue already exists
        issue_exists = False
        issue_id = None
        for issue in existing_issues:
            issue_exists = title in issue['title'] and body in issue['body']
            if issue_exists:
                issue_id = issue['number']
                break

        if issue_exists:
            print(f"Issue already exists for {title}, with id {issue_id}, skipping...")
            continue

        # 3. Use the `gh` CLI to create the issue
        subprocess.run([
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', 'bug,pylint,Needs Triage'
            ], check=True, capture_output=True
        )

    print("Successfully processed all Pylint errors into GitHub issues!")


if __name__ == "__main__":
    main()
