import json
import subprocess
from pathlib import Path

from excel_fetcher import ExcelFetcher

class AdExecutor:

    @staticmethod
    def resolve_scripts_path():
        # Looking for a file locally
        # It has to be seated in 'excel' folder
        project_root = Path(__file__).resolve().parents[1]

        # sets a path where excel should be located
        scripts_dir = project_root / "scripts"

        if not scripts_dir:
            raise FileNotFoundError(f"No scripts folder in {scripts_dir}")
        return scripts_dir


    @staticmethod
    def is_list_of_tuples(value):
        if not isinstance(value, list):
            return False
        return all(
            isinstance(item, tuple) and len(item) == 2
            for item in value
        )

# this function executes powershell function that takes reference users
# and returns reference user groups in JSON format
    @staticmethod
    def get_reference_user_groups(tuples):
        if AdExecutor.is_list_of_tuples(tuples):
            # Convert to PowerShell format: @("title","name"), ...
            ps_array = "@(" + ",".join(
                f'@("{t[0]}", "{t[1]}")' for t in tuples
            ) + ")"
            print(ps_array)
            ps_cmd = f"""
            $tuples = {ps_array}
            . "{AdExecutor.resolve_scripts_path()}\\getReferenceUserGroups.ps1"
            Get-UserGroupsFromTuples -UserTuples $tuples
            """

            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True
            )

            # Parse JSON back into Python dict
            groups = json.loads(result.stdout)
            print(groups)
        else:
            raise Exception("Invalid list of tuples, should be: [(str,str)]")

    #@staticmethod
    #def get_all_users_groups_grouped_by_jobtitle:




fetcher = ExcelFetcher()
print(AdExecutor.resolve_scripts_path())
#print(fetcher.rows) this is not up to date
AdExecutor.get_reference_user_groups(fetcher.rows)