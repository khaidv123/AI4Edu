from prompts import *
from utils import *
from AI_talk import *

USER_NAME = "Khải"
AI_NAMES = ["Alice", "Bob", "Charlie"]
CURRENT_STAGE = "1"
STAGE = ["1", "2", "3", "4"]


# vào stage 1:
# HISTORY = [
#     ("Khải", '''Cho bài toán \"Xét tính đơn điệu của hàm số $f(x) = \frac{x-1}{x+1}$.\". Nào bắt đầu cùng nhau giải bài này nào.'''),
# ]

# vào stage 2:

HISTORY = [
    ("Khải", '''Cho bài toán "Xét tính đơn điệu của hàm số $f(x) = \\frac{x-1}{x+1}$.". Nào bắt đầu cùng nhau giải bài này nào.'''),
]


HISTORY_TEST_1 = [
    ("Khải", '''Cho bài toán "Xét tính đơn điệu của hàm số $f(x) = \\frac{x-1}{x+1}$.". Nào bắt đầu cùng nhau giải bài này nào.'''),
    ("Bob", '''Để bắt đầu, chúng ta cần xác định rõ bài toán cho những gì, đâu là ẩn số, dữ liệu và điều kiện đã cho. Mọi người cùng nhau làm rõ phần này nhé!'''),
    ("Khải", '''okok'''),
    ("Charlie", '''Khải nói chuẩn luôn! Cứ từ từ mà tiến, ai có ý gì cứ thoải mái chia sẻ nha. Tớ nghĩ mình nên bắt đầu làm rõ những cái Bob vừa nói đi.'''),
    ("Alice", '''"Ẩn số" ở đây chắc không phải là đi tìm kho báu bị chôn vùi đâu ha? Chắc chỉ là tìm xem hàm số này "lúc lên lúc xuống" ở đâu thôi nhỉ?'''),
    ("Khải", '''thì bài toán yêu cầu tìm khoảng đơn điệu của hàm số mà'''),
    ("Bob", '''Đúng vậy Khải, bài này đích thị là dạng toán xét tính đơn điệu của hàm số bậc nhất trên bậc nhất rồi.'''),
    ("Alice", '''Ủa mà khoan, trước khi "lên đường" tìm hiểu "lúc lên lúc xuống" của hàm số, có ai quên mang "bản đồ" đạo hàm không? Không nhớ đạo hàm thì coi như lạc đường đó nha! *nháy mắt*'''),
    ("Bob", '''Alice nhắc đến đạo hàm chuẩn luôn! Để làm bài này, mình cần nhớ lại định nghĩa về tính đơn điệu và liên hệ giữa đạo hàm với tính đơn điệu nữa. Mọi người còn nhớ không?'''),
    ("Charlie", '''Đúng rồi đó Alice và Bob! Để làm bài này, mình cần "combo" kiến thức về đạo hàm và định nghĩa đơn điệu đó! Ai xung phong nhắc lại định nghĩa không?'''),
    ("Khải", '''Charlie nói thử phần định nghĩa đơn điệu đi'''),
    ("Charlie", '''Đơn điệu là xét xem hàm số đồng biến hay nghịch biến trên một khoảng K nào đó. Tức là xét xem nó "lúc lên" hay "lúc xuống" đó. Ai nhớ rõ hơn thì bổ sung thêm nha!'''),
    ("Khải", '''bạn có thể nói một cách toán học hơn được không'''),
    ("Bob", '''Đúng là cần chính xác hơn! Định nghĩa đơn điệu cần xét với mọi $x_1, x_2$ thuộc K. Nếu $x_1 < x_2$ mà $f(x_1) < f(x_2)$ thì hàm đồng biến. Còn $f(x_1) > f(x_2)$ thì hàm nghịch biến.'''),
    ("Charlie", '''Khải ơi, để dễ hình dung, mình cứ tưởng tượng đồ thị hàm số như một con dốc đi! Đồng biến là "lên dốc", nghịch biến là "xuống dốc" đó.'''),
    ("Khải", '''ok hiểu rồi'''),
    ("Bob", '''Khải hiểu rồi thì tốt! Thế còn liên hệ giữa đạo hàm và tính đơn điệu thì sao nhỉ? Nếu đạo hàm dương trên một khoảng thì hàm số sẽ như thế nào trên khoảng đó?'''),
    ("Khải", '''nó sẽ nghịch biến'''),
    ("Bob", '''Khải ơi, hình như có chút nhầm lẫn rồi! Đạo hàm dương thì hàm số đồng biến chứ không phải nghịch biến nha.'''),
    ("Khải", '''à okok mình nhầm'''),
    ("Bob", '''Đúng rồi đó Khải! Đạo hàm dương thì hàm số đồng biến, còn đạo hàm âm thì hàm số nghịch biến. Để chắc chắn, Khải nhắc lại giúp mình liên hệ giữa đạo hàm và tính đơn điệu được không?'''),
    ("Charlie", '''Khải ơi, đừng lo lắng quá! Mình nghĩ thế này, ví dụ vận tốc của xe luôn dương thì quãng đường đi được tăng lên, tức là đồng biến đó!'''),
    ("Khải", '''à ok mình hiểu rồi nếu đạo hàm dương thì hàm số đồng biến và ngược lại'''),
    ("Charlie", '''Khải ơi, không sao đâu, chuyện nhầm lẫn là bình thường mà!\nĐể dễ nhớ, mình lấy ví dụ khác nhé: Nếu vận tốc của một vật luôn dương, thì quãng đường đi được sẽ tăng lên, tức là hàm số đồng biến đó! Tương tự, vận tốc âm thì quãng đường giảm, hàm nghịch biến.'''),
    ("Khải", '''sao mà vận tốc âm được :))'''),
    ("Alice", '''Khải ơi, vận tốc âm kiểu như em đi bộ lùi trên băng chuyền siêu thị đó! Em vẫn đang di chuyển, nhưng so với "mặt đất" thì em đang đi ngược lại!'''),
    ("Khải", '''ò ok được rồi tiếp đi'''),
    ("Bob", '''Khải ơi, để chắc chắn, bạn có thể phát biểu lại chính xác liên hệ giữa đạo hàm và tính đơn điệu không?'''),
    ("Khải", '''nếu đạo hàm âm thì hàm số nghịch biến và ngược lại'''),
    ("Bob", '''Khải nắm chắc kiến thức rồi đó! Vậy giờ mình chuyển sang bước tiếp theo nhé? Mọi người thấy sao?'''),
    ("Charlie", '''Khải đỉnh thật! Nắm vững kiến thức rồi đó. Mình nghĩ giờ mình bắt đầu làm bài tập luôn đi Bob nhỉ? Alice thấy sao?'''),
    ("Alice", '''Ngoài cách dùng đạo hàm, mình nghĩ bài này có thể khảo sát trực tiếp bằng định nghĩa được không nhỉ? Hoặc là dùng tính chất của hàm phân thức bậc nhất trên bậc nhất?'''),
    ("Charlie", '''Alice ơi, mình thấy ý tưởng khảo sát trực tiếp bằng định nghĩa cũng hay đó! Bạn có thể nói rõ hơn về cách làm của bạn được không? Mình muốn nghe thêm về nó!'''),
    ("Alice", '''Ừm, ý mình là xét $x_1 < x_2$, sau đó so sánh $f(x_1)$ và $f(x_2)$ xem cái nào lớn hơn đó mà!'''),
    ("Bob", '''Alice và Charlie có ý tưởng hay đó! Để hệ thống lại, mình nhắc lại nhiệm vụ của nhóm là đề xuất các phương pháp giải bài này nhé. Theo mình thì dùng đạo hàm là cách phổ biến nhất, mọi người thấy sao?'''),
    ("Khải", '''uh mình biết cách đấy thôi'''),
    ("Bob", '''Mình thấy Khải cũng quen với cách dùng đạo hàm rồi. Vậy mình thống nhất dùng đạo hàm nha. Mọi người có ai có ý kiến gì khác không?'''),
    ("Alice", '''Mình nghĩ còn một cách nữa là sử dụng phép biến đổi đại số để đưa về dạng dễ khảo sát hơn, mọi người thấy sao?'''),
    ("Khải", '''là sao'''),
    ("Alice", '''Khải ơi, để tớ giải thích rõ hơn nhé! $f(x) = \\frac{x-1}{x+1} = \\frac{x+1-2}{x+1} = 1 - \\frac{2}{x+1}$. Đến đây bạn thấy gì không?'''),
    ("Khải", '''mình chưa hiểu lắm'''),
    ("Alice", '''Đến đây, Khải thấy là khi $x$ tăng thì $x+1$ tăng, kéo theo $\\frac{2}{x+1}$ giảm, nên $-\\frac{2}{x+1}$ tăng, cuối cùng $1 - \\frac{2}{x+1}$ cũng tăng đó!'''),
    ("Khải", '''thì sao'''),
    ("Charlie", '''Khải ơi, Alice biến đổi hay thật! Chỗ biến đổi $\\frac{x-1}{x+1} = \\frac{x+1-2}{x+1}$ là một kỹ thuật tách phân số đó, bạn xem lại kiến thức cũ nha!'''),
    ("Khải", '''cách này hơi khó với tớ'''),
    ("Bob", '''Khải ơi, bạn đang gặp khó khăn ở chỗ nào vậy? Để Alice giảng lại cho bạn chỗ đó nha!'''),
    ("Khải", '''mình nghĩ vẫn nên dùng đạo hàm'''),
    ("Bob", '''Mình thấy cách của Alice cũng khá hay, nhưng mà hơi khó nhìn ra ngay. Với lại, không phải bài nào cũng biến đổi được như vậy. Dùng đạo hàm có vẻ tổng quát hơn nhỉ?'''),
    ("Alice", '''Tớ thấy dùng đạo hàm thì tổng quát hơn thật, đỡ phải "nhìn hình đoán ý" như cách của tớ. Với lại, đạo hàm còn dùng được cho nhiều hàm phức tạp khác nữa!'''),
    ("Khải", '''uh thế dùng đạo hàm nhá'''),
    ("Bob", '''Vậy là mình thống nhất dùng đạo hàm để giải bài này nha. Cách của Alice hay nhưng hơi khó nhìn ra. Giờ mình bắt đầu tính đạo hàm rồi xét dấu nha?'''),
    ("Khải", '''okok'''),
    ("Charlie", '''Tuyệt vời! Vậy cả nhóm mình thống nhất dùng đạo hàm nha. Giờ mình bắt tay vào làm thôi! Chia việc ra cho nhanh nào!'''),
    ("Khải", '''ok làm thôi'''),
    ("Charlie", '''Khải xung phong tính đạo hàm đi, tớ nghĩ bạn làm được đó! Nếu cần giúp đỡ cứ hú tớ một tiếng nhé!'''),
    ("Khải", '''uh, tớ nháp ra được thì có f'(x) = 2x/(x+1)^2'''),
    ("Alice", '''Khải ơi, tớ thấy đạo hàm của bạn có vẻ chưa đúng lắm. Bạn kiểm tra lại công thức tính đạo hàm của $\\frac{u}{v}$ xem sao nhé!'''),
    ("Khải", '''thế à bạn ra bao nhiêu'''),
    ("Alice", '''Tớ ra $f'(x) = \\frac{2}{(x+1)^2}$. Khải xem lại công thức đạo hàm của phân thức $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$ nha. Tử của bạn đang bị sai đó!'''),
    ("Khải", '''à okok rồi'''),
    ("Bob", '''Khải ơi, bạn tính lại đạo hàm đi nhé. Có cần tớ nhắc lại công thức tính đạo hàm không?'''),
    ("Khải", '''u tớ bị nhầm, tớ tính lại rồi'''),
    ("Alice", '''Khải tính lại đạo hàm rồi hả? Cho tớ xin kết quả mới với, xem có giống của tớ không!'''),
    ("Bob", '''Khải ơi, đạo hàm mới của bạn ra bao nhiêu rồi? Để Alice kiểm tra cho chắc chắn nè. Sau khi có đạo hàm rồi, mình xét dấu của nó nha!'''),
    ("Khải", '''tớ bảo ra giống Alice mà'''),
    ("Alice", '''Vậy là Khải ra đạo hàm giống tớ rồi đúng không? $f'(x) = \\frac{2}{(x+1)^2}$. Để chắc chắn, Khải có thể trình bày cách tính nhanh để mọi người cùng xem lại không?'''),
    ("Khải", '''thì áp dụng công thức thôi, tại tớ bị nhầm dấu trên tử'''),
    ("Alice", '''Khải ơi, bạn trình bày cách tính đạo hàm cụ thể đi. Tớ muốn xem bạn áp dụng công thức như thế nào để chắc chắn là không còn sai sót nữa!'''),
    ("Khải", '''f' = 1(x+1) - (x-1).1/(x+1)^2 = 2/(x+1)^2'''),
    ("Alice", '''Oke Khải, cách tính của bạn ổn rồi đó! Mẫu số $(x+1)^2$ luôn dương với mọi $x \\neq -1$, tử số là 2 cũng dương. Vậy đạo hàm $f'(x)$ luôn dương trên tập xác định.'''),
    ("Bob", '''Đạo hàm ngon rồi Khải! Giờ mình xét dấu $f'(x)$ và kết luận về khoảng đồng biến, nghịch biến của hàm số thôi.'''),
    ("Khải", '''uh hàm số luôn đồng biến trên R'''),
    ("Alice", '''Khải ơi, hàm số đồng biến trên $\\mathbb{R}$ là chưa chính xác đâu. Mình cần loại điểm $x = -1$ ra nữa nhé!'''),
    ("Khải", '''à đúng rồi'''),
    ("Bob", '''Khải ơi, hàm số không xác định tại $x = -1$ nên không thể nói đồng biến trên $\\mathbb{R}$ được. Phải là trên $(-\\infty; -1)$ và $(-1; +\\infty)$ nhé!'''),
    ("Khải", '''okok hiểu rồi'''),
    ("Bob", '''Đúng rồi Khải, hàm số đồng biến trên $(-\\infty; -1)$ và $(-1; +\\infty)$. Nhớ loại bỏ điểm không xác định $x = -1$ nha!'''),
    ("Khải", '''ok'''),
    ("Bob", '''Khải ơi, để trực quan hơn, bạn thử vẽ bảng biến thiên của hàm số này xem sao? Như vậy sẽ thấy rõ hơn khoảng đồng biến và nghịch biến đó!'''),
    ("Khải", '''ở vẽ ở đây hơi lâu với khó, có ai vẽ thử cho tớ để so sánh không'''),
    ("Charlie", '''Khải ơi, đừng ngại! Vẽ tay ra giấy rồi chụp ảnh gửi lên cũng được mà. Bảng biến thiên giúp mình nhìn rõ hơn đó! Cố lên!'''),
    ("Khải", '''uh vậy Charlie cho tớ xem kết quả của bạn đi, với lại từng bước bạn vẽ nữa'''),
    ("Charlie", '''Ok Khải, để tớ gửi bảng biến thiên của tớ nhé. Tớ chụp ảnh gửi lên đây nha.\n\n| $x$    | $-\\infty$ |       $-1$       | $+\\infty$ |\n| :------- | :-------: | :----------------: | :-------: |\n| $f'(x)$ |    $+$    |          $\\|$          |    $+$    |\n| $f(x)$  |     1 $\\nearrow$  $+\\infty$     | $\\|$  |    $-\\infty$ $\\nearrow$  1 |'''),
    ("Khải", '''ủa cậu vẽ khó nhìn quá, vẽ lại đi'''),
    ("Bob", '''Khải ơi, bảng biến thiên của Charlie nhìn hơi rối thật. Để dễ nhìn hơn, bạn nên thêm giới hạn của $f(x)$ khi $x$ tiến đến $-1$ và $\\pm \\infty$ vào nhé, với cả vẽ mũi tên cho đúng chiều nữa!'''),
    ("Khải", '''Bob show bảng biến thiên của bạn đi'''),
    ("Bob", '''Đây là bảng biến thiên chi tiết hơn nè Khải. Tớ thêm chú thích để bạn dễ theo dõi nhé!\n\n| $x$    | $-\\infty$ |       $-1$       | $+\\infty$ |\n| :------- | :-------: | :----------------: | :-------: |\n| $f'(x)$ |    $+$    |          $\\|$          |    $+$    |\n| $f(x)$  |     1 $\\nearrow$  $+\\infty$     | $\\|$  |    $-\\infty$ $\\nearrow$  1 |\n\nTrong đó:\n$\\lim_{x \\to -1^+} f(x) = -\\infty$; $\\lim_{x \\to -1^-} f(x) = +\\infty$\n$\\lim_{x \\to +\\infty} f(x) = 1$; $\\lim_{x \\to -\\infty} f(x) = 1$'''),
    ("Khải", '''à okok rồi giống tớ rồi'''),
    ("Charlie", '''Tuyệt vời Khải! Giống Bob rồi là đúng hướng đó. Cố lên, sắp xong rồi!'''),
    ("Khải", '''còn làm gì nữa không nhỉ'''),
    ("Bob", '''Khải ơi, để chắc chắn, bạn giải thích lại tại sao hàm số đồng biến trên $(-\\infty; -1)$ và $(-1; +\\infty)$ được không?'''),
    ("Khải", '''thì đạo hàm của chúng luôn >0 với mọi x khác -1'''),
    ("Alice", '''Ơ Khải, đạo hàm lúc nào cũng dương, thế thì hàm số này có "vui vẻ" quá không? Haha! Ý tớ là, mình có cần xét thêm điều kiện gì nữa không nhỉ?'''),
    ("Khải", '''tớ nghĩ là không :)))'''),
    ("Bob", '''Khải ơi, vậy kết luận cuối cùng của bài này là gì nhỉ? Với cả, theo bạn thì phương pháp dùng đạo hàm để xét tính đơn điệu này có hiệu quả không?'''),
    ("Khải", '''Hàm số đồng biến trên R/{-1} và mình thấy cách này khá dễ làm, nhớ công thức là được'''),
    ("Alice", '''Khải ơi, hình như tập xác định của hàm số này không phải là R/{-1} đâu nhỉ? Mình có cần xem lại chỗ này không?'''),
    ("Khải", '''ở tớ kết luận thế không được à'''),
    ("Bob", '''Khải ơi, tập xác định $D = \\mathbb{R} \\setminus \\{-1\\}$ là đúng rồi, nhưng kết luận về khoảng đồng biến cần chính xác hơn nhé!'''),
    ("Khải", '''thì 2 cái có gì khác nhau, đều bỏ -1 đi mà'''),
    ("Alice", '''Khải ơi, tập xác định là nơi hàm số "sống", còn khoảng đồng biến là nơi nó "vui vẻ" đi lên. Hai cái này khác nhau đó nha!'''),
    ("Khải", '''????'''),
    ("Charlie", '''Khải ơi, cứ tưởng tượng tập xác định là cái nhà, còn khoảng đồng biến là con đường đi dạo. Nhà có thể to, nhưng đường đi dạo phải liền mạch, không đứt quãng!'''),
    ("Khải", '''thôi bạn giải thích theo toán học vì sao mình không thể kết luận như thế đi'''),
    ("Bob", '''Khải ơi, để tớ giúp bạn hiểu rõ hơn nhé. Khoảng đồng biến là khoảng mà hàm số liên tục và đạo hàm dương trên khoảng đó. Còn tập xác định chỉ là điều kiện để hàm số có nghĩa thôi!'''),
    ("Khải", '''vậy là mình phải chia ra để kết luận đồng biến à'''),
    ("Bob", '''Khải ơi, mục tiêu của bài này là xét tính đơn điệu của hàm số. Bạn đã hiểu rõ vì sao phải chia khoảng đồng biến chưa? Nếu chưa thì mình cùng thảo luận tiếp nhé!'''),
    ("Khải", '''ok rồi vậy bài này xong rồi đúng không'''),
    ("Bob", '''Khải ơi, bạn giải thích lại tại sao không được kết luận hàm số đồng biến trên $\\mathbb{R} \\setminus \\{-1\\}$ cho cả nhóm cùng hiểu đi!'''),
    ("Khải", '''vì kết luận đồng biến thì phải liên tục'''),
    ("Bob", '''Khải nói đúng rồi đó, hàm số đồng biến thì phải liên tục. Nhưng mà, tập xác định của hàm số này có bị gián đoạn tại x = -1. Nên mình không thể kết luận như vậy được!'''),
    # Kết thúc
    ("Charlie", '''Khải đỉnh quá! Để chắc chắn, Khải tóm tắt lại các bước làm bài này cho cả nhóm mình cùng nắm vững luôn đi!'''),
    ("Khải", '''Đạo hàm, xét dấu, vẽ bảng biến thiên và kết luận'''),
    ("Bob", '''Khải tóm tắt ngắn gọn quá! Bạn có thể nói rõ hơn về từng bước được không? Ví dụ, sau khi đạo hàm xong thì mình làm gì tiếp theo?'''),
    ("Khải", '''thì xét dấu của nó xem âm hay dương'''),
    ("Bob", '''Khải mới tóm tắt vắn tắt quá. Để mọi người dễ hình dung, Khải có thể diễn giải chi tiết hơn từng bước được không?'''),
    ("Khải", '''ơ giải xong bài rồi đây'''),
    ("Bob", '''Khải ơi, tóm tắt của bạn vẫn còn hơi chung chung. Bạn có thể nói rõ hơn về từng bước, đặc biệt là sau khi xét dấu đạo hàm thì mình làm gì tiếp theo không?'''),
    ("Khải", '''thế không phải là xét dấu của đạo hàm à'''),
    ("Bob", '''Khải ơi, mình đang muốn cả nhóm nắm vững cách làm dạng này. Bạn có thể trình bày chi tiết hơn các bước làm bài này được không? Mục tiêu của mình là rút ra cách làm tổng quát cho dạng bài này đó!'''),
    ("Khải", '''thôi bạn nói đi'''),
    ("Bob", '''Để mình tóm tắt lại nhé: Đầu tiên tìm tập xác định, tính đạo hàm, xét dấu đạo hàm, lập bảng biến thiên, rồi kết luận. Mọi người thấy ổn không?'''),
    ("Khải", '''à mình thiếu bước tìm điều kiện à'''),
    ("Bob", '''Mình thấy Khải nhắc đến tìm điều kiện là đúng rồi đó. Theo mọi người, bước "lập bảng biến thiên" có cần nói rõ hơn không nhỉ?'''),
    ("Charlie", '''Khải siêu thật! Nhớ ra bước tìm điều kiện quan trọng ghê. Theo tớ, bảng biến thiên cần làm rõ hơn đó. Khải có thể giúp nhóm mình phần này không?'''),
    ("Bob", '''Đúng rồi đó Charlie, bảng biến thiên quan trọng lắm! Để chắc chắn, mình nhắc lại: tìm tập xác định, tính đạo hàm, xét dấu đạo hàm, lập bảng biến thiên và cuối cùng là kết luận. Khải giúp nhóm mình làm rõ hơn bước lập bảng biến thiên được không?'''),
    ("Khải", '''thì cứ vẽ thôi'''),
    ("Bob", '''Khải ơi, "cứ vẽ thôi" nghe hơi đơn giản quá! Trong bảng biến thiên mình cần thể hiện những thông tin gì nhỉ? Bạn có thể nói rõ hơn không?'''),
    ("Khải", '''điểm cho đạo hàm bằng 0, rồi kẻ mấy đường đồng biến, nghịch biến'''),
    ("Bob", '''Khải ơi, mấy đường đồng biến, nghịch biến đó có ý nghĩa gì trong việc kết luận về tính đơn điệu của hàm số nhỉ?'''),
    ("Khải", '''đi lên thì đồng biến, xuống dưới thì nghịch biến'''),
    ("Charlie", '''Khải ơi, "đi lên thì đồng biến, xuống dưới thì nghịch biến" đúng rồi đó! Nhưng mà sao mình biết chỗ nào đi lên, chỗ nào đi xuống nhỉ? Giải thích thêm đi!'''),
    ("Bob", '''Tóm lại, mình có các bước: tìm tập xác định, tính đạo hàm, xét dấu đạo hàm, lập bảng biến thiên, kết luận. Còn thiếu gì không mọi người?'''),
    ("Alice", '''Tóm lại là, đầu tiên phải dò xem "em nó" sống ở đâu (tập xác định), sau đó "vặn" em nó (tính đạo hàm), rồi xem "em nó" thích "âm" hay "dương" (xét dấu), cuối cùng mới vẽ vời kết luận!'''),
    ("Khải", '''ok đã hiểu'''),
    ("Bob", '''Khải hiểu rồi, vậy Alice và Charlie có chỗ nào chưa rõ không? Cần mình giảng lại chỗ nào không?'''),
    ("Charlie", '''Khải đỉnh quá! Tớ thấy cách tóm tắt của cậu dễ hiểu thật đó. Hay là cậu thử nói rõ hơn về từng bước một xem sao, kiểu như là mình cần làm gì ở mỗi bước ấy?'''),
    ("Khải", '''thôi mình hiểu bài rồi'''),
    ("Bob", '''Vậy là Khải hiểu rồi, tốt quá! Để cả nhóm mình cùng nắm chắc, Alice và Charlie thử tóm tắt lại các bước giải xem sao?'''),
    ("Alice", '''Tóm lại vầy nè, đầu tiên mình tìm "quỹ đạo" của hàm số (tập xác định), rồi "chọc ngoáy" xem nó có điểm gì đặc biệt (tính đạo hàm), sau đó "đo" xem nó "nóng" hay "lạnh" (xét dấu), cuối cùng "vẽ vời" ra kết luận! Nghe có vẻ hơi "tào lao" nhưng dễ nhớ đúng không?'''),
]


