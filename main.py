import os
import shutil
import psutil

def terminate_revit_process():
    """Terminate any running Revit process."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] and process.info['name'].lower() == 'revit.exe':
            print("Revit is running. Terminating process...")
            process.terminate()
            process.wait()
            print("Revit process terminated.")

def delete_files_and_folders(base_path):
    """Delete all files and folders in the specified path."""
    if os.path.exists(base_path):
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Remove file or symbolic link
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directory
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")

def clean_revit_journals_and_cache():
    """Clean Revit journals and CollaborationCache for specified versions."""
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("Unable to find user profile directory.")
        return

    base_revit_path = os.path.join(user_profile, "AppData", "Local", "Autodesk", "Revit")
    revit_versions = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024','2025']

    # Clean journal files for all versions
    for version in revit_versions:
        journals_path = os.path.join(base_revit_path, f"Autodesk Revit {version}", "Journals")
        print(f"Cleaning journal files for Revit {version}...")
        delete_files_and_folders(journals_path)

    # Clean CollaborationCache for 2022, 2023, 2024
    for version in ['2022', '2023', '2024','2025']:
        collab_cache_path = os.path.join(base_revit_path, f"Autodesk Revit {version}", "CollaborationCache")
        print(f"Cleaning CollaborationCache for Revit {version}...")
        delete_files_and_folders(collab_cache_path)

if __name__ == "__main__":
    terminate_revit_process()
    clean_revit_journals_and_cache()
    print("Cleanup completed.")
