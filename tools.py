import subprocess
import tempfile
import os

def run_flake8(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)
    return result.stdout if result.stdout else "No flake8 issues found."

def run_pylint(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    result = subprocess.run(["pylint", tmp_path], capture_output=True, text=True)
    os.remove(tmp_path)
    return result.stdout if result.stdout else "No pylint issues found."

if __name__== "__main__":
    sample_code = "import os\nx=1\nprint(x)\n"
    print("FLAKE8 RESULTS:")
    print(run_flake8(sample_code))
    print("PYLINT RESULTS:")
    print(run_pylint(sample_code))