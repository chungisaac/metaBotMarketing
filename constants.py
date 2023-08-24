from string import Template

## For the LLM Prompting
USER_ID = 'meta'
APP_ID = 'Llama-2'
MODEL_ID = 'llama2-70b-chat'
MODEL_VERSION_ID = '6c27e86364ba461d98de95cddc559cb3'

PROMPT_TEMPLATE = Template("Prepare an example facebook post to promote Clarifai's $highlight. Only output the raw text of the example. Do not include instructions. Include the hashtags '$hashtags'. Include the relevant link $optional `$link`. Limit the entire example to 2000 characters including the link.")
PROMOTION_HASHTAG_LINK_TUPLES = [
    ("LLM finetuning capabilities", "#LLM", "to a blogpost", "https://www.clarifai.com/blog/fine-tuning-gpt-neo-for-text-classification"),
    ("LLM finetuning capabilities", "#LLM", "to a video tutorial", "https://www.youtube.com/watch?v=Ycl7xVA2wHk"),
    ("vector search capabilities", "#LLM", "", "https://www.clarifai.com/use-cases/visual-search"),
    ("generative AI capabilities", "#generativeAI", "", "https://www.clarifai.com/products/generative-ai"),
    ("content moderation capabilities", "#LLM", "", "https://www.clarifai.com/solutions/content-moderation"),
    ("DAM capabilities", "#Clarifai", "", "https://www.clarifai.com/solutions/digital-asset-management"),
    ("predictive maintenance capabilities", "#Clarifai", "", "https://www.clarifai.com/use-cases/predictive-maintenance"),
    ("Edge AI capabilities", "#Clarifai", "", "https://www.clarifai.com/use-cases/isr-edge-ai"),
    ("open positions", "#hiring", "", "https://www.clarifai.com/company/careers"),
    ("LLM prompt capabilities", "#LLM", "", "https://docs.clarifai.com/api-guide/predict/llms/#via-raw-text"),
    ("serverless inference capabilities", "#LLM", "", "https://docs.clarifai.com/api-guide/predict/llms/#via-raw-text")
]

PROMPTS = [
    PROMPT_TEMPLATE.safe_substitute(
        highlight=tup[0], 
        hashtags=tup[1],
        optional=tup[2],
        link=tup[3]
    ) for tup in PROMOTION_HASHTAG_LINK_TUPLES
]

FB_PAGE_ID='122309344291300'

## For uploading the link to clarifai
UPLOAD_USER_ID = 'Isaac'
UPLOAD_APP_ID = 'fb-post-links'
