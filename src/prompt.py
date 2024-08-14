# implement File
import os
from openai import OpenAI
MODEL = "gpt-4-turbo"
#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4o-mini"

def output_context(model):
    content = "Stepwise Discrete Controller Synthesis is a method that aims to efficiently control the overall system by reducing the state space for parallel synthesis by performing controller synthesis for each part of the environmental and monitoring models.\nIn stepwise discrete controller synthesis, the cost of exploring the computational space depends on the order in which the environmental and monitoring models are synthesized.\n\nThe choice of the environment model and the monitoring model for partial controller synthesis is not free to choose, but a restriction exists.The restriction is that the actions of the \"environment model used for synthesis\" must include all the actions of the \"requirement model used for synthesis,\" and the actions of the \"environment model not used for synthesis\" must not include the actions of the requirement model.\n\nSuppose we are given a set of environment model $R$ and a set of requirement model $R$. First, the requirement model $r^*$ to be analyzed is determined by Stepwise Policy, and $E^*$ which is defined as the set of environment models to be synthesized with $r^*$ is derived. Next, executing of DCS between $r^*$ and $E^*$ leads to create a new environmental model $e^*$ under which the requirements of $r^*$ are satisfied. Finally, the sum of E nor included in $E^*$ and $e^*$ is redefined as a new $E$ and $R$ not included in $r^*$ is redefined as a new $R$. By repeating the above process until $R$ is an empty set, a controller which satisfies $R$ can be created."
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content},
        ]
    )
    msg = completion.choices[0].message.content
    print("-----CONTEXT-----")
    print(msg)
    return content,msg

def output_EnvReqInformation(context_content, context_response, input_env, input_req, input_reqenv, model):
    with open(r"src/input/environment_model.txt") as f:
        envmodel = f.read()
    with open(r"src/input/requirement_model.txt") as f:
        reqmodel = f.read()
    content =  "I give you the LTS of the environment models and a summary of the relationship between an environment model and the actions it has in JSON format.\n\n" + envmodel + "\n\n" + input_env + "\n\nI give you requirement models and a summary of the relationship between an requirement model and the actions it has in JSON format.\n\n" + reqmodel + "\n\n" + input_req + "\n\nFor each requirement model, the following is a summary in JSON format of the \"environment model that has the actions that the requirement model has\".The set of environmental models corresponding to the requirement model is called the monitored model.\n\n" + input_reqenv

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": context_content},
            {"role": "assistant", "content": context_response},
            {"role": "user", "content": content},
        ]
    )
    msg = completion.choices[0].message.content
    print("-----READ INFORMATION-----")
    print(msg)
    return content,msg


def output_chooseRequirement(context_content, context_response, inf_content, inf_response, model):
    content = "I want to perform a stepwise discrete controller synthesis with low computational cost. Please create a set of requirement models to be synthesized firstly.\nOnly output requirement models and their monitored models.\n\n##Reference##\nWhen selecting requirement models, it is desirable to have as many of the monitored models in common as possible."
    + "\nWhen selecting a requirement model, it is best to choose the one with the least number of monitored models for that requirement model."
    + "\n\n##Example##\nWhen the relationship between requirement model and monitored model is as follows,\n[{\"Requirement\": P_DO_NOT_UP, \"Environment\": ALTITUDE},{\"Requirement\: P_DO_NOT_MOVE_X, \"Environment\": AREA},{\"Requirement\: P_DO_NOT_MOVE_Y, \"Environment\": AREA},{\"Requirement\": P_LOW_BATTERY, \"Environment\": [BATTERY, ALTITUDE]}]\nThe order of selecting the set of requirement models should be P_DONT_UP, (P_DO_NOT_MOVE_X,P_DO_NOT_MOVE_X), and P_LOW_BATTERY, in that order."
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": context_content},
            {"role": "assistant", "content": context_response},
            {"role": "user", "content": inf_content},
            {"role": "assistant", "content": inf_response},
            {"role": "user", "content": content},
        ]
    )
    msg = completion.choices[0].message.content
    print("-----Choose Requirement-----")
    print(msg)
    return content,msg





client = OpenAI()

with open(r"src/input/env_action.txt") as f:
    input_env = f.read()
with open(r"src/input/req_action.txt") as f:
    input_req = f.read()
with open(r"src/input/req_env.txt") as f:
    input_reqenv = f.read()



context_content, context_response = output_context(MODEL)
inf_content, inf_response = output_EnvReqInformation(context_content, context_response, input_env, input_req, input_reqenv, MODEL)
req_content, req_response = output_chooseRequirement(context_content, context_response, inf_content, inf_response, MODEL)