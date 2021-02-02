import math
import module
from openpyxl import load_workbook
import pandas as pd

# 순번, 단과대학이름, 단과대학 재적생수, 직선석 수임. 이건 수동으로 둘거라서 알아서 수정해서 돌리면 됨.
College = [
    [0, "IT대학", 4298, 11],
    [1, "공과대학", 3683, 12],
    [2, "경상대학", 2763, 3],
    [3, "과학기술대학", 2866, 15],
    [4, "농업생명대학", 2413, 15],
    [5, "자연대학", 2370, 10],
    [6, "인문대학", 2062, 12],
    [7, "사회대학", 1510, 8],
    [8, "사범대학", 1476, 17],
    [9, "생태환경대학", 1346, 9],
    [10, "예술대학", 690, 5],
    [11, "의과대학", 655, 1],
    [12, "간호대학", 561, 1],
    [13, "생활과학대학", 515, 4],
    [14, "행정학부", 523, 1],
    [15, "수의대학", 387, 2],
    [16, "치과대학", 349, 1],
    [17, "자율정공", 229, 9],
    [18, "약학대학", 121, 1],
    [19, "글로벌인재학부", 4, 1]
]

# 단과대학 당 최대 의석수, 수정해서쓰면됨
max_Seat = 18

# 전 전학대회 총 의원 수, 수정해서쓰면됨
before_Council = 169

# 단과대학 갯수
max_College = len(College)
print("1. 단과대학 갯수 :", max_College)

# 총 재적생 수
all_KNU = sum([College[i][2] for i in range(max_College)])
print("2. 총 재적생 수 :", all_KNU)

# 최소 정수 N
minimal_N = int(all_KNU**(1/3))
print("3. 최소 정수 :", minimal_N)

# 전학대회 총 할당 의원 수
max_Associate = module.get_Now_Council(minimal_N, before_Council)
print("4. 전학대회 총 할당 의원 수 : ", max_Associate)

# 단과대학별 할당 의원 수
priority_Initial, priority_Sorted, associated_Seat = module.get_Priority_To_Associate(
    College, max_Seat, max_Associate)
print("5. 단과대학별 총 할당 의원 수 : ", associated_Seat)

# 단과대학별 고정 의원 수
fixed_Seat = [1 for i in range(max_College)]
print("6. 단과대학별 고정 의원 수 : ", fixed_Seat)

# 단과대학별 비례 의원 수
proportional_Seat = module.get_Proportional(
    College, associated_Seat, fixed_Seat)
print("7. 단과대학별 비례 의원 수 : ", proportional_Seat)

# 단과대학별 소수 비레 의원 수
low_proportional_Seat = module.get_Low_proportional(
    max_Seat, max_College, minimal_N, max_Associate, associated_Seat, priority_Initial, priority_Sorted)
print("8. 단과대학별 소수 비례 의원 수 : ", low_proportional_Seat)

# 단과대학별 총 의원 수
final_Seat = module.get_Final(
    fixed_Seat, College, proportional_Seat, low_proportional_Seat)
print("9. 단과대학별 총 의원 수 : ", final_Seat)


College_List = []
College_Attend = []
College_Direct = []
Population_Per1 = []

for i in range(max_College):
    College_List.append(College[i][1])
    College_Attend.append(College[i][2])
    College_Direct.append(College[i][3])
    Population_Per1.append(round(College[i][2]/final_Seat[i], 2))

writer = pd.ExcelWriter(
    'test.xlsx', engine='openpyxl')  # pylint: disable=abstract-class-instantiated
wb = writer.book
df = pd.DataFrame({
    '단과대학': College_List,
    '할당의석': associated_Seat,
    '고정석': fixed_Seat,
    '직선석': College_Direct,
    '비례석': proportional_Seat,
    '소수비례석': low_proportional_Seat,
    '총 의석': final_Seat,
    '재적생수': College_Attend,
    '의원 1인당 인구수': Population_Per1
})
df.to_excel(writer, index=False)
wb.save('test.xlsx')
