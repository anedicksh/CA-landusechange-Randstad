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
    secondfactor = mapmaximum(landuseMap/total)
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
    categoryTable = "category_model3.tbl"
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

    #init enrichfactors
    closeResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 3, self.total)
    closeRecreationEnrich = MyFirstModel.enrichment(self.category, 2, 3, self.total)
    closeGreenhouseEnrich = MyFirstModel.enrichment(self.category, 3, 3, self.total)
    closeAgriEnrich = MyFirstModel.enrichment(self.category, 4, 3, self.total)
    closeNatureEnrich = MyFirstModel.enrichment(self.category, 5, 3, self.total)
    closeWaterEnrich = MyFirstModel.enrichment(self.category, 6, 3, self.total)
    closeIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 3, self.total)
    closeAirportEnrich = MyFirstModel.enrichment(self.category, 8, 3, self.total)
    closeRoadEnrich = MyFirstModel.enrichment(self.category, 9, 3, self.total)
    closeTrainEnrich = MyFirstModel.enrichment(self.category, 10, 3, self.total)
    closeSemiUrbanEnrich = MyFirstModel.enrichment(self.category, 11, 3, self.total)

    middleResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 5, self.total)
    middleRecreationEnrich = MyFirstModel.enrichment(self.category, 2, 5, self.total)
    middleGreenhouseEnrich = MyFirstModel.enrichment(self.category, 3, 5, self.total)
    middleAgriEnrich = MyFirstModel.enrichment(self.category, 4, 5, self.total)
    middleNatureEnrich = MyFirstModel.enrichment(self.category, 5, 5, self.total)
    middleWaterEnrich = MyFirstModel.enrichment(self.category, 6, 5, self.total)
    middleIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 5, self.total)
    middleAirportEnrich = MyFirstModel.enrichment(self.category, 8, 5, self.total)
    middleRoadEnrich = MyFirstModel.enrichment(self.category, 9, 5, self.total)
    middleTrainEnrich = MyFirstModel.enrichment(self.category, 10, 5, self.total)
    middleSemiUrbanEnrich = MyFirstModel.enrichment(self.category, 11, 5, self.total)

    distantResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 7, self.total)
    distantRecreationEnrich = MyFirstModel.enrichment(self.category, 2, 7, self.total)
    distantGreenhouseEnrich = MyFirstModel.enrichment(self.category, 3, 7, self.total)
    distantAgriEnrich = MyFirstModel.enrichment(self.category, 4, 7, self.total)
    distantNatureEnrich = MyFirstModel.enrichment(self.category, 5, 7, self.total)
    distantWaterEnrich = MyFirstModel.enrichment(self.category, 6, 7, self.total)
    distantIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 7, self.total)
    distantAirportEnrich = MyFirstModel.enrichment(self.category, 8, 7, self.total)
    distantRoadEnrich = MyFirstModel.enrichment(self.category, 9, 7, self.total)
    distantTrainEnrich = MyFirstModel.enrichment(self.category, 10, 7, self.total)
    distantSemiUrbanEnrich = MyFirstModel.enrichment(self.category, 11, 7, self.total)

    self.report(closeResidentialEnrich,"close1F")
    self.report(closeRecreationEnrich,"close2F")
    self.report(closeGreenhouseEnrich, "close3F")
    self.report(closeAgriEnrich, "close4F")
    self.report(closeNatureEnrich, "close5F")
    self.report(closeWaterEnrich, "close6F")
    self.report(closeIndustrialEnrich, "close7F")
    self.report(closeAirportEnrich, "close8F")
    self.report(closeRoadEnrich, "close9F")
    self.report(closeTrainEnrich, "close10F")
    self.report(closeSemiUrbanEnrich, "close11F")

    self.report(middleResidentialEnrich,"mid1F")
    self.report(middleRecreationEnrich,"mid2F")
    self.report(middleGreenhouseEnrich, "mid3F")
    self.report(middleAgriEnrich, "mid4F")
    self.report(middleNatureEnrich, "mid5F")
    self.report(middleWaterEnrich, "mid6F")
    self.report(middleIndustrialEnrich, "mid7F")
    self.report(middleAirportEnrich, "mid8F")
    self.report(middleRoadEnrich, "mid9F")
    self.report(middleTrainEnrich, "mid10F")
    self.report(middleSemiUrbanEnrich, "mid11F")

    self.report(distantResidentialEnrich,"dis1F")
    self.report(distantRecreationEnrich,"dis2F")
    self.report(distantGreenhouseEnrich, "dis3F")
    self.report(distantAgriEnrich, "dis4F")
    self.report(distantNatureEnrich, "dis5F")
    self.report(distantWaterEnrich, "dis6F")
    self.report(distantIndustrialEnrich, "dis7F")
    self.report(distantAirportEnrich, "dis8F")
    self.report(distantRoadEnrich, "dis9F")
    self.report(distantTrainEnrich, "dis10F")
    self.report(distantSemiUrbanEnrich, "dis11F")

    
  def dynamic(self): 
    #random
    uniformMap = uniform(scalar(self.category) > 0)

    #residentialswitch
    resToRes = pcrand(self.category == 1, uniformMap <= 0.916944)
    resToRec = pcrand(self.category == 1, pcrand(0.916944 < uniformMap, uniformMap <= 0.943153))
    resToAgri = pcrand(self.category == 1, pcrand(0.943153 < uniformMap, uniformMap <= 0.952012))
    resToNature = pcrand(self.category == 1, pcrand(0.952012 < uniformMap, uniformMap <= 0.956442))
    resToWater = pcrand(self.category == 1, pcrand(0.956442 < uniformMap, uniformMap <= 0.962717))
    resToIndustrial = pcrand(self.category == 1, pcrand(0.962717 < uniformMap, uniformMap <= 0.985973))
    resToAirport = pcrand(self.category == 1, pcrand(0.985973 < uniformMap, uniformMap <= 0.986342))
    resToRoad = pcrand(self.category == 1, pcrand(0.986342 < uniformMap, uniformMap <= 0.994463))
    resToRailway = pcrand(self.category == 1, pcrand(0.994463 < uniformMap, uniformMap <= 0.994832))
    resToSemiurban = pcrand(self.category ==1, 0.994832 < uniformMap)

    #recreationswitch
    recToRes = pcrand(self.category == 2, uniformMap <= 0.058880)
    recToRec = pcrand(self.category == 2, pcrand(0.058880 < uniformMap, uniformMap <= 0.863899))
    recToAgri = pcrand(self.category == 2, pcrand(0.863899 < uniformMap, uniformMap <= 0.889961))
    recToNature = pcrand(self.category == 2, pcrand(0.889961 < uniformMap, uniformMap <= 0.932432))
    recToWater = pcrand(self.category == 2, pcrand(0.932432 < uniformMap, uniformMap <= 0.94498))
    recToIndustrial = pcrand(self.category == 2, pcrand(0.94498 < uniformMap, uniformMap <= 0.957528))
    recToRoad = pcrand(self.category == 2, pcrand(0.957528 < uniformMap, uniformMap <= 0.974903))
    recToRailway = pcrand(self.category == 2, pcrand(0.974903 < uniformMap, uniformMap <= 0.975868))
    recToSemiurban = pcrand(self.category == 2, 0.975868 < uniformMap)

    #greenhouseswitch
    greenToRes = pcrand(self.category == 3, uniformMap <= 0.063232)
    greenToRec = pcrand(self.category == 3, pcrand(0.063232 < uniformMap, uniformMap <= 0.070258))
    greenToGreen = pcrand(self.category == 3, pcrand(0.070258 < uniformMap, uniformMap <= 0.723654))
    greenToAgri = pcrand(self.category == 3, pcrand(0.723654 < uniformMap, uniformMap <= 0.922717))
    greenToWater = pcrand(self.category == 3, pcrand(0.922717 < uniformMap, uniformMap <= 0.925059))
    greenToIndustrial = pcrand(self.category == 3, pcrand(0.925059 < uniformMap, uniformMap <= 0.960188))
    greenToRoad = pcrand(self.category == 3, pcrand(0.960188 < uniformMap, uniformMap <= 0.969556))
    greenToSemiurban = pcrand(self.category == 3, 0.969556 < uniformMap)

    #agriswitch
    agriToRes = pcrand(self.category == 4, uniformMap <= 0.019636)
    agriToRec = pcrand(self.category == 4, pcrand(0.019636 < uniformMap, uniformMap <= 0.034805))
    agriToGreen = pcrand(self.category == 4, pcrand(0.034805 < uniformMap, uniformMap <= 0.040831))
    agriToAgri = pcrand(self.category == 4, pcrand(0.040831 < uniformMap, uniformMap <= 0.944))
    agriToNature = pcrand(self.category == 4, pcrand(0.944 < uniformMap, uniformMap <= 0.959273))
    agriToWater = pcrand(self.category == 4, pcrand(0.959273 < uniformMap, uniformMap <= 0.969247))
    agriToIndustrial = pcrand(self.category == 4, pcrand(0.969247 < uniformMap, uniformMap <= 0.978702))
    agriToAirport = pcrand(self.category == 4, pcrand(0.978702 < uniformMap, uniformMap < 0.979014))
    agriToRoad = pcrand(self.category == 4, pcrand(0.979014 < uniformMap, uniformMap <= 0.985352))
    agriToRailway = pcrand(self.category == 4, pcrand(0.985352 < uniformMap, uniformMap < 0.986079))
    agriToSemiurban = pcrand(self.category == 4, 0.986079 < uniformMap)

    #natureswitch
    natToRes = pcrand(self.category == 5, uniformMap <= 0.015739)
    natToRec = pcrand(self.category == 5, pcrand(0.015739 < uniformMap, uniformMap <= 0.037661))
    natToAgri = pcrand(self.category == 5, pcrand(0.037661 < uniformMap, uniformMap <= 0.086565))
    natToNature = pcrand(self.category == 5, pcrand(0.086565 < uniformMap, uniformMap <= 0.960089))
    natToWater = pcrand(self.category == 5, pcrand(0.960089 < uniformMap, uniformMap <= 0.973018))
    natToIndustrial = pcrand(self.category == 5, pcrand(0.973018 < uniformMap, uniformMap <= 0.980888))
    natToRoad = pcrand(self.category == 5, pcrand(0.980888 < uniformMap, uniformMap <= 0.98932))
    natToRailway = pcrand(self.category == 5, pcrand(0.98932 < uniformMap, uniformMap < 0.990444))
    natToSemiurban = pcrand(self.category == 5, 0.990444 < uniformMap)

    #waterswitch
    watToRes = pcrand(self.category == 6, uniformMap <= 0.001357)
    watToRec = pcrand(self.category == 6, pcrand(0.001357 < uniformMap, uniformMap <= 0.002714))
    watToAgri = pcrand(self.category == 6, pcrand(0.002714 < uniformMap, uniformMap <= 0.005598))
    watToNature = pcrand(self.category == 6, pcrand(0.005598 < uniformMap, uniformMap <= 0.011026))
    watToWater = pcrand(self.category == 6, pcrand(0.011026 < uniformMap, uniformMap <= 0.991179))
    watToIndustrial = pcrand(self.category == 6, pcrand(0.991179 < uniformMap, uniformMap <= 0.994063))
    watToRoad = pcrand(self.category == 6, pcrand(0.994063 < uniformMap,uniformMap <= 0.994911))
    watToRailway = pcrand(self.category == 6, pcrand(0.994911 < uniformMap, uniformMap < 0.995081))
    watToSemiurban = pcrand(self.category == 6, 0.995081 < uniformMap)

    #industrialswitch
    indToRes = pcrand(self.category == 7, uniformMap <= 0.057692)
    indToRec = pcrand(self.category == 7, pcrand(0.057692 < uniformMap, uniformMap <= 0.065384))
    indToAgri = pcrand(self.category == 7, pcrand(0.065384 < uniformMap, uniformMap <= 0.071794))
    indToNature = pcrand(self.category == 7, pcrand(0.071794 < uniformMap, uniformMap <= 0.073076))
    indToWater = pcrand(self.category == 7, pcrand(0.073076 < uniformMap, uniformMap <= 0.079486))
    indToIndustrial = pcrand(self.category == 7, pcrand(0.079486 < uniformMap, uniformMap <= 0.961537))
    indToAirport = pcrand(self.category == 7, pcrand(0.961537 < uniformMap, uniformMap <= 0.964101))
    indToRoad = pcrand(self.category == 7, pcrand(0.964101 < uniformMap, uniformMap <= 0.971793))
    indToRailway = pcrand(self.category == 7, pcrand(0.971793 < uniformMap, uniformMap < 0.975639))
    indToSemiurban = pcrand(self.category == 7, 0.975639 < uniformMap)

    #airportswitch
    airToAgri = pcrand(self.category == 8, uniformMap <= 0.088235)
    airToNature = pcrand(self.category == 8, pcrand(0.088235 < uniformMap, uniformMap <= 0.147059))
    airToIndustrial = pcrand(self.category == 8, pcrand(0.147059 < uniformMap, uniformMap <= 0.205883))
    airToAirport = pcrand(self.category == 8, pcrand(0.205883 < uniformMap, uniformMap <= 0.911765))
    airToSemiurban = pcrand(self.category == 8, 0.911765 < uniformMap)
                  
    #roadswitch
    roadToRes = pcrand(self.category == 9, uniformMap <= 0.038748)
    roadToRec = pcrand(self.category == 9, pcrand(0.038748 < uniformMap, uniformMap <= 0.053651))
    roadToAgri = pcrand(self.category == 9, pcrand(0.053651 < uniformMap, uniformMap <= 0.110283))
    roadToNature = pcrand(self.category == 9, pcrand(0.110283 < uniformMap, uniformMap <= 0.119225))
    roadToWater = pcrand(self.category == 9, pcrand(0.119225 < uniformMap, uniformMap <= 0.123696))
    roadToIndustrial = pcrand(self.category == 9, pcrand(0.123696 < uniformMap, uniformMap <= 0.128167))
    roadToAirport = pcrand(self.category == 9, pcrand(0.128167 < uniformMap, uniformMap <= 0.129657))
    roadToRoad = pcrand(self.category == 9, pcrand(0.129657 < uniformMap, uniformMap <= 0.979135))
    roadToRailway = pcrand(self.category == 9, pcrand(0.979135 < uniformMap, uniformMap < 0.982116))
    roadToSemiurban = pcrand(self.category == 9, 0.982116 < uniformMap)

    #railwayswitch
    railToRes = pcrand(self.category == 10, uniformMap <= 0.026316)
    railToRec = pcrand(self.category == 10, pcrand(0.026316 < uniformMap, uniformMap <= 0.070176))
    railToAgri = pcrand(self.category == 10, pcrand(0.070176 < uniformMap, uniformMap <= 0.13158))
    railToWater = pcrand(self.category == 10, pcrand(0.13158 < uniformMap, uniformMap <= 0.140352))
    railToIndustrial = pcrand(self.category == 10, pcrand(0.140352 < uniformMap, uniformMap <= 0.201756))
    railToRoad = pcrand(self.category == 10, pcrand(0.201756 < uniformMap, uniformMap <= 0.0254388))
    railToRailway = pcrand(self.category == 10, 0.0254388 < uniformMap)

    #semiurbanswitch
    semiToRes = pcrand(self.category == 11, uniformMap <= 0.217469)
    semiToRec = pcrand(self.category == 11, pcrand(0.217469 < uniformMap, uniformMap <= 0.349376))
    semiToGreen = pcrand(self.category == 11, pcrand(0.349376 < uniformMap, uniformMap <= 0.356506))
    semiToAgri = pcrand(self.category == 11, pcrand(0.356506 < uniformMap, uniformMap <= 0.438502))
    semiToNature = pcrand(self.category == 11, pcrand(0.438502 < uniformMap, uniformMap <= 0.474153))
    semiToWater = pcrand(self.category == 11, pcrand(0.474153 < uniformMap, uniformMap <= 0.529411))
    semiToIndustrial = pcrand(self.category == 11, pcrand(0.529411 < uniformMap, uniformMap <= 0.727272))
    semiToAirport = pcrand(self.category == 11, pcrand(0.727272 < uniformMap, uniformMap < 0.730837))
    semiToRoad = pcrand(self.category == 11, pcrand(0.730837 < uniformMap, uniformMap <= 0.778965))
    semiToRailway = pcrand(self.category == 11, pcrand(0.778965 < uniformMap, uniformMap < 0.78966))
    semiToSemiurban = pcrand(self.category == 11, 0.78966 < uniformMap)

      
    newRes = pcror(resToRes, pcror(recToRes, pcror(greenToRes, pcror(agriToRes,\
                    pcror(natToRes, pcror(watToRes, pcror(indToRes, pcror(\
                      roadToRes, pcror(railToRes, semiToRes)))))))))
    self.report(newRes, "newres")

    newRec = pcror(resToRec, pcror(recToRec, pcror(greenToRec, pcror(agriToRec,\
                    pcror(natToRec, pcror(watToRec, pcror(indToRec, pcror(\
                      roadToRec, pcror(railToRec, semiToRec)))))))))

    newGreen = pcror(greenToGreen, pcror(agriToGreen, semiToGreen))

    newAgri = pcror(resToAgri, pcror(recToAgri, pcror(greenToAgri, pcror(agriToAgri,\
                    pcror(natToAgri, pcror(watToAgri, pcror(indToAgri, pcror(\
                      airToAgri, pcror(roadToAgri, pcror(railToAgri,\
                        semiToAgri))))))))))

    newNature = pcror(resToNature, pcror(recToNature, pcror(agriToNature,\
                  pcror(natToNature, pcror(watToNature, pcror(indToNature,\
                   pcror(roadToNature, pcror(airToNature, semiToNature))))))))

    newWater = pcror(resToWater, pcror(recToWater, pcror(greenToWater,\
                pcror(agriToWater, pcror(natToWater, pcror(watToWater,\
                 pcror(indToWater, pcror(roadToWater, pcror(railToWater, semiToWater)))))))))
    
    newIndustrial = pcror(resToIndustrial, pcror(recToIndustrial,\
                    pcror(greenToIndustrial, pcror(agriToIndustrial,\
                    pcror(natToIndustrial, pcror(watToIndustrial,\
                    pcror(indToIndustrial, pcror(airToIndustrial, pcror(\
                    roadToIndustrial, pcror(railToIndustrial, semiToIndustrial))))))))))
    
    newAirport = pcror(resToAirport, pcror(agriToAirport, pcror(indToAirport,\
                  pcror(airToAirport, pcror(roadToAirport, semiToAirport)))))
    
    newRoad = pcror(resToRoad, pcror(recToRoad, pcror(greenToRoad, pcror(agriToRoad,\
                    pcror(natToRoad, pcror(watToRoad, pcror(indToRoad, pcror(\
                      roadToRoad, pcror(railToRoad, semiToRoad)))))))))
    
    newRailway = pcror(resToRailway, pcror(recToRailway, pcror(agriToRailway,\
                    pcror(natToRailway, pcror(watToRailway, pcror(indToRailway,\
                     pcror(roadToRailway, pcror(railToRailway, semiToRailway))))))))
    
    newSemi = pcror(resToSemiurban, pcror(recToSemiurban, pcror(greenToSemiurban,\
                   pcror(agriToSemiurban, pcror(natToSemiurban, pcror(watToSemiurban,\
                    pcror(indToSemiurban, pcror(airToSemiurban,\
                     pcror(roadToSemiurban, semiToSemiurban)))))))))

    closeResidentialEnrich = MyFirstModel.enrichment(self.category, 1, 3, self.total)
    closeRecreationEnrich = MyFirstModel.enrichment(self.category, 2, 3, self.total)
    closeGreenhouseEnrich = MyFirstModel.enrichment(self.category, 3, 3, self.total)
    closeAgriEnrich = MyFirstModel.enrichment(self.category, 4, 3, self.total)
    closeNatureEnrich = MyFirstModel.enrichment(self.category, 5, 3, self.total)
    closeWaterEnrich = MyFirstModel.enrichment(self.category, 6, 3, self.total)
    closeIndustrialEnrich = MyFirstModel.enrichment(self.category, 7, 3, self.total)
    closeAirportEnrich = MyFirstModel.enrichment(self.category, 8, 3, self.total)
    closeRoadEnrich = MyFirstModel.enrichment(self.category, 9, 3, self.total)
    closeTrainEnrich = MyFirstModel.enrichment(self.category, 10, 3, self.total)
    closeSemiUrbanEnrich = MyFirstModel.enrichment(self.category, 11, 3, self.total)

    self.report(closeResidentialEnrich, "cre")
    
    self.category = ifthenelse(pcrand(newRes, closeResidentialEnrich > 1), 1, self.category)
    self.category = ifthenelse(pcrand(newRec, closeRecreationEnrich > 1), 2, self.category)
    self.category = ifthenelse(pcrand(newGreen, closeGreenhouseEnrich > 1), 3, self.category)
    self.category = ifthenelse(pcrand(newAgri, closeAgriEnrich > 1), 4, self.category)
    self.category = ifthenelse(pcrand(newNature, closeNatureEnrich > 1), 5, self.category)
    self.category = ifthenelse(pcrand(newWater, closeWaterEnrich > 1), 6, self.category)
    self.category = ifthenelse(pcrand(newIndustrial, closeIndustrialEnrich > 1), 7, self.category)
    self.category = ifthenelse(pcrand(newAirport, closeAirportEnrich > 1), 8, self.category)
    self.category = ifthenelse(pcrand(newRoad, closeRoadEnrich > 1), 9, self.category)
    self.category = ifthenelse(pcrand(newRailway, closeTrainEnrich > 1), 10, self.category)
    self.category = ifthenelse(pcrand(newSemi, closeSemiUrbanEnrich > 1), 11, self.category)

    self.report(self.category, "category")
    

nrOfTimeSteps=40
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

  




