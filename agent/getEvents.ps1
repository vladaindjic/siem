param(
[string] $logFile,
[string] $datum
)
$datum_datum =[datetime]::ParseExact($datum,'ddMMyyyy_HHmmss',$null)
$logFile
$datum_datum
Get-EventLog -LogName $logFile -After ($datum_datum) | Format-List -Property *