
import numpy as np
import pandas as pd
import streamlit as st

from optimizer import PriceOptimizer


def main():

    data_full = load_local_data()

    with st.sidebar:
        energy_daily = st.slider(
            "Daily energy, kcal", min_value=1000, max_value=4000, value=2500)

        protein_daily = st.slider(
            "Daily protein, %", min_value=10, max_value=90, value=15)

        fat_daily = st.slider(
            "Daily fat, %", min_value=10, max_value=90, value=30)

        carbo_daily = 100 - protein_daily - fat_daily

        st.write(f'Protein: {protein_daily} %')
        st.write(f'Fat: {fat_daily} %')
        st.write(f'Carbo: {carbo_daily} %')

        # [protein, fat, carbo]
        nutrient_energetic_ratios = [
            0.01*protein_daily, 0.01*fat_daily, 0.01*carbo_daily]

        button1_pressed = st.button('Restore')

    with st.empty():
        names_selected = st.multiselect('Select nutrition', key=1, options=data_full.name,
                                        default=data_full.name)
        if button1_pressed:
            names_selected = st.multiselect('Select nutrition', key=2, options=data_full.name,
                                            default=data_full.name)

    data_selected = data_full.query('name in @names_selected')

    upper_bound = st.slider(
        "Bounds, g", min_value=0, max_value=400, value=200)

    col1, col2, col3 = st.columns(3, gap='small')

    # col1.dataframe(data_selected)

    opter = PriceOptimizer()

    opter.define_constraints(energy_daily, nutrient_energetic_ratios)

    col1.markdown('**Constraints**')
    col1.dataframe(opter.print(opter.beq))

    opter.optimize_price(data_selected, (0, upper_bound/100))

    col2.markdown('**Result**')
    col2.dataframe(opter.print(
        (opter.Aeq@opter.nutrition_amount_opt).round(1)))

    col2.write(
        f'Daily cost: {round((opter.price.T@opter.nutrition_amount_opt).item(), 2)} rub')

    col3.markdown('**Diet**')
    col3.dataframe(opter.res_out('a')['a'])


@ st.cache
def load_local_data() -> pd.DataFrame:
    df = pd.read_csv(r'nutrition_eng.csv')
    return df


if __name__ == "__main__":
    main()
