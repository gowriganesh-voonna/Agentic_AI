from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
 
# Step 1: Prompt to generate company name
name_prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)
 
# Step 2: Prompt to generate slogan based on name
slogan_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Write a catchy slogan for a company named {company_name}."
)
 
# LLM: Initialize OpenAI GPT model
llm = OpenAI(model_name="text-davinci-003", temperature=0.7)
 
# Step 1 Chain: product → company_name
name_chain = LLMChain(llm=llm, prompt=name_prompt, output_key="company_name")
 
# Step 2 Chain: company_name → slogan
slogan_chain = LLMChain(llm=llm, prompt=slogan_prompt, output_key="slogan")
 
# Combine chains sequentially
overall_chain = SequentialChain(
    chains=[name_chain, slogan_chain],
    input_variables=["product"],
    output_variables=["company_name", "slogan"],
    verbose=True
)
 
# Run the full chain
result = overall_chain.run({"product": "sports shoes"})
print(result)
 