# đề xuất bay nhảy quá:
# 32. Bob: 'Vậy giờ chúng ta bắt đầu lên kế hoạch giải bài này nhé! Mọi người có ý tưởng gì không? Mình nghĩ có thể dùng đạo hàm để xét khoảng đồng biến, nghịch biến nè.'    
# 33. Khải: 'mình cũng nghĩ thê'
# 34. Bob: 'Mình thấy dùng đạo hàm là một cách hay. Còn cách nào khác ngoài đạo hàm mà chúng ta có thể áp dụng để giải bài này không nhỉ? Mọi người cùng suy nghĩ thêm xem sao?'
# 35. Alice: 'Ngoài đạo hàm, mình nghĩ có thể khảo sát trực tiếp sự biến thiên của hàm số bằng cách xét hiệu $f(x_1) - f(x_2)$ với $x_1 < x_2$ xem sao?'
# 36. Khải: 'Alice đấy là phương pháp dựa trên kiến thức nào đấy'
# 37. Alice: 'Khải hỏi hay đó! Ý mình là, nếu $x_1 < x_2$ mà $f(x_1) < f(x_2)$ thì hàm số đồng biến trên khoảng đang xét. Ngược lại thì nghịch biến.'
# 38. Khải: 'à bạn dựa vào lý thuyết à'
# 39. Bob: 'Alice và Khải đã đề xuất 2 cách rồi. Còn ai có ý tưởng gì khác nữa không? Cứ thoải mái chia sẻ nha!'
# 40. Alice: 'Tớ nghĩ ngoài đạo hàm và xét hiệu, mình có thể dùng đồ thị hàm số để nhìn trực quan sự đơn điệu của nó nữa đó!'
# 41. Khải: 'nghĩa là vẽ đồ thị ra à'
# 42. Charlie: 'Khải ơi, hay là thử vẽ đồ thị hàm số này ra đi, rồi mình cùng nhau nhận xét xem sao? Biết đâu lại có thêm ý tưởng hay!'
# 43. Khải: 'thôi mình nghĩ tìm cách tôi ưu nhất làm là được rồi'
# 44. Bob: 'Mình thấy cả nhóm mình đã đưa ra được nhiều ý tưởng hay rồi đó! Nhưng Khải ơi, mình đừng quên mục tiêu của nhóm là tìm ra phương án tối ưu nhất để giải bài này nhé!'
# 45. Khải: 'okok, vậy chọn cách nào nhỉ'
# 46. Bob: 'Chúng ta có đạo hàm, xét hiệu, và đồ thị. Khải thấy cách nào "tối ưu" nhất trong 3 cách này?'
# 47. Khải: 'nên xét hiệu chăng?'
# 48. Alice: 'Ừ, xét hiệu cũng hay đó Khải! Cách này giúp mình hiểu rõ bản chất của sự biến thiên mà không cần dùng đến công cụ đạo hàm.'
# 49. Khải: 'mọi người đồng ý không'
# 50. Bob: 'Mọi người thấy phương pháp xét hiệu có ưu điểm gì và nhược điểm gì không? Mình muốn nghe thêm ý kiến của mọi người về cách này!'
# 51. Charlie: 'Khải tự tin lên! Tớ thấy xét hiệu cũng ổn áp đó. Mình cùng nhau mổ xẻ xem cách này có những điểm mạnh, điểm yếu gì không? Như vậy sẽ rõ ràng hơn mà!'
# 52. Alice: 'Xét hiệu có cái hay là không cần tính đạo hàm, đỡ phải lo lắng về việc tính toán phức tạp đó Khải! Với lại, nó giúp mình hiểu rõ hơn về định nghĩa đồng biến, nghịch biến.'
# 53. Khải: 'Bob thấy sao'
# 54. Bob: 'Khải hỏi hay đó! Alice, Charlie, hai bạn thấy sao về việc xét hiệu? Cho mình xin ý kiến với!'
# 55. Alice: 'Tớ thấy xét hiệu còn có ưu điểm là trực quan, dễ hiểu nữa đó Bob! Mình chỉ cần so sánh $f(x_1)$ và $f(x_2)$ thôi mà.'
# 56. Charlie: 'Khải ơi, tớ thấy ý kiến của cậu rất hay đó! Mình cùng nhau phân tích kỹ hơn về phương pháp xét hiệu này đi. Như vậy, mình sẽ có cái nhìn toàn diện hơn về nó!'
# 57. Khải: 'uh Alice thử đề xuất các bước thực hiện đi'
# 58. Alice: 'Để xét hiệu, đầu tiên mình chọn $x_1, x_2$ thuộc khoảng xác định, $x_1 < x_2$. Sau đó, mình tính $f(x_1)$ và $f(x_2)$, rồi xét dấu hiệu $f(x_2) - f(x_1)$.'     
# 59. Khải: 'ok cụ thể hơn nữa đi, mình thấy cách này môn lung quá, tại mình biết chọn x1, x2 như thế nào đâu'
# 60. Bob: 'Đúng rồi đó Khải, Alice nói rõ hơn đi! Mục tiêu của mình là xét hiệu $f(x_2) - f(x_1)$ để xem nó dương hay âm mà, đúng không?'
# 61. Alice: 'Khải ơi, ví dụ mình muốn xét trên khoảng $(0; +\\infty)$ thì mình có thể chọn $x_1 = 1$ và $x_2 = 2$, vì $1 < 2$ và cả hai đều thuộc khoảng này đó!'
# 62. Bob: 'Alice nè, mình nhắc lại là mục tiêu của xét hiệu là gì nhỉ? Với lại, có cách nào chọn $x_1$, $x_2$ tổng quát hơn không, chứ ví dụ cụ thể như bạn thì hơi khó hình dung!'
# 63. Alice: 'Bob nói đúng đó! Mục tiêu của xét hiệu là xét dấu của $f(x_2) - f(x_1)$ để biết hàm tăng hay giảm. \nThay vì chọn số cụ thể, mình cứ gọi $x_1, x_2$ là hai số bất kì thuộc khoảng đang xét, với $x_1 < x_2$ đi!'


