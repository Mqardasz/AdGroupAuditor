# ta funkcja musi dostawać listę stanowisk [KAM, Logistyka ...]
# musi pobierać dla każdego stanowiska każdego usera i jego grupy
# JSON wygląda na tej zasadzie:
# Job Title: Employee: group A,group B, group C

function Get-UsersAndGroupsFromJobtitle {
    param(
    [Parameter(Mandatory = $true)]
    [System.Collections.IEnumerable]$JobTitles
    )

    $output = @{}

    foreach($job in $JobTitles) {
        $users = Get-ADUser -Filter "Title -eq '$job'" -Properties Title | Sort-Object -Property Name

        $userMap = @{}

        if($users.Count -eq 0) {
            $userMap["USER NOT FOUND"] = @()
        }
        else {
            foreach ($u in $users) {
                $groups (Get-ADPrincipalGroupMembership $u.samaccountname | Select-Object -ExpandProperty Name)

                $userMap[$u.Name] = $groups
            }
        }

        $output[$job] = $userMap

    }
    return $output | ConvertToJson -Depth 10
}