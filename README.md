# adium_chatlogsToHTML | Jack Nelson, 2019

Tested on Windows, Mac and Linux with log data created by Adium 1.4.

Adium chatlogs are typically stored within a tree of directories, starting at:
`Home Folder → Library → Application Support → Adium <VERSION> → Users → Default → Logs`

They are stored in XML format under both .xml and .chatlog suffixes, and they are best viewed with Adium's chat transcript viewer.
However, if you would like to take these chat logs, and convert them into clean, readable HTML, this script will help to do that.

## Usage overview
```
usage: adium_chatlogsToHTML.py [-h] [-r rootfolder] [-o outfolder]

Adium Chatlogs To HTML: Chatlog Converter

optional arguments:
  -h, --help     show this help message and exit
  -r rootfolder  Specify the root directory of where all the conversations are
  -o outfolder   Specify the output directory of processed chatlogs
```

1. Place all your adium chatlog folders/files in the "conversations" directory. This directory will be searched by the script for valid chatlogs.
2. Run the script.
3. The organized HTML chatlogs will be placed in a directory named "chatlogs_processed" in the same directory as the script. They will be sorted into folders by whichever email address is present in the chatlog filename.
4. To check to see if the script encountered any problems, check the logfile.txt inside "chatlogs_processed".

## Typical "conversations" folder layout
An example layout for the conversations folder is given in the included files. There is some flexibility with this however - if the Adium chatlog folder structure hasn't been changed, each conversation with a different user will be inside their own directory, but if this isnt the case and the files are completely loose in there, they should still be processed without issue (and will be placed within a "conversations" folder inside "chatlogs_processed")

## HTML chatlog structure
The actual HTML template in which the chatlog data will be inserted into can be seen in format_stripped.html
There are 3 lines of HTML/CSS in this file (these line breaks must be maintained or the script will break the formatting)
You can pretty much change whatever you want with this HTML.

The tags in which the chatlog data will be copied into:
[ALIAS] - The user's chat alias/name (if available)
[SENDER] - The user's email address
[MESSAGE] - The message contents
[TIME] - The time the message was sent

## Conversion notes
Several types of messages are stripped out of the chatlogs and are not included in the HTML messages.
They are outlined below:
1. Status messages - ie when a user goes offline/online 50 times to get their crush's attention
2. Name change messages - when a user changes their alias
