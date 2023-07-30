import os
import subprocess
import shutil


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(f"Command {command} ran successfully")
            return True, result.stdout
        print(f"Command {command} failed to run..")
        print(result.stderr)
        return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Exception while running the command.. {e.stderr}")
        return False, command


if __name__ == "__main__":

    # password = toor
    status, output = run_command("jupyter --config-dir")
    try:
        os.remove(os.path.join(output.strip("\n"), "jupyter_lab_config.py"))
        os.remove(os.path.join(output.strip("\n"), "jupyter_server_config.json"))
    except shutil.Error:
        pass
    shutil.copy("config/jupyter_lab_config.py", output.strip("\n"))
    shutil.copy("config/jupyter_server_config.json", output.strip("\n"))
    shutil.copy("config/migrated", output.strip("\n"))
    print("configs already exists..")
    os.chdir("notebooks")
    run_command("jupyter lab --ip 0.0.0.0")
    print("Server is running...")
