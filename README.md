# CoxiReduxer

CoxiReduxer is an ML data analysis pipeline to assist with better understanding the needs of fellow students. In order to be able to create good guidelines for large group chats and create effective knowledge bases (like FAQs), one needs to be aware of the topics being discussed, and with what frequency. The analysis needs to both a) condense information, so that more general answers for more specific questions can be provided (wherever possible), but it also needs to b) offer a reasonable amount of granularity, so that nuanced information from individual messages is retained.

ML solutions seem enticing here because technologies like LLMs allow more general semantic clustering of this type of informal information where other methods (like simply comparing the lexica of different messages) might fall short.

## CoxiReduxer Pipeline

### 1 Pre-processing

Relatively straight-forward: the data comes exported from Telegram in JSON format. Some simple clean-up is needed, and irrelevant data is removed.

## 2 Points-of-interest extraction

Not every message is going to contain some kind of valuable information. Some are merely part of a larger discussion, some are very simple questions from which no "wisdom" can be generated from (like "is this one course not happening today?"), etc. To get a first summary of what might be valuable and what not, this first step is the most semantically abstract. 

We iterate over each message with a sliding context window (10 anterior, 10 posterior), and pass it to an LLM. The LLM is tasked to simply summarise the message at hand (the "focus message"). It is coerced into returning data in a format that is useful to us using structured output. Essentially, the LLM is instructed to return an array of *Points Of Interest*. This is simply an abstraction of all things that could be useful (the reason why this approach was chosen instead of presenting a more explicit model like "hasQuestion" is because LLMs are extremely susceptible to confirmation bias and merely *implying* that there *might* be a question in the message makes the LLM much more likely to "invent" a question. This problem becomes more and more exaggerated the more elaborate the structured output model is). 

These *Points Of Interest* can be questions, facts, insights, ... The goal is to have the LLM choose primarily between these three, but also have it be able to add a new category when nothing else fits. Though the problem here is, again, that the LLM is not necessarily all that good at figuring out what a good category is.

For one, this approach leads to a much semantically summarised version of the chat history, but it also leads to *syntactically cleaned* version. People make typos, and the LLM can, in many circumstances, correct them.

**This already gives us our first results**. While further processing will take place, after this step we can already start to assemble some of the information, for example by filtering for classifications which are of type "fact". These can simply be collected and manually processed.

## 3 Topic clustering

This is the