# Bắt nghĩ nhiều cách nhưng hơi bay nhảy, không chọn được cách tốt nhất

# 32. Alice: 'Mình thấy bài này có dạng phân thức hữu tỉ. Hay là mình đạo hàm trực tiếp rồi xét dấu thử xem sao?'
# 33. Khải: 'vì sau bạn nghĩ vậy'
# 34. Alice: "Tại vì mình thấy nó có dạng $\\frac{u}{v}$ nên nghĩ ngay đến công thức đạo hàm $(\\frac{u}{v})' = \\frac{u'v - uv'}{v^2}$ ấy mà! Tính xong nhìn dấu của đạo hàm là biết ngay đồng biến hay nghịch biến!"
# 35. Khải: 'ò vậy có vẻ đây là một cách nhỉ'
# 36. Bob: 'Hiện tại mình thấy Alice đề xuất đạo hàm trực tiếp rồi xét dấu. Khải thấy phương pháp này thế nào? Có ý tưởng nào khác không Khải ơi?'
# 37. Khải: 'mình không có'
# 38. Bob: 'Alice và Khải, cách đạo hàm trực tiếp thì ổn đó, nhưng mình còn cách nào khác để xét tính đơn điệu của hàm này không nhỉ? Thử suy nghĩ thêm xem sao!'
# 39. Khải: 'Bob có nghĩ ra cách nào không'
# 40. Bob: 'Khải hỏi hay đó! Ngoài đạo hàm, mình còn có thể dùng định nghĩa xét dấu của $f(x_1) - f(x_2)$ không nhỉ? Hoặc có bạn nào nhớ cách xét khoảng bằng cách xét dấu của tử và mẫu không?'
# 41. Khải: 'bạn thử nói ưu điểm của nó xem, có nhanh hơn cách trên không'
# 42. Alice: 'Thật ra, đạo hàm trực tiếp có ưu điểm là "một phát ăn ngay" ấy! Tính đạo hàm xong, mình chỉ cần xét dấu của nó trên các khoảng xác định là xong. Đỡ phải biến đổi lằng nhằng như mấy cách khác.'
# 43. Bob: 'Đúng là đạo hàm "ăn ngay", nhưng mình đang muốn tìm thêm các hướng khác nữa. Còn bạn nào có ý tưởng gì khác không?'
# 44. Khải: 'chắc dùng đạo hàm thôi'
# 45. Bob: 'Mình hiểu là đạo hàm nhanh, nhưng mình muốn cả nhóm thử sức với các cách khác nữa! Biết đâu lại có cách hay hơn thì sao? Mọi người cố gắng thêm nhé!'
# 46. Charlie: 'Khải ơi, đừng vội nản! Biết đâu có cách nào đó "hack não" hơn thì sao? Cứ thử "brainstorming" thêm chút nữa đi, biết đâu lại ra ý tưởng hay!'
# 47. Khải: ':)))'


