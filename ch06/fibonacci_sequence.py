def generate_fibonacci(n):
    fib_sequence = [1, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# 예시: 첫 10개의 피보나치 수 출력
print(generate_fibonacci(10))