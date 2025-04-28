from llm import *
from prompts import *
from roles import *
from stage import *

import json
import asyncio
import os
import time
from typing import List, Tuple, Dict, Any
import re
import copy


USER_NAME = "Khải"
AI_NAMES = ["Alice", "Bob", "Charlie"]


# client = OpenAI(
#     base_url="https://api.studio.nebius.com/v1/",
#     api_key=os.environ.get("NEBIUS_API_KEY")
# )

# def llm(prompt, tem = 0.4):
#     response = client.chat.completions.create(
#             model="google/gemma-3-27b-it",
#             max_tokens=2048,
#             temperature= tem,
#             top_p=0.9,
#             messages=[ {
#                 "role": "user",
#                 "content": [
#                     {"type" : "text", "text" : prompt},
#                 ]
#             }],
#         )
#     return response.choices[0].message.content


gemini = LLM(provider="Google", model="gemini-2.0-flash", temperature = 0.5)
def llm(prompt):
    return gemini.generate(prompt)




PRE_HISTORY = [
    ("Bob", 'Này các bạn, chúng ta cần giải hệ phương trình này: $2x + 3y = 6$ và $4x - y = 7$. Bắt đầu nào!'),
    ("Charlie", 'Mình nghĩ dùng phương pháp thế hoặc loại là được. Theo mình thì loại biến sẽ nhanh.'),
    ("Alice", 'Ừ, nhưng nếu loại biến thì có thể ra phân số đó. Ví dụ, nếu nhân phương trình thứ hai lên $3$, ta được $12x - 3y = 21$, rồi cộng với phương trình đầu $2x + 3y = 6$, sẽ ra $14x = 27$, tức là $x = 27/14$, hơi lằng nhằng.'),
    ("Khải", 'Đúng vậy, mà nếu dùng phương pháp thế thì cũng ra phân số thôi. Chẳng hạn, từ phương trình thứ hai, ta rút $y = 4x - 7$, rồi thế vào phương trình kia.'),
    ("Bob", 'Ồ, hay là dùng ma trận nhỉ? Nhưng mà chắc phức tạp :))'),
    ("Charlie", 'Ừ, hệ $2x2$ thế này thì thế hoặc loại là đủ rồi. Chọn một cái đi, khỏi phức tạp thêm.'),
    ("Alice", 'Nếu không thì vẽ đồ thị tìm giao điểm cũng được, nhưng mà cách đó không chính xác lắm.'),
    ("Khải", 'Trừ phi chỉ cần đáp án gần đúng, nhưng đây là đại số nên chắc cần đáp án chính xác hơn.'),
    ("Bob", 'Thôi được, vậy thử loại biến đi. Nhân phương trình đầu lên $2$ để hệ số của x bằng nhau xem sao.'),
    ("Alice", 'Khoan, phương trình đầu là $2x + 3y = 6$, nhân $2$ thì thành $4x + 6y = 12$. Phương trình thứ hai là $4x - y = 7$, đúng là hệ số $x$ đều thành $4x$ rồi.'),
    ("Bob", 'Ok, vậy là bài này ok rồi đó, chúng ta cùng sang bài mới nha.'),
    ("Charlie", 'Yee, tiếp tục thôi.'),
]



#######################
####### PROMPT ########
#######################

def prompt_TRIGGER():
    pass

def prompt_STAGE_MANAGER(problem, current_stage_description, history):
    return STAGE_MANAGER.format(
        problem = problem,
        current_stage_description = current_stage_description,
        history = history
    )

def prompt_AGENT_INNER_THOUGTS(AI_name, problem, current_stage_description, AI_description, previous_thoughts, history, poor_thinking):
    return AGENT_INNER_THOUGTS.format(
        AI_name = AI_name,
        problem = problem,
        current_stage_description = current_stage_description,
        AI_description = AI_description,
        previous_thoughts = previous_thoughts,
        history = history,
        poor_thinking = poor_thinking
    )

