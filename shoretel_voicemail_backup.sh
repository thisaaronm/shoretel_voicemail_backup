#!/bin/bash

# -------------------------------- VARIABLES --------------------------------- #
st_mailbox="/Volumes/z$/Shoreline Data/Vms/SHORETEL"
st_messages="/Volumes/z$/Shoreline Data/Vms/Message"
st_integer='^[0-9]+$'


# -------------------------------- FUNCTIONS --------------------------------- #
function CheckMount () {
  if [[ ! -d $st_mailbox ]]; then
    echo
    echo "$st_mailbox not found."
    echo
    exit 10
  elif [[ ! -d $st_messages ]]; then
    echo
    echo "$st_mailbox not found."
    echo
    exit 20
  fi
}


function CheckArgument () {
  if [[ -z $1 ]] || ! [[ $1 =~ $st_integer ]]; then
    while [[ -z $st_extension ]] || ! [[ $st_extension =~ $st_integer ]];
    do
      echo
      echo '####################################################################'
      echo "WARNING: Extension argument missing, or non-integer!"
      echo
      echo "For a less interactive experience, pass an extension as an argument:"
      echo "    e.g.) ./shoretel_voicemail_backup.sh 1234"
      echo '####################################################################'
      echo
      read -p "Enter the extension you wish to export voicemails for: " st_extension
    done
  else
    st_extension=$1
  fi
}


function CheckExtension () {
  if [[ -e "$st_mailbox"/$st_extension ]]; then
    folder=$HOME/Desktop/$(date +%Y-%m%d_%H%M%S_$st_extension)
    echo
    echo "Creating $folder"
    mkdir $folder
    echo "Directory created."
    echo
  else
    echo
    echo "There is no mailbox associated with that extension."
    echo
    exit 30
  fi
}


function GetVoicemails () {
  for i in $(strings "$st_mailbox"/$st_extension/Mailbox.dat | \
    awk 'length($1) == 9 {print $1}');
  do
    if [[ -e "$st_messages"/$i.wav ]]; then
      echo
      echo "$i.wav exists and will be copied."
      cp -p "$st_messages"/$i.wav $folder/$i.wav
      echo "Copying $i.wav complete."
      echo "Renaming $i.wav to $(stat -f %Sm -t %Y-%m%d_%H%M%S \
        $folder/$i.wav)_$(strings "$st_messages"/$i.msg | \
        awk 'FNR==4{print $0}').wav."
      mv $folder/$i.wav $folder/$(stat -f %Sm -t %Y-%m%d_%H%M%S \
        $folder/$i.wav)_$(strings "$st_messages"/$i.msg | \
        awk 'FNR==4{print $0}').wav
      echo "Renaming complete."
      echo
    else
      echo
      echo "Skipping $i, because $i.wav does not exist."
      echo
    fi
  done
}

# --------------------------------- RUN IT! ---------------------------------- #
CheckMount
CheckArgument $1
CheckExtension
GetVoicemails
