# Setup project for unittest discovery
from phases.commands.test import Test as PhasesTest
from pyPhases.test import TestCase


def _setup_project():
    """Setup the project for testing - called when tests module is imported."""
    if TestCase.project is None:
        phasesTest = PhasesTest({})
        phasesTest.prepareConfig()
        testConfig = phasesTest.loadConfig("tests/config.yml")
        phasesTest.config.update(testConfig)
        project = phasesTest.createProjectFromConfig(phasesTest.config)
        TestCase.project = project


_setup_project()
