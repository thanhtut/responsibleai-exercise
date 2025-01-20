# TinyPII

A POC PII compoment that identifies and scraps out the personal identifiable information from the text.

Currently it detects and removes the following.
* names
* emails
* phone numbers
* NRICs
* addresses 


## Thoughts process

For simplest route, I could have used Spacy and it will lead to pretty nice results. Spacy has NER and it has entity classes for Names and Addresses. As for the email, phone number and NRICs regular expressions should do a decent job. As a bonus I have been using Spacy in production over three years so its realiable.

But to make it more intersting, I tried to find a dataset and opensource model on Huggingface. If I have a lot of time to work on this project I would defnitely look into open source dataset for PII such as [pii-masking-300k](https://huggingface.co/datasets/ai4privacy/pii-masking-300k) and [the The Learning Agency Lab - PII Data Detection](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/leaderboard) datasets. These can be used to fine-tune Llama or Bert models. However, I can only really work on this test on the weekends so I ended up using with a generic decent NER model.

I will use [dslim/bert-base-NER](https://huggingface.co/dslim/bert-base-NER) model to detect person names and location. The model card does not specify the evaluation results per category (Person and Location) but it is f1 91.3, precision 90.7 and recall 91.9 on the test set which is decent. 

## Implemtation
`dslim/bert-base-NER` will be used to detect person names and locations. Through testing I have noticed that it does not tag post codes as location. Therefore, postcodes will be detected as a part of addresses using regular expressions. Regular expressions are more appropirate than train models for detecting patterns that can be specificed using regular expression as they are 100% accurate if the pattern matches. In summary the detection method are as follows.
* names - NER class: B-PER, I-PER
* emails - Regex
* phone numbers - Regex 
* NRICs - Regex
* addresses - B-LOC, I-LOC and regex for post codes.

For the implementation steps, I will start by something I have found works great for data intensive applications that is defining the types first. I will use Pydantic for this as it is pretty much industry standard at this point.

The input to the API/method will be just text. The output will be an instance of pydantic class called `TinyPIIOutput` that has the following fields 
* text - The original text
* name - 1 or 0
* email - 1 or 0
* phone - 1 or 0
* nric - 1 or 0
* address - 1 or 0
* detections - list[TinyPIIDetection]
* redacted_text - Text with PII masked. 

The class `TinyPIIDetection` has the following fields
* detected class - Enum of 'TinyPIICategories' (name, email, phone, nric, address, location, )
* text - string
* confidence - float 0.0 to 1.0 
* position - (int,int)
* detector 0 Enum of 'TinyPIIDetectors' (HuggingFaceBertDetector, RegexDetector)

After that the flow of the logic of the detection
* Run HiggingFaceBertDetector (input text, output TinyPIIDetection)
* Run RegexDetector (input text, output TinyPIIDetection)
* Produce the TinyPIIOutput by aggregating these results 
* Convert these results to the requested CSV file output. 


# Running the script 
`poetry run python tiny_pii/scripts/process_csv1.py data/pii_data.csv --output_file data/pii_data_redacted.csv`


# Evaluation 
Since, this PII can be treated as a named entity recognition (NER) detection challenge for each category, it is appropirate to use F1-score for the evaluation. Also including precision and recall next to F1-score will add useful metrics to evaluate the performance and do necessary adjustments. 

There are other evaluation methods proposed which addresses downsides with using F1, precision and recall. For instance, [Interpretable Multi-dataset Evaluation for Named Entity Recognition](https://arxiv.org/abs/2011.06854). However, I would still stick to F1-score, precision and recall since they are widely adopted in the industry and easier to compute in existing workflows. 