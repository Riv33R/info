param (
    [string]$SearchQuery
)

# Указание домена
$domain = "yourdomine.com"

# Указание OU, из которых нужно собирать данные
$organizationalUnits = @(
    "OU=example,DC=example,DC=com",
)

# Создание пустого массива для хранения данных
$userData = @()

foreach ($ou in $organizationalUnits) {
    # Получение всех пользователей из указанного OU
    $users = Get-ADUser -Filter * -SearchBase $ou -Server $domain -Property DisplayName, Title, TelephoneNumber

    foreach ($user in $users) {
        # Приведение номера телефона к строковому типу
        $phoneNumber = $user.TelephoneNumber
        if ($phoneNumber -ne $null) {
            $phoneNumber = $phoneNumber.ToString()
        }

        # Добавление данных пользователя в массив
        $userData += New-Object PSObject -Property @{
            "name"       = $user.DisplayName
            "jobtitle" = $user.Title
            "phone"   = $phoneNumber
        }
    }
}

# Экспорт данных в CSV файл
$userData | Export-Csv -Path "userdata.csv" -NoTypeInformation -Encoding UTF8
