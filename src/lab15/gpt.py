'''
Ask ChatGPT a question. Copy the response into a string. Regenerate the response.
(2pts) Split both the text into sentences. Compare the sentences across the two responses 
for similarity using sentence transformers. 
Sentence transformer's sentence similarity will give you a score for similarity between two sentences 
in the range of [0, 1].
(3pts) Come up with a metric to assess overall similarity between the two texts. Best answer is unknown. 
Please describe the metric you came up with comments.
'''

import statistics # Importing the statistics module
from sentence_transformers import SentenceTransformer, util

#Compare individual sentences from separate 2-sentence responses 

#sentences of first response to question
sentences = ["The immune system is a complex network of cells, tissues, and organs that work together to defend the body against harmful pathogens such as viruses, bacteria, and parasites.", "It does this by recognizing and attacking foreign invaders while also maintaining a memory of previous infections to better respond to future threats."]

sentences2 = ["The immune system is a complex network of cells, tissues, and organs that work together to protect the body from harmful pathogens by recognizing and attacking foreign invaders while also maintaining a memory of previous infections to better respond to future threats.", "It does this through a variety of mechanisms including physical barriers, innate immune responses, and adaptive immune responses."]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1 = model.encode(sentences[0], convert_to_tensor=True) # first sentence, response 1
embedding_2 = model.encode(sentences[1], convert_to_tensor=True) # second sentence, response 1

embedding_3 = model.encode(sentences2[0], convert_to_tensor=True) # first sentence, response 2
embedding_4 = model.encode(sentences2[1], convert_to_tensor=True) # second sentence, response 2

score1 = util.pytorch_cos_sim(embedding_1, embedding_2).item()
score2 = util.pytorch_cos_sim(embedding_3, embedding_4).item()

scores = [score1, score2] 
metric_val = round(statistics.mean(scores)*100, 2) #metric is the mean of cos_sim values for responses, multiplied by 100 and rounded to nearest 100th
print("Response similarity: " + str(metric_val) + "%")

