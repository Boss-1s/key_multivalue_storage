import json
import subprocess

def main():
    # 1. Load the Pylint JSON report
    with open('pylint_report.json', 'r') as f:
        errors = json.load(f)

    # 2. Iterate through errors and create issues
    for error in errors:
        msg_id = error['message-id']
        line = error['line']
        path = error['path']
        message = error['message']

        # Construct the GitHub Issue title and body
        title = f"[{msg_id}] Lint error in {path} at line {line}"
        body = f"**File:** {path}\n**Line:** {line}\n**Error ID:** {msg_id}\n\n**Description:**\n{message}"

        # 3. Use the `gh` CLI to create the issue
        subprocess.run([
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', 'bug,pylint,Needs Triage'
            ], check=True
        )

    print("Successfully processed all Pylint errors into GitHub issues!")


if __name__ == "__main__":
    main()
