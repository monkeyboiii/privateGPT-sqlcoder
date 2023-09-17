from barfi import st_barfi, barfi_schemas, Block
from st_pages import add_page_title
import streamlit as st


add_page_title()


##############################
feed = Block(name='Feed')
feed.add_output()


def feed_func(self):
    self.set_interface(name='Output', value=4)


feed.add_compute(feed_func)

splitter = Block(name='Splitter')
splitter.add_input()
splitter.add_output()
splitter.add_output()


def splitter_func(self):
    in_1 = self.get_interface(name='Input')
    value = (in_1/2)
    self.set_interface(name='Output 1', value=value)
    self.set_interface(name='Output 2', value=value)


splitter.add_compute(splitter_func)

mixer = Block(name='Mixer')
mixer.add_input()
mixer.add_input()
mixer.add_output()


def mixer_func(self):
    in_1 = self.get_interface(name='Input 1')
    in_2 = self.get_interface(name='Input 2')
    value = (in_1 + in_2)
    self.set_interface(name='Output', value=value)


mixer.add_compute(mixer_func)

result = Block(name='Result')
result.add_input()


def result_func(self):
    in_1 = self.get_interface(name='Input')


result.add_compute(result_func)


prompt_template = Block(name="Prompt Template")
prompt_template.add_input("Question")
prompt_template.add_input("Few shot examples")
prompt_template.add_input("History")
prompt_template.add_input("Table info")
prompt_template.add_input("Preest arguments")
prompt_template.add_output("Prompt")


flow = Block(name="flow")
flow.add_input("Input")
flow.add_output("Output")

database = Block(name="database")
database.add_input("Schema Query")
database.add_input("Result Query")
database.add_output("Schema Output")
database.add_output("Result Output")


########################################
load_schema = st.selectbox('Select a saved schema:', barfi_schemas())

compute_engine = st.checkbox('Activate barfi compute engine', value=False)

barfi_result = st_barfi(base_blocks=[feed, result, mixer, splitter, prompt_template, flow, database],
                        compute_engine=compute_engine, load_schema=load_schema)

if barfi_result:
    st.write(barfi_result)
