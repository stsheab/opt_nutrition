import numpy as np

# nutrient energetic capacity in kcal/g
PROTEIN_1g_kcal = 4.1
FAT_1g_kcal = 9.2
CARBO_1g_kcal = 4.1

all_1g_kcal = np.array([PROTEIN_1g_kcal, FAT_1g_kcal,
                       CARBO_1g_kcal]).reshape(-1, 1)
