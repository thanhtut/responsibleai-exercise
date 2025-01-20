## Introduction

This document descirbes the answers to the questions regarding the paper [LionGuard: Building a Contextualized Moderation 
Classifier to Tackle Localized Unsafe Content](https://arxiv.org/abs/2407.10995). In addition it contains potential improvements.

1. Why are low-resource languages challenging for natural language processing and large language models? Discuss this with reference to tokenisation.

If I have to explain this to a layperson (non NLP/AI person), I would say that all current NLP/LLM approaches scales with data/compute. That is the capaiblities of the models gets better with more data and more compute usually. For the low-resource languages, there are usually not much a lot of datasets available to train the models. Lack of quality and quantity of training data for low-resource languages usually means that it is more difficult to train models and perform research in low-resource languages. Thus training models and performing research for low-resource languages will always be like playing a catchup game. [Interesting read](https://arxiv.org/html/2410.20817v1)

Tokenization is the process of breaking down text into smaller units known as tokens. A token can be subwords, words or characters. Tokenization essential in any NLP workflows. In traditional NLP (non LLMs), tokenization is usually done at word level. 

Lets imagine you are trying to work in a high-resource language, English. We will use a popular NLP library called Spacy. Here we can see that there tokenizer for English is 100% accurate by [this documentation](https://spacy.io/models/en#en_core_web_sm-accuracy). However, if you want to work with a (medium) low-resource language like Thai, you will have to use [a plugin](https://spacy.io/universe/project/spacy-pythainlp) with potentially outdated wrapping methods. For even (very low) low-resource languages like Burmese or Cambodian, they are not even mentioned on the radar of the industry's popular NLP toolkits. 

Regarding the LLM, Open AI's uses [tiktoken](https://github.com/openai/tiktoken) which uses Byte-Pair Encoding (BPE). It allows efficient way to compress text and a token usually is equipvalent to 4 characers in English. However we can see that to Burmese languages using 3x more tokens than English for the same characters. This token system is not as efficient with non English and especially non latin low-resource languages.


2. What implications does this paper have for the development of safety guardrails for LLMs in countries with low-resource languages?

The paper showed that the general guardrail models perform poorly on low-resource language, in particular Singlish, an English creole. The paper also emphasized the importance of considering local context for content moderation. For instance, the category 'public harm' is usually missing in western-dominated category of unsafe content but added by the authors as a sperate category. That is probably due to local's regulations and culture.

The paper also hilighted that with local context and the right knowledge from the smart people, it is possible to develop a siginificantly better guardrail for a low-resource language without requiring a lot of data labelling and computational resources. 

3. Why was PR-AUC used as the evaluation metric for LionGuard over other performance metrics? In what situations would a F1-score be preferable? 

The choice of evaluation metric depends on the balance of dataset and the goal of the model. In the LionGuard(Foo and Khoo, 2024) paper, the dataset consists of a much lower percentage of positive labels, 6.15% for unsafe labels and 0.06% for self-harm. As a bad measure example, using Accuracy measure for a classifier that always says safe will result in 93% accuracy. Both F1-score and PR-AUC are usually used with imbalanced datasets. 

When it comes to a guardrails model, it is necessary to consider the threadshold of the score where the label should be considered a positive label or negative label. The thredshold can be adjusted based on the how sensitive of a guardrails is necessary. Therefore, PR-AUC measure is more relevant as it evaluates precision and recall tradeoff across all thredsholds. 

F1-score would be preferable if whenever there is not a need to consider the model's performance curve across all thredshold. It is because it gives a more direct value of both precision and recall.

4. What are some weaknesses in LionGuard’s methodology? 

Note: These arguments are made with regard to LionGuard the paper. As a tool for content moderation in Singlish it is a really promising product with the modely openly available on Hugging face. 

Please excuse me as I will go into a conference's reviewer mode. 

I have worked with subjective judements as well and it is very difficult to correctly reach a consistency even among human regarding whether a text should be considered safe or unsafe. First of all the initial 200 samples of expert labelled dataset. It is probably quite a small dataset with 7 categories. In addition, the term expert labelled dataset should be quantified as there might be people who do the content moderation as their profession and considered experts in content moderation. The crowdsourcing experitment also revealed that the it is very hard to reach consensus by (non-expert)humans on the most important category "unsafe" with only 52.9% aggrement.

It would also be interesting to see the societal and legal context for adding the category "public harm" as well as how the definitions of safe and unsafe context differs. In a related note, it would be interesting to see if the crowd sourced users were to do a small calibration quiz before labelling, would it lead to more consensus between them and the LLM prompt generated labels.

And one other limitation of the applicability of the paper against low-resources languages is that the heavy lifting of the LionGuard model seems to be coming from the embedding model as all the classifiers produces similar results given the same embedding model. The embedding models will not work just as well for actual non English based low-resource languages. Though the technique is applicable for local contextualized content moderation, it wont necessarily apply to low-resource language approaches where the language is not a creole language of a high-resource language.  

## References 
https://arxiv.org/html/2410.20817v1#S7
