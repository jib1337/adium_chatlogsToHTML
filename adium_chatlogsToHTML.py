# Jack Nelson | Adium chatlog to HTML converter

import os
import xml.etree.ElementTree as ET

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

        file = open('chatlogs_processed/' + chatName + '/' + chatName + '_' + str(convoNumber) + '.html', 'w', encoding = 'utf-8')
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

htmlLoad = False
try:
    file = open('format_stripped.html', 'r')
    htmlPrefix = file.readline()
    htmlMessage = file.readline()
    htmlSuffix = file.readline()
    htmlLoad = True
    logFile = []
    errorCount = 0
    conversionCount = 0
except:
    print('Error reading HTML format file.')

currentRoot = None
if htmlLoad == True:
    print('Starting conversion process now...')
    logFile.append('Starting conversion process now...' + '\n')
    for root, dirs, files in os.walk('.'):
        if currentRoot == root.split("\\")[-1].split(' ')[0]:
            # If the root directory is under the same email we previously processed, do not create a new folder
            pass
        else:
            currentRoot = root.split("\\")[-1].split(' ')[0]
            try:
                if currentRoot == 'conversations' or currentRoot == 'chatlogs_processed' or currentRoot == '.':
                    pass
                else:
                    logFile.append('New working directory: ' + currentRoot + '\n')
                    os.makedirs('chatlogs_processed/' + currentRoot)
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
                except:
                    logFile.append('An error occured when opening the file ' + xmlPath + '\n')
                    errorCount += 1

                try:
                    conversationJSON = getConvo(convoRoot)
                    createHTML(getConvo(convoRoot), currentRoot, convoNumber)
                except:
                    logFile.append('An error occured when making JSON data from ' + xmlPath + '\n')
                    errorCount +=1

                try:
                    if createHTML(conversationJSON, currentRoot, convoNumber) == True:
                        logFile.append('Created HTML file for: ' + currentRoot + ' #' + str(convoNumber) + '\n')
                        convoNumber += 1
                        conversionCount += 1
                    else:
                        logFile.append('File creation for ' + xmlfile + ' skipped - no message data present\n')
                except:
                    logFile.append('An error occured when making HTML data from ' + xmlPath + '\n')


    logFile.append('Conversion process finished.' + '\n')
    logFile.append('Completed operations on ' + str(conversionCount) + ' logs.' + '\n')
    logFile.append('Error count: ' + str(errorCount) + '\n')
    file = open('chatlogs_processed/logfile.txt', 'w')
    file.writelines(logFile)
    file.close()
    print('Done.')