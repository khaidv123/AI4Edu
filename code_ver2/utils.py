import time
import re
import threading
import sys
import select
import queue 
import json
import time

from openai import OpenAI
import os
import base64

from llm import *
from prompts import *

USER_NAME = "Khải"
AI_NAMES = ["Alice", "Bob", "Charlie"]


client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

def llm(prompt, tem = 0.3):
    response = client.chat.completions.create(
            model="google/gemma-3-27b-it",
            max_tokens=2048,
            temperature= tem,
            top_p=0.9,
            messages=[ {
                "role": "user",
                "content": [
                    {"type" : "text", "text" : prompt},
                ]
            }],
        )
    return response.choices[0].message.content


gemini = LLM(provider="Google", model="gemma-3-27b-it", temperature = 0.3)
def gemini_resp(prompt):
    return gemini.generate(prompt)

# gemini = LLM(provider="Google", model="gemini-2.0-flash", temperature = 0.5)
# def llm(prompt):
#     return gemini.generate(prompt)



# Thảo mai quá --> thiết kế khác, chỉ thỉnh thoảng nêu tên người khác
# PRE_HISTORY = [
#     ("Bob", '''Rồi, chào cả nhà! Chúng ta lại gặp nhau để chuẩn bị cho buổi học nhé. Mọi người sẵn sàng chưa? Khải ơi, cậu thấy sao, đã xem trước bài hôm nay chưa?'''),
#     ("Khải", '''Mình đây rồi Bob ơi! Mình cũng có đọc qua một chút rồi, cũng có vài chỗ thấy hơi khó hiểu.'''),
#     ("Alice", '''Ồ la la! Khó hiểu cỡ nào Khải? Có giống như cố gắng giải thích màu sắc cho người chưa từng thấy không? Hay chỉ như tìm đôi tất cùng màu vào sáng thứ Hai thôi? *cười khúc khích*'''),
#     ("Charlie", '''Alice hài hước ghê! Nhưng mà Khải nè, cụ thể là phần nào cậu thấy lấn cấn vậy? Có khái niệm hay công thức nào làm cậu phải nhíu mày không? Chia sẻ để tụi mình mổ xẻ kỹ hơn xem.'''),
#     ("Bob", '''Đúng đó Khải, cậu cứ nói rõ những thắc mắc ban đầu của cậu đi. Để tớ nắm được tình hình chung và chúng ta cùng nhau tìm hướng giải quyết từng bước một.'''),
#     ("Khải", '''Ừm... thì mình thấy phần... Mà khoan đã, sao mọi người cứ hỏi mình thế nhỉ? Mình cũng muốn nghe ý kiến của các cậu trước mà. Bob thấy tổng quan bài này thế nào? Alice có thấy điểm nào thú vị không? Charlie có dự đoán phần nào sẽ 'khoai' không?'''),
#     ("Bob", '''Ồ, Khải nói đúng. Xin lỗi nhé, bọn tớ hơi tập trung hỏi cậu quá. Theo tớ thấy, bài hôm nay có cấu trúc khá logic, nhưng phần liên hệ thực tế có thể cần đào sâu thêm để hiểu rõ ứng dụng.'''),
#     ("Alice", '''Hehe, bị Khải 'bắt bài' rồi! Tớ thì lại thấy mấy cái ví dụ minh họa khá buồn cười, không biết tác giả cố tình hay vô ý nữa. Nhưng đúng là nó giúp nhớ bài hơn đấy! Có ai thấy giống tớ không?'''),
#     ("Charlie", '''Khải nhắc hay lắm! Tớ đồng ý với Bob về phần liên hệ thực tế. Còn tớ thì đang tò mò về cái định lý X cuối bài ấy, đọc qua thấy có vẻ trừu tượng, chắc chắn là phần cần thảo luận kỹ. Có khi nào nó liên quan tới bài tuần trước không nhỉ?'''),
#     ("Khải", '''Đấy, như vậy có phải tốt hơn không! Mỗi người một góc nhìn. Giờ mình thấy hào hứng hơn rồi đó. Vậy mình bắt đầu từ việc tóm tắt lại ý chính như Bob nói rồi đi vào các phần chi tiết như Alice và Charlie đề cập nhé?'''),
# ]

