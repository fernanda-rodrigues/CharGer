#!/usr/bin/python
# CharGer - Characterization of Germline variants
# author: Adam D Scott (ascott@genome.wustl.edu)
# version: v0.0 - 2015*12

import sys
import getopt
from entrezAPI import entrezAPI
from exacAPI import exacAPI
import variant

def parseArgs( argv ):
	helpText = "python main.py" + " "
	helpText += "-i \"input (.maf)\" "
	helpText += "(-c suppress ClinVar, "
	helpText += "-x suppress ExAC, "
	helpText += "-o \"output\")\n"
	inputFile = ""
	output = ""
	clinvar = True
	exac = True
	try:
		opts, args = getopt.getopt( argv , "cxh:i:o:" , ["input=" , "output="] )
	except getopt.GetoptError:
		print "ADSERROR: Command not recognized"
		print( helpText ) 
		sys.exit(2)
	if not opts:
		print "ADSERROR: Expected flagged input"
		print( helpText ) 
		sys.exit(2)
	for opt, arg in opts:
		#print opt + " " + arg
		if opt in ( "-h" , "--help" ):
			print( helpText )
			sys.exit()
		elif opt in ( "-i" , "--inputFile" ):
			inputFile = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
		elif opt in ( "-c" , "--help" ):
			clinvar = False
		elif opt in ( "-x" , "--help" ):
			exac = False
	return { "input" : inputFile , "output" : output , "clinvar" : clinvar , "exac" : exac }
	
def checkConnection():
	print "\tChecking Connection!"
	entrezInstance = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]"
	summaryTest = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=20113659,20074456"
	res = requests.get( entrezInstance )
	if res:
		print "have response"
	else:
		print res.status_code

def splitByVariantType( inputFile ):
	print "\tSplitting .maf by variant type!"
	variants = {}
	variantsBySampleAndType = {}
	if inputFile:
		inFile = open( inputFile , 'r' )
		next(inFile)
		gv = {}
		for line in inFile:
			fields = line.split( "\t" )
			var = variant.variant()
			var.mafLine2Variant( line )
			#var.printVariant("\t")
			sample = fields[15]
			variantClass = var.variantClass
			genVar = var.genomicVar()
			vc = {}
			s = {}
			gv = {}
			if variantClass in variantsBySampleAndType:
				#print variantClass
				vc = variantsBySampleAndType[variantClass] #dict of variants by variantClass=>samples dict
			if sample in vc:
				#print sample
				s = vc[sample] #dict of samples by sample=>genVars dict
			if genVar in s:
				#print genVar
				gv = s[genVar]
			tempgv = { "line" : line , "variant" : var }
			gv.update( tempgv )
			temps = { genVar : gv }
			s.update( temps )
			tempvc = { sample : s }
			vc.update( tempvc )
			#print genVar + "=>" + s[genVar]
			tempVariants = { variantClass : tempvc }
			variantsBySampleAndType.update( tempVariants )
			variants[genVar] = var
	return { "variants" : variants , "variantsBySampleAndType" : variantsBySampleAndType }
	#nonsense, frameshift, canonical 1 or 2 splice sites, initiation codon, single exon or multiexon deletion

def PVS1( variants ):
	return None
def PS1( inputVariants , clinvarVariants , clinvarClinical ):
	print "CharGer module PS1"
	print "- same peptide change that is pathogenic and is a different genomic variant of the same reference peptide"
	peptideChange( inputVariants , clinvarVariants , clinvarClinical , "PS1" )
def PM5( inputVariants , clinvarVariants , clinvarClinical ):
	print "CharGer module PM5"
	print "- different peptide change of a pathogenic variant at the same reference peptide"
	peptideChange( inputVariants , clinvarVariants , clinvarClinical , "PM5" )
