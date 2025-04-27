from utils import *

from pydantic import BaseModel, Field, ValidationError
from typing import Tuple, Union
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time

USER_NAME = "Khải"
AI_NAMES = ["Alice", "Bob", "Charlie"]
CURRENT_STAGE = "1"
STAGE = ["1", "2", "3", "4"]


# prompts = [
#         "Viết một đoạn văn ngắn mô tả về vẻ đẹp của Vịnh Hạ Long.",
#         "Sự khác biệt chính giữa học máy (machine learning) và học sâu (deep learning) là gì?",
#         "Tóm tắt nội dung chính của truyện 'Số đỏ' của Vũ Trọng Phụng."
# ]

# results = []

# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     futures = []
#     for p in prompts:
#         future = executor.submit(llm, prompt=p)
#         futures.append(future)


#     for future in concurrent.futures.as_completed(futures):
#         try:
#             result = future.result() 
#             results.append(result) 
#         except Exception as exc:
#             print(f'Một prompt tạo ra exception: {exc}')
#             results.append(f"Lỗi: {exc}")


HISTORY = [
    {
        "num" : "1",
        "name" : "Khải",
        "utterance" : '''Cho bài toán "Xét tính đơn điệu của hàm số $f(x) = \\frac{x-1}{x+1}$.". Nào bắt đầu cùng nhau giải bài này nào.''',
        "thoughts" : []
    }
]

# class StageResponse(BaseModel):
#     explain: str = Field(..., description="Giải thích về stage của nhóm")
#     signal: Tuple[str, str] = Field(..., description= "Tín hiệu của stage manager")

# class ErrorResponse(BaseModel):
#     error: str = Field(..., description="Mô tả lỗi xảy ra.")



# stage_prompt = prompt_STAGE_MANAGER(problem= PROBLEM,
#                                     current_stage_description= stage_description(CURRENT_STAGE),
#                                     history= format_history(HISTORY))
# stage = llm(stage_prompt)

# print("====== STAGE ======")
# print(parse_json(stage))
# print("===================")


# Nếu như event cuối cùng là user nói thì cả 3 agent đều suy nghĩ, nếu là Agent nói thì chỉ 3

list_AI_name = remaining_AI(HISTORY)
print(list_AI_name)


thoughts_prompt = []

for AI_name in list_AI_name:
    # previous_thoughts : lấy ra khoảng 3 previous

    # poor_thinking : chỉ số < 2.0 ở phần external

    thoughts_str, avg_motivation = previous_thoughts(AI_name, HISTORY, num=3)

    external_score = avg_motivation[1]
    poor_thinking = ""
    if external_score < 2.0 and len(HISTORY) > 1:
        # Gửi tín hiệu agent suy nghĩ không tốt
        poor_thinking = "Những suy nghĩ gần đây của bạn bị đánh giá kém, vì bạn thực hiện những hành động, lời nói LẶP LẠI nhiều lần mà KHÔNG giúp ích cho sự tham gia của các bạn học khác. Bạn cần lập tức thay đổi cách suy nghĩ cho đa dạng, phù hợp hơn."

    description, _ = AI_description(AI_name, ROLES)

    prompt = prompt_AGENT_INNER_THOUGTS(AI_name= AI_name,
                                        problem= PROBLEM,
                                        current_stage_description= stage_description(CURRENT_STAGE),
                                        AI_description = description,
                                        previous_thoughts= thoughts_str,
                                        history= format_history(HISTORY),
                                        poor_thinking = poor_thinking
                                        )
    
    thoughts_prompt.append((AI_name, prompt, avg_motivation))


thoughts_result = {}
future_to_task_info = {}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    for agent in thoughts_prompt:
        name = agent[0]
        prompt = agent[1]

        future = executor.submit(llm, prompt=prompt)
        future_to_task_info[future] = (name, prompt)

    for future in concurrent.futures.as_completed(future_to_task_info):
        name, prompt = future_to_task_info[future]

        try:
            result = future.result()
            thoughts_result[name] = parse_json(result)
        except Exception as exc:
            thoughts_result[name] = f"Error: {exc}"


for ai_name, result in thoughts_result.items():
    print(f"\nAI Name: {ai_name}")
    print(f"Kết quả: {result}")



evaluator_prompt = prompt_THOUGHTS_EVALUATOR(list_AI_name= list_AI_name,
                                             problem= PROBLEM,
                                             current_stage_description= stage_description(CURRENT_STAGE),
                                             history= format_history(HISTORY),
                                             AI_thoughts= format_AI_thoughts(thoughts_result=thoughts_result))



# print(evaluator_prompt)


evaluator = llm(evaluator_prompt)
# print(evaluator)
evaluator = parse_json(evaluator)
print(evaluator)

# [{'name': 'Bob', 'internal_score': '3.8', 'external_score': '4.2'}, {'name': 'Charlie', 'internal_score': '3.5', 'external_score': '3.7'}, {'name': 'Alice', 'internal_score': '3.5', 'external_score': '3.7'}]



# Cập nhật history u_i sau, se return về cùng hàm AI_talk()

# Chọn người điểm cao nhất, tuy nhiên dựa vào số lượt agent đó bao lấu chưa tương tác (theta)^num ; theta = 1.01
next_speaker = max(
    evaluator,
    key=lambda x: (float(x['internal_score']) + float(x['external_score'])) / 2
)['name']

print("next speaker: ", next_speaker)

_, info = AI_description(next_speaker, ROLES)
friends= "\n".join(f"- {role['name']}" for role in ROLES if role["name"] != next_speaker)


classmate_prompt = prompt_CLASSMATE_SPEAK(AI_name= next_speaker,
                                          AI_role= info[0],
                                          AI_goal= info[1],
                                          AI_backstory= info[2],
                                          AI_tasks= info[3],
                                          problem= PROBLEM,
                                          friends= friends,
                                          current_stage_description= stage_description(CURRENT_STAGE),
                                          inner_thought= thoughts_result[next_speaker]['thought'],
                                          to_user= analysis_user(HISTORY),
                                          history= format_history(HISTORY)
                                          )


print(classmate_prompt)

classmate_speak = llm(classmate_prompt)

print(classmate_speak)



