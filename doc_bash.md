# Overview: shoretel_voicemail_backup.sh
Each ShoreTel voicemail has two components:
- the WAV file: This is the actual audio.
- the MSG file: This is what you receive in Communicator, informing you that you have a message. The MSG file contains information about the voicemail, like the Caller ID, which we want.

You will only have either a WAV **AND** MSG, or only a MSG.

The `check_path` function will:
- check to make sure the necessary directories on HQ/DVS are accessible.
  - if they are inaccessible:
    - inform user which of the two directories are inaccessible.
    - depending on the inaccessible directory, script will exit with exit code `10` or `20`.
    - **NOTE: if either is inaccessible, the script will exit, as both are needed.**
  - if they _are_ accessible:
    - silently continue

The `check_argument` function will check to make sure that:
- an argument is passed
- the argument (if passed) is an integer
  - if there is no argument, or the argument is a non-integer:
    - inform user, and include an example command
    - prompt user for an extension
      - while extension is null or non-integer, repeat prompt until an integer is passed, or user breaks out of loop.
      - if user provides an integer, assign integer to `extension` and continue on
  - if there is an integer passed as an argument:
    - assign integer to `extension` and continue on

The `check_extension` function will:
- check HQ/DVS for the required voicemail directories of the provided extension
  - if found:
    - a directory, named with the current date and time, and the provided extension, will be created on your Desktop
      - e.g. $HOME/Desktop/2017-1023_131000_1234
    - the contents of the necessary directories for that extension on the HQ/DVS server will be copied to this new folder
    - the information from Mailbox.dat will be parsed and the voicemail files will be renamed accordingly.
  - if NOT found:
    - script will exit with exit code `30`.

The `backup_voicemails` function will:
- use `strings` to remove the binary from the _Mailbox.dat_ file
- `awk` for anything that is exactly 9 characters, which, for our environment, is the Message ID, which we want.
- `backup_voicemails` then checks for a WAV with that Message ID
  - if a WAV with the Message ID is found:
    - tell us the WAV exists
    - copy the WAV (with -p to preserve file attributes, such as Date Modified) from HQ/DVS to the directory created by the `backup_voicemails` function
    - next, tell us renaming of the WAV will take place (again, only the local copy is being modified)
      - Note: Renaming of the WAV renames it from the Message ID, to include:
        - Date Modified: when the message was received (YYYY-MMDD_HHMMSS)
        - Caller ID: which we are awking from the MSG file.
  - if a WAV with the Message ID is NOT found:
    - tell us the WAV does not exist, then continue on.
