# Validation

Find below a description of the validation scenarios.

## MA
- Initial gut amount scenario (48 hours).
- Model parametrisation for mass action kinetics.
- Evaluate concentration in arterial blood and liver.
- Compare against results obtained with R/deSolve.
- Diffs show near-exact agreement (residuals ~1e-7–1e-6).

## MM
- Initial gut amount scenario (48 hours).
- Model parametrisation for Michaelis Menten kinetics.
- Evaluate concentration in arterial blood and liver.
- Compare against results obtained with R/deSolve.
- Diffs show near-exact agreement (residuals ~1e-7–1e-6).

## Oral
- Repeated oral bolus dosing scenario (1 per day, 100 days).
- Use model parametrisation for imazalil.
- Evaluate concentration in arterial blood and liver.
- Compare against results obtained with R/deSolve.
- Diffs show near-exact agreement (residuals ~1e-6–1e-5).

## Dermal
- Repeated dermal bolus dosing scenario (100 days).
- Evaluate concentration in exposed and unexposed viable epidermis of skin, arterial blood, and liver.
- Compare against results obtained with R/deSolve.
- Diffs show near-exact agreement (residuals ~1e-6–1e-5).

## Inhalation
- Repeated continuous inhalation dosing scenario (duration 0.4/day over 10 days).
- Evaluate concentration in air, arterial blood, and liver.
- No comparison against results obtained with R/deSolve.
