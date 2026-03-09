# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customise  Your Smoothie!")
st.write(
  """Choose the fruits you want in your custom smoothie"""
)

#import streamlit as st

name_on_order = st.text_input("Name on smoothie")
st.write("Name on your smoothie will be : ", name_on_order)

#import streamlit as st

# option = st.selectbox(
#     'What is favorate fruit?',
#     ('Banana', 'Strawberriers', 'Peaches')
#)

#st.write('Your Favorite fruit selected:', option)

from snowflake.snowpark.functions import col

cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list =st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response.json())
