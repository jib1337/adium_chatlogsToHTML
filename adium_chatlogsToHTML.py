#!/usr/bin/env python3
# Jack Nelson | Adium chatlog to HTML converter

import os
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET

argparser = argparse.ArgumentParser(description='Adium Chatlogs To HTML: Chatlog Converter')
argparser.add_argument('-r', '--root', default='conversations', help='Specify the root directory of where all the conversations are')
argparser.add_argument('-o', '--out', default='chatlogs_processed', help='Specify the output directory of processed chatlogs')
args = argparser.parse_args()

def convertPath(rootFilePath):
    # convert os.walk file path to one we can use to open the file
    return(rootFilePath.replace('\\', '/')[2:])

def createHTML(conversationJSON, chatName, convoNumber):
    # Take the JSON - formatted conversation, construct and output HTML file.

    htmlComplete = htmlPrefix

    for convo in conversationJSON:
        if 'alias' in convo:
            user1 = convo['alias']
            break
    messages = []
    for message in conversationJSON:
        newMessage = htmlMessage.replace('[SENDER]', message['sender'])

        # Here we are attempting to assign a different colors to differentiate between the different users.
        # Dark red for user 1 and dark blue for user 2.
        # If user 1 changes their name mid-chat, this will stop working.
        try:
            if message['alias'] != user1:
                newMessage = newMessage.replace('[ALIAS]', '<user2>' + message['alias'] + '</user2>')
            else:
                newMessage = newMessage.replace('[ALIAS]', '<user1>' + message['alias'] + '</user1>')
        except:
            newMessage = newMessage.replace('[ALIAS]', '<user3>' + message['sender'] + '</user3>')

        newMessage = newMessage.replace('[TIME]', message['time'])
        
        try:
            newMessage = newMessage.replace('[MESSAGE]', message['message'])
        except TypeError:
            # In the case of certain events, there will be no message field. Usually when a name change happens.
            # Including this as a message just clutters the conversation more, so we won't add them.
            continue
        
        messages.append(newMessage)

    if len(messages) > 0:
        # We only want to proceed if there is at least one valid message in the conversation.

        htmlComplete += ''.join(messages) + htmlSuffix

        file = open(outFolder + '/' + chatName + '/' + chatName + '_' + str(convoNumber) + '.html', 'w', encoding = 'utf-8')
        file.write(htmlComplete)
        file.close()
        
        return(True)
    else:
        # If there are no valid messages in the conversation, we do not want to process any file.
        return(False)

def getConvo(root):
    # Recieve parsed XML content and convert nessecary components to form JSON data.

    conversation = []
    for i in range(len(root)):
        try:
            conversation.append({'sender' : root[i].attrib['sender'], 'alias' : root[i].attrib['alias'],
            'time' : root[i].attrib['time'][:-6].replace('T', ' '), 'message' : root[i][0][0].text})
        except:
            if 'alias' not in root[i].attrib:
                try:
                    # For some conversations, the chat log did not save an alias, so that field is missing.
                    # So instead we'll use the sender's email address for their alias.
                    conversation.append({'sender' : root[i].attrib['sender'], 'alias' : root[i].attrib['sender'],
                    'time' : root[i].attrib['time'][:-6].replace('T', ' '), 'message' : root[i][0][0].text})
                except:
                    # There are also event messages, which we will not bother including.
                    pass
            else:
                pass

    return(conversation)

rootFolder = args.root.rstrip('/')
outFolder = args.out.rstrip('/')

htmlLoad = False
try:
    with open('format_stripped.html', 'r') as file:
        htmlPrefix = file.readline()
        htmlMessage = file.readline()
        htmlSuffix = file.readline()
    htmlLoad = True
    logFile = []
    errorCount = 0
    conversionCount = 0
except Exception as e:
    print('Error reading HTML format file: ' + str(e))

# If the specified output directory doesn't exist, create it
try:
    os.makedir(rootFolder)
    os.makedir(outFolder)
except:
    pass

currentRoot = None
if htmlLoad == True:
    print('Starting conversion process now...')
    logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] Starting conversion process now...' + '\n')

    for root, dirs, files in os.walk('.\\' + rootFolder):
        if currentRoot == root.split("\\")[-1].split(' ')[0]:
            # If the root directory is under the same email we previously processed, do not create a new folder
            pass
        else:
            currentRoot = root.split("\\")[-1].split(' ')[0]
            try:
                logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] New working directory: ' + currentRoot + '\n')
                os.makedirs(outFolder + '/' + currentRoot)
            except:
                # If there is already a directory with that name
                pass
            convoNumber = 1
        for xmlfile in files:
            # Traverse all the directories and only operation on .xml and .chatlog files
            if xmlfile.endswith('.xml') or xmlfile.endswith('.chatlog'):
                try:
                    xmlPath = (convertPath(root) + '/' + xmlfile)
                    convoRoot = ET.parse(xmlPath).getroot()
                except Exception as e:
                    logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] An error occured when opening the file ' + xmlPath + ': ' + str(e) + '\n')
                    errorCount += 1

                try:
                    if createHTML(getConvo(convoRoot), currentRoot, convoNumber) == True:
                        logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] Created HTML file for: ' + currentRoot + ' #' + str(convoNumber) + '\n')
                        convoNumber += 1
                        conversionCount += 1
                    else:
                        logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] File creation for ' + xmlfile + ' skipped - no message data present\n')
                except Exception as e:
                    logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] An error occured when making HTML data from ' + xmlPath + ': ' + str(e) + '\n')
                    errorCount += 1

    logFile.append('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] Conversion process finished.' + '\n')
    logFile.append('Completed operations on ' + str(conversionCount) + ' logs.' + '\n')
    logFile.append('Error count: ' + str(errorCount) + '\n')
    file = open(outFolder + '/' + 'logfile.txt', 'w')
    file.writelines(logFile)
    file.close()
    print('Done.')