# PRE_HISTORY = [
#     ("Bob", '''Này các bạn, chúng ta cần giải hệ phương trình này: $2x + 3y = 6$ và $4x - y = 7$. Bắt đầu nào!'''),
#     ("Charlie", '''Mình nghĩ dùng phương pháp thế hoặc loại là được. Theo mình thì loại biến sẽ nhanh.'''),
#     ("Alice", '''Ừ, nhưng nếu loại biến thì có thể ra phân số đó. Ví dụ, nếu nhân phương trình thứ hai lên $3$, ta được $12x - 3y = 21$, rồi cộng với phương trình đầu $2x + 3y = 6$, sẽ ra $14x = 27$, tức là $x = 27/14$, hơi lằng nhằng.'''),
#     ("Khải", '''Đúng vậy, mà nếu dùng phương pháp thế thì cũng ra phân số thôi. Chẳng hạn, từ phương trình thứ hai, ta rút $y = 4x - 7$, rồi thế vào phương trình kia.'''),
#     ("Bob", '''Ồ, hay là dùng ma trận nhỉ? Nhưng mà chắc phức tạp :))'''),
#     ("Charlie", '''Ừ, hệ $2x2$ thế này thì thế hoặc loại là đủ rồi. Chọn một cái đi, khỏi phức tạp thêm.'''),
#     ("Alice", '''Nếu không thì vẽ đồ thị tìm giao điểm cũng được, nhưng mà cách đó không chính xác lắm.'''),
#     ("Khải", '''Trừ phi chỉ cần đáp án gần đúng, nhưng đây là đại số nên chắc cần đáp án chính xác hơn.'''),
#     ("Bob", '''Thôi được, vậy thử loại biến đi. Nhân phương trình đầu lên $2$ để hệ số của x bằng nhau xem sao.'''),
#     ("Alice", '''Khoan, phương trình đầu là $2x + 3y = 6$, nhân $2$ thì thành $4x + 6y = 12$. Phương trình thứ hai là $4x - y = 7$, đúng là hệ số $x$ đều thành $4x$ rồi.'''),
#     ("Bob", '''Ok, vậy là bài này ok rồi đó, chúng ta cùng sang bài mới nha.'''),
#     ("Charlie", '''Yee, tiếp tục thôi.'''),
# ]

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



################################
#########  PROMPTS  ############
################################


def prompt_Human_AI_Speaker_Controller(history_for_manager, user_name = USER_NAME):
    return Human_AI_Speaker_Controller.format(
        user_name = user_name,
        history_for_manager = history_for_manager
    )

def prompt_AI_Speaker_Controller(remaining_AI_roles, 
                                 current_stage, stage_act, 
                                 history_for_manager, 
                                 user_name = USER_NAME):
    return SPEAKER_CONTROLLER.format(
        user_name = user_name,
        remaining_AI_roles = remaining_AI_roles,
        current_stage = current_stage,
        stage_act = stage_act,
        history_for_manager = history_for_manager
    )


def prompt_Stage_Controller(problem, current_stage,  history_for_manager):
    return STAGE_CONTROLLER.format(
        problem = problem,
        current_stage = current_stage,
        history_for_manager = history_for_manager
    )


def prompt_verifier(current_stage, 
                    output_from_stage_controller, 
                    history_for_manager, 
                    output_from_ai_speaker_controller, 
                    user_name = USER_NAME):
    return VERIFIER.format(user_name = user_name,
                           current_stage = current_stage,
                           output_from_stage_controller = output_from_stage_controller,
                           history_for_manager = history_for_manager,
                           output_from_ai_speaker_controller = output_from_ai_speaker_controller)



def prompt_Classmate_Agent(AI_name, AI_role, problem, friends, current_stage,
                           output_from_stage_controller, history, to_user, act, ref):
    return CLASSMATE_AGENT.format(AI_name = AI_name, 
                                  AI_role = AI_role,
                                  problem = problem,
                                  friends = friends,
                                  output_from_stage_controller = output_from_stage_controller,
                                  current_stage = current_stage,
                                  history = history,
                                  to_user = to_user,
                                  act = act,
                                  ref = ref)



################################
###### HELPER FUNCTIONS  #######
################################

def remaining_AI(history, user_name= USER_NAME):
    last_speaker = history[-1][0]

    if last_speaker == user_name:
        remaining_roles = [role for role in ROLES if role["name"] != user_name]
    elif last_speaker in AI_NAMES:
        remaining_roles = [role for role in ROLES if role["name"] in AI_NAMES and role["name"] != last_speaker]
    else:
        remaining_roles = ROLES

    output_lines = []
    for role in remaining_roles:
        output_lines.append(f"Tên: {role['name']}")
        output_lines.append(f"Mô tả vai trò của \"{role['name']}\": {role['description']}")
        output_lines.append("\n") 

    result = "\n".join(output_lines).strip()
    return result


def acts_stage(current_stage):
    for stage in STAGES:
        if current_stage == stage['stage']:
            formatted = ""
            for act in stage['acts']:
                formatted += f"- {act}\n"
            
            return formatted
        

