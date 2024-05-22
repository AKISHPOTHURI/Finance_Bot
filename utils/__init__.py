from app import model_id

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