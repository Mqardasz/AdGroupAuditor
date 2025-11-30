import json
import subprocess

from excel_fetcher import ExcelFetcher

class AdExecutor:

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
        if tuples.is_list_of_tuples:
            # Convert to PowerShell format: @("title","name"), ...
            ps_array = "@(" + ",".join(
                f'@("{t[0]}", "{t[1]}")' for t in tuples
            ) + ")"

            ps_cmd = f"""
            $tuples = {ps_array}
            . .\\getReferenceUserGroups.ps1
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
#print(fetcher.rows) this is not up to date
AdExecutor.get_reference_user_groups(fetcher.rows)