# Vẫn phải có con người vào để chọn cách đạo hàm, và cần đổi prompt của stage để k nhầm lẫn

# 32. Alice: 'Ngoài cách dùng đạo hàm, mình nghĩ bài này có thể khảo sát trực tiếp bằng định nghĩa được không nhỉ? Hoặc là dùng tính chất của hàm phân thức bậc nhất trên bậc nhất?'
# 33. Charlie: 'Alice ơi, mình thấy ý tưởng khảo sát trực tiếp bằng định nghĩa cũng hay đó! Bạn có thể nói rõ hơn về cách làm của bạn được không? Mình muốn nghe thêm về nó!'
# 34. Alice: 'Ừm, ý mình là xét $x_1 < x_2$, sau đó so sánh $f(x_1)$ và $f(x_2)$ xem cái nào lớn hơn đó mà!'
# 35. Bob: 'Alice và Charlie có ý tưởng hay đó! Để hệ thống lại, mình nhắc lại nhiệm vụ của nhóm là đề xuất các phương pháp giải bài này nhé. Theo mình thì dùng đạo hàm là cách phổ biến nhất, mọi người thấy sao?'
# 36. Khải: 'uh mình biết cách đấy thôi'
# 37. Bob: 'Mình thấy Khải cũng quen với cách dùng đạo hàm rồi. Vậy mình thống nhất dùng đạo hàm nha. Mọi người có ai có ý kiến gì khác không?'
# 38. Alice: 'Mình nghĩ còn một cách nữa là sử dụng phép biến đổi đại số để đưa về dạng dễ khảo sát hơn, mọi người thấy sao?'
# 39. Khải: 'là sao'
# 40. Alice: 'Khải ơi, để tớ giải thích rõ hơn nhé! $f(x) = \\frac{x-1}{x+1} = \\frac{x+1-2}{x+1} = 1 - \\frac{2}{x+1}$. Đến đây bạn thấy gì không?'
# 41. Khải: 'mình chưa hiểu lắm'
# 42. Alice: 'Đến đây, Khải thấy là khi $x$ tăng thì $x+1$ tăng, kéo theo $\\frac{2}{x+1}$ giảm, nên $-\\frac{2}{x+1}$ tăng, cuối cùng $1 - \\frac{2}{x+1}$ cũng tăng đó!'
# 43. Khải: 'thì sao'
# 44. Charlie: 'Khải ơi, Alice biến đổi hay thật! Chỗ biến đổi $\\frac{x-1}{x+1} = \\frac{x+1-2}{x+1}$ là một kỹ thuật tách phân số đó, bạn xem lại kiến thức cũ nha!'
# 45. Khải: 'cách này hơi khó với tớ'
# 46. Bob: 'Khải ơi, bạn đang gặp khó khăn ở chỗ nào vậy? Để Alice giảng lại cho bạn chỗ đó nha!'
# 47. Khải: 'mình nghĩ vẫn nên dùng đạo hàm'
# 48. Bob: 'Mình thấy cách của Alice cũng khá hay, nhưng mà hơi khó nhìn ra ngay. Với lại, không phải bài nào cũng biến đổi được như vậy. Dùng đạo hàm có vẻ tổng quát hơn nhỉ?'
# 49. Alice: 'Tớ thấy dùng đạo hàm thì tổng quát hơn thật, đỡ phải "nhìn hình đoán ý" như cách của tớ. Với lại, đạo hàm còn dùng được cho nhiều hàm phức tạp khác nữa!'
# 50. Khải: 'uh thế dùng đạo hàm nhá'
# 51. Bob: 'Vậy là mình thống nhất dùng đạo hàm để giải bài này nha. Cách của Alice hay nhưng hơi khó nhìn ra. Giờ mình bắt đầu tính đạo hàm rồi xét dấu nha?'
# 52. Khải: 'okok'
# 53. Charlie: 'Tuyệt vời! Vậy cả nhóm mình thống nhất dùng đạo hàm nha. Giờ mình bắt tay vào làm thôi! Chia việc ra cho nhanh nào!'