# def history_for_manager(history, leader = "Bob", user_name="Khải"):
#     '''Thêm kí hiệu user người thật cho manager biết'''
#     if len(history) < 15:
#         empty = []
#         for i in range(len(PRE_HISTORY)):
#             empty.append(("", ""))

#         history = empty + history

#     formatted = []

#     for index, (speaker, msg) in enumerate(history):
#         if speaker == user_name:
#             formatted.append(f"{index}. {speaker} (học sinh thật): {msg}\n")
#         elif speaker == leader:
#             formatted.append(f"{index}. {speaker} (học sinh AI - nhóm trưởng): {msg}\n")
#         else:
#             formatted.append(f"{index}. {speaker} (học sinh AI): {msg}\n")

#     last = formatted[-15:]

#     return ''.join(last)


# def format_history(history, user_name="Khải"):
#     last = history[-15:]
#     formatted = ""
#     for index, (speaker, msg) in enumerate(last):
#         # if index == len(last) - 1:
#         #     formatted += "\n*Đây là tin nhắn mới nhất:\n"
#         if speaker == user_name:
#             formatted += f"{speaker}: {msg}\n"
#         else:
#             formatted += f"{speaker}: {msg}\n"
#     return formatted


# def format_history(history, user_name="Khải"):
#     # Nếu độ dài history nhỏ hơn 15, chèn PRE_HISTORY vào đầu
#     if len(history) < 15:
#         history = PRE_HISTORY + history

#     formatted = []

#     for index, (speaker, msg) in enumerate(history):
#         formatted.append(f"{index}. {speaker}: {msg}\n")

#     last = formatted[-15:]

#     return ''.join(last)


def format_history(history, user_name="Khải"):
    # Đánh số từ 1 cho hội thoại thật
    formatted_real = []
    for idx, (speaker, msg) in enumerate(history, start=1):
        formatted_real.append(f"{idx}. {speaker}: {msg}\n")

    formatted = [f"{speaker}: {msg}\n" for speaker, msg in PRE_HISTORY] + formatted_real

    # Lấy 15 tin nhắn mới nhất
    last = formatted[-15:]
    return ''.join(last)


def history_for_manager(history, leader="Bob", user_name="Khải"):
    '''Thêm ký hiệu user người thật cho manager biết'''
    formatted_real = []
    for idx, (speaker, msg) in enumerate(history, start=1):
        if speaker == user_name:
            formatted_real.append(f"{idx}. {speaker} (học sinh thật): {msg}\n")
        elif speaker == leader:
            formatted_real.append(f"{idx}. {speaker} (học sinh AI - nhóm trưởng): {msg}\n")
        else:
            formatted_real.append(f"{idx}. {speaker} (học sinh AI): {msg}\n")

    empty = []
    for i in range(len(PRE_HISTORY)):
        empty.append(("", ""))
    formatted = [f"{speaker}: {msg}\n" for speaker, msg in empty] + formatted_real

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
                result += f" Nhiệm vụ {idx + 1}: {item}\n"
                
            result += "- Các mục tiêu cần đạt được để kết thúc quá trình này:\n"
            for idx, item in enumerate(stage_goals):
                result += f" Mục tiêu {idx + 1}: {item}\n\n" 
            return result
        

def parse_json_lines(data_string):
    lines = data_string.strip().split("\n")
    result = []

    for line in lines:
        line = line.strip()
        if line:  
            try:
                obj = json.loads(line)
                result.append(obj)
            except json.JSONDecodeError as e:
                print(f"Error: {line}")
                print(e)
    return result



# def format_output_stage_controller(resp):
#     s = f"- Nhiệm vụ và mô tả mà nhóm đang thực hiện: {resp[0]['a']}\n"
#     s += f"- Trạng thái của nhiệm vụ:  {resp[1]['a']}\n"
#     s += f"- Mục tiêu kết hợp: {resp[2]['a']}\n"
#     return s

def format_output_stage_controller(resp):
    s = f"- Mô tả tình hình của lớp: {resp['explain']}.\n"
    s += f"- Nhóm nên \"{resp['signal'][1]}\" quá trình này.\n"
    return s



def format_output_AI_speaker_controller(resp):
    s = ""
    for i in resp:
        s += f"Tên : {i['name']}\n"

        for idx, thought in enumerate(i['inner_thought']):
            s += f"Đây là suy nghĩ của {i['name']}: \"{thought}\"\n"

        s += f"Đây là chỉ số của những tin nhắn trước đó ảnh hưởng tới suy nghĩ này: {i['ref']}:\n"
        s += '\n'
    return s


def parse_json(resp):
    return json.loads(resp.strip('```json').strip('\n```'))



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
