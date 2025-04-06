import subprocess

def git_push():
    try:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "auto update"])
        subprocess.run(["git", "push origin master --force"])
    except Exception as e:
        print(f"Git push failed: {e}")

if __name__ == "__main__":
    git_push()
