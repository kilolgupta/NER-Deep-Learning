import glob
import os
import re
import itertools
import unidecode

def createTrainValTestFiles():
	wordfilename = "testb.words.txt"
	tagfilename = "testb.tags.txt"
	wordfile = open(wordfilename,"w+")
	tagfile = open(tagfilename,"w+")

	infilename = "test.txt"
	lines = open(infilename).read().splitlines()

	sentence = ""
	tags = ""
	for line in lines:
		if(line==""):
			if(sentence!=""):
				wordfile.write(sentence.lower() + "\n")
				#sentences.append(sentence.lower())

				tagfile.write(tags + "\n")
				#taglist.append(tags)
				tags = ""
				sentence = ""
		else:
			elements = line.split(' ')
			sentence = sentence + " " + elements[0]
			tags = tags + " " + elements[3]

	wordfile.close()
	tagfile.close()

def createLeadersWordAndTagFile():
	wordfile = open("leaders.words.txt","w+")
	tagfile = open("leaders.tags.txt","w+")

	leaders = open("leadersNames.txt").read().splitlines()
	for l in leaders:
		if(" " in l):
			names = l.split(' ')
			names_length = len(names)
			wordfile.write(l.lower() + "\n")

			tagfile.write("B-PER")
			for i in range(1, len(names)):
				tagfile.write(" I-PER")
			tagfile.write("\n")
		else:
			wordfile.write(l.lower() + "\n")
			tagfile.write("B-PER\n")

	wordfile.close()
	tagfile.close()

def createTestDataFromHistoryCables():
	mypath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/*.txt"
	onlyfiles = glob.glob(mypath)
	print(len(onlyfiles))
	count = 0
	for file in onlyfiles:
		count += 1
		outfile = open(os.path.basename(file), "w+")
		infile = open(file).read()
		lines = infile.split(". ")
		for line in lines:
			line = line.lower()
			#line = re.sub(ur"[^\w\d'\s]+","",line).strip()
			if line:
				outfile.write(line.lower() + "\n")
		outfile.close()
	print(count)

def addSpacesAroundPunctuation():
	mypath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/splitlined/*.txt"
	onlyfiles = glob.glob(mypath)
	count = 0
	for file in onlyfiles:
		count += 1
		outfile = open(os.path.basename(file), "w+")
		lines = open(file).read().splitlines()
		for line in lines:
			line = re.sub(r'([.,!?()]":\'-)', r' \1 ', line)
			line = re.sub(r'\s{2,}', ' ', line).strip()
			if line:
				outfile.write(line + "\n")
		outfile.close()
	print(count)


def removingPunctuationExceptApostrophe():
	mypath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/splitlined/*.txt"
	onlyfiles = glob.glob(mypath)
	count = 0
	for file in onlyfiles:
		count += 1
		outfile = open(os.path.basename(file), "w+")
		lines = open(file).read().splitlines()
		for line in lines:
			#line = re.sub(ur"[^\w\d'\s]+","",line).strip()
			if line:
				outfile.write(line + "\n")
		outfile.close()
	print(count)


def formatPredictionFiles():
	mypath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/predictions_cables_2632/*_predictions.txt"
	onlyfiles = glob.glob(mypath)
	count = 0
	for file in onlyfiles:
		count += 1
		outfile = open(os.path.basename(file), "w+")
		lines = open(file).read().splitlines()
		for line in lines:
			line = re.sub('\n ', ' ', line)
			if line:
				outfile.write(line + "\n")
		outfile.close()
	print(count)


def getPersonsFromFile(filename):
	print(filename)

	outfile = open(filename, "w+")
	
	predictionfile = open("/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/predictions/" + filename[:-4] + "_predictions.txt")
	predictions = predictionfile.read().splitlines() # list: predictions for ith file

	textfile = open("/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/no_punctuation_splitlined/" + filename)
	sentences = textfile.read().splitlines() # list: sentences for ith file
	if(len(sentences) != len(predictions)):
		print("incorrect")
		exit()

	names = []
	for i in range(len(sentences)):
		p = predictions[i]
		s = sentences[i]
		words = s.split()
		if("3" in p):
			p = p[1:-1] # removing the square brackets
			tag_indices = p.split(', ')
			if(len(words) != len(tag_indices)):
				print("incorrect")
				print(s + "\n")
				print(p)
				exit()
			
			for i in range(len(words)-1): # going till second last word
				if tag_indices[i] == "3":
					if tag_indices[i+1] != "7": # single word name
						names.append(words[i])
					else: # multi-word name
						name = words[i]
						i += 1
						while tag_indices[i] == "7":
							name = name + " " + words[i]
							i += 1
							if i >= len(tag_indices):
								break
						i -= 1 # to avoid double increment
						names.append(name)

			if tag_indices[len(words)-1] == "3": # checking if the last word is a single-word name. A multi-word name can't begin at last index of the sentence
				names.append(s[len(words)-1])
	set_names = set(names)
	for n in set_names:
		outfile.write(n + "\n")
	outfile.close()

def getPersonsFromEachFile():
	f = 0
	textfilespath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/no_punctuation_splitlined/*.txt"
	textfiles = glob.glob(textfilespath)
	for file in textfiles:
		filename = os.path.basename(file)
		print(filename)
		getPersonsFromFile(filename)
		f+=1

	print("count of files processed: " + str(f))

def createGoldLabelData():
	textfilespath = "/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/original_gold_label_training_files/*.txt"
	textfiles = glob.glob(textfilespath)
	for file in textfiles:
		filename = os.path.basename(file)
		print(filename)
		outfile = open(filename, "w+")
		textfile = open("/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/original_gold_label_training_files/" + filename)
		sentences = textfile.read().splitlines()
		for s in sentences:
			if s.strip() == "@@@" or s.strip() == "":
				break
			else:
				words = s.strip().split()
				tag = words[-1]
				if tag.startswith("PER.IND"):
					name = ""
					for i in range(1, len(words)-1):
						if words[i][0].isdigit(): continue

						name = name + words[i] + " "
					name = name[:-1]
					print(name + "\n")
					unaccented_name = unidecode.unidecode(name)
					print(unaccented_name)
					outfile.write(unaccented_name.lower() + "\n")
		outfile.close()


#getPersonsFromEachFile()
#getPersonsFromFile("1973BAGHDA00113.txt")
#getPersonsFromEachFile()

#createTestDataFromHistoryCables()

createGoldLabelData()




