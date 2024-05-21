# Import python packages
import streamlit as st 
from snowflake.snowpark.functions import col
import snowflake.connector

# Write directly to the app
st.title(":cup_with_straw:  Customise your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want to have in your smoothie.
    """)

name_on_order= st.text_input('Name on Smoothie:')
st.write('The Name on your smoothie is:',name_on_order)

cnx=st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 Ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
    #st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' ,'""" + name_on_order + """')"""
    #st.write(my_insert_stmt)

    time_to_insert= st.button('Submit order')
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!:' , icon="✅")
        
        
