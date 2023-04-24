"""chatGPT.py
This file imports openAI and defines a method for getting reponses for queries
to chatGPT

contains:
    getResponse(prompt)
"""

import openai
openai.api_key = "####################################################3"

# Set up the model and prompt
model_engine = "text-davinci-003"

def getResponse(prompt): #get ChatGPT's response to a prompt 
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
    response = completion.choices[0].text
    return response 
