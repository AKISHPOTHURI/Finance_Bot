import re
from flask import Flask, render_template, request, jsonify


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

from transformers import pipeline
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
            You are an AI assistant that follows instructions extremely well. Your are responsible for answering questions related to finance. Give answers only related to finance.
            If the questions are not related finance try to answer in financial terms only.Help as much as you can. Please be truthful,polite and give direct answers in 100 words. 

            ### User:
            {input}

            ### Response:
            """
            # return get_Chat_response(input)
            # return "Akish"
            response = hf.predict(prompt)
    # print(response)
            match = re.search(r"### Response:\n(.*?)(?=###|$)", response, flags=re.DOTALL)

            if match:
                response = match.group(1).strip()  # Remove leading/trailing whitespace
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