# Phần 3: Hơi lặp đi lặp lại nhiệm vụ, cần có cơ chế khác.


def print_history(history):
    print("\n--- LỊCH SỬ HỘI THOẠI ---")
    if not history:
        print("(Lịch sử trống)")
    for i, (speaker, talk) in enumerate(history):
        print(f"{i+1}. {speaker}: {repr(talk)}")
    print(f"--- Giai đoạn hiện tại: {CURRENT_STAGE} ---")
    print("---------------------------\n")


def run_conversation():
    global CURRENT_STAGE 

    print("Bắt đầu cuộc hội thoại:")
    print_history(HISTORY)
    time.sleep(1)

    max_turns = 150
    turn_count = 0

    while turn_count < max_turns:
        turn_count += 1
        print(f"====== Lượt {turn_count} ======")

        if not HISTORY:
             print("Lỗi: Lịch sử trống!")
             break
             
        last_speaker, last_talk = HISTORY[-1]

        if last_speaker == USER_NAME:
            # Lượt của AI
            
            ai_response = AI_talk(HISTORY, CURRENT_STAGE) 
            
            cleaned_talk = clean_ai_response(ai_response["talk"]) 
            
            ai_name = ai_response["name"]
            HISTORY.append((ai_name, cleaned_talk))
            
            # 4. In lịch sử cập nhật
            print(f"\n>> {ai_name} nói:")
            print_history(HISTORY) 

            # 5. Kiểm tra và cập nhật stage
            if ai_response["stage"] == "yes":
                try:
                    current_index = STAGE.index(CURRENT_STAGE)
                    if current_index < len(STAGE) - 1:
                        CURRENT_STAGE = STAGE[current_index + 1]
                        print(f"*** Chuyển sang giai đoạn {CURRENT_STAGE} ***\n")
                    else:
                        print("*** Đã ở giai đoạn cuối cùng ***\n")
                except ValueError:
                     print(f"Lỗi: Không tìm thấy giai đoạn {CURRENT_STAGE} trong danh sách STAGE.\n")

        elif last_speaker in AI_NAMES:

            # 1. Chuẩn bị history cho manager
            history_fm = history_for_manager(HISTORY)

            # 2. Chạy pipeline của Human_AI_Speaker_Controller
            # prompt4 = prompt_Human_AI_Speaker_Controller(history_for_manager=history_fm) 
            # res4_raw = gemini_resp(prompt4)
            # controller_decision = parse_json(res4_raw)

            # Thử nghiệm
            controller_decision = {"Explain" : "", "Speaker" : "Both"}

            # Lấy kết quả
            next_speaker_type = controller_decision.get("Speaker", "AI")
            explanation = controller_decision.get("Explain", "(Không có giải thích)")
            print(f"Người nói tiếp theo: {next_speaker_type}")

            # 3. Xử lý kết quả
            if next_speaker_type == "Human":
                 print(f"\n>> Lượt của {USER_NAME}:")
                 user_input = ""
                 while not user_input.strip():
                    user_input = input("Nhập lời nói của bạn: ")
                    if not user_input.strip():
                         print("Vui lòng nhập nội dung.")
                 # Append vào HISTORY *trước khi* in
                 HISTORY.append((USER_NAME, user_input))
                 print_history(HISTORY) 

            elif next_speaker_type == "AI":
                # Chạy luôn AI_talk
                print(f"[{CURRENT_STAGE}] Để AI tiếp tục...")

                ai_response = AI_talk(HISTORY, CURRENT_STAGE) 
                cleaned_talk = clean_ai_response(ai_response["talk"])
                ai_name = ai_response["name"]
                HISTORY.append((ai_name, cleaned_talk))

                print(f"\n>> {ai_name} nói:")
                print_history(HISTORY)
                if ai_response["stage"] == "yes":
                    try:
                        current_index = STAGE.index(CURRENT_STAGE)
                        if current_index < len(STAGE) - 1:
                            CURRENT_STAGE = STAGE[current_index + 1]
                            print(f"*** Chuyển sang giai đoạn {CURRENT_STAGE} ***\n")
                        else:
                            print("*** Đã ở giai đoạn cuối cùng ***\n")
                    except ValueError:
                         print(f"Lỗi: Không tìm thấy giai đoạn {CURRENT_STAGE} trong danh sách STAGE.\n")

            elif next_speaker_type == "Both":
                print(f"\n>> Lượt của user (hoặc AI nếu bạn bỏ qua).")
                action = input("Bạn có muốn nói không? Nhập 'yes' để nói, nhấn Enter (hoặc nhập gì khác) để bỏ qua: ").strip().lower()

                if action == "yes":
                    # Human nói
                    user_input = ""
                    while not user_input.strip():
                        user_input = input("Nhập lời nói của bạn: ")
                        if not user_input.strip():
                             print("Vui lòng nhập nội dung.")
                    HISTORY.append((USER_NAME, user_input))
                    print_history(HISTORY)
                else:
                    # Human bỏ qua, AI nói
                    print(f"[{CURRENT_STAGE}] {USER_NAME} bỏ qua. Để AI nói...")
                    ai_response = AI_talk(HISTORY, CURRENT_STAGE) 
                    cleaned_talk = clean_ai_response(ai_response["talk"])
                    ai_name = ai_response["name"]
                    HISTORY.append((ai_name, cleaned_talk))

                    print(f"\n>> {ai_name} nói:")
                    print_history(HISTORY)
                    # 5. Kiểm tra và cập nhật stage
                    if ai_response["stage"] == "yes":
                        try:
                            current_index = STAGE.index(CURRENT_STAGE)
                            if current_index < len(STAGE) - 1:
                                CURRENT_STAGE = STAGE[current_index + 1]
                                print(f"*** Chuyển sang giai đoạn {CURRENT_STAGE} ***\n")
                            else:
                                print("*** Đã ở giai đoạn cuối cùng ***\n")
                        except ValueError:
                             print(f"Lỗi: Không tìm thấy giai đoạn {CURRENT_STAGE} trong danh sách STAGE.\n")
            else:
                print(f"Lỗi: Loại người nói không xác định từ Controller '{next_speaker_type}'. Dừng demo.")
                break

        else:
            print(f"Lỗi: Người nói cuối cùng không xác định '{last_speaker}'. Dừng demo.")
            break

        time.sleep(1.5)

    print(f"\n--- CUỘC HỘI THOẠI KẾT THÚC (Đạt giới hạn {max_turns} lượt) ---")
    print("Lịch sử cuối cùng:")
    print_history(HISTORY)

# --- Chạy chương trình ---
if __name__ == "__main__":
    run_conversation()