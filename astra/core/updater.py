import os
import subprocess

class Updater:
    def update(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        git_dir = os.path.join(repo_root, ".git")
        if not os.path.isdir(git_dir):
            print("AstraCLI updater: git repository not found; update unavailable.")
            return

        try:
            result = subprocess.run(
                ["git", "pull", "--ff-only"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip() or result.stderr.strip()
            print(output or "AstraCLI updated successfully.")
        except FileNotFoundError:
            print("AstraCLI updater: git is not installed.")
        except subprocess.CalledProcessError as exc:
            error = exc.stderr.strip() or exc.stdout.strip()
            print("AstraCLI updater failed:", error)
