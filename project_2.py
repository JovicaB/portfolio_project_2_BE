import datetime
import random

from data.database import DatabaseManager
from data.data import COLLATERAL_DATA, COLLATERAL_WEIGHTS


class Collateral:
    """
    A class that manages collateral data for each collateral category.

    Attributes:
    - collateral_data (dict): A dictionary containing collateral data for different categories.
    - collateral_weights (list): A list of weights associated with each collateral category.

    Methods:
    - collateral_weighted_average(collateral_category: str) -> float:
      Calculates the weighted average of collateral values for a specific collateral category.

      Parameters:
      - collateral_category (str): The category of collateral data to calculate the weighted average for.

      Returns:
      float: The weighted average of collateral values for the specified category.

    Usage:
    ```
    collateral_manager = Collateral()
    cwa = collateral_manager.collateral_weighted_average('A')
    print(cwa)
    ```
    """
    def __init__(self) -> None:
        self.collateral_data = COLLATERAL_DATA
        self.collateral_weights = COLLATERAL_WEIGHTS

    def collateral_weighted_average(self, collateral_category: str):
        """
        Calculates the weighted average of collateral values for a specific collateral category.

        Parameters:
        - collateral_category (str): The category of collateral data to calculate the weighted average for.

        Returns:
        float: The weighted average of collateral values for the specified category.
        """
        collateral_data_category = self.collateral_data[collateral_category]
        cwa = round(sum(x * y for x, y in zip(collateral_data_category, self.collateral_weights)), 2)
        return cwa


