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


class PortfolioData:
    """
    A class for structuring credit data for Credit portfolio screen [portfolio + statistics] 
    """

    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.credit_data = self.database.read_data('p2_credit_portfolio')

    def credit_life_left_calculation(self, credit_life, credit_approval_year):
        '''
        Calculates the remaining years of credit life.

        Parameters:
        - credit_life (int): The total lifespan of the credit.
        - credit_approval_year (int): The year in which the credit was approved.

        Returns:
        int: The number of years left in the credit life.
        '''
        current_year = datetime.date.today().year
        credit_life_left = credit_approval_year + credit_life - current_year
        return credit_life_left

    def credit_table_data(self):
        '''
        Displays credit data with ECL (Expected Credit Loss) calculation.

        Returns:
        list: A list of lists containing credit data with ECL calculations.
        '''
        ecl_data = []
        idx = 1

        for element in self.credit_data:
            ecl = ECL(element[2], element[4], element[5],
                      element[7], element[8], element[9])
            credit_data = [
                idx,
                element[1],
                round(element[2]),
                round(element[3], 2),
                element[4],
                self.credit_life_left_calculation(element[4], element[5]),
                element[8],
                round(element[7]),
                ecl.ead(),
                ecl.lgd(),
                ecl.pd(),
                ecl.ecl_calculation()

            ]
            ecl_data.append(credit_data)
            idx += 1
        return ecl_data

    def weighted_average_portfolio_risk(self, portolfio_risk, weights):
        '''
        Calculates the weighted average risk of a portfolio.

        Parameters:
        - portfolio_risk (list): A list of credit risks for the portfolio.
        - weights (list): A list of weights for each credit in the portfolio.

        Returns:
        float: The weighted average portfolio risk.
        '''
        wapr = round(sum(x * y for x, y in zip(portolfio_risk, weights)), 2)
        return wapr

    def portfolio_statistics(self):
        '''
        Displays credit portfolio statistics including the number of credits, the gross value of the portfolio, the gross value of collateral, and the weighted average portfolio risk.

        Returns:
        list: A list of portfolio statistics.
        '''
        total_portfolio_credit_value = round(
            sum(credit_data[2] for credit_data in self.credit_data))
        credit_share_of_portfolio = [round(
            credit_value[2] / total_portfolio_credit_value, 2) for credit_value in self.credit_data]
        credit_risks = [credit_data[3] for credit_data in self.credit_data]
        weighted_average_portfolio_risk = self.weighted_average_portfolio_risk(
            credit_risks, credit_share_of_portfolio)

        statistics = [
            len(self.credit_data),
            total_portfolio_credit_value,
            round(sum(credit_data[7] for credit_data in self.credit_data)),
            weighted_average_portfolio_risk
        ]
        return statistics


class RiskCalculation:
    """
    A class for weighted average risk calculation
    """
    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.risk_data = self.database.read_data('p2_risk_weights')
        self.risk_status = self.risk_data[0][1]
        self.weight_status = self.risk_data[0][2]

    def weighted_risk_calculation(self):
        '''
        calculates weighted average credit risk
        '''
        risk = [int(x)/100 for x in self.risk_status.split(':')]
        weight = [int(x)/100 for x in self.weight_status.split(':')]
        weighted_risk = round(sum([x * y for x, y in zip(risk, weight)]), 2)
        return weighted_risk


class WeightsCalibration:
    """
    A class for setting weight relationships with a sum strength of 1. 
    It addresses the challenge of equal distribution of positive and negative values from an HTML input slider by randomizing the weight iterator.
    """
    def __init__(self, input_data) -> None:
        self.database = DatabaseManager('mysql')
        self.input_data = input_data
        self.weight_index = self.input_data[0] - 1
        self.modified_weights_status = [
            int(x) for x in self.input_data[1].split(':')]

    def set_iterator(self):
        """
        Defines a random iterator list without the element that is selected.
        """
        raw_seq = [0, 1, 2, 3, 4]
        raw_seq.remove(self.weight_index)
        random.shuffle(raw_seq)

        return raw_seq

    def weights_calibration(self):
        """
        Calibrates weights based on changes in the chosen ponder value.

        Returns:
        list: Updated weights status after calibration.
        """
        sequence = self.set_iterator()
        value_to_distribute = 100 - sum(self.modified_weights_status)
        while value_to_distribute != 0:
            if value_to_distribute > 0:
                for i in sequence:
                    self.modified_weights_status[i] += 1
                    value_to_distribute -= 1
                    if value_to_distribute == 0:  
                        break
            else:
                for i in reversed(sequence):
                    self.modified_weights_status[i] -= 1
                    value_to_distribute += 1
                    if value_to_distribute == 0: 
                        break
        return self.modified_weights_status


class ModelWeightsStatus:
    """
    A class for managing weights status (reading/saving)
    """
    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.weight_data = self.database.read_data('p2_risk_weights')[0]

    def get_weights_status(self):
        """
        Retrieves the current weights status.

        Returns:
        list: Current weights status.
        """
        return self.weight_data[2]

    def set_weights_status(self, weights_status):
        '''
        Saves the calibration of the risk weights.

        Parameters:
        - weights_status (list): A list representing the updated weights status.

        Returns:
        str: A message indicating that the weights status has been updated.
        '''
        sql_query = "UPDATE p2_risk_weights SET weights = %s WHERE id = %s"
        data = (weights_status, 1)
        self.database.save_data(sql_query, data)
        return 'Weights status updated'
