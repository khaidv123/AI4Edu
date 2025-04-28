# TODO : Những thứ cần xem xét, điều chỉnh.

## Trigger module
1. Có cần thêm prompt xác định isOnlyHuman? Nếu lượt Agent A nói có thể vẫn chạy hệ thống cho agent inner thought nhưng mong muốn họ sẽ trả về listen.
2. 

## Improve FUNC, Task of agent
1. Chia các FUNC#id thành các acts riêng biệt, khi thực hiện inner_thought thì chọn act để suy nghĩ dựa trên đó
2. Có cần placeholder {tasks} của agent vào?

## Improve Inner thought module
1. Tune persona-based prompting --> role và persona (backstory) để kiểm tra tác động đến cách suy nghĩ
2. Nếu chỉ dựa trên các agent lựa chọn "speak" thì sẽ chấm (evaluator) như thế nào:
    - Tất cả muốn nói (>= 2 agents) --> evaluator chấm để lựa chọn. --> vẫn cập nhật được score như thường.
    - Chỉ 1 người muốn nói --> evaluator vẫn chấm.
    - Không một ai muốn nói. Nếu tin nhắn mới nhất đang chỉ định trực tiếp đến Human --> hợp lý; Nếu là agent thì không ai nói hơi nguy hiểm (silence pause trigger).





