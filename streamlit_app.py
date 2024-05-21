#orginal which run successfully in browser
import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector
import requests
snowflake_config = st.secrets._file_paths=["/workspaces/melanies_smoothies/secrets.toml"]

st.title(":cup_with_staw: Cup with straw:cup_with_staw:")

st. write(
    "Choose the fruit you want to custome smoothiekjjlkjjk"
)
name_of_order = st.text_input('name_of_smoothee')
st.write('The Name of Smoothie :', name_of_order) 
 
cnx=st.connection('snowflake')
session = cnx.session()
 

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.toPandas()
#st.dataframe(pd_df)
#st.stop()
ingredent_list=st.multiselect('choose 5 ingredent',my_dataframe);
if ingredent_list:
    ingredents_string=''
    for fruit_choosen in ingredent_list:
        ingredents_string+=fruit_choosen+' ';
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen + '  Nutrition Information')
        rewq=requests.get("https://fruityvice.com/api/fruit/" + search_on)
        df=st.dataframe(data=rewq.json(),use_container_width=True)
        st.write(ingredents_string);

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredents_string + """','""" + name_of_order + """' )"""
    
    time_to_insert=st.button("submit order" )
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!  ' + name_of_order ,icon='✅')
       
