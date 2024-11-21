import numpy as np
import pandas as pd
import scipy.optimize as opt
from typing import List, Tuple, Dict

from const_ import all_1g_kcal


class ResOutMixin:

    def res_out(self, diet_key: str) -> Dict[str, pd.DataFrame]:
        optimal_nutrition = self.table
        val = (100 * self.nutrition_amount_opt).round(1)
        optimal_nutrition.insert(
            len(optimal_nutrition.columns), column='opt_amount', value=val)
        self.diets[diet_key] = optimal_nutrition
        return self.diets

    def print(self, vect: np.array) -> None:
        out = pd.DataFrame(
            vect, index=['energy, kcal', 'protein, g', 'fat, g', 'carbo, g'], columns=[''])
        return out


class PriceOptimizer(ResOutMixin):

    def __init__(self):
        self.diets = {}

    def define_constraints(self, energy: int, nutrient_ratios: List[float]) -> None:
        """
        nutrient params constraints
        """
        energy_daily = np.array([energy]).reshape(1, 1)
        nutrient_energetic_ratios = np.array(
            nutrient_ratios).reshape(-1, 1)  # nutrient energetic fractions
        nutrient_mass = energy_daily * nutrient_energetic_ratios / all_1g_kcal
        self.beq = np.vstack([energy_daily, nutrient_mass]).round(1)

    def optimize_price(self, data: pd.DataFrame, bounds: Tuple[float, float]) -> None:
        self.table = data[['name']]
        self.price = data.price.values.reshape(-1, 1)  # in rub
        self.Aeq = data.iloc[:, 1:5].T.values
        self.res = opt.linprog(self.price, A_eq=self.Aeq,
                               b_eq=self.beq, method='simplex', bounds=bounds)
        self.nutrition_amount_opt = self.res.x.reshape(-1, 1)
