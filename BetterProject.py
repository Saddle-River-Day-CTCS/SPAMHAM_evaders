import pickle as pkl
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import numpy as np

class FileStuff:
    #Opens and reads the pkl file
    def openFile(file):
        with open(file, "rb") as f:
            data = pkl.load(f)
        return data

class Analysis:
    totalHam = 0
    totalSpam = 0

    hamCount = dict()
    spamCount = dict()

# doEverything Takes the text of an email and returns wether the program believes it is spam or ham and to what degree it believes that
    def doEverything(email):
        
        for i in PreprocessTokenize.punctuationList:
            email.replace(i, "")
        
        email = email.split()

        emailTxt = []
        for i in range(len(email)):
            if email[i] not in PreprocessTokenize.stop:
                emailTxt.append(email[i])

        return Analysis.spamHam(Analysis.testEmail(emailTxt)), Analysis.testEmail(emailTxt)

# spamHam Takes the integer variable spamChance and determines wether it is spam or ham
    def spamHam(num):
        if num >= 0:
            return "Spam"
        else:
            return "Ham"

# testEmail Takes a one-dimensional array and returns the numeric representation of how much it thinks it is spam or ham
    def testEmail(email):
        spamChance = 0
        #spamChance2 = 0


        #p = (len(PreprocessTokenize.bigHam)/len(PreprocessTokenize.bigSpam)) - 2 - (len(PreprocessTokenize.bigSpam)/len(PreprocessTokenize.bigHam))

        for i in email:
            spamChance += Analysis.spamCount[i] - Analysis.hamCount[i]
            #spamChance += (Analysis.spamCount[i]/len(PreprocessTokenize.bigSpam)) - (Analysis.hamCount[i]/len(PreprocessTokenize.bigHam))





        #print(spamChance2 * p)
        return spamChance #* (len(PreprocessTokenize.bigSpam)+len(PreprocessTokenize.bigHam))

# getAccuracy Takes a three-dimensional array of tokenized emails and if they are actually spam or ham according to the dataset
# getAccuracy also takes a starting email index and how many emails to test
# getAccuracy uses the method testEmail to determine what the machine thinks and the compares it with the answer
# getAccuracy returns the percentage of the time that it was correct over the amount of emails it was told to read

    def getAccuracy(data, x, n):
        correct = 0

        for i in range(x,x+n):
            if (Analysis.testEmail(data[i][1]) >= 0 and data[i][0] == "spam") or (Analysis.testEmail(data[i][1]) < 0 and data[i][0] == "ham"):
                correct += 1

        return str((correct/n) * 100) + "%"
    
# graph creates a graph of commonly found words in the spam and ham word banks
    def graph():
            fig, axs = plt.subplots(1, 2, figsize=(15, 6))

            sorted_sci_fi_freq_dist = dict(sorted(Analysis.spamCount.items(), key=lambda item: item[1], reverse=True)[:50])
            axs[0].bar(sorted_sci_fi_freq_dist.keys(), sorted_sci_fi_freq_dist.values())
            axs[0].set_title('Spam Frequency Distribution')
            axs[0].set_xlabel('Words')
            axs[0].set_ylabel('Frequency')
            axs[0].tick_params(axis='x', rotation=90)

            # Non-Sci-Fi CFD
            sorted_not_sci_fi_freq_dist = dict(sorted(Analysis.hamCount.items(), key=lambda item: item[1], reverse=True)[:50])
            axs[1].bar(sorted_not_sci_fi_freq_dist.keys(), sorted_not_sci_fi_freq_dist.values())
            axs[1].set_title('Ham Word Frequency Distribution')
            axs[1].set_xlabel('Words')
            axs[1].set_ylabel('Frequency')
            axs[1].tick_params(axis='x', rotation=90)

            plt.tight_layout()
            plt.show()
  


class PreprocessTokenize:
    stop = ["subject", "Subject"]
    stop += stopwords.words("english")
    stop.remove("you")
    stop.remove("your")

    
    punctuationList = ["1","2","3","4","5","6","7","8","9","0",'.',"!" ,'?', ',', ':', ';', '(', ')',"-","_","'", '@', '=', "'", '#', '$', '%', '^', '&', '*', '<', '>', '[', ']',"{","}","|","\\","\\\\", "/", '"']
    spam = []
    ham = []

    bigSpam = []
    bigHam = []

# countWords is pretty useless but we use it for some reason
    def countWords(lst):
        return Counter(lst)
    
