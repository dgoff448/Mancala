import random

# index 7 = player's bank
# index 0 = computer's bank

class Mancala:
    def __init__(self, gMode):
        gameModes = {'norm': [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0],
                     'long': [9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 0]}
        if gMode == 'rand':
            r = []
            nums = []
            [r.append(random.randint(1,9)) for i in range(0, 6)]
            r.append(0)
            r += r
            self.board = r
        else:
            self.board = gameModes[gMode]

    def isGameOver(self):
        p = 0
        c = 0
        for i in range(0, len(self.board)):
            if i < 6:
                p += self.board[i]
            elif i > 6 and i != 13:
                c += self.board[i]
        if p == 0:
            self.board[13] += c
            for i in range(7, 13):
                self.board[i] = 0
            return True
        elif c == 0:
            self.board[6] += p
            for i in range(0, 6):
                self.board[i] = 0
            return True
        return False
       
    def playerMove(self, ind, amt):
        otherSide = {0:12, 1:11, 2:10, 3:9, 4:8, 5:7}
        self.board[ind] = 0
        j = ind
        for i in range(ind+1, ind+amt+1):
            j += 1
            if i in [13, 27, 41, 55, 69]:
                j += 1    # Skip Computer's bank
                self.board[j%14] += 1
            else:
                self.board[j%14] += 1
            print(i, j, f"Updating board[{j%14}] from {self.board[j%14]-1} to {self.board[j%14]}")
        
        if self.board[j%14] == 1 and j not in [6, 20, 34, 48, 62] and j%14 < 6 and self.board[otherSide[j%14]] != 0:
            self.board[6] += self.board[j%14]
            self.board[j%14] = 0

            self.board[6] += self.board[otherSide[j%14]]
            self.board[otherSide[j%14]] = 0

        print(self.board)
        return (j in [6, 20, 34, 48, 62])

    def findVulns(self):
        otherSide = {12:0, 11:1, 10:2, 9:3, 8:4, 7:5}
        val = 0
        ind = -1
        for i in range(12, 6, -1):
            interVal = 0
            interInd = -1
            if self.board[otherSide[i]] == 0 and self.board[i] > val:
                interVal = self.board[i]
                interInd = i
                pInd = otherSide[i]
                # Find if capture is really possible
                for j in range(0, 6):
                    if self.board[j]%13 + j == pInd and self.board[j]%13 != 0:
                        val = interVal
                        ind = interInd
        if ind == -1:
            print("No Vulnerability Detected.")
        return ind, val

    def findExtraTurn(self):
        ind = -1
        for i in range(12, 6, -1):
            if self.board[i] == 13 - i:
                return i
        print("No Extra Turn Found")
        return ind

    def findCapture(self):
        otherSide = {12:0, 11:1, 10:2, 9:3, 8:4, 7:5}
        zInd = -1
        zVal = -1
        amt = -1
        for i in range(12, 6, -1):
            zi = -1
            zv = -1
            if self.board[i] == 0 and self.board[otherSide[i]] > zVal:
                zi = i
                zv = self.board[otherSide[i]]
                for j in range(12, 6, -1):
                    if j + self.board[j]%13 == zi and self.board[j]%13 != 0:
                        zInd = j
                        amt = self.board[j]
                        zVal = zv
        if zInd == -1:
            print("No Capture Found.")
        return zInd, amt, zVal

    def randBankIndex(self):
        if self.board[12] != 0:
            return 12, self.board[12]
        flip = {0:12, 1:11, 2:10, 3:9, 4:8, 5:7}
        nums = []
        for i in range(12, 6, -1):
            nums.append(self.board[i] + i)
        ind = flip[nums.index(max(nums))]
        amt = self.board[ind]
        return ind, amt

    def compPick(self):
        amt = 0
        ind = self.findExtraTurn()
    
        if ind != -1:
            amt = self.board[ind]
            print(f"Found Extra Turn at index {ind}.")
            return ind, amt
        else:
            capInd, capAmt, capVal = self.findCapture()
            vInd, vVal = self.findVulns()
            if (capInd != -1) or (vInd != -1 ):
                print(f"Capture Ind: {capInd}, Vulnerability Ind: {vInd}")
                print(f"Capture Val: {capVal}, Vulnerability Val: {vVal}")
                if capVal > vVal or vInd == -1:
                    print(f"Found Capture at index {capInd}")
                    return capInd, capAmt
                else:
                    print(f"Found Vulnerability: {vVal} on Index {vInd}")
                    return vInd, self.board[vInd]
            else:
                print("Picking random banking index.")
                ind, amt = self.randBankIndex()
                return ind, amt

    def computerMove(self, ind, amt):
        otherSide = {12:0, 11:1, 10:2, 9:3, 8:4, 7:5}
        self.board[ind] = 0
        j = ind
        for i in range(ind+1, ind+amt+1):
            j += 1
            if i in [6, 20, 34, 48, 62]:
                j += 1    # Skip Player's bank
                self.board[j%14] += 1
            else:
                self.board[j%14] += 1
            print(f"Updating board[{j%14}] from {self.board[j%14]-1} to {self.board[j%14]}")
        
        if self.board[j%14] == 1 and j not in [13, 27, 41, 55, 69] and j%14 > 6 and self.board[otherSide[j%14]] != 0:
            self.board[13] += self.board[j%14]
            self.board[j%14] = 0

            self.board[13] += self.board[otherSide[j%14]]
            self.board[otherSide[j%14]] = 0

        print(self.board)
        return (j in [13, 27, 41, 55, 69])
    
    def getCell(self, ind):
        return self.board[ind]

"""
                  P                    C
0  1  2  3  4  5  6  7  8  9  10 11 12 13
14 15 16 17 18 19 20 21 22 23 24 25 26 27
28 29 30 31 32 33 34 35 36 37 38 39 40 41
"""
"""
12 11 10 9  8  7
0  1  2  3  4  5
"""