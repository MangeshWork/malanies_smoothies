# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app.
st.title(f"Customise your smoothie :cup_with_straw:")
st.write(""" Choose the fruits you want in your custom smoothie! """)

# ❄️ The Snowpark COL Function
name_on_order = st.text_input('Name of Smoothie:')
st.write('Your smoothie name is', name_on_order )

cnx = st.connection("snowflake")
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# 🧰 The Streamlit Multi-select Widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    ,my_dataframe 
    ,max_selections = 5
    ) 


# 🔀 Converting a LIST to a STRING
if ingredients_list:   
    
    ingredients_string = ''
    
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ''

    if st.button('Submit Order'):
        session.sql(f""" 
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}','{name_on_order}')""").collect()

        st.success('Your Smoothie is ordered!', icon="✅")
