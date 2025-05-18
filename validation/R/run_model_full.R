# This R script is used as a standalone program to test the PBK dll
rm(list=ls()) 

library(deSolve)

R.version

# Filename of the model
dllName <- "PBPK_generic_model_v6"
dllPath <- paste("validation/R/", dllName, sep="")
resultsPath <- "validation/R/results"
parametrisationsFilename <- "validation/R/EuroMix-KineticModels-Cosmos to be completed_6.csv"
idModelInstance <- "CosmosClothianidin6"

###############################################
# Helper functions
###############################################

loadParametrisation <- function(
  filename,
  idModelInstance
) {
  # Set parameters
  parameterIndexes <- read.csv("validation/R/parameters_6.csv", header = TRUE,sep=",")$parameters

  # Get parameter values from file
  data <- read.csv(filename, header = TRUE,sep=",")
  data <- subset(data, idModelInstance == idModelInstance)

  readParameters = data$Parameter
  params <- rep(c(0),length(parameterIndexes))
  for (ii in 1:length(parameterIndexes)){
    for(jj in 1:length(readParameters)){
      if (toString(parameterIndexes[ii]) == toString(readParameters[jj])){
        params[ii] <- data$Value[jj]
      }
    }
  }

  names(params) <- parameterIndexes

  # Initialize correlations, normally done within MCRA
  params["log_aPoor"] <- log(params["PCPoor"]/params["PCFat"])
  params["log_aRich"] <- log(params["PCRich"]/params["PCFat"])
  params["log_aLiver"] <- log(params["PCLiver"]/params["PCFat"])
  params["log_aSkin"] <- log(params["PCSkin"]/params["PCFat"])
  params["log_aSkin_sc"] <- log(params["PCSkin_sc"]/params["PCFat"])
  params["ResampledPCFat"] <- params["PCFat"]
  params["log_PCFat"] <- log(params["PCFat"])

  for (ii in 1:length(parameterIndexes)){
    print(paste(ii, ': ', parameterIndexes[ii],'=', params[ii]))
  }
  return(params)
}

###############################################
# Set dosing
###############################################

# set number of simulated days
days <- 1
steps <- 24

# set number of oral, dermal and inhalation doses
doseOral <- 0
doseDermal <- 0
doseInhalation <- 0

events <- c(0:(days*steps-1))

oralEvent <- c(1,2)
oralDosing <- rep(0,steps)
oralDosing[oralEvent] <- doseOral
oralDosing <- rep(c(oralDosing),days) 
 
dermalEvent <- c(1,2)
dermalDosing <- rep(0,steps)
dermalDosing[dermalEvent] <- doseDermal
dermalDosing <- rep(c(dermalDosing),days) 

inhalationEvent <- c(1)
inhalationDosing <- rep(0,steps)
inhalationDosing[inhalationEvent] <- doseInhalation
inhalationDosing <- rep(c(inhalationDosing),days) 

# collect all doses for call to ode
allDoses <- list(cbind(events, oralDosing), cbind(events, dermalDosing), cbind(events, inhalationDosing))
eventLevels <- sort(unique(c(events[oralDosing>0], events[dermalDosing>0],events[inhalationDosing>0])))

###############################################
# Load model
###############################################

# Unload dll when loaded
tryCatch({
  dyn.unload(paste(dllName, .Platform$dynlib.ext, sep=""))
}, error = function(err) {}, finally = {})

# Compile dll, note dll is only compiled when changed
system(paste('R CMD SHLIB "', dllPath, '.c"', sep=""))
dyn.load(paste(dllPath, .Platform$dynlib.ext, sep=""))

# Set resolution and times
resolution <- 3
times  <- seq(from=0, to= days*steps*60, by=resolution)/60

###############################################
# Run for MM
###############################################

params <- loadParametrisation(parametrisationsFilename, idModelInstance)
params['Michaelis'] <- 1
params['Km'] <- 1
params <- .C("getParms",  as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out

# Output names
outputNames <- c("CTotal","CVen","CArt","CFat","CPoor","CRich","CLiver","CSkin_u","CSkin_e","CSkin_sc_u","CSkin_sc_e")

y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname=dllName, 
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventLevels), 
              nout=length(outputNames), outnames=outputNames)

write.csv(outnew, paste(resultsPath, "/euromix_r_results_MM.csv", sep=""))

###############################################
# Run for MA
###############################################

params <- loadParametrisation(parametrisationsFilename, idModelInstance)
params['Michaelis'] <- 0
params['Km'] <- 1
params <- .C("getParms",  as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out
y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname = dllName,
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventLevels),
              nout=length(outputNames), outnames=outputNames )

write.csv(outnew, paste(resultsPath, "/euromix_r_results_MA.csv", sep=""))

# Unload dll
dyn.unload(paste(dllPath, .Platform$dynlib.ext, sep=""))
