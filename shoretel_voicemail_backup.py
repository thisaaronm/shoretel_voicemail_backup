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
    	# print("\nINFO: {0} is accessible.\n".format(p))
    	pass
    elif not os.path.isdir(p):
    	print("\nERROR: {0} is inaccessible.\n".format(p))
    	sys.exit(10)
    else:
    	print("\nERROR: An unknown error has occurred.\n")
    	# raise
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
    	# raise
    	sys.exit(50)


def check_extension(p, e):
    """
    Checks for the mailbox of the provided extension.
    """
    if os.path.isdir(os.path.join(p, str(e))):
    	print("\nINFO: Mailbox for {0} found.".format(str(e)))
    else:
    	print("\nERROR: There is no mailbox associated with that extension.\n")
    	sys.exit(60)


def check_message_ids(m_ids, e):
    """
    Check if there are any Message IDs (for the voicemails) for the provided extension.
    If not, exit.
    If so, create new directory on user's Desktop.
    """
    if len(m_ids) == 0:
    	print("\nERROR: No voicemails for {0} found.\n".format(e))
    	sys.exit(70)
    else:
    	try:
    		## swap datenow comments to test FileExistsError exception
    		# datenow = datetime.now().strftime('%Y%m%d')
    		datenow = datetime.now().strftime('%Y%m%d_%H%M%S')

    		homedir = os.path.expanduser('~')
    		newdirname = "{0}_{1}".format(datenow, str(e))
    		newdirpath = os.path.join(homedir, 'Desktop', newdirname)

    		print("INFO: Attempting to create {0}.".format(newdirpath))
    		os.mkdir(newdirpath)
    		if os.path.isdir(newdirpath):
    			print("INFO: Successfully created {0}.\n".format(newdirpath))
    			return newdirpath
    		else:
    			print("\nERROR: Failed to create {0}.\n".format(newdirpath))
    			sys.exit(80)
    	except FileExistsError as err_fee:
    		print("\nERROR: Unable to create {0}. It already exists.\n".format(newdirpath))
    		sys.exit(90)
    	except:
    		print("\nERROR: An unknown error has occurred.\n")
    		# raise
    		sys.exit(100)


def backup_voicemails(message_ids):
    """
    Copies the WAVs from HQ/DVS to the new directory on the user's Desktop.
    Renames the WAVs as the time the voicemail was received, and the caller ID.
    	e.g. "2017-1026_130203_+18883222822.wav"
    """
    new_dir = check_message_ids(message_ids, extension)
    for msg_id in message_ids:
    	if os.path.isfile("{0}.wav".format(os.path.join(messages, msg_id))):
    		print("\nINFO: {0}.wav exists and will be copied to {1}.".format(msg_id, new_dir))
    		shutil.copy2("{0}.wav".format(os.path.join(messages, msg_id)), "{0}".format(new_dir))
    		if os.path.isfile("{0}.wav".format(os.path.join(new_dir, msg_id))):
    			print("INFO: Successfully copied {0}.wav to {1}.".format(msg_id, new_dir))

    			uxts = os.path.getmtime("{0}.wav".format(os.path.join(new_dir, msg_id)))
    			ts = datetime.fromtimestamp(uxts).strftime('%Y-%m%d_%H%M%S')
    			cid = pstrings("{0}.msg".format(os.path.join(messages, msg_id)), 1)
    			new_wav_name = "{0}_{1}".format(ts, cid[3])

    			old_name = os.path.join(new_dir, msg_id)
    			new_name = os.path.join(new_dir, new_wav_name)

    			print("INFO: Renaming {0}.wav to {1}.wav".format(old_name, new_name))
    			os.rename("{0}.wav".format(old_name), "{0}.wav".format(new_name))
    			if os.path.isfile("{0}.wav".format(new_name)):
    				print("INFO: Successfully renamed {0}.wav to {1}.wav\n".format(old_name, new_name))
    			else:
    				print("\nWARNING: Failed to rename {0}.wav to {1}.wav\n".format(old_name, new_name))
    		else:
    			print("\nWARNING: Failed to copy {0}.wav to {1}.\n".format(msg_id, new_dir))
    	else:
    		print("WARNING: {0}.wav does not exist.".format(msg_id))


def pstrings(filename, min=9):
    """
    Python version of UNIX "strings" utility.
    Adapted from: https://stackoverflow.com/a/17197027/5473041
    """
    if sys.version_info[0] < 3:
    	f = open(filename, "rb")
    else:
    	f = open(filename, "r", errors="ignore")

    l = []
    pstring = ""
    for i in f.read():
    	if i in string.printable:
    		pstring += i
    		continue
    	if min == 9:			## use for getting Message IDs from Mailbox.dat
    		if len(pstring) == min:
    			l.append(pstring)
    	else:			   		## use for getting Caller ID from msg_id.msg
    		if len(pstring) > min:
    			l.append(pstring)
    	pstring = ""

    if len(pstring) > 0:
    	l.append(pstring)

    f.close()
    return l


# --------------------------------- RUN IT! ---------------------------------- #
check_path(mailbox)
check_path(messages)
extension = check_argument()
check_extension(mailbox, extension)
message_ids = pstrings(os.path.join(mailbox, str(extension), "Mailbox.dat"))
backup_voicemails(message_ids)

print("Successfully completed voicemail backup of {0}.\n".format(extension))
