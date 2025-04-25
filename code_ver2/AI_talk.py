from concurrent.futures import ThreadPoolExecutor

from utils import *

PROBLEM = """Xét tính đơn điệu của hàm số $f(x) = \frac{x-1}{x+1}$."""


def AI_talk(HISTORY, CURRENT_STAGE):


    # Xác định một số AI có thể tham gia và một số act có thể làm
    prompt1 =  prompt_AI_Speaker_Controller(remaining_AI_roles = remaining_AI(HISTORY),
                                            current_stage= stage_description(CURRENT_STAGE),
                                            stage_act= acts_stage(CURRENT_STAGE),
                                            history_for_manager= history_for_manager(HISTORY))

    # Phân tích quá trính hiện tại của cả nhóm
    prompt2 = prompt_Stage_Controller(problem = PROBLEM,
                                    current_stage = stage_description(CURRENT_STAGE),
                                    history_for_manager= history_for_manager(HISTORY))
    
    # parallel
    def run_in_parallel():
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(llm, prompt1)
            future2 = executor.submit(llm, prompt2)
            res1 = future1.result()
            res2 = future2.result()
        return res1, res2
    
    res1, res2 = run_in_parallel()

    # time.sleep(1)
    # print(res2)

    res1 = parse_json_lines(res1)
    res2 = parse_json(res2)

    print("====== AI_Speaker_Controller =======")
    print(res1)

    print("====== Stage_Controller =======")
    print(res2)

    # Chọn ra AI và act tốt nhất
    prompt3= prompt_verifier(current_stage = stage_description(CURRENT_STAGE),
                         output_from_stage_controller= format_output_stage_controller(res2),
                         history_for_manager= history_for_manager(HISTORY),
                         output_from_ai_speaker_controller= format_output_AI_speaker_controller(res1))
    
    res3 = llm(prompt3)
    res3 = parse_json(res3)

    # print(res3)

    # next_speaker = res3['name']
    # act = res3['act']
    # Ai_role = next(role["description"] for role in ROLES if role["name"] == next_speaker)
    # friends= "\n".join(f"- {role['name']}" for role in ROLES if role["name"] != next_speaker)

    next_speaker = res3['name']
    Ai_role = next(role["description"] for role in ROLES if role["name"] == next_speaker)
    friends= "\n".join(f"- {role['name']}" for role in ROLES if role["name"] != next_speaker)


    thought = [item['inner_thought'] for item in res1 if item['name'] == next_speaker][0]
    ref = next((item['ref'] for item in res1 if item['name'] == next_speaker), [])
    last = len(HISTORY)
    ref = [last] + ref
    act = thought


    print("====== verifier =======")
    print(res3)
    print(f"tên : {next_speaker}, inner_thought: {thought}")
    print(f"tên : {next_speaker}, ref: {ref}")

    time.sleep(1)


    # AI talk
    prompt_agent = prompt_Classmate_Agent(AI_name= next_speaker,
                                      AI_role= Ai_role,
                                      problem= PROBLEM,
                                      friends= friends,
                                      output_from_stage_controller= format_output_stage_controller(res2),
                                      current_stage= stage_description(CURRENT_STAGE),
                                      history= format_history(HISTORY),
                                      to_user= analysis_user(HISTORY),
                                      act = act,
                                      ref = ref)
    
    # print("promt agent")
    # print(prompt_agent)
    
    res_agent = llm(prompt_agent)

    print(f"====== agent {next_speaker}: =======")
    print(res_agent)

    print(f"====== CURRENT_STAGE: =======")
    print(CURRENT_STAGE)
    print("==============================")

    next_stage = "no"
    if res2['signal'][0] == "4":
        next_stage = "yes"
        
    return {"name" : next_speaker, "talk" : res_agent, "stage" : next_stage}