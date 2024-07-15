# This r script is used as a standalone program to test the PBPK dll
rm(list=ls()) 

library(deSolve)

R.version

# Filename of the model
dllName <- "PBPK_generic_model_v6"
dllPath <- paste("validation/R/", dllName, sep="")
resultsPath <- "validation/R/results"

# Get parameter values from file
data <- read.csv("validation/R/EuroMix-KineticModels-Cosmos to be completed_6.csv", header = TRUE,sep=",")
nominal <- read.csv("validation/R/parameters_6.csv", header = TRUE,sep=",")$parameters
data <- subset(data, idModelInstance == "CosmosClothianidin6")

readInputs <- function() {
  # Set parameters
  readParameters = data$Parameter
  Inputs <- rep(c(0),length(nominal))

  for (ii in 1:length(nominal)){
    for(jj in 1:length(readParameters)){
      if (toString(nominal[ii]) == toString(readParameters[jj])){
        Inputs[ii] <- data$Value[jj]
      }
    }
  }

  names(Inputs) <- nominal

  # Initialize correlations, normally done within MCRA
  Inputs["log_aPoor"] <- log(Inputs["PCPoor"]/Inputs["PCFat"])
  Inputs["log_aRich"] <- log(Inputs["PCRich"]/Inputs["PCFat"])
  Inputs["log_aLiver"] <- log(Inputs["PCLiver"]/Inputs["PCFat"])
  Inputs["log_aSkin"] <- log(Inputs["PCSkin"]/Inputs["PCFat"])
  Inputs["log_aSkin_sc"] <- log(Inputs["PCSkin_sc"]/Inputs["PCFat"])
  Inputs["ResampledPCFat"] <- Inputs["PCFat"]
  Inputs["log_PCFat"] <- log(Inputs["PCFat"])

  for (ii in 1:length(nominal)){
    print(paste(ii, ': ', nominal[ii],'=', Inputs[ii]))
  }
  return(Inputs)
}
Inputs <- readInputs()

#######################################################################

# set number of simulated days
days <- 1
steps <- 24

# set number of oral, dermal and inhalation doses
doseOral <- 0
doseDermal <- 0
doseInhalation <- 0

events <- c(0: (days*steps-1))

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

# Unload dll when loaded
result <- tryCatch({
  dyn.unload(paste(dllName, .Platform$dynlib.ext, sep=""))
}, error = function(err) {}, finally = {})

# Compile dll, note dll is only compiled when changed
system(paste('R CMD SHLIB "', dllPath, '.c"', sep=""))
dyn.load(paste(dllPath, .Platform$dynlib.ext, sep=""))

# Output names
Outputs <- c("CTotal","CVen","CArt","CFat","CPoor","CRich","CLiver","CSkin_u","CSkin_e","CSkin_sc_u","CSkin_sc_e")

# Set resolution and times
resolution <- 3
times  <- seq(from=0, to= days*steps*60, by=resolution)/60

# Run for MM
Inputs <- readInputs()
Inputs$Michaelis <- 1
Inputs$Km <- 1
Inputs <- .C("getParms",  as.double(Inputs), out= double(length(Inputs)), as.integer(length(Inputs)), PACKAGE = dllName)$out
Y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
outnew <- ode(y=Y, times=times, func="derivs", parms=Inputs, dllname = dllName, 
              initfunc = "initmod", initforc = "initforc", forcings = allDoses, events = list(func="event", time=eventLevels), 
              nout = length(Outputs), outnames = Outputs )

write.csv(outnew, paste(resultsPath, "/euromix_r_results_MM.csv", sep=""))

# Run for MA
Inputs <- readInputs()
Inputs$Michaelis <- 0
Inputs$Km <- 1
Inputs <- .C("getParms",  as.double(Inputs), out= double(length(Inputs)), as.integer(length(Inputs)), PACKAGE = dllName)$out
Y <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
outnew <- ode(y=Y, times=times, func="derivs", parms=Inputs, dllname = dllName,
              initfunc = "initmod", initforc = "initforc", forcings = allDoses, events = list(func="event", time=eventLevels),
              nout = length(Outputs), outnames = Outputs )

write.csv(outnew, paste(resultsPath, "/euromix_r_results_MA.csv", sep=""))

# Unload dll
dyn.unload(paste(dllPath, .Platform$dynlib.ext, sep=""))
