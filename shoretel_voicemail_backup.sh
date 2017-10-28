#!/bin/bash

# -------------------------------- VARIABLES --------------------------------- #
mailbox="/Volumes/z$/Shoreline Data/Vms/SHORETEL"
messages="/Volumes/z$/Shoreline Data/Vms/Message"
integer='^[0-9]+$'


# -------------------------------- FUNCTIONS --------------------------------- #
function check_path () {
  if [[ ! -d $mailbox ]]; then
    echo
    echo "$mailbox not found."
    echo
    exit 10
  elif [[ ! -d $messages ]]; then
    echo
    echo "$mailbox not found."
    echo
    exit 20
  fi
}


function check_argument () {
  if [[ -z $1 ]] || ! [[ $1 =~ $integer ]]; then
    while [[ -z $extension ]] || ! [[ $extension =~ $integer ]];
    do
      echo
      echo '####################################################################'
      echo "WARNING: Extension argument missing, or non-integer!"
      echo
      echo "For a less interactive experience, pass an extension as an argument:"
      echo "    e.g.) ./shoretel_voicemail_backup.sh 1234"
      echo '####################################################################'
      echo
      read -p "Enter the extension you wish to export voicemails for: " extension
    done
  else
    extension=$1
  fi
}


function check_extension () {
  if [[ -e "$mailbox"/$extension ]]; then
    folder=$HOME/Desktop/$(date +%Y-%m%d_%H%M%S_$extension)
    echo
    echo "Creating $folder"
    mkdir $folder
    echo "Directory created."
  else
    echo
    echo "There is no mailbox associated with that extension."
    echo
    exit 30
  fi
}


function backup_voicemails () {
  for i in $(strings "$mailbox"/$extension/Mailbox.dat | \
    awk 'length($1) == 9 {print $1}');
  do
    if [[ -e "$messages"/$i.wav ]]; then
      echo
      echo "$i.wav exists and will be copied."
      cp -p "$messages"/$i.wav $folder/$i.wav
      echo "Copying $i.wav complete."
      echo "Renaming $i.wav to $(stat -f %Sm -t %Y-%m%d_%H%M%S \
        $folder/$i.wav)_$(strings "$messages"/$i.msg | \
        awk 'FNR==4{print $0}').wav."
      mv $folder/$i.wav $folder/$(stat -f %Sm -t %Y-%m%d_%H%M%S \
        $folder/$i.wav)_$(strings "$messages"/$i.msg | \
        awk 'FNR==4{print $0}').wav
      echo "Renaming complete."
    else
      echo
      echo "Skipping $i, because $i.wav does not exist."
    fi
  done
}

# --------------------------------- RUN IT! ---------------------------------- #
check_path
check_argument $1
check_extension
backup_voicemails

echo
echo "Successfully completed voicemail backup of $1"
echo