# seperate seperates all of the spam emails and all of the ham emails
    def seperate(data):
        for i in data:
            if i[0] == "ham" :
                PreprocessTokenize.ham.append(i[1])
                Analysis.totalHam += 1
            else:
                PreprocessTokenize.spam.append(i[1])
                Analysis.totalSpam += 1

# makeBig creates a one-dimensional array containing all of the preprocessed and tokenized words in the given parameter
    def makeBig(lst):
        big = []
        for i in lst:
            big.extend(i)
        for i in big:
            i = str(i)
        return big
    

    def removeStopwords(lst):  #Also Tokenizes

        #lst to pandas dataframe
        frame = pd.DataFrame(lst)
        frame.columns = ["class","email"]

        #Remove stopwords
        frame["email"] = frame["email"].apply(lambda x: [word for word in x.split() if word not in (PreprocessTokenize.stop)])

        #back to list and return
        return frame.values.tolist()
    

    def removePunc(lst): 
        #lst to pandas dataframe
        frame = pd.DataFrame(lst)
        frame.columns = ["class","email"]

        #Remove punctuation
        frame["email"] = frame["email"].apply(lambda y: ''.join([letter for letter in y if letter not in (PreprocessTokenize.punctuationList)]))

        #back to list and return
        return frame.values.tolist()
            
    
    '''
    remove stop
    tokenize
    seperate
    countExc
    remove punc
    '''
#                        ["spam", [email]]
def main():
    data = FileStuff.openFile("student_sample.pkl") #                                       Open file

    moreData = FileStuff.openFile("teacher_sample.pkl")

    for i in data:
        i[1] = i[1].lower()

    data = PreprocessTokenize.removePunc(data) #                                             Remove punc
    data = PreprocessTokenize.removeStopwords(data) #                                        Remove stopwords and tokenizes

    moreData = PreprocessTokenize.removePunc(moreData) #                                             Remove punc
    moreData = PreprocessTokenize.removeStopwords(moreData) #    

    PreprocessTokenize.seperate(data) #                                                      Seperates into spam and ham lists

    PreprocessTokenize.smallSpam = PreprocessTokenize.spam
    PreprocessTokenize.smallHam = PreprocessTokenize.ham

    np.random.shuffle(PreprocessTokenize.smallSpam)
    np.random.shuffle(PreprocessTokenize.smallHam)

    PreprocessTokenize.smallSpam = PreprocessTokenize.spam
    PreprocessTokenize.smallHam = PreprocessTokenize.ham[:len(PreprocessTokenize.spam)]

    PreprocessTokenize.bigSpam = PreprocessTokenize.makeBig(PreprocessTokenize.smallSpam) 
    PreprocessTokenize.bigHam = PreprocessTokenize.makeBig(PreprocessTokenize.smallHam) #    2D list into 1D list


    Analysis.hamCount = PreprocessTokenize.countWords(PreprocessTokenize.bigHam)
    Analysis.spamCount = PreprocessTokenize.countWords(PreprocessTokenize.bigSpam) #         Counts words

    tempdict1 = dict()
    tempdict2 = dict()

    for i in Analysis.hamCount:
        if Analysis.hamCount[i] > 3:
            tempdict1.update({i : Analysis.hamCount[i]})
        
    for i in Analysis.spamCount:
        if Analysis.spamCount[i] > 3:
            tempdict2.update({i : Analysis.spamCount[i]})
            
    #Analysis.hamCount.update(tempdict1)
    #Analysis.spamCount.update(tempdict2)

    runs = 0
    totalAcc = 0

    for i in range(50):
        totalAcc += float(Analysis.getAccuracy(moreData, 0, len(moreData)-1)[:-1]) #                               Tests models accuracy with labeled samples
        runs += 1 
    
    print(totalAcc/runs)
    #print(Analysis.doEverything("Matthew, We think you'd make an excellent Golden Ram. Why? Because we know you'll love West Chester University's broad range of majors, opportunities for real–world experiences, and beautiful campus. Plus, our location puts you right in the center of some of the world's most exciting cities. Simply put, WCU is an incredible experience we'd love to share with you. Start your application today! Whether you're passionate about people or plants, ready to work in business or start your own, you'll find your element at WCU. Ready to charge into your future? See what financial aid you might be eligible to receive—WCU awarded more than $175 million last year alone."))
    


if __name__ == "__main__":
    main()