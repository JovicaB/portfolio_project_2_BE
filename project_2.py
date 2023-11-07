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


class ECL:
    """
    A class representing ECL (Expected Credit Loss) credit calculations.

    Attributes:
    - credit_value (float): The initial credit value.
    - credit_life (int): The lifespan of the credit in years.
    - credit_approval_year (int): The year in which the credit was approved.
    - collateral_value (float): The value of the collateral associated with the credit.
    - collateral_category (str): The category of the collateral used for calculations.
    - risk (float): A numerical representation of credit risk.

    Methods:
    - credit_value_adjuster() -> float:
      Adjusts the credit value based on the current year of the credit's lifespan.

    - ead() -> float:
      Calculates the Exposure at Default (EAD) using the adjusted credit value.

    - lgd() -> float:
      Calculates the Loss Given Default (LGD) based on the probable rate of return if collateral needs to be liquidated.

    - pd() -> float:
      Returns the Probability of Default (PD), a numerical representation of credit risk.

    - ecl_calculation() -> int:
      Calculates the Expected Credit Loss (ECL) using the EAD, LGD, and PD values.

    Usage:
    ```
    ecl_calculator = ECL(credit_value, credit_life, credit_approval_year, collateral_value, collateral_category, risk)
    adjusted_credit_value = ecl_calculator.credit_value_adjuster()
    ead_value = ecl_calculator.ead()
    lgd_value = ecl_calculator.lgd()
    pd_value = ecl_calculator.pd()
    ecl = ecl_calculator.ecl_calculation()
    print(f"Adjusted Credit Value: {adjusted_credit_value}")
    print(f"EAD: {ead_value}")
    print(f"LGD: {lgd_value}")
    print(f"PD: {pd_value}")
    print(f"ECL: {ecl}")
    ```
    """

    def __init__(self, credit_value, credit_life, credit_approval_year, collateral_value, collateral_category, risk) -> None:
        self.credit_value = credit_value
        self.credit_life = credit_life
        self.credit_approval_year = credit_approval_year
        self.collateral_value = collateral_value
        self.collateral_category = collateral_category
        self.risk = risk

    def credit_value_adjuster(self):
        '''
        Adjusts the credit value based on the current year of the credit's lifespan.

        Returns:
        float: Adjusted credit value.
        '''
        current_year = datetime.date.today().year
        cva = (self.credit_life + self.credit_approval_year -
               current_year) / self.credit_life
        return cva

    def ead(self):
        '''
        Exposure at default (EAD) calculation. Current adjusted credit value.

        Returns:
        float: EAD value.
        '''
        multiplier = self.credit_value_adjuster()
        ead = self.credit_value * multiplier
        return ead

    def lgd(self):
        '''
        Loss given default (LGD) calculation. The probable rate of return if collateral needs to be liquidated.

        Returns:
        float: LGD value.
        '''
        lgd = self.collateral_value * \
            Collateral().collateral_weighted_average(self.collateral_category)
        return lgd

    def pd(self):
        '''
        Probability of default (PD) calculation. A numerical representation of credit risk.

        Returns:
        float: PD value.
        '''
        pd = self.risk
        return pd

    def ecl_calculation(self):
        '''
        Expected credit loss (ECL) calculation model.

        Returns:
        int: ECL value.
        '''
        ead = self.ead()
        lgd = self.lgd() / ead
        pd = self.pd()

        ecl = round(ead * lgd * pd)
        return ecl
