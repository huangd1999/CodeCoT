import re
import json

def extract_doctests(docstring: str):
    # 修改正则表达式，只提取函数参数
    pattern = re.compile(r'>>> \w+\((.*)\)\n(.*?)(?=\n|$)', re.MULTILINE)
    matches = pattern.findall(docstring)
    return matches

def update_test_field(data):
    tests = extract_doctests(data["prompt"])
    
    test_statements = []
    for test_input, expected_output in tests:
        if not expected_output.strip():
            expected_output = "None"
        
        # 使用 candidate 函数并插入参数
        statement = f"assert candidate({test_input}) == {expected_output}"
        test_statements.append(statement)

    test_content = data["test"]
    position = test_content.find("def check(candidate):") + len("def check(candidate):")
    test_content = test_content[:position] 
    for stmt in test_statements:
        test_content = test_content[:position] + "\n    " + stmt + test_content[position:]
        position += len("\n    " + stmt)

    data["test"] = test_content

data_list = []

with open('HumanEval.jsonl', 'r') as file:
    for line in file:
        obj = json.loads(line.strip())
        data_list.append(obj)

temp = 0
for i in range(len(data_list)):
    if ">>>" not in data_list[i]["prompt"]:
        temp+=1

print(len(data_list))

for data in data_list:
    update_test_field(data)

with open("./self-exam-human-eval.json","w") as f:
    for data in data_list:
        f.write(json.dumps(data))
        f.write('\n')


print(temp)