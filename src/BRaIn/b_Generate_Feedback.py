import json

from transformers import AutoTokenizer

from vllm import LLM, SamplingParams
from tqdm import tqdm
from Utils import JSON_File_IO
from transformers import AutoTokenizer


def load_dataframe(file_path):
    return JSON_File_IO.load_JSON_to_Dataframe(file_path)


def load_json_to_dict(file_path):
    return JSON_File_IO.load_JSON_to_Dict(file_path)


def llm_scoring(es_results, bug_title, bug_description, llm):
    tokenizer = AutoTokenizer.from_pretrained("MODEL_PATH")

    user_role = {"role": "user", "content": ""}
    assistant_role = {"role": "assistant", "content": ""}

    user_text = """You are a helpful AI software engineer specializing in identifying buggy code segments given a bug report. Analyze the provided bug report and the JAVA code segment to determine if the code segment is responsible for causing the bug described in the bug report. You need to understand the functionality of the code segment and the details of the bug report to determine the relevance of the code segment to the bug report.

There are three possible outputs: 'yes', 'no', 'possible'.
-'yes': The code is responsible for the bug described in the bug report.
-'no': The code is NOT responsible for the bug described in the bug report.
-'possible': The code can be partially responsible for the bug described in the bug report.

Provide your output in JSON format like this sample: {"relevance": "yes"}.

Act like a rational software engineer and provide output. Avoid emotion and extra text other than JSON.

### 
Analyze the following bug report and code segment for relevance:"""

    instruction = '''Please determine if the code segment is responsible for the bug described in the bug report.'''

    bug_report = f'''Bug Report: \n- {bug_title} \n- {bug_description}'''

    for result in es_results:
        # file_url = result['file_url']
        # bm25_score = result['bm25_score']

        methods = result['methods']

        prompts = []

        # now, iterate over the key/value pairs of the methods in dictionary
        for method_name, method_body in methods.items():
            # add the method_body to the context

            code_context = f'''Code Segment: \n {method_body} '''

            # now, create the prompt
            prompt = user_text + '\n\n' + bug_report + '\n\n' + code_context + '\n\n' + instruction + '\n###'

            chat = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": ""},
            ]

            template = tokenizer.apply_chat_template(chat, tokenize=False)
            prompts.append(template)

        outputs = llm.generate(prompts)

        # zip through outputs and methods
        for output, method_name in zip(outputs, methods.keys()):
            # prompt = output.prompt
            response = output.outputs[0].text

            is_relevant = 'no'

            # check if the response contains 'yes', 'no'
            if 'yes' in response:
                is_relevant = 'yes'
            elif 'no' in response:
                is_relevant = 'no'

            # is_relevant = json.loads(response)['relevance']

            # add the score to the es_results
            result['methods'][method_name] = is_relevant

    return es_results


import html

if __name__ == '__main__':
    llm = LLM(model="MODEL_PATH", quantization="GPTQ", dtype="half",
              max_model_len=8192)

    sample_path = "SAVED_RESULTS_PATH"

    # load the json to dictionary
    df = load_dataframe(sample_path)

    # convert this to json string
    json_string = JSON_File_IO.convert_Dataframe_to_JSON_string(df)

    # iterate over the json string
    json_bugs = json.loads(json_string)

    # iterate over the json array
    for bug in tqdm(json_bugs, desc="Processing JSON Bugs"):
        # for bug in json_bugs:
        bug_title = html.unescape(bug['bug_title'])
        bug_description = html.unescape(bug['bug_description'])
        project = bug['project']
        sub_project = bug['sub_project']
        version = bug['version']
        es_results = bug['es_results']

        score_llm_results = llm_scoring(es_results, bug_title, bug_description, llm=llm)

        bug['es_results'] = score_llm_results

    json_save_path = "../../Output/Intelligent_Feedback/"
    JSON_File_IO.save_Dict_to_JSON(json_bugs, json_save_path, "Mistral_ZERO.json")
