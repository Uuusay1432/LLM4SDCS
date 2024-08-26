# implement File
import os
from openai import OpenAI
#MODEL = "gpt-4-turbo"
MODEL = "gpt-3.5-turbo"
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
    with open(r"src/input/fixed_example/environment_model.txt") as f:
        envmodel = f.read()
    with open(r"src/input/fixed_example/requirement_model.txt") as f:
        reqmodel = f.read()
    content =  "I give you the LTS of the environment models\n\n" + envmodel + "\n\nAnd I give you a summary of the relationship between an environment model and the actions it has in JSON format.\n\n" + input_env + "\n\nI give you requirement models\n\n" + reqmodel + "\n\nAnd I give you a summary of the relationship between an requirement model and the actions it has in JSON format.\n\n" + input_req + "\n\nFor each requirement model, the following is a summary in JSON format of the \"environment model that has the actions that the requirement model has\".The set of environment models corresponding to the requirement model is called the monitored model.\n\n" + input_reqenv

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
    print(input_reqenv)
    print(msg)
    return content,msg


def output1_chooseRequirement(context_content, context_response, inf_content, inf_response, model):
    content = "{\"task\": \"I want to perform a stepwise discrete controller synthesis with low computational cost. Please create a set of requirement models to be synthesized firstly reference to following advice.\", \"##1st Advice##\": \"When selecting requirement models, it is desirable to have as many of the monitored models of the requirement models in common as possible.\", \"##2nd Advice##\": \"When selecting a requirement model, it is desirable to choose the one with the least number of monitored models for that requirement model. This perspective is most important.\"}"
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
    print("----- Choose Requirement 1 -----")
    print(msg)
    return content,msg

def output2_chooseRequirement(context_content, context_response, inf_content, inf_response, req1_content, req1_response, model):
    with open(r"src/input/fixed_example/demo.txt") as f:
        demo = f.read()
    content = "{\"task\": \"I want to perform a stepwise discrete controller synthesis with low computational cost !in above drone systems!. Please create a set of requirement models to be synthesized firstly reference to following advice., ##3rd Advice##:Although this criterion is not a high priority, you should use the following technique if you have troubles. We first analyze the requirement model with the highest percentage of violations in the game space.The game space is an LTS model in which all the environment models and the corresponding requirement models are synthesized in parallel.Parallel synthesis takes multiple LTSs as inputs and outputs LTSs that represent the behavior when all input LTSs are executed simultaneously.\nWe can analyze the lts of the environment and requirement models given following, deduce what kind of controller will be completed when synthesized in parallel, and identify the monitoring model with the highest percentage of violation states.\n\nSynthesizing a requirement model may reduce the number of states and transitions compared to simply synthesizing its monitored model. The amount of reduction is defined as the \'semantic impact range\'.\nThe semantic impact is greater when the monitored model of the requirement model is more complex, and when the number of transitions or states is reduced or limited more.\n\nWhen executing SDCS, the cost can be reduced by synthesizing from those that have a large range of influence on semantic.\n\nFor the drone environment model and requirement model given earlier, in order to perform SDCS with lower cost, analyze each lts using experience and intuition, and derive a requirement model with a large reduction in the range of influence on semantic.\nPlease refer to the Demonstration for how to use experience and intuition.\", \"Demonstrarition\":"+ demo + "}"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": context_content},
            {"role": "assistant", "content": context_response},
            {"role": "user", "content": inf_content},
            {"role": "assistant", "content": inf_response},
            {"role": "user", "content": req1_content},
            {"role": "assistant", "content": req1_response},
            {"role": "user", "content": content},
        ]
    )
    msg = completion.choices[0].message.content
    print("----- Choose Requirement 2 -----")
    print(msg)
    return content,msg


def output_result(context_content, context_response, inf_content, inf_response, req1_content, req1_response, req2_content, req2_response, model):
    content = "Considering the totality of what you have analyzed so far, choose the best set of requirement models that should be synthesized at the beginning of the SDCS from this state in drone system, not in room system. And then, Create a set of environmental models to be synthesized with that requirement model."
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": context_content},
            {"role": "assistant", "content": context_response},
            {"role": "user", "content": inf_content},
            {"role": "assistant", "content": inf_response},
            {"role": "user", "content": req1_content},
            {"role": "assistant", "content": req1_response},
            {"role": "user", "content": req2_content},
            {"role": "assistant", "content": req2_response},
            {"role": "user", "content": content},
        ]
    )
    msg = completion.choices[0].message.content
    print("----- Output Result-----")
    print(msg)
    return content,msg


client = OpenAI()

#input_env = input("環境モデルとその環境モデルが持つアクションとの関係をJSON形式で表したもの\n")
with open(r"src/input/env_action.txt") as f:
    input_env = f.read()
#input_req = input("監視モデルとその監視モデルが持つアクションとの関係をJSON形式で表したもの\n")
with open(r"src/input/req_action.txt") as f:
    input_req = f.read()
#input_reqenv = input("その監視モデルが持つアクションを持っている環境モデルをJSON形式で表したもの\n")
with open(r"src/input/req_env.txt") as f:
    input_reqenv = f.read()



context_content, context_response = output_context(MODEL)
inf_content, inf_response = output_EnvReqInformation(context_content, context_response, input_env, input_req, input_reqenv, MODEL)
req1_content, req1_response = output1_chooseRequirement(context_content, context_response, inf_content, inf_response, MODEL)
req2_content, req2_response = output2_chooseRequirement(context_content, context_response, inf_content, inf_response, req1_content, req1_response, MODEL)
out_content, out_response = output_result(context_content, context_response, inf_content, inf_response, req1_content, req1_response, req2_content, req2_response, MODEL)