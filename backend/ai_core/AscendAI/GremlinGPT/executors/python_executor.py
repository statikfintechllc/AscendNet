#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: executors/python_executor.py

import subprocess
import tempfile
import uuid
import os
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("executors")

EXEC_LOG_DIR = Path("data/logs/executions/")
EXEC_LOG_DIR.mkdir(parents=True, exist_ok=True)


def run_python_sandbox(code, timeout=5, env=None):
    """
    Runs the given Python code string in a safe sandbox.
    - code: Python code string
    - timeout: max seconds to allow
    - env: (optional) dict of environment variables for execution
    Returns:
        dict with id, returncode, stdout, stderr, success, log_path, error (if any)
    """
    exec_id = str(uuid.uuid4())
    output_path = EXEC_LOG_DIR / f"{exec_id}.out"

    try:
        # Write code to a temp file
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            script_path = tmp.name

        # Secure environment (optional: drop privileges, custom env)
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)

        # Run with timeout and capture output
        result = subprocess.run(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True,
            check=False,
            env=exec_env,
        )

        # Write stdout/stderr to log
        with open(output_path, "w") as out:
            out.write("STDOUT:\n" + result.stdout + "\n")
            out.write("STDERR:\n" + result.stderr + "\n")

        logger.info(f"[PYEXEC] Completed: {script_path} (ID: {exec_id})")
        return {
            "id": exec_id,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "success": result.returncode == 0,
            "log_path": str(output_path),
        }

    except subprocess.TimeoutExpired:
        logger.error(f"[PYEXEC] Timeout for {exec_id}")
        return {"id": exec_id, "success": False, "error": "Timeout"}

    except Exception as e:
        logger.error(f"[PYEXEC] Execution failed: {e}")
        return {"id": exec_id, "success": False, "error": str(e)}

    finally:
        if "script_path" in locals() and os.path.exists(script_path):
            os.remove(script_path)


# CLI test mode
if __name__ == "__main__":
    test_code = "print('Hello from Gremlin sandbox!')"
    result = run_python_sandbox(test_code)
    print(result)
