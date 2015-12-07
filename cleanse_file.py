import os, re, string
from nltk.corpus import stopwords


def cleanse_data(text):

##
	##  Remove all non relevent symbols and get the text
	## that can be used to clean our data with noise
##
#	temp = text.lower()
	print "cleanse data"
	temp = text

#	temp = re.sub(r'(\w{3}( )\d\d\d\d)'," YEAR ",temp)
	temp = re.sub(r'(\d+(\s)?(yrs|year|years|Yrs|Years|Year|yr))'," TIME ",temp)
	temp = re.sub(r'[\w\.-]+@[\w\.-]+'," EMAIL ",temp)
	temp = re.sub(r'(((\+91|0)?( |-)?)?\d{10})',' MOBILE ',temp)
#	temp = re.sub(r'[\d(.\d+)?]+'," NUMERIC ",temp)
	temp = re.sub(r"[\t\s]+"," ",temp)
	temp = re.sub(r"[\r\n]+","\n",temp)	
	cachedStopWords = stopwords.words("english")
	text = ' '.join([word for word in temp.split(" ") if word not in cachedStopWords])
#	wordFilter = set(string.punctuation)
#	temp = ''.join(ch for ch in text if ch not in wordFilter)
	#temp = re.sub(r'[^\w.]+',' ',temp)
	wF = string.punctuation
	for c in wF:
        	temp =text.replace(c," ")

	return temp


def scan_file(dir_name):

##
	##  scan every file in a directory 
	##  and extract text from it
##
	print "scanning directory"
	for fname in os.listdir(dir_name):
		print "scanning lines"
		fp = open(os.path.join(dir_name, fname),"r")
		text = fp.read()
		yield cleanse_data(text)

def main():

	dir_name = '/home/viswanath/workspace/resume_data/accepted_profiles'
	text_seq = scan_file(dir_name)
	text_ = ''
	for text in text_seq:
		text_ += '\n'
		text_ += text
	
	print 'writing data'
	fp = open('cleanse_text_ads.txt',"w")
	fp.write(text_)
	fp.close()

if __name__ == '__main__': main()
