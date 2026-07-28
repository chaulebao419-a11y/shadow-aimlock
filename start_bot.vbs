Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -WindowStyle Hidden -Command ""while($true){try{python C:\Users\BAOCHAU-PC\Desktop\app\aimlock_bot.py}catch{Start-Sleep -Seconds 5}}""", 0, False
