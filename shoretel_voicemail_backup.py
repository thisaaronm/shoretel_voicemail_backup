#!/usr/bin/env python3

import os
import sys
from datetime import datetime
import string
import shutil


# -------------------------------- VARIABLES --------------------------------- #
mailbox = "/Volumes/d$/Shoreline Data/Vms/SHORETEL"
messages = "/Volumes/d$/Shoreline Data/Vms/Message"


# -------------------------------- FUNCTIONS --------------------------------- #
def check_path(p):
    """
    Check if required HQ/DVS directory is accessible.
    """
    if os.path.isdir(p):
        # print("\nINFO: {0} exists.\n".format(a))
        pass
    elif not os.path.isdir(p):
        print("\nERROR: {0} does not exist.\n".format(p))
        sys.exit(10)
    else:
        print("\nERROR: An unknown error has occurred.\n")
        raise
        sys.exit(20)


def check_argument():
    """
    Check for extension argument
    """
    try:
        ext = int(sys.argv[1])
        return ext
    except IndexError as err_idx:
        print("\nERROR: Extension argument not provided.\n")
        sys.exit(30)
    except ValueError as err_val:
        print("\nERROR: Extension argument is non-integer.\n")
        sys.exit(40)
    except:
        print("\nERROR: An unknown error has occurred.\n")
        raise
        sys.exit(50)


def check_extension(p, e):
    """
    Checks for the mailbox of the provided extension.
    """
    if os.path.isdir("{0}/{1}".format(p, str(e))):
        homedir = os.path.expanduser('~')

        ## swap datenow comments to test FileExistsError exception
        # datenow = datetime.now().strftime('%Y%m%d')
        datenow = datetime.now().strftime('%Y%m%d_%H%M%S')

        newdir = "{0}/Desktop/{1}_{2}".format(homedir, datenow, str(e))

        print("\nINFO: Mailbox for {0} found.".format(str(e)))
        print("INFO: Attempting to create {0}.".format(newdir))
        try:
            os.mkdir(newdir)
            print("INFO: {0} created.\n".format(newdir))
            return newdir
        except FileExistsError as err_fee:
            print("\nERROR: Can not create {0}. It already exists.\n".format(newdir))
            sys.exit(60)
        except:
            print("\nERROR: An unknown error has occurred.\n")
            # raise
            sys.exit(70)
    else:
        print("\nERROR: There is no mailbox associated with that extension.\n")
        sys.exit(80)


def pstrings(filename, min=9):
    """
    Python version of UNIX "strings" utility.
    Adapted from: https://stackoverflow.com/a/17197027/5473041
    """
    with open(filename, "r", errors="ignore") as f:
        l = []
        pstring = ""
        for i in f.read():
            if i in string.printable:
                pstring += i
                continue
            if min == 9:        ## use for getting Message IDs from Mailbox.dat
                if len(pstring) == min:
                    l.append(pstring)
            else:               ## use for getting Caller ID from msg_id.msg
                if len(pstring) > min:
                    l.append(pstring)
            pstring = ""
        return l


def backup_voicemails(message_ids):
    if len(message_ids) == 0:
        print("\nERROR: No voicemails for {0} found.\n".format(extension))
        sys.exit(90)
    for msg_id in message_ids:
        if os.path.isfile("{0}/{1}.wav".format(messages, msg_id)):
            print("INFO: {0}.wav exists and will be copied to {1}.".format(msg_id, new_dir))
            shutil.copy2("{0}/{1}.wav".format(messages, msg_id), "{0}".format(new_dir))
            if os.path.isfile("{0}/{1}.wav".format(new_dir, msg_id)):
                print("INFO: Successfully copied {0}.wav to {1}.".format(msg_id, new_dir))
            else:
                print("\nWARNING: Failed to copy {0}.wav to {1}.\n".format(msg_id, new_dir))
        else:
            print("WARNING: {0}.wav does not exist.".format(msg_id))

        uxts = os.path.getmtime("{0}/{1}.wav".format(new_dir, msg_id))
        ts = datetime.fromtimestamp(uxts).strftime('%Y-%m%d_%H%M%S')
        cid = pstrings("{0}/{1}.msg".format(messages, msg_id), 1)

        print("INFO: Renaming {0}/{1}.wav to {0}/{1}_{2}.wav".format(new_dir, msg_id, cid[3]))
        os.rename("{0}/{1}.wav".format(new_dir, msg_id), "{0}/{1}_{2}.wav".format(new_dir, ts, cid[3]))
        if os.path.isfile("{0}/{1}_{2}.wav".format(new_dir, ts, cid[3])):
            print("INFO: Successfully renamed {0}/{1}.wav to {0}/{1}_{2}.wav\n".format(new_dir, msg_id, cid[3]))
        else:
            print("\nWARNING: Failed to rename {0}/{1}.wav to {0}/{1}_{2}.wav\n".format(new_dir, msg_id, cid[3]))


# --------------------------------- RUN IT! ---------------------------------- #
check_path(mailbox)
check_path(messages)
extension = check_argument()
new_dir = check_extension(mailbox, extension)
message_ids = pstrings("{0}/{1}/Mailbox.dat".format(mailbox, extension))
backup_voicemails(message_ids)

print("Voicemail backup of {0} completed successfully.\n".format(extension))
