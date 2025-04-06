import subprocess

def git_push():
    try:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "auto update"])
        command = ["git", "push", "--force"]
        subprocess.run(command)
        print(f"Git push command: {' '.join(command)}")
    except Exception as e:
        print(f"Git push failed: {e}")

if __name__ == "__main__":
    git_push()
