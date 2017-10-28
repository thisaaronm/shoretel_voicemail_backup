# shoretel_voicemail_backup
---
# What's New
- 2017-1027
  - Updated shoretel_voicemail_backup.py
    - Supports Python 2.x and 3.x
    - Supports macOS _(tested on 10.12.6)_ and Windows _(tested on Windows 10 1703)_
  - Updated README.md
    - Moved _Overview_ to individual docs due to variations in the bash and python versions.
  - Created docs_bash.md
    - Outlines execution/logic flow of shoretel_voicemail_backup.sh
  - Created docs_py.md
    - Outlines execution/logic flow of shoretel_voicemail_backup.py

# Prerequisites
- shoretel_voicemail_backup.sh:
  - macOS (tested on 10.12.6)
- shoretel_voicemail_backup.py:
  - macOS (tested on 10.12.6), OR
  - Windows (tested on Windows 10 1703)
- "Vms" on HQ/DVS accessible. Should be able to navigate to:
  - `/Volumes/z$/Shoreline Data/Vms/SHORETEL`
  - `/Volumes/z$/Shoreline Data/Vms/Message`

# How To
- confirm above prerequisites are met
- clone and cd into this repo on your workstation
- execute the script(s), while passing a VALID extension as an argument
  - examples:
    - `./shoretel_voicemail_backup.sh 1234`
    - `./shoretel_voicemail_backup.py 1234`
    - `python shoretel_voicemail_backup.py 1234`

# Documentation  
- [doc_bash.md](https://github.com/thisaaronm/shoretel_voicemail_backup/blob/python/doc_bash.md)
- [doc_py.md](https://github.com/thisaaronm/shoretel_voicemail_backup/blob/python/doc_py.md)

---
# DISCLAIMER
This is only for use with locally hosted ShoreTel HQ/DVS. This does not apply to ShoreTel Cloud.  
This will not modify anything on HQ/DVS - file renaming only take place on your own workstation.

That being said:
- **READ THROUGH THE SCRIPTS FIRST!**
- **CUSTOMIZE `mailbox` AND `messages` FOR YOUR OWN ENVIRONMENT.**
- **I AM NOT RESPONSIBLE IF YOU HOSE YOUR HQ/DVS. SO, TEST.**
  - **TEST.**
    - **TEST AGAIN.**
---
### For any questions or comments, please contact me. Thanks!
