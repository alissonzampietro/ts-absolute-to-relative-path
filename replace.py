import os
import re

def findLineWithIncorrectImport(directory):
    with open(directory, 'r') as fp:
        lines = fp.readlines()
        for row in lines:
            if row.find('from \'src') != -1:
                return row


def generateNewLine(importStatement, filePath):
    piecesFilePath = filePath[2:].split('/')
    urlImportStatement = importStatement.split('\'')[1]
    piecesImportStatement = urlImportStatement.split('/')
    backCommand = 0
    equalPath = 0
    samePath = True

    statementLength = len(piecesImportStatement)
    for currentPosition in range(len(piecesFilePath)):
        if currentPosition < statementLength:
            if samePath and piecesFilePath[currentPosition] == piecesImportStatement[currentPosition]:
                equalPath = equalPath + 1
            else:
                samePath = False
                backCommand = backCommand + 1
        else:
            backCommand = backCommand + 1
    
    del piecesImportStatement[:equalPath]
    backCommand = backCommand - 1
    newPath = ('../'*backCommand)+('/'.join(piecesImportStatement))
    return importStatement.replace(urlImportStatement, newPath)


def replaceLine(newImportLine, lineWithWrongImport, filePath):
    print(newImportLine, lineWithWrongImport, filePath)
    with open(filePath, 'r') as file:
        content = file.read()

    content = content.replace(lineWithWrongImport, newImportLine)

    with open(filePath, 'w') as file:
        file.write(content)
    

def replace_ts_absolute_imports(directory):
    for root, dirs, files in os.walk(directory):
        if "./src/" in root:
            for file in files:
                filePath = root+'/'+file
                lineWithWrongImport = findLineWithIncorrectImport(filePath)
                if lineWithWrongImport is not None:
                    newImportLine = generateNewLine(lineWithWrongImport, filePath)
                    replaceLine(newImportLine, lineWithWrongImport, filePath)

if __name__ == '__main__':
    replace_ts_absolute_imports('.')
