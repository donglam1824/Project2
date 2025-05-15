import subprocess
import os
import time

def run_script(script_name):
    """Run a Python script and print its output"""
    print(f"\n{'='*50}")
    print(f"Running {script_name}...")
    print(f"{'='*50}")
    
    try:
        # Run the script and capture output
        result = subprocess.run(['python', script_name], 
                                capture_output=True, 
                                text=True, 
                                check=True)
        
        # Print stdout
        print("\nOutput:")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nError running {script_name}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    # List of scripts to run in order
    scripts = [
        "map_generate.py",
        "waypoint_gpt.py",
        "waypoint_evaluation.py"
    ]
    
    # Check if all scripts exist before running
    missing_scripts = []
    for script in scripts:
        if not os.path.isfile(script):
            missing_scripts.append(script)
    
    if missing_scripts:
        print("Error: The following script files are missing:")
        for script in missing_scripts:
            print(f"- {script}")
        return
    
    # Run each script in sequence
    test = 10
    for i in range(test):
        print(f"Test{i}/{test}")
        for script in scripts:
            success = run_script(script)
            if not success:
                print(f"Pipeline stopped due to error in {script}")
                continue
            time.sleep(1)  # Small delay between scripts
    
    print("\nPipeline completed!")

if __name__ == "__main__":
    main()