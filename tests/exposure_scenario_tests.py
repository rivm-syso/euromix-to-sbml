import unittest
import os
from pathlib import Path
import roadrunner as rr
import libsbml as ls
import pandas as pd
from parameterized import parameterized
from helpers import plot_simulation_results, load_parametrisation

__test_outputs_path__ = './tests/__testoutputs__'
__model_code__ = 'euromix'
__sbml_file_path__ = os.path.join(f'model/{__model_code__}.sbml')
__default_params_file_path__ = os.path.join(f'./parametrisations/{__model_code__}_default_params.csv')

class ExposureScenarioTests(unittest.TestCase):

    def setUp(self):
        Path(__test_outputs_path__).mkdir(parents=True, exist_ok=True)

    def test_single_oral_bolus(self):
        # Load the PBPK model from the SBML file
        rr_model = rr.RoadRunner(__sbml_file_path__)
        scenario_id = 'single_bolus_scenario_1'
        input_species = 'QGut'
        intake = 1 # 1 unit bolus dose
        num_days = 2
        evaluation_frequency = 24 # evals per unit of time

        # Set initial amount set constant and boundary for Gut
        rr_model.setInitAmount(input_species, intake)
        rr_model.setConstant(input_species, False)
        rr_model.setBoundary(input_species, False)

        # Run simulation
        results = rr_model.simulate(
            start=0,
            end=num_days * 24,
            points=num_days * evaluation_frequency + 1
        )
        df = pd.DataFrame(results, columns=results.colnames)

        # Save to CSV file
        csv_filename = os.path.join(__test_outputs_path__, f'{scenario_id}.csv')
        df.to_csv(csv_filename, index=False)
        fig = plot_simulation_results(results, rr_model.timeCourseSelections)
        png_filename = os.path.join(__test_outputs_path__, f'{scenario_id}.png')
        fig.savefig(png_filename)

    @parameterized.expand([
        (1, 10),
        (2, 100),
        (3, 1000)
    ])
    def test_daily_oral_bolus(self, id_scenario, days_of_exposure):
        # Exposure scenario
        scenario_id = f'test_daily_oral_bolus_{id_scenario}'
        input_id = 'QGut'
        daily_intake = 1 # 1 unit dose per day
        days_after_exposure = int(days_of_exposure / 10)
        num_days = days_of_exposure + days_after_exposure
        evaluation_frequency = 24 # evals per day

        # Load the PBPK model from the SBML file
        rr_model = rr.RoadRunner(__sbml_file_path__)

        # Make sure QGut is not constant and does not have boundary conditions
        rr_model.setInitAmount(input_id, 0)
        rr_model.setConstant(input_id, False)
        rr_model.setBoundary(input_id, False)

        # Set chemical parameters
        load_parametrisation(rr_model, __default_params_file_path__, __model_code__)

        # Create a repeating daily oral dosing
        eid = "oral_daily_exposure"
        rr_model.addEvent(eid, False, f"time % 24 == 0 && time < {days_of_exposure*24}", False)
        rr_model.addEventAssignment(eid, input_id, f"{input_id} + {daily_intake} * BM", False)
        rr_model.regenerateModel(True, True)

        # Simulate the PBPK model
        plot_params = rr_model.timeCourseSelections + ['BM']
        results = rr_model.simulate(
            start = 0,
            end = num_days * 24,
            points = evaluation_frequency * num_days + 1,
            selections = plot_params
        )

        # Save to CSV file
        csv_filename = os.path.join(__test_outputs_path__, f'{scenario_id}.csv')
        df = pd.DataFrame(results, columns=results.colnames)
        df.to_csv(csv_filename, index=False)
        fig = plot_simulation_results(results, rr_model.timeCourseSelections)
        png_filename = os.path.join(__test_outputs_path__, f'{scenario_id}.png')
        fig.savefig(png_filename)

    @parameterized.expand([
        ('./parametrisations/euromix_default_params.csv'),
        ('./parametrisations/parametrisations_euromix.csv'),
    ])
    def test_parametrisation(self, filename):

        # Get parameters of the model
        document = ls.readSBML(__sbml_file_path__)
        model = document.getModel()
        model_params = []
        for i in range(0,model.getNumParameters()):
            param = model.getParameter(i)
            if param.isSetConstant():
                model_params.append(param.getId())

        # Iterate over model instances
        df = pd.read_csv(filename)
        instance_ids = df['idModelInstance'].unique()
        for instance_id in instance_ids:
            df = df.loc[df['idModelInstance'] == instance_id]
            # Check for each instance parameter whether it is defined in the model
            for index, row in df.iterrows():
                self.assertIn(
                    row['Parameter'],
                    model_params,
                    f"Parameter {row['Parameter']} of instance {row['idModelInstance']} is not an assignable parameter of the model."
                )

if __name__ == '__main__':
    unittest.main()
