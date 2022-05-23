if "%SUCCESS%" == "1" (
    %CD%\AmatsukazeNotifier\AmatsukazeNotifier.exe PostEncSuccess
)  else (
    %CD%\AmatsukazeNotifier\AmatsukazeNotifier.exe PostEncFailed
)
