import unittest
import nbformat
from parameterized import parameterized
from nbconvert.preprocessors import ExecutePreprocessor

__test_outputs_path__ = './tests/__testoutputs__'

class NotebookTests(unittest.TestCase):

    @parameterized.expand([
        ("notebooks/get_sbml_model_info.ipynb"),
        ("notebooks/run_sbml_model.ipynb"),
        ("notebooks/validate_antimony_model.ipynb")
    ])
    def test_notebooks(self, notebook):
        with open(notebook, encoding="utf8") as f:
            nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            try:
                self.assertIsNotNone(
                    ep.preprocess(nb, {'metadata': {'path':"notebooks"}}),
                    f"Got empty notebook for {notebook}")
            except Exception:
                self.fail(f"Failed executing {notebook}")

if __name__ == '__main__':
    unittest.main()
