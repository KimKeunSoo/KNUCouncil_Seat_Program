import numpy as np
import math


# 전의 전학대회의원수를 이용한 차기 전학대회 총 할당 의원수
def get_Now_Council(minimal_N, before_Council):
    times = 1
    while True:
        now_Council = minimal_N*times
        if(now_Council < before_Council):
            times += 1
        else:
            times -= 1
            return minimal_N*times


# 우선순위 계산 후 단대별 할당 의원 수 반환
def get_Priority_To_Associate(College, max_Seat, max_Associate):
    max_College = len(College)   # 단과대학 갯수
    priority_Initial = np.zeros((20, max_Seat))   # 우선순위값 초기화&할당
    priority_Not_sorted = []  # 우선순위값 1차원으로 입력할 곳 할당

    for row in range(max_College):
        P = int(College[row][2])  # 단과대학별 재적생수
        for col in range(max_Seat):
            priority_Initial[row][col] = format(  # 우선순위값 계산
                P/(math.sqrt((col+1)*(col+2))), '.2f')
            priority_Not_sorted.append(
                priority_Initial[row][col])  # 값 1차원으로 PUSH

    associated_Seat = [0 for i in range(max_College)]  # 각 단과대학별 할당 의원 수
    priority_Sorted = sorted(
        priority_Not_sorted, reverse=True)    # 1차원 내림차순 SORTING
    for index in range(max_Associate):   # 1차원 비교군
        value = priority_Sorted[index]
        for row in range(max_College):   # 2차원 대조군-행
            for col in range(max_Seat):  # 2차원 대조군-열
                if value == priority_Initial[row][col]:  # 값 탐색
                    associated_Seat[row] += 1  # 해당 단과대학 할당의원 수 + 1
    return priority_Initial, priority_Sorted, associated_Seat

# 단과대학별 비례 의원수 계산 후 반환


def get_Proportional(College, associated_Seat, fixed_Seat):
    proportional_Seat = []  # 반환할 값 초기화&할당
    max_College = len(College)   # 단과대학 갯수
    for i in range(max_College):
        value = associated_Seat[i]-fixed_Seat[i]-College[i][3]
        if(value > 0):  # 비례의원수 넣어야된다면 넣고
            proportional_Seat.append(value)
        else:  # 비례의원수 넣지말아야 된다면 0을 넣는다
            proportional_Seat.append(0)
    return proportional_Seat

# 단과대학별 소수 비례 의원 수 계산 후 반환


def get_Low_proportional(max_Seat, max_College, minimal_N, max_Associate, associated_Seat, priority_Initial, priority_Sorted, fixed_Seat, College_Direct):
    low_Proportional_Seat = [0 for i in range(max_College)]  # 반환할 값 초기화&할당
    is_Low_College = [0 for i in range(max_College)]  # 소수 단과대학인지 판별할 리스트 초기화
    max_Low_Seat = int(max_Seat/2)  # 소수 단과 대학일지 판별한 기준 값(단과대학별 최대 할당 위원수/2)
    for i in range(max_College):
        # 소수 단과 대학 판별 후 flag 1값 설정
        if((max_Low_Seat > associated_Seat[i]) & (max_Seat > fixed_Seat[i] + College_Direct[i])):
            is_Low_College[i] = 1

    index = max_Associate    # 총 할당 위원 maxAssociate 값부터 탐색
    low_Max = int(minimal_N/4)    # 소수 비례 의석에 할당할 수
    times = 0   # 할당 횟수

    while(times < low_Max):
        breakAll = True
        value = priority_Sorted[index]  # 탐색할 값
        while(breakAll):
            for row in range(max_College):   # 2차원 대조군-행
                for col in range(max_Seat):  # 2차원 대조군-열
                    # 값 탐색 후 소수 단과대학 일때
                    if (value == priority_Initial[row][col]):
                        if is_Low_College[row] != 0:
                            # 해당 단과대학 소수 비례 의원 수 + 1
                            low_Proportional_Seat[row] += 1
                            times += 1  # 할당 횟수 + 1
                        index += 1
                        breakAll = False
    return low_Proportional_Seat


def get_Final(fixed_Seat, College, proportional_Seat, low_proportional_Seat):
    max_College = len(College)  # 단과대학 갯수
    final_Seat = []  # 단과대학별 최종 의석 수
    for i in range(max_College):  # 고정석+직선석+비례석+소수비례석 더함
        final_Seat.append(fixed_Seat[i]+College[i][3] +
                          proportional_Seat[i]+low_proportional_Seat[i])
    return final_Seat
