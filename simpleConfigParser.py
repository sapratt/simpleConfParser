import re
import json
import collections
'''
This python script will parse Cisco Conf files for active ethernet connections.
For simplicity the constructor will take boolean arguments depending on
what information the user wants.

args:   getOpenPorts(bool) - True to return list of active ports
        getChild    (bool) - True to return attributes of active ports
        getJson     (bool) - True to return JSON notation of ports and
                             attributes
'''

class CiscoConfParser:
    #Constructor
    def __init__(self, fileToRead, getOpenPorts, getChild, getJson):
        self.fileToRead = fileToRead                    # Cisco Config file
        self.interfaceDict = collections.OrderedDict()  # Dictionary to story {Port:Attributes}
        self.getOpenPorts = getOpenPorts                # Option to print active ports
        self.getChild = getChild                        # Option to obtain port attributes
        self.getJson = getJson                          # Option to return port:attributes in JSON

        #Avoiding specific method calling by inititing the parsing
        self.parseParent()

    #Print the file    
    def printFile(self):
        fOpen = open(self.fileToRead, "r")
        for x in fOpen:
          print(x)

    #Find active Eth connections at a minimum
    def parseParent(self):
        with open(self.fileToRead) as infile:
            for line in infile:
                #if 'FastEthernet' is found save it as a key
                if "interface" in line and re.search("FastEthernet\S+", line):
                    parentRes = re.search("FastEthernet\S+", line)
                    parent = parentRes.group()
                    self.interfaceDict[parent] = ""
                    #set getChild = true to get port attributes
                    if self.getChild:
                        self.parseChild(parent, infile)
                #if 'Ethernet' is found save it as a key
                elif "interface" in line and re.search("Ethernet\S+", line):
                    parentRes = re.search("Ethernet\S+", line)
                    parent = parentRes.group()
                    self.interfaceDict[parent] = ""
                    #set getChild = true to get port attributes
                    if self.getChild:
                        self.parseChild(parent, infile)
        #set getJson = true to return JSON 
        if self.getJson:
            self.confToJson(self.interfaceDict)
        #set getOpenPorts = true to get list of active ports
        if self.getOpenPorts:
            self.showOpenPorts(self.interfaceDict)


    def showOpenPorts(self, confDictionary):
        print("Open Ports:")
        for x in confDictionary:
            print(x)

    def confToJson(self, confDictionary):
        print("Json:")
        jsonFormat = json.dumps(confDictionary)
        print(jsonFormat)

    def parseChild(self, parent, infile):
        for line in infile:
            if "!" not in line:
                self.interfaceDict[parent] = self.interfaceDict[parent] + line
            if "!" in line:
                break


testParse = CiscoConfParser("sampleCiscoConf.txt", True, True, True)
