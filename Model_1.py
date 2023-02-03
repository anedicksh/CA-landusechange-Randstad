from pcraster import *
from pcraster.framework import *

class MyFirstModel(DynamicModel):

  def toScalar(categoryMap, categoryInt):
    mapName = scalar(categoryMap == categoryInt)
    return mapName

  def noofNei(categoryMap, categoryInt, neiSize):
    noofNei = windowtotal(MyFirstModel.toScalar(categoryMap, categoryInt),\
                          celllength()*neiSize)
    return noofNei

  def enrichment(categoryMap, categoryInt, neiSize, total):
    landuseNei = MyFirstModel.noofNei(categoryMap, categoryInt, neiSize)
    firstfactor = ifthenelse(landuseNei/(neiSize*neiSize)>0, landuseNei/(neiSize*neiSize), 0)
    landuseMap = areatotal(MyFirstModel.toScalar(categoryMap, categoryInt),\
                 categoryMap == categoryInt)
    secondfactor = ifthenelse(landuseMap/total>0,landuseMap/total,0)
    enrichment = ifthenelse(firstfactor == 0,scalar(0),ifthenelse(secondfactor==0,scalar(0),firstfactor/secondfactor))
    return enrichment

  def meanenrichment(enrichment, categoryMap, categoryInt):
    meanenrichment = areatotal(enrichment, categoryMap == categoryInt)/\
                     areatotal(MyFirstModel.toScalar(categoryMap, categoryInt),\
                     categoryMap == categoryInt)
    return meanenrichment
      
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('randstad.map')

  def initial(self):
        
    #reading landuse map
    self.landuse = self.readmap('randstad')
    self.report(self.landuse,'randstad')

    #category
    categoryTable = "category.tbl"
    self.category = lookupnominal(categoryTable, self.landuse)
    self.report(self.category, 'category')
    #urban
    self.residential = self.category == 1
    self.report(self.residential,'resident')

    initcategory = self.category
    self.report(initcategory, 'initcat')

    #initial urban
    initresidential = self.category == 1
    self.report(initresidential, 'initres')

    #counting total number of cells
    totalScalar = ifthenelse(self.landuse == -1, scalar(0), scalar(1))
    totalNominal = nominal(totalScalar)
    self.total = areatotal(totalScalar, totalNominal)
    
  def dynamic(self):

    #initializing scalars
    #urbanScalar = scalar(self.urban)
    airportScalar = MyFirstModel.toScalar(self.category, 8)
    #trafficScalar = scalar(self.category == 8)
    #recreationScalar = scalar(self.category == 2)
    #greenhouseScalar = scalar(self.category == 3)
    #agriScalar = scalar(self.category == 4)
    #natureScalar = scalar(self.category == 5)
    waterScalar = MyFirstModel.toScalar(self.category, 6)
    #outsideWaterScalar = scalar(self.category == 7)
    #counting # close neighbours of each category
    #closenoOfUrban=windowtotal(urbanScalar, celllength()*3)
    #closenoOfAirport=windowtotal(airportScalar, celllength()*3)-airportScalar
    #closenoOfTraffic=windowtotal(trafficScalar, celllength()*3)-trafficScalar
    #closenoOfRecreation=windowtotal(recreationScalar, celllength()*3)-recreationScalar
    #closenoOfGreenhouse=windowtotal(greenhouseScalar, celllength()*3)-greenhouseScalar
    #closenoOfAgri=windowtotal(agriScalar, celllength()*3)-agriScalar
    #closenoOfNature=windowtotal(natureScalar, celllength()*3)-natureScalar
    #closenoOfInsideWater=windowtotal(insideWaterScalar, celllength()*3)-insideWaterScalar
    #closenoOfOutsideWater=windowtotal(outsideWaterScalar, celllength()*3)-outsideWaterScalar
    
    #counting # distant neighbours of each category
    #distantnoOfUrban=windowtotal(urbanScalar, celllength()*7)-urbanScalar
    #distantnoOfAirport=windowtotal(airportScalar, celllength()*7)-airportScalar
    #distantnoOfTraffic=windowtotal(trafficScalar, celllength()*7)-trafficScalar
    #distantnoOfRecreation=windowtotal(recreationScalar, celllength()*7)-recreationScalar
    #distantnoOfGreenhouse=windowtotal(greenhouseScalar, celllength()*7)-greenhouseScalar
    #distantnoOfAgri=windowtotal(agriScalar, celllength()*7)-agriScalar
    #distantnoOfNature=windowtotal(natureScalar, celllength()*7)-natureScalar
    #distantnoOfInsideWater=windowtotal(insideWaterScalar, celllength()*7)-insideWaterScalar
    #distantnoOfOutsideWater=windowtotal(outsideWaterScalar, celllength()*7)-outsideWaterScalar

    #enrichment factors
    closeResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 3, self.total)
    closeIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 3, self.total)
    closeNatureEnrich = MyFirstModel.enrichment(self.category, 5, 3, self.total)
    distantResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 7, self.total)
    distantIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 7, self.total)
    self.report(closeResidentialEnrich, "cre")
    self.report(closeIndustrialEnrich, "cie")
    self.report(closeNatureEnrich, "cne")
    self.report(distantResidentialEnrich,"dre")
    self.report(distantIndustrialEnrich,"die")


    #assigning coefficents for each category
    constant = -5.537

    #cellUrbanWeight = 0.364
    cellAirportWeight = -1000
    #cellTrafficWeight = -0.5
    #cellRecreationWeight = -0.5
    #cellGreenhouseWeight = -0.5
    #cellAgriWeight = 0
    #cellNatureWeight = -0.201
    cellWaterWeight = -1000
    #cellOutsideWaterWeight = -1000
    
    closeResidentialWeight = 0.864
    closeIndustrialWeight = 0.823
    #closeAirportWeight = 0.364
    #closeTrafficWeight = 0.364
    #closeRecreationWeight = 0.2
    #closeGreenhouseWeight = 0
    #closeAgriWeight = -0.05
    closeNatureWeight = -0.101
    #closeInsideWaterWeight = 0.1
    #closeOutsideWaterWeight = 0
    
    distantResidentialWeight = 0.890
    distantIndustrialWeight = 0.828
    #distantAirportWeight = 0.01
    #distantTrafficWeight = 0.01
    #distantRecreationWeight = 0.01
    #distantGreenhouseWeight = 0
    #distantAgriWeight = 0
    #distantNatureWeight = 0
    #distantInsideWaterWeight = 0.01
    #distantOutsideWaterWeight = 0

    #formula
    #newUrban = constant + cellUrbanWeight * urbanScalar + cellAirportWeight *\
    #airportScalar + cellTrafficWeight * trafficScalar + cellRecreationWeight *\
    #recreationScalar + cellGreenhouseWeight * greenhouseScalar + cellAgriWeight*\
    #agriScalar + cellNatureWeight * natureScalar + cellInsideWaterWeight*\
    #insideWaterScalar + cellOutsideWaterWeight * outsideWaterScalar +\
    #closeUrbanWeight * closenoOfUrban + closeAirportWeight * closenoOfAirport +\
    #closeTrafficWeight * closenoOfTraffic + closeRecreationWeight *\
    #closenoOfRecreation + closeGreenhouseWeight * closenoOfGreenhouse +\
    #closeAgriWeight * closenoOfAgri + closeNatureWeight * closenoOfNature +\
    #closeInsideWaterWeight * closenoOfInsideWater + closeOutsideWaterWeight *\
    #closenoOfOutsideWater + distantUrbanWeight * distantnoOfUrban +\
    #distantAirportWeight * distantnoOfAirport + distantTrafficWeight *\
    #distantnoOfTraffic + distantRecreationWeight * distantnoOfRecreation +\
    #distantGreenhouseWeight * distantnoOfGreenhouse + distantAgriWeight *\
    #distantnoOfAgri + distantNatureWeight * distantnoOfNature+\
    #distantInsideWaterWeight * distantnoOfInsideWater +\
    #distantOutsideWaterWeight * distantnoOfOutsideWater
    exponent = exp(constant + cellAirportWeight * airportScalar + cellWaterWeight *\
               waterScalar + closeResidentialWeight * closeResidentialEnrich +\
               closeIndustrialWeight * closeIndustrialEnrich + closeNatureWeight*\
               closeNatureEnrich + distantResidentialWeight *\
               distantResidentialEnrich + distantIndustrialWeight *\
               distantIndustrialEnrich)
    self.report(exponent, 'exp')
    localprob = exp(constant + cellAirportWeight * airportScalar + cellWaterWeight *\
               waterScalar + closeResidentialWeight * closeResidentialEnrich +\
               closeIndustrialWeight * closeIndustrialEnrich + closeNatureWeight*\
               closeNatureEnrich + distantResidentialWeight *\
               distantResidentialEnrich + distantIndustrialWeight *\
               distantIndustrialEnrich)/ (1 + exp(constant + cellAirportWeight * airportScalar + cellWaterWeight *\
               waterScalar + closeResidentialWeight * closeResidentialEnrich +\
               closeIndustrialWeight * closeIndustrialEnrich + closeNatureWeight*\
               closeNatureEnrich + distantResidentialWeight *\
               distantResidentialEnrich + distantIndustrialWeight *\
               distantIndustrialEnrich))

    self.report(localprob, 'locprob')

    numberDeveloped = MyFirstModel.noofNei(self.category, 1, 3) +\
                      MyFirstModel.noofNei(self.category, 7, 3)

    devdens = numberDeveloped/(3*3-1)
    self.report(devdens, "devdens")

    stochTestFac = 1
    stochTestEff = 10

    stochdis = (1+(-ln(stochTestFac)**stochTestEff))
    self.report(stochdis,"stodis")

    newResidential = localprob * devdens * stochdis
    self.report(newResidential, 'newres')

    potentRes = newResidential > 0.5
    self.report(potentRes, "potRes")

    residentialTreshold = pcrand(newResidential > 0.5, pcrnot(self.residential))
    self.report(residentialTreshold,'restres')                     

    # update residential map
    self.residential = pcror(residentialTreshold, self.residential)
    self.report(self.residential,'resident')
    self.category = ifthenelse(self.residential, 1, self.category)
    self.report(self.category, 'category')
    

nrOfTimeSteps=20
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

  




