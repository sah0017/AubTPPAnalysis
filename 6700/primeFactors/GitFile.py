import re
        self.commits = 0
        self.commits = self.commits + 1
            self.commits = self.commits + 1
        commitAddedLines = 0
        commitDeletedLines = 0
        testFiles = 0
        prodFiles = 0
        self.myTransformations = []
            addedLines, deletedLines, testFile = self.analyzeFile()
            commitAddedLines = commitAddedLines + addedLines
            commitDeletedLines = commitDeletedLines + deletedLines
            if testFile:
                testFiles = testFiles + 1
            else:
                prodFiles = prodFiles + 1
        self.newCommit = Commit.Commit(self.commits, commitAddedLines,commitDeletedLines, testFiles, prodFiles)
        for trans in self.myTransformations:
            self.newCommit.addTransformation(trans)
   
    def analyzeFile(self):
        fileAddedLines = 0
        fileDeletedLines = 0
        fileName = splLine[len(splLine) - 1]
        if fileName.startswith('test'):
            testFile = True
        else:
            testFile = False
        matchObj = re.match('new file mode',self.line)
        if matchObj:
            self.newFile = File.File(fileName,testFile,self.commits)
            fileIndex = len(self.myFiles) - 1
        else:
            for x in self.myFiles:
                if x.getFileName() == fileName: 
                    fileIndex = self.myFiles.index(x) 
        fileAddedLines, fileDeletedLines = self.evaluateTransformations()
        self.myFiles[fileIndex].setCommitDetails(self.commits, fileAddedLines, fileDeletedLines)
        return fileAddedLines, fileDeletedLines, testFile
    
    def returnWithNull(self):
        rtnMatchObj = re.search("return", self.line)
        rtnBoolean = False
        rtnValue = ''
        if rtnMatchObj:
            strLine = self.line.rstrip()
            splLine = strLine.split(" ")
            if len(splLine) > 1:
                rtnValue = splLine[len(splLine) - 1]
            if (len(splLine) == 1) or (rtnValue == 'None'): ## return with no value is basically Null
                rtnBoolean = True
            else:
                rtnBoolean = False
        return rtnBoolean, rtnValue

    def evaluateTransformations(self):
        addedLines = 0
        deletedLines = 0
        deletedNullValue = False
        while not self.pythonFileFound():   ## this would indicate a new python file within the same commit
            if self.line[0] == '-':
                deletedLines = deletedLines + 1
                if self.line.find("pass") > -1:
                    deletedNullValue = False
            if self.line[0] == '+':
                addedLines = addedLines + 1
                if self.line.find("pass") > -1:
                    self.myTransformations.append(myTrans.NULL)
                rtnBoolean, rtnValue = self.returnWithNull()
                if rtnBoolean == True:
                    self.myTransformations.append(myTrans.NULL)
                else:
                    if rtnValue.isalnum() or rtnValue == '[]':
                        if deletedNullValue == True:
                            self.myTransformations.append(myTrans.N2C)
                        else:
                            self.myTransformations.append(myTrans.ConstOnly)
            self.line = self.gitFile.readline()
        
        if self.line.find('green') > -1:   ## using the key word 'green' in the commit comment line to find the next commit 