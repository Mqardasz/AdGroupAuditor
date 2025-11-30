function Get-UserGroupsFromTuples {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IEnumerable]$UserTuples
    )

    $output = @{}

    foreach ($tuple in $UserTuples) {
        $jobTitle = $tuple[0]
        $fullName = $tuple[1]

        # Try to find user in AD
        $user = Get-ADUser -Filter "Name -eq '$fullName'" -Properties MemberOf -ErrorAction SilentlyContinue

        if ($null -eq $user) {
            $output[$jobTitle] = @("USER NOT FOUND")
            continue
        }

        # Collect group names
        $groups = $user.MemberOf | ForEach-Object {
            (Get-ADGroup $_).Name
        }

        $output[$jobTitle] = $groups
    }

    # return JSON
    return ($output | ConvertTo-Json -Depth 5)
}
