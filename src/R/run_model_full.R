R.version
#this r program is used as a standalone program to test the PBPK dll
#setwd("D:/Data/EuroMix/PBPK/QUASAR")
#if you change versions, close R first, environment is not cleaned up with dll's

#normally retrieved from database and XML, see guide
#read values from file
data <- read.csv("EuroMix-KineticModels-Cosmos to be completed_6.csv", header = TRUE,sep=",")
nominal <- read.csv("parameters_6.csv", header = TRUE,sep=",")$parameters

data <- subset(data, idModelInstance == "CosmosClothianidin6")

# set parameters
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

#initialize correlations, normally done within MCRA
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

library(deSolve)
#######################################################################
individuals <- 1
#set number of simulated days
days <- 1
steps <- 24

#set number of oral, dermal and inhalation doses
#bolus 27 mg/kg BW, dose is in mmoles
bolus <- 27
molweight <- 249.678
doseWeight <- unname(bolus * Inputs["BM"])
#doseOral <- doseWeight/molweight
doseOral <- 0
doseDermal <- 0
doseInhalation <- 0
#######################################################################
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

#collect all doses for call to ode
allDoses <- list(cbind(events, oralDosing), cbind(events, dermalDosing), cbind(events, inhalationDosing))
eventLevels <- sort(unique(c(events[oralDosing>0], events[dermalDosing>0],events[inhalationDosing>0])))

dllName <- "PBPK_generic_model_v6"
#Unload dll when loaded
result <- tryCatch({
  dyn.unload(paste(dllName, .Platform$dynlib.ext, sep=""))
}, error = function(err) {}, finally = {})


#Compile dll, note dll is only compiled when changed

system("R CMD SHLIB PBPK_generic_model_v6.c")
dyn.load(paste(dllName, .Platform$dynlib.ext, sep=""))

#collect y for call to ode, normally retrieved from  XML, see guide

Y <- c(0,0,0, 0,0,0, 0,0,0, 0,1,0, 0)
Outputs <- c("CTotal","CVen","CArt","CFat","CPoor","CRich","CLiver","CSkin_u","CSkin_e","CSkin_sc_u","CSkin_sc_e")


#set resolution and times
resolution <- 60
times  <- seq(from=0, to= days*steps*60, by=resolution)/60

write.csv(Inputs, "../../tmp/r_inputs_raw.csv")

#collect inputs for call to ode
Inputs <- .C("getParms",  as.double(Inputs), out= double(length(Inputs)), as.integer(length(Inputs)), PACKAGE = dllName)$out


for (ii in 1:length(nominal)){
  print(paste(ii, ': ', nominal[ii],'=', Inputs[ii]))
}


outnew <- ode(y=Y, times=times, func="derivs", parms=Inputs, dllname = dllName, 
              initfunc = "initmod", initforc = "initforc", forcings = allDoses, events = list(func="event", time=eventLevels), 
              nout = length(Outputs), outnames = Outputs )
#again
names(Inputs) <- nominal
write.csv(Inputs, "../../tmp/r_inputs.csv")

VLiver <- outnew[,"CLiver"] * Inputs["BM"] * Inputs["scVLiver"] * molweight

plot(VLiver, type="l")
mean(VLiver)

write.csv(outnew, "../../tmp/r_out.csv")

