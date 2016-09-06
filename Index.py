import xml.etree.ElementTree as ET
import numpy as np
from nltk.stem.porter import PorterStemmer
import re
from math import log10
from math import isnan
from math import pow
from math import sqrt
from scipy import spatial
from numpy import linalg as LA
from Query import *
from Document import *
from Ranker import *

class IndexEnvironment:

    def __init__(self):
        self.ITerms = {} # dictionery - keys: terms (strings) , values - arreys of Doc_IDs
        self.IStems = {} # dictionery - keys: terms (strings) , values - arreys of Doc_IDs
        self.DocIndex = {} # dictionery - keys: Doc_IDs , values - Documents
        self.Tf_Idf_Flag = 0 # flag that indicates whether the TfIdf values in this index is up to date

    def Doc_Exists_In_Index(self, Doc_ID):
        """
        :param Doc_ID: type - string/int - a Document's Doc_ID
        :return: True if the doc exists in the index already and False if not
        """
        if Doc_ID in self.DocIndex :
            return True
        else:
            return False

    def addIndex(self, pathname):
        """
        :param pathname: a path to a file
        :return: the function open the file and fills the IndexEnvironment type according to it
        :exceptions: throws exceptions if one of the Documents in the file from pathname already exists in the Index
        and if the file cannot be opened
        """
        try:
            f = open(pathname, 'r')
        except (OSError, IOError) as e:
            raise Exception("file from -'",pathname,"'is not found")
        tree = ET.parse(f)
        root = tree.getroot()
        for DOC in root.findall('DOC'):
            Doc_ID = (DOC.find('DOCNO').text).strip()
            Text = DOC.find('TEXT').text
            if self.Doc_Exists_In_Index(Doc_ID):
                raise Exception("the doc titeled -'", Doc_ID, "' is already inside the index")
            temp = Document(Doc_ID, Text)
            self.Break_Text_Into_Doc(temp, Text)
        self.Tf_Idf_Flag = 0
        f.close()
        return

    def Update_Index(self, Doc):
        """
        :param Doc: type - Document
        :return: fills the IndexEnvironment's arguments and updates them according to the Doc
        """
        if Doc.Doc_ID in self.DocIndex:
            for Term in Doc.Terms:
                if Term in self.ITerms:
                    if Doc.Doc_ID not in self.ITerms[Term]:
                        self.ITerms[Term] = np.append(self.ITerms[Term], (Doc.Doc_ID))
                else:
                    self.ITerms[Term] = np.array(Doc.Doc_ID)
            for Stem in Doc.Stems:
                if Stem in self.IStems:
                    if Doc.Doc_ID not in self.IStems[Stem]:
                        self.IStems[Stem] = np.append(self.IStems[Stem], (Doc.Doc_ID))
                else:
                    self.IStems[Stem] = np.array(Doc.Doc_ID)
        else:
            self.DocIndex[Doc.Doc_ID] = Doc
            for Term in Doc.Terms:
                if Term in self.ITerms:
                    self.ITerms[Term] = np.append(self.ITerms[Term],(Doc.Doc_ID))
                else:
                    self.ITerms[Term] = np.array(Doc.Doc_ID)
            for Stem in Doc.Stems:
                if Stem in self.IStems:
                    self.IStems[Stem] = np.append(self.IStems[Stem],(Doc.Doc_ID))
                else:
                    self.IStems[Stem] = np.array(Doc.Doc_ID)
        return

    def Break_Text_Into_Doc(self, Doc, Text):
        """
        :param Doc: type - Document
        :param Text: type - string
        :return: the function breaks the words in the text and adds it to the Doc + updates the Index
        """
        Text = str(Text)
        TextVec = re.split("\s|[!-&]|[(-/]|[:-@]|[[-`]|[{-~]|(?='s)|[']", Text)
        TextVec = filter(None, TextVec)
        st = PorterStemmer()
        for i in range(len(TextVec)) :
            term = TextVec[i].lower()
            stem = st.stem(term).lower()
            Doc.addTerm(term, i)
            Doc.addStem(stem, i)
        self.Update_Index(Doc)
        return

    def getDocuments(self, documentIDs):
        """
        :param documentIDs: type - list of Document.Doc_ID
        :return: a list of the requested Documents according to the documentIDs
        :exceptions: if one of the IDs does'nt exists in the Index throws an Exception
        """
        resultlist = []
        for docID in documentIDs:
            if self.Doc_Exists_In_Index(docID):
                tempdoc = self.DocIndex[docID]
                temp = {'terms': tempdoc.Terms.keys(), 'stems': tempdoc.Stems.keys(), 'termsPositions': tempdoc.Terms.values(), 'stemsPositions': tempdoc.Stems.values()}
                resultlist.append(temp)
            else:
                raise Exception('the requested Doc with doc id -', docID, ' does not exists in the index')
        return resultlist

    def getDocumentsMetadata(self, metaData):
        """
        :param metaData: type - string - either DOCNO or TEXT (not capital sensitive)
        :return: returns a list of the required metadata from all the Documents in the Index
        :exceptions: if the metadata isn't DOCNO or TEXT trows an Exception
        """
        result = []
        if metaData.upper() == 'DOCNO':
            for key in self.DocIndex:
                result.append(key)
            return result
        elif metaData.upper() == 'TEXT':
            for key in self.DocIndex:
                temp = self.DocIndex[key].RestoreText()
                result.append(temp)
            return result
        else :
            raise Exception('metadata -',metaData,' does not exists (from getDocumentsMetadata)')

    def count(self):
        """
        :return: returns the number or words (terms/stems) in the index
        """
        result = 0
        for key in self.DocIndex:
            for key1 in self.DocIndex[key].Terms:
                result = result + self.DocIndex[key].Terms[key1].size
        return result

    def termCount(self, term = 0):
        """
        :param term: type - string - a term, without input to the function then value is 0
        :return: without input returns the number of words (with repeats) in the index, with a term input returns the
        :exceptions: if the term isn't inside the index trows an exception
        number of repeats
        """
        result = 0
        if term == 0:
            result = self.count()
            return result
        else :
            if term not in self.ITerms:
                raise Exception("the requested term -'",term,"' does not exist in the index (from termCount)")
            elif self.ITerms[term].size == 1:
                result = self.DocIndex[str(self.ITerms[term])].Terms[term].size
            else:
                for i in range (self.ITerms[term].size):
                    result = result + (self.DocIndex[self.ITerms[term][i]]).Terms[term].size
            return result

    def stemCount(self, stem = 0):
        """
        :param stem: type - string - a stem, without input to the function then value is 0
        :return: without input returns the number of words (with repeats) in the index, with a stem input returns the
        :exceptions: if the stem isn't inside the index trows an exception
        number of repeats
        """
        result = 0
        if stem == 0:
            result = self.count()
            return result
        else:
            if stem not in self.IStems:
                raise Exception("the requested stem -'", stem, "' does not exist in the index (from stemCount)")
            elif self.IStems[stem].size == 1:
                result = self.DocIndex[str(self.IStems[stem])].Stems[stem].size
            else:
                for i in range(self.IStems[stem].size):
                    result = result + self.DocIndex[self.IStems[stem][i]].Stems[stem].size
            return result

    def documentCount(self, term = 0):
        """
        :param term: type - string - a term, without input to the function then value is 0
        :return: returns the total number of documents in the Index (without input), returns the number
        of documents in the Index containing the term(with a term input)
        :exceptions: if the term isn't inside the index trows an exception
        """
        result = 0
        if term == 0 :
            result = len(self.DocIndex)
            return result
        else :
            if term in self.ITerms:
                result = self.ITerms[term].size
                return result
            else:
                raise Exception("the requested term -'", term, "' does not exist in the index (from documentCount)")

    def documentStemCount(self, stem):
        """
        :param stem: type - string - a stem
        :return: the number of documents in the Index containing the stem
        :exceptions: if the stem isn't inside the index trows an exception
        """
        result = 0
        if stem in self.IStems:
            result = self.IStems[stem].size
            return result
        else :
            raise Exception("the requested stem -'", stem, "' does not exist in the index (from documentStemCount)")

    def documentLength(self, documentID ):
        """
        :param documentID: type - string/int - a Document's Doc_ID
        :return: returns the length of the Document with the Doc_ID - documentID
        :exceptions: if there isn't a Document inside the Index with Doc_ID - documentID trows an exception
        """
        if  self.Doc_Exists_In_Index(documentID):
            length = 0
            for key in self.DocIndex[documentID].Terms:
                length = length + self.DocIndex[documentID].Terms[key].size
            return length
        else:
            raise Exception ("the doc_id -'",documentID,"' that it's length was requested does not exist in the Index")

    def UniqueTermsInIndex(self):
        """
        :return: returns the amount of unique terms in index (int)
        """
        return len(self.ITerms)

    def UniqueStemsInIndex(self):
        """
        :return: returns the amount of unique stems in index (int)
        """
        return len(self.IStems)

    def Idf_For_Stem(self, stem):
        """
        :param stem: type - string - a stem
        :return: the Idf rank of the stem in the Index, if the stem does not exist inside the Index returns 0
        """
        N = self.documentCount()
        try:
            n = self.documentStemCount(stem)
        except Exception as e:
            return 0
        else:
            return log10(float(N)/n)

    def runQuery(self, query, limit = 0):
        """
        :param query: type - string
        :param limit: type - int (positive) - without input the value is 0
        :return: returns a list of Documents that fits the query the most according to cosine similarity the length
        of the list is limit and if limit is 0 the length is the amount of Documents in the Index
        :exceptions: trows an exception if the query is empty (or contains only spaces) and if the input
        limit is bigger then the amount of Documents inside the Index
        """
        query = query.lower()
        if not query.strip():
            raise Exception('the query is empty')
        elif limit > self.documentCount():
            raise Exception('limit is bigger then amount of documents inside the Index')
        InputQuery = Query('TempQuery',query) # creates a temp Query without updating Ranker
        """
        ranklist = []
        for key in self.DocIndex:
            query_tfidf = np.array(0) # the zero just for initialize, doesn't have effect on result
            doc_tfidf = np.array(0)  # the zero just for initialize, doesn't have effect on result
            for key1 in InputQuery.Stems :
                if key1 in self.DocIndex[key].Stems: # creats the Tf_Idf vector only for words that are inside the query and Doc
                    idf = self.Idf_For_Stem(key1)
                    query_tfidf = np.append(query_tfidf, InputQuery.Tf_For_Stem(key1)*idf)
                    doc_tfidf = np.append(doc_tfidf, self.DocIndex[key].Tf_For_Stem(key1)*idf)
            if np.count_nonzero(doc_tfidf) == 0 or  np.count_nonzero(query_tfidf) == 0:# checks there's no division by 0 in cosine calculation
                CosinSimilarity = 0 # need to find out if exception is needed
            else:
                CosinSimilarity =  1.0 - spatial.distance.cosine(doc_tfidf, query_tfidf)
            if isnan(CosinSimilarity):
                CosinSimilarity = 0
            ranklist.append((self.DocIndex[key], CosinSimilarity))
        ranklist.sort(key=lambda tup: tup[1], reverse=True) # sorts in reverse order according to CosinSimilarity
        resultlist = []
        """
        ranker = RankerEnvironment(self)
        ranklist = ranker.Rank(InputQuery, limit)
        resultlist = []
        if limit == 0 :
            for i in range(len(ranklist)):
                resultlist.append(ranklist[i][0])
            return resultlist
        else:
            for i in range(limit):
                resultlist.append(ranklist[i][0])
        return resultlist

    def TfIdfUpdate(self):
        """
        :return: this method updates the TfIdf values of all the stems for all the documents in the index.
                  at the end it update the relevant flag.
        """
        for doc in self.DocIndex.values():
            for stem in doc.Stems:
                tf = doc.Tf_For_Stem(stem)
                idf = self.Idf_For_Stem(stem)
                doc.Tf_Idf_Ranks[stem] = tf*idf
        self.Tf_Idf_Flag = 1
        return




