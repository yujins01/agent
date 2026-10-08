def fibonacci(n):
    sequence = [1, 1]  # 첫 번째 항은 1, 두 번째 항은 1
    while len(sequence) < n:
        next_value = sequence[-1] + sequence[-2]  # 다음 항 계산
        sequence.append(next_value)
    return sequence

# 피보나치 수열의 첫 10개 항 출력
fibonacci_sequence = fibonacci(10)
print(fibonacci_sequence)