import re
from flask import Flask, render_template, request, jsonify


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
# from utils import examples,METADATA

from transformers import pipeline
import comet_llm
import time


model_id = "Akish/GPT2-QA-Finetuned"
# model_id = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
                 model_id
                 )
pipe = pipeline("text-generation", 
               model=model, 
               tokenizer=tokenizer, 
               max_new_tokens=300
               )

examples = [
    {
        "question": "Where should I be investing my money?",
        "answer": """
Pay off your debt. As you witnessed, no investment % is guaranteed. 
But your debt payments are... so if you have cash, the best way to "invest" it is to pay off your debt. 
Since your car is depreciating while your house may be appreciating (don't know but it's possible) you should pay off your car loan first.
You're losing money in more than one way on that investment.
"""
    },
    {
        "question": "Investment strategy for retired couple",
        "answer": """
You need to have them consult with a financial adviser that has a focus on issues for seniors. 
This is because they are beyond the saving for retirement phase and are now in the making-their-money-last phase. 
They also have issues related to health insurance, IRA RMDs, long term care insurance. 
The adviser will need to review what they have and determine how to make sure it is what they need. 
It is great idea for you to go along with them so you can understand what needs to be done. 
You will want an adviser that charges you a fee for making the plan, not one that makes a commission based on what products you buy or invest in.
"""
    },
]

METADATA = {
    "model": model_id,
    "max_new_tokens": 1024,
    "skip_special_tokens": True,
}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')
    # return "Akish"


@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input = msg
        if "hi" == input.lower():
            return "Hello, I am AI Assistant For your Personal finance related queries. Ask me questions related to finance."
        elif "hello" == input.lower():
            return "Hi, I am AI Assistant For your Personal finance related queries. Ask me questions related to finance."
        else:   
            hf = HuggingFacePipeline(pipeline=pipe)
            prompt = f"""
            ### System:
            You're a highly obedient AI assistant tasked with addressing finance-related queries exclusively. 
            In the absence of financial inquiries, respond with financial terminology. 
            Offer maximum assistance within ethical boundaries, ensuring honesty, courtesy, and brevity, limiting responses to 100 words.

            below are some examples related to finance related question and answers. Please answer user questions accordingly
            ### Examples
            {examples}

            ### User:
            {input}

            ### Response:
            """
            # return get_Chat_response(input)
            # return "Akish"
            start = time.time()
            response = hf.predict(prompt)
    # print(response)
            match = re.search(r"### Response:\n(.*?)(?=###|$)", response, flags=re.DOTALL)

            if match:
                response = match.group(1).strip()  # Remove leading/trailing whitespace
                duration = time.time() - start
                comet_llm.init(project="finetuned-model")
                comet_llm.log_prompt(
                    prompt=input,
                    output=response,
                    duration=duration * 1000,
                    metadata=METADATA,
                )
                return response
            else:
                return "No 'Response' section found."

    except Exception as e:
        print(e)


# def get_Chat_response(text):

#     # Let's chat for 5 lines
#     for step in range(5):
#         # encode the new user input, add the eos_token and return a tensor in Pytorch
#         new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

#         # append the new user input tokens to the chat history
#         bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

#         # generated a response while limiting the total chat history to 1000 tokens,
#         chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

#         # pretty print last ouput tokens from bot
#         return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

if __name__ == '__main__':
    app.run()