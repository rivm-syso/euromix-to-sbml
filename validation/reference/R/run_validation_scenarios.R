# This R script is used as a standalone program to test the PBK dll
rm(list=ls()) 

library(deSolve)

# Filename of the model
dllName <- "PBPK_generic_model_v6"
dllPath <- paste("validation/reference/R/", dllName, sep="")
resultsPath <- "validation/reference/R/outputs"

if (!dir.exists(file.path(resultsPath))) {
  dir.create(file.path(resultsPath))
}

###############################################
# Helper functions
###############################################

loadParametrisation <- function(
  filename,
  idModelInstance
) {
  # Set parameters
  parameterIndexes <- read.csv("validation/reference/R/parameters_6.csv", header = TRUE,sep=",")$parameters

  # Get parameter values from file
  data <- read.csv(filename, header = TRUE,sep=",")
  data <- data[data$idModelInstance == idModelInstance,]

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

  return(params)
}

###############################################
# Set dosing
###############################################

createTimesAndDoses <- function(
  days,
  resolution = 1,
  oral = 0,
  dermal = 0,
  inhalation = 0,
  interval = 24
) {

  # set number of oral, dermal and inhalation doses
  doseOral <- oral
  doseDermal <- dermal
  doseInhalation <- inhalation

  eventTimings <- seq(from=0, to=days*24, by=interval)

  oralEvent <- c(1,2)
  oralDosing <- rep(oral,length(eventTimings))

  dermalEvent <- c(1,2)
  dermalDosing <- rep(dermal,length(eventTimings))

  inhalationEvent <- c(1)
  inhalationDosing <- rep(inhalation,length(eventTimings))

  # collect times and forcings
  list(
    times = seq(from=0, to=days*24, by=resolution),
    allDoses = list(
      cbind(eventTimings, oralDosing),
      cbind(eventTimings, dermalDosing),
      cbind(eventTimings, inhalationDosing)
    ),
    eventTimings = eventTimings
  )
}

###############################################
# Load model
###############################################

# Unload dll when loaded
tryCatch({
  dyn.unload(paste(dllName, .Platform$dynlib.ext, sep=""))
}, error = function(err) {}, error = function(err) {}, finally = {})

# Compile dll, note dll is only compiled when changed
system(paste('R CMD SHLIB "', dllPath, '.c"', sep=""))
dyn.load(paste(dllPath, .Platform$dynlib.ext, sep=""))

###############################################
# Run for MM
###############################################

# Set resolution and times
scenario <- createTimesAndDoses(
  days = 3,
  resolution = 1/20
)
times <- scenario$times
allDoses <- scenario$allDoses
eventTimings <- scenario$eventTimings

params <- loadParametrisation("validation/reference/R/parametrisations.csv", "ValClothianidinMM")
params['Michaelis'] <- 1
params['Km'] <- 1
params <- .C("getParms", as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out

# Output names
outputNames <- c("CTotal","CVen","CArt","CFat","CPoor","CRich","CLiver","CSkin_u","CSkin_e","CSkin_sc_u","CSkin_sc_e")

y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname=dllName, 
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventTimings),
              nout=length(outputNames), outnames=outputNames)

write.csv(outnew, paste(resultsPath, "/results_MM.csv", sep=""))

###############################################
# Run for MA
###############################################

# Set resolution and times
scenario <- createTimesAndDoses(
  days = 3,
  resolution = 1/20
)
times <- scenario$times
allDoses <- scenario$allDoses
eventTimings <- scenario$eventTimings

params <- loadParametrisation("validation/reference/R/parametrisations.csv", "ValClothianidinMA")
params <- .C("getParms", as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out
y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname = dllName,
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventTimings),
              nout=length(outputNames), outnames=outputNames)

write.csv(outnew, paste(resultsPath, "/results_MA.csv", sep=""))

###############################################
# Oral (imazalil)
###############################################

# Set resolution and times
scenario <- createTimesAndDoses(
  days = 150,
  resolution = 1,
  oral = 100
)
times <- scenario$times
allDoses <- scenario$allDoses
eventTimings <- scenario$eventTimings

params <- loadParametrisation("validation/reference/R/parametrisations.csv", "ValImazalil")
params <- .C("getParms", as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out
y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname = dllName,
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventTimings),
              nout=length(outputNames), outnames=outputNames)

write.csv(outnew, paste(resultsPath, "/results_oral.csv", sep=""))

###############################################
# Dermal (imzazlil)
###############################################

# Set resolution and times
scenario <- createTimesAndDoses(
  days = 100,
  resolution = 1,
  dermal = 100
)
times <- scenario$times
allDoses <- scenario$allDoses
eventTimings <- scenario$eventTimings

params <- loadParametrisation("validation/reference/R/parametrisations.csv", "ValImazalil")
params <- .C("getParms", as.double(params), out= double(length(params)), as.integer(length(params)), PACKAGE = dllName)$out
y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
outnew <- ode(y=y, times=times, func="derivs", parms=params, dllname = dllName,
              initfunc="initmod", initforc="initforc", forcings=allDoses, events=list(func="event", time=eventTimings),
              nout=length(outputNames), outnames=outputNames)

write.csv(outnew, paste(resultsPath, "/results_dermal.csv", sep=""))

# Unload dll
dyn.unload(paste(dllPath, .Platform$dynlib.ext, sep=""))

