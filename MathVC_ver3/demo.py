from prompts import *
from utils import *
from AI_talk import *

import copy

USER_NAME = "Khải"
AI_NAMES = ["Alice", "Bob", "Charlie"]
CURRENT_STAGE = "1"
STAGE = ["1", "2", "3", "4"]


HISTORY = [
    {
        "num" : 1,
        "name" : "Khải",
        "utterance" : '''Cho bài toán "Xét tính đơn điệu của hàm số $f(x) = \\frac{x-1}{x+1}$.". Nào bắt đầu cùng nhau giải bài này nào.''',
        "thoughts": None
    }
]


'''
{"name" : next_speaker,
            "speak" : classmate_speak,
            "thoughts" : thoughts_result,
            "evaluator" : evaluator,
            "stage" : stage}
'''



def run_conversation():
    global HISTORY, CURRENT_STAGE

    print("Bắt đầu cuộc hội thoại:")
    print_history(HISTORY, CURRENT_STAGE)
    # time.sleep(1)

    max_turns = 150
    turn_count = 0

    while turn_count < max_turns:
        turn_count += 1
        print(f"====== Lượt {turn_count} ======")

        if not HISTORY:
             print("Lỗi: Lịch sử trống!")
             break
        
        last_speaker = HISTORY[-1]['name']



        # Human nói cuối
        if last_speaker == USER_NAME:

            ai_response = AI_talk(HISTORY, CURRENT_STAGE)

            # cập nhật history
            HISTORY = update_history(ai_response, HISTORY)

            # CẬP NHẬT STAGE:
            next_stage = "no"
            if ai_response["stage"]['signal'][0] == "4":
                next_stage = "yes"

            if next_stage == "yes":
                try:
                    current_index = STAGE.index(CURRENT_STAGE)
                    if current_index < len(STAGE) - 1:
                        CURRENT_STAGE = STAGE[current_index + 1]
                        print(f"*** Chuyển sang giai đoạn {CURRENT_STAGE} ***\n")
                    else:
                        print("*** Đã ở giai đoạn cuối cùng ***\n")
                except ValueError:
                     print(f"Lỗi: Không tìm thấy giai đoạn {CURRENT_STAGE} trong danh sách STAGE.\n")
            
            # In lịch sử cập nhật
            print(f"\n>> {ai_response['name']} nói:")
            print_history(HISTORY, CURRENT_STAGE)

        elif last_speaker in AI_NAMES:

            # trigger có phải Human nói không

            # Thử nghiệm mặc định là để Both - cả 2 type có thể nói.
            controller_decision = {"Explain" : "", "Speaker" : "Both"}

            next_speaker_type = controller_decision.get("Speaker", "AI")
            explanation = controller_decision.get("Explain", "(Không có giải thích)")
            print(f"Người nói tiếp theo: {next_speaker_type}")


            if next_speaker_type == "Human":
                 pass
            elif next_speaker_type == "AI":
                pass
            elif next_speaker_type == "Both":
                print(f"\n>> Lượt của user (hoặc AI nếu bạn bỏ qua).")
                action = input("Bạn có muốn nói không? Nhập 'y' để nói, nhấn Enter (hoặc nhập gì khác) để bỏ qua: ").strip().lower()

                if action == "y":
                    user_input = ""
                    while not user_input.strip():
                        user_input = input("Nhập lời nói của bạn: ")
                        if not user_input.strip():
                             print("Vui lòng nhập nội dung.")
                    

                    HISTORY.append({"num" : HISTORY[-1]['num'] + 1,
                            "name" : USER_NAME,
                            "utterance" : user_input,
                            "thoughts" : None})
                    
                    print_history(HISTORY, CURRENT_STAGE)

                else:
                    print(f"[{CURRENT_STAGE}] {USER_NAME} bỏ qua. Để AI nói...")
                    ai_response = AI_talk(HISTORY, CURRENT_STAGE) 

                    HISTORY = update_history(ai_response, HISTORY)

                    # CẬP NHẬT STAGE:
                    next_stage = "no"
                    if ai_response["stage"]['signal'][0] == "4":
                        next_stage = "yes"

                    if next_stage == "yes":
                        try:
                            current_index = STAGE.index(CURRENT_STAGE)
                            if current_index < len(STAGE) - 1:
                                CURRENT_STAGE = STAGE[current_index + 1]
                                print(f"*** Chuyển sang giai đoạn {CURRENT_STAGE} ***\n")
                            else:
                                print("*** Đã ở giai đoạn cuối cùng ***\n")
                        except ValueError:
                            print(f"Lỗi: Không tìm thấy giai đoạn {CURRENT_STAGE} trong danh sách STAGE.\n")
                    
                    # In lịch sử cập nhật
                    print(f"\n>> {ai_response['name']} nói:")
                    print_history(HISTORY, CURRENT_STAGE)
            else:
                print(f"Lỗi: Loại người nói không xác định từ Controller '{next_speaker_type}'. Dừng demo.")
                break


        else:
            print(f"Lỗi: Người nói cuối cùng không xác định '{last_speaker}'. Dừng demo.")
            break

        time.sleep(1)

    print(f"\n--- CUỘC HỘI THOẠI KẾT THÚC (Đạt giới hạn {max_turns} lượt) ---")
    print("Lịch sử cuối cùng:")
    print_history(HISTORY, CURRENT_STAGE)


# --- Chạy chương trình ---
if __name__ == "__main__":
    run_conversation()


            













