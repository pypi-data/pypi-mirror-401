import subprocess

def get_git_diff():
    result = subprocess.run(
        ["git", "diff", "--staged"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()