#**************----tests---******************
#try:
 #   Index.getDocuments(['hey','123','zubi'])
#except Exception as e:
 #   print(e)
#*********************************************
#for keys,values in Index.DocIndex.items():
#    print(keys)
#for keys,values in Index.DocIndex['hey'].Terms.items():
#   print(keys,values)
#print ('123:')
#for keys, values in Index.DocIndex['999'].Terms.items():
#   print(keys, values)
#print ('stems:')
#for keys, values in Index.DocIndex['hey'].Stems.items():
#   print(keys, values)
#print ('123:')
#for keys, values in Index.DocIndex['123'].Stems.items():
 #   print(keys, values)
#print("index:")
#for keys,values in Index.ITerms.items():
#    print(keys,values)
#print ('stems:')
#for keys,values in Index.IStems.items():
 #   print(keys, values)
 #*******************************************
#a = Index.DocIndex['hey'].Textlen
#b =Index.DocIndex['123'].RestoreText()
#print (a,b)
#*************************************************
#try:
#    y = Index.getDocumentsMetadata('TExT')
#except Exception as e:
#    print (e)
#else :
#    for i in range (len(y)):
#        print y[i]
#**************************************************
#print(Index.termCount())
#print(Index.termCount('5'))
#print(Index.stemCount())
#print(Index.stemCount('it'))
# *************************************************
#print(Index.documentCount())
#print(Index.documentCount('hey'))
#print(Index.documentStemCount('walk'))
#**************************************************
#print(Index.documentLength('123'))
#**************************************************
#a = ['hey','123']
#lis = Index.getDocuments(a)
#for i in range(len(lis)):
#    print a[i]
#    print lis[i]['terms']
#    print lis[i]['stems']
#    print lis[i]['termsPositions']
#    print lis[i]['stemsPositions']

#************************************************************
#print Index.UniqueTermsInIndex()
#print Index.UniqueStemsInIndex()
#***********************************************************
#list = Index.runQuery('hello in haifa i walk" very am')
#for i in range(len(list)):
#    print list[i]
#ranker = RankerEnvironment(Index)
#ranker.loadQueries("C:/Users/Ziv/Desktop/q.xml")
#ranker.runQuery('1',None,'C:/Users/Ziv/Desktop/jg')
