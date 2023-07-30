import os
import subprocess
import shutil


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"Command {command} ran successfully")
            return True, result.stdout
        print(f"Command {command} failed to run..")
        print(result.stderr)
        return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Exception while running the command.. {e}")
        return False, command


if __name__ == "__main__":

    # password = toor
    status, output = run_command("jupyter --config-dir")
    try:
        shutil.move("config/jupyter_lab_config.py", output.strip("\n"))
        shutil.move("config/jupyter_server_config.json", output.strip("\n"))
        print("copied the configs..")
    except shutil.Error:
        os.remove(os.path.join(output.strip("\n"), "jupyter_lab_config.py"))
        os.remove(os.path.join(output.strip("\n"), "jupyter_server_config.json"))
        shutil.move("config/jupyter_lab_config.py", output.strip("\n"))
        shutil.move("config/jupyter_server_config.json", output.strip("\n"))
        print("configs already exists..")
    os.chdir("notebooks")
    run_command("jupyter lab")
