if "%SUCCESS%" == "1" (
    python %CD%\AmatsukazeNotifier\AmatsukazeNotifier.py PostEncSuccess
)  else (
    python %CD%\AmatsukazeNotifier\AmatsukazeNotifier.py PostEncFailed
)