def prompt_THOUGHTS_EVALUATOR(list_AI_name, problem, current_stage_description, history, AI_thoughts):
    return THOUGHTS_EVALUATOR.format(
        list_AI_name = list_AI_name,
        problem = problem,
        current_stage_description = current_stage_description,
        history = history,
        AI_thoughts = AI_thoughts
    )

def prompt_CLASSMATE_SPEAK(AI_name, AI_role, AI_goal, AI_backstory, AI_tasks, problem, friends, current_stage_description, inner_thought, to_user, history):
    return CLASSMATE_SPEAK.format(
        AI_name = AI_name,
        AI_role = AI_role,
        AI_goal = AI_goal,
        AI_backstory = AI_backstory,
        AI_tasks = AI_tasks,
        problem = problem,
        friends = friends,
        current_stage_description = current_stage_description,
        inner_thought = inner_thought,
        to_user = to_user,
        history = history
    )

#######################
## HELPER FUNCTIONS ###
#######################


def AI_description(name, roles):
    info = next(role['description'] for role in roles if role["name"] == name)

    formatted = f"{info['role']}\n{info['goal']}\n{info['backstory']}\n{info['tasks']}"
 
    return formatted, (info['role'], info['goal'], info['backstory'], info['tasks'])

#print(AI_description("Bob", ROLES))


def format_AI_thoughts(thoughts_result):
    formatted = ""
    for ai_name, result in thoughts_result.items():
        print(f"\nAI Name: {ai_name}")
        print(f"Kết quả: {result}")

        formatted += f"- {ai_name} : \"{result['thought']}\"\n"
    return formatted


def remaining_AI(history, user_name= USER_NAME):
    last = history[-1]
    last_speaker = last['name']

    if last_speaker == user_name:
        remaining_roles = [role["name"] for role in ROLES if role["name"] != user_name]
    elif last_speaker in AI_NAMES:
        remaining_roles = [role["name"] for role in ROLES if role["name"] in AI_NAMES and role["name"] != last_speaker]
    else:
        remaining_roles = []

    return remaining_roles


# HISTORY = [
#     {
#         "num" : "1",
#         "name" : "Alice",
#         "utterance" : "alo...",
#         "thoughts" : [ # có trường hợp chỉ có 2 Agent nghĩ do trước đó agent A đã nói, nếu là Human nói thì sẽ có 3 agent suy nghĩ
#             {
#                 "agent_id" : "1",
#                 "agent_name" : "Bob",
#                 "inner_thought" : "...",
#                 "stimuli" : [], # từ CON#id, TASK#id, THO#id
#                 "intrinsic_motivation" : (0, 0) # internal and external
#             },
#         ]
#     },

#     {
#         "num" : "2",
#         "name" : "Bob",
#         "utterance" : "okok",
#         "thoughts" : [ # có trường hợp chỉ có 2 Agent nghĩ do trước đó agent A đã nói, nếu là Human nói thì sẽ có 3 agent suy nghĩ
#             {
#                 "agent_id" : "1",
#                 "agent_name" : "Bob",
#                 "inner_thought" : "...",
#                 "stimuli" : [], # từ CON#id, TASK#id, THO#id
#                 "intrinsic_motivation" : (0, 0) # internal and external
#             },
#         ]
#     }
# ]

def format_history(history, user_name="Khải"):
    # Đánh số từ 1 cho hội thoại thật
    formatted_real = []
    for utt in history:
        formatted_real.append(f"(CON#{utt['num']}) - {utt['name']}: {utt['utterance']}\n")

    formatted = [f"{speaker}: {msg}\n" for speaker, msg in PRE_HISTORY] + formatted_real

    # Lấy 15 tin nhắn mới nhất
    last = formatted[-15:]
    return ''.join(last)


def stage_description(current_stage):
    for stage in STAGES:
        if current_stage == stage['stage']:
            stage_name = stage["name"]
            stage_description = stage["description"]
            stage_tasks = stage['tasks']
            stage_goals = stage['goals']

            result = f"- Quá trình: \"{stage_name}\"\n- Mô tả quá trình: {stage_description}\n- Các nhiệm vụ cần thực hiện:\n"

            for idx, item in enumerate(stage_tasks):
                result += f"  (STEP#{idx + 1}): {item}\n"
                
            result += "- Các mục tiêu cần đạt được để kết thúc quá trình này:\n"
            for idx, item in enumerate(stage_goals):
                result += f"  (GOAL#{idx + 1}): {item}\n"

            result += "- Quan trọng: mỗi mục tiêu cần được nhắc đến khi thực hiện nhiệm vụ liên quan đến nó, cần lựa chọn thời điểm thích hợp, khéo léo để nêu ra." 
            return result


