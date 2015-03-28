from subprocess import call
import sys
import re

MAX_LEN = 100 # Maximum length of a segment to send to Google for TTS
LANGUAGE = "en" # Language to use with TTS - this won't do any translation, just the voice it's spoken with

fullMsg = ""
i = 1

# Read our system arguments and add them into a single string
while i<len(sys.argv):
   fullMsg += sys.argv[i] + " "
   i+=1

# Split our full text by any available punctuation
parts = re.split("[\.\,\;\:]", fullMsg)

# The final list of parts to send to Google TTS
processedParts = []

while len(parts)>0: # While we have parts to process
   part = parts.pop(0) # Get first entry from our list

   if len(part)>MAX_LEN:
      # We need to do some cutting
      cutAt = part.rfind(" ",0,MAX_LEN) # Find the last space within the bounds of our MAX_LEN

      cut = part[:cutAt]

      # We need to process the remainder of this part next
      # Reverse our queue, add our remainder to the end, then reverse again
      parts.reverse()
      parts.append(part[cutAt:])
      parts.reverse()
   else:
      # No cutting needed
      cut = part

   cut = cut.strip() # Strip any whitespace
   if cut is not "": # Make sure there's something left to read
      # Add into our final list
      processedParts.append(cut.strip())

for part in processedParts:
   # Use mpg123 to play the resultant MP3 file from Google TTS
   call(["mpg123","-q","http://translate.google.com/translate_tts?tl=%s&q=%s" % (LANGUAGE,part)])