def peptideChange( inputVariants , clinvarVariants , clinvarClinical , mod ):
	calls = {}
	for thisVar in inputVariants:
		inVar = inputVariants[thisVar]
		genVar = inVar.genomicVar()
		print "\tInput variant: " + genVar , 
		canBePM1 = True
		canBePM5 = True
		pm1Call = False
		pm5Call = False
		call = {}
		if genVar in calls:
			call = calls[genVar]
		else:
			call = { genVar : False }
		if not call[genVar]: #is already true
			print "checking"
			call[genVar] = False
			for uid in clinvarVariants:
				var = clinvarVariants[uid]
				if uid in clinvarClinical:
					clin = clinvarClinical[uid]
					if inVar.chromosome == var.chromosome and \
						inVar.start == var.start and \
						inVar.stop == var.stop and \
						inVar.reference == var.reference and \
						inVar.referencePeptide == var.referencePeptide and \
						inVar.positionPeptide == var.positionPeptide: #same genomic position & reference
						if inVar.mutantPeptide == var.mutantPeptide: #same amino acid change
							if clin["description"] == "Pathogenic":
								print "Already called pathogenic: " ,
								var.printVariant(' ')
								canBePM1 = False
								canBePM5 = False
							else:
								print "This is NOT called as pathogenic: " ,
								var.printVariant(' ')
								if mod == "PM1":
									pm1Call = True
						else: #different amino acid change ( CAN BE USED FOR PM5 )
							if clin["description"] == "Pathogenic":
								print "Alternate peptide change called pathogenic: " ,
								var.printVariant(' ')
								if mod == "PM5":
									pm5Call = True
							else:
								print "Alternate peptide change NOT called as pathogenic: " ,
								var.printVariant(' ')
				else:
					print "Not given a clinical call: " ,
					var.printVariant(' ')
			if mod == "PM1":
				if canBePM1:
					call[genVar] = pm1Call
			if mod == "PM5":
				if canBePM5:
					call[genVar] = pm5Call
		calls.update( call )
	return calls

def PVS1( inputFile , searchVariants , inputVariants , ClinVarVariants , ClinVarClinical ):
	geneList = readGeneList( inputFile )
	calls = {}
	if geneList: #gene, disease, mode of inheritance
		for gene in geneList: #want only autosomal dominant
			line = geneList[gene]
		#variant expression calls from Kuan function
		getExpression( var )
	return calls

def getExpression( var ): #Kuan 
	print ""

def isFrequentAllele( freq , threshold ):
	if freq > threshold:
		return True
	return False
def readGeneList( inputFile , col ):
	geneList = {}
	if inputFile:
		inFile = open( inputFile , 'r' )
		next(inFile)
		gv = {}
		for line in inFile:
			fields = line.split( "\t" )
			geneList[fields[col]] = line
	return geneList

def prepQuery( inputFile , ent , searchVariants ):
	for variantClass in searchVariants:
		for sample in searchVariants[variantClass]:
			for genVar in searchVariants[variantClass][sample]:
				thisGroup = sample+genVar
				var = searchVariants[variantClass][sample][genVar]["variant"]
				ent.addQuery( var.gene , field="gene" , group=thisGroup )
				ent.addQuery( var.chromosome , field="chr" , group=thisGroup )
				ent.addQuery( var.start + ":" + var.stop , field="chrpos37" , group=thisGroup )
				ent.addQuery( "human" , field="orgn" , group=thisGroup )
				#ent.addQuery( var.variantClass , "vartype" )
				#ent.addQuery( var.referencePeptide + var.positionPeptide + var.mutantPeptide , "Variant name" )
				#var.referencePeptide , var.positionPeptide , var.mutantPeptide
	return ent

def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFormat = values["output"]
	doClinVar = values["clinvar"]
	doExAC = values["exac"]

	userVariants = splitByVariantType( inputFile )
	inputVariants = userVariants["variants"]
	variantsBySampleAndType = userVariants["variantsBySampleAndType"]
	
	if doClinVar:
		ent = entrezAPI()	
		ent = prepQuery( inputFile , ent )
		ent.database = entrezAPI.clinvar
		clinvarEntries = ent.doBatch( 5 )
		clinvarVariants = clinvarEntries["variants"]
		clinvarTraits = clinvarEntries["traits"]
		clinvarClinical = clinvarEntries["clinical"]

		PVS1( variantsBySampleAndType , inputVariants , clinvarVariants , clinvarClinical )
		PS1( inputVariants , clinvarVariants , clinvarClinical )
		PM5( inputVariants , clinvarVariants , clinvarClinical )

	if doExAC:
		exac = exacAPI(harvard=True)
		exacEntries = exac.getAlleleFrequencies( inputVariants )
		thresh = 0
		for genVar in exacEntries:
			alleleFrequency = exacEntries[genVar]
			if isFrequentAllele( alleleFrequency , thresh ):
				print genVar + " is NOT rare(" + str(thresh) + "): " + str(alleleFrequency)

if __name__ == "__main__":
	main( sys.argv[1:] )
