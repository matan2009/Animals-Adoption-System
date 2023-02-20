from common.database_helper import DatabaseHelper
from configurations.animals_adoption_system_configurations import AnimalsAdoptionSystemConfiguration
from configurations.animals_system_helper_configurations import AnimalsSystemHelperConfigurations


class AnimalsSystemHelper(AnimalsAdoptionSystemConfiguration):

    def __init__(self):
        super().__init__()
        helper_config = self.config["animals_system_helper"]
        self.configurations = AnimalsSystemHelperConfigurations(helper_config["table_name"])
        create_animals_table_query = """CREATE TABLE animals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            weight INT NOT NULL,
            owner_name VARCHAR(255) NOT NULL,
            owner_phone_number VARCHAR(255) NOT NULL)"""
        self.database_helper = DatabaseHelper(self.configurations, create_animals_table_query)

    def add_animal(self, animal_details):
        self.database_helper.insert_to_db(animal_details)
