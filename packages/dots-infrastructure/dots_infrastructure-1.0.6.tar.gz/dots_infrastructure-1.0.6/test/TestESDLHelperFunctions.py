import unittest
import esdl

from dots_infrastructure.EsdlHelperFunctions import EsdlHelperFunctions
from esdl.esdl_handler import EnergySystemHandler

class TestLogicAddingCalculations(unittest.TestCase):

    def setUp(self):
        energy_system_handler = EnergySystemHandler()
        self.energy_system = energy_system_handler.load_file("test.esdl")

    def test_find_all_esdl_objects_of_type(self):
        # Arrange
        esdl_type = esdl.PVInstallation

        # Execute
        all_pv_installations = EsdlHelperFunctions.get_all_esdl_objects_from_type(self.energy_system.eAllContents(), esdl_type)

        # Assert
        self.assertEqual(len(all_pv_installations), 2)

    def test_find_object_by_id(self):
        # Arrange
        market_id = "b612fc89-a752-4a30-84bb-81ebffc56b50"

        # Execute
        market = EsdlHelperFunctions.get_esdl_object_with_id(self.energy_system.eAllContents(), market_id)

        # Assert
        self.assertEqual(market.id, market_id)
        self.assertIsInstance(market, esdl.EnergyMarket)

if __name__ == '__main__':
    unittest.main()