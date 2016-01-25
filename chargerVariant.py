#!/usr/bin/python
# chargerVariant - CharGer annotated variants
# author: Adam D Scott (ascott@genome.wustl.edu) & Kuan-lin Huang (khuang@genome.wustl.edu)
# version: v0.0 - 2016*01*13

from WebAPI.Variant.clinvarVariant import clinvarVariant

class chargerVariant(clinvarVariant):
	pathogenic = "Pathogenic"
	likelyPathogenic = "Likely Pathogenic"
	likelyBenign = "Likely Benign"
	benign = "Benign"
	uncertain = "Uncertain Significance"
	def __init__( self , **kwargs ):
		super(chargerVariant,self).__init__(**kwargs)
		self.PVS1 = kwargs.get( 'PVS1' , False )
		self.PS1 = kwargs.get( 'PS1' , False )
		self.PS2 = kwargs.get( 'PS2' , False )
		self.PS3 = kwargs.get( 'PS3' , False )
		self.PS4 = kwargs.get( 'PS4' , False )
		self.PM1 = kwargs.get( 'PM1' , False )
		self.PM2 = kwargs.get( 'PM2' , False )
		self.PM3 = kwargs.get( 'PM3' , False )
		self.PM4 = kwargs.get( 'PM4' , False )
		self.PM5 = kwargs.get( 'PM5' , False )
		self.PM6 = kwargs.get( 'PM6' , False )
		self.PP1 = kwargs.get( 'PP1' , False )
		self.PP2 = kwargs.get( 'PP2' , False )
		self.PP3 = kwargs.get( 'PP3' , False )
		self.PP4 = kwargs.get( 'PP4' , False )
		self.PP5 = kwargs.get( 'PP5' , False )
		self.alleleFrequency = kwargs.get( 'alleleFrequency' , None )
		self.pathogenicity = kwargs.get( 'pathogenicity' , chargerVariant.uncertain )
		self.clinical = kwargs.get( 'clinical' , { "description" : chargerVariant.uncertain , "review_status" : "" } )
	def check( self , mod ):
		checks = self.checks()
		return checks[mod]
	def checks( self ):
		checks = {}
		mods = self.modules()
		checks[mods[0]] = self.PVS1
		checks[mods[1]] = self.PS1
		checks[mods[2]] = self.PS2
		checks[mods[3]] = self.PS3
		checks[mods[4]] = self.PS4
		checks[mods[5]] = self.PM1
		checks[mods[6]] = self.PM2
		checks[mods[7]] = self.PM3
		checks[mods[8]] = self.PM4
		checks[mods[9]] = self.PM5
		checks[mods[10]] = self.PM6
		checks[mods[11]] = self.PP1
		checks[mods[12]] = self.PP2
		checks[mods[13]] = self.PP3
		checks[mods[14]] = self.PP4
		checks[mods[15]] = self.PP5
		return checks
	def modules( self ):
		return ['PVS1' , \
		'PS1' , 'PS2' , 'PS3' , 'PS4' , \
		'PM1' , 'PM2' , 'PM3' , 'PM4' , 'PM5' , 'PM6' , \
		'PP1' , 'PP2' , 'PP3' , 'PP4' , 'PP5' ]
	def hasAlleleFrequency( self ):
		if var.alleleFrequency == None:
			return False
		return True
	def isFrequentAllele( self , threshold ):
		if self.alleleFrequency > threshold:
			return True
		return False
	def countStrong( self ):
		count = 0
		if self.PS1:
			count += 1
		if self.PS2:
			count += 1
		if self.PS3:
			count += 1
		if self.PS4:
			count += 1
		return count
	def countModerate( self ):
		count = 0
		if self.PM1:
			count += 1
		if self.PM2:
			count += 1
		if self.PM3:
			count += 1
		if self.PM4:
			count += 1
		if self.PM5:
			count += 1
		if self.PM6:
			count += 1
		return count
	def countSupport( self ):
		count = 0
		if self.PP1:
			count += 1
		if self.PP2:
			count += 1
		if self.PP3:
			count += 1
		if self.PP4:
			count += 1
		if self.PP5:
			count += 1
		return count
	def isPathogenic( self ):
		numStrong = self.countStrong()
		numModerate = self.countModerate()
		numSupport = self.countSupport()
		if self.PVS1:
			if numStrong >= 1 or \
			numModerate >= 2 or \
			(numModerate+numSupport) >= 2 or \
			numSupport >= 2:
				self.setAsPathogenic()
				return True
		elif numStrong >= 2:
			self.setAsPathogenic()
			return True
		elif numStrong >= 1:
			if numModerate >= 3 or \
			(numModerate == 2 and numSupport >= 2) or \
			(numModerate == 1 and numSupport >= 4):
				self.setAsPathogenic()
				return True
	def isLikelyPathogenic( self ):
		numStrong = self.countStrong()
		numModerate = self.countModerate()
		numSupport = self.countSupport()
		if numStrong and numModerate == 1:
			self.setAsLikelyPathogenic()
			return True
		if numStrong == 1 and ( numModerate == 1 or numModerate == 2 ):
			self.setAsLikelyPathogenic()
			return True
		if numStrong == 1 and numSupport >= 2:
			self.setAsLikelyPathogenic()
			return True
		if numModerate >= 3:
			self.setAsLikelyPathogenic()
			return True
		if numModerate == 2 and numSupport >= 2:
			self.setAsLikelyPathogenic()
			return True
		if numModerate == 1 and numSupport >= 4:
			self.setAsLikelyPathogenic()
			return True
	def isLikelyBenign( self ):
		NotImplemented
	def isBenign( self ):
		NotImplemented
	def isUncertainSignificance( self ):
		if ( self.isPathogenic() or self.isLikelyPathogenic() )and \
		( self.isBenign() or self.isLikelyBenign() ):
			self.setAsUncertainSignificance()
			return True
	def setAsPathogenic( self ):
		self.pathogenicity = chargerVariant.pathogenic
	def setAsLikelyPathogenic( self ):
		self.pathogenicity = chargerVariant.likelyPathogenic
	def setAsLikelyBenign( self ):
		self.pathogenicity = chargerVariant.likelyBenign
	def setAsBenign( self ):
		self.pathogenicity = chargerVariant.benign
	def positiveEvidence( self ):
		positive = []
		checks = self.checks()
		for k in sorted(checks.keys()):
			if checks[k]:
				positive.append(k)
		return ",".join(positive)