def parse_json(resp):
    return json.loads(resp.strip('```json').strip('\n```'))



def previous_thoughts(AI_name: str, history: List[Dict[str, Any]], num: int = 3) -> Tuple[str, List[float]]:

    recent_thoughts_formatted = []
    total_internal_motivation = 0.0
    total_external_motivation = 0.0
    thoughts_found_count = 0 

    for turn in reversed(history):
        if "thoughts" in turn and isinstance(turn["thoughts"], list):
            turn_num = turn.get("num")

            if turn_num is None:
                continue

            for thought in turn["thoughts"]:
                if thoughts_found_count >= num:
                    break

                if (isinstance(thought, dict) and
                    thought.get("agent_name") == AI_name):

                    inner_thought_text = thought.get("inner_thought")
                    motivation_scores = thought.get("intrinsic_motivation")

                    if (inner_thought_text and
                        motivation_scores and
                        isinstance(motivation_scores, list) and
                        len(motivation_scores) == 2 and
                        all(isinstance(score, (int, float)) for score in motivation_scores)):

                        formatted_thought = f"(THO#{turn_num}) : {inner_thought_text}"
                        recent_thoughts_formatted.append(formatted_thought)

                        total_internal_motivation += motivation_scores[0]
                        total_external_motivation += motivation_scores[1]

                        thoughts_found_count += 1

        if thoughts_found_count >= num:
            break

    avg_internal = 0.0
    avg_external = 0.0
    if thoughts_found_count > 0:
        avg_internal = total_internal_motivation / thoughts_found_count
        avg_external = total_external_motivation / thoughts_found_count

    return "\n".join(recent_thoughts_formatted), [avg_internal, avg_external]


def last_turn(name):
    pass


def analysis_user(history, user_name = USER_NAME):
    last = history[-6:]
    num_interact = 0

    return ""

    for i in last:
        if i[0] == user_name:
            num_interact += 1

    if int(num_interact) == 0:
        return f"Bạn học {user_name} đang có mức độ tương tác THẤP, bạn phải có các hành động khuyến khích bạn tham gia."
    return ""


def clean_ai_response(text):
    """Removes <think>...</think> blocks from AI responses."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def print_history(history, CURRENT_STAGE):
    print("\n--- LỊCH SỬ HỘI THOẠI ---")
    if not history:
        print("(Lịch sử trống)")
    for turn in history:
        print(f"{turn['num']}. {turn['name']}: {repr(turn['utterance'])}")
    print("\n---------------------------")
    print(f"--- Giai đoạn hiện tại: {CURRENT_STAGE} ---")
    print("---------------------------")


def update_history(ai_response, history):
    HISTORY = copy.deepcopy(history)

    AI_thoughts = ai_response['thoughts']
    evaluator = ai_response['evaluator']

    inner_thoughts = []

    for ai in evaluator:
        name = ai['name']
        internal_score = ai['internal_score']
        external_score = ai['external_score']

        thought = AI_thoughts[name]['thought']
        stimuli = AI_thoughts[name]['stimuli']

        t = {
            "agent_name": name,
            "inner_thought": thought,
            "stimuli": stimuli,
            "intrinsic_motivation": [internal_score, external_score]
        }

        inner_thoughts.append(t)
    
    HISTORY[-1]['thoughts'] = inner_thoughts


    # Cập nhật u_i
    ai_name = ai_response["name"]
    cleaned_talk = clean_ai_response(ai_response["speak"])

    num = HISTORY[-1]['num'] + 1
    HISTORY.append({"num" : num,
                    "name" : ai_name,
                    "utterance" : cleaned_talk,
                    "thoughts" : None})
    
    return HISTORY