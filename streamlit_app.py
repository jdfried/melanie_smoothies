# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you would like in your smoothie!
    """
)

name_on_order= st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)


# session = get_active_session()
cnx = st.connection("snowflake")
session= cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe,
                                 max_selections= 5)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+ ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width = True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert= st.button('Submit Order')
    
#    if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        message = """ Your Smoothie is ordered, """ + name_on_order + """! """
        st.success(message, icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/all")
sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width = True)
