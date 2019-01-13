# adium_chatlogsToHTML
-------------------------------------------------------------------------------------------------------
Tested with log data created by Adium 1.4.

Adium chatlogs are typically stored within a tree of directories, starting at:
Home Folder → Library → Application Support → Adium <v> → Users → Default → Logs

They are stored in XML format under both .xml and .chatlog suffixes, and they are best viewed with Adium's chat transcript viewer.
However, if you would like to take these chat logs, and convert them into clean, readable HTML which are readable on other operating systems or devices without Adium installed, it is possible through use of this script.

## Usage overview
The "logs" folder containing all of the chatlog folders should be placed in the same folder as this script. The script will traverse forward, locating all valid .xml and .chatlog files, converting them into HTML files. For group of conversations which take place for one user, the user will have a single folder inside the outputted "chatlogs_processed" folder. The script will generate a logfile which can be used to identify any issues with file handling or conversion.
