import time

collatz_cache = {1:0}

def test_collatz(n):
    collatz_cache = {1:0}
    return collatz(n)

def collatz(n):
    if n not in collatz_cache:
        if n%2 == 0:
            collatz_cache[n] = collatz(n//2)+1
        else:
            collatz_cache[n] = collatz(3*n+1)+1
    return collatz_cache[n]
    
def timing_table(f, batch_range, inner_reps, outer_reps):
    results = []
    for _ in range(outer_reps):
        for k in batch_range:
            start = time.process_time()
            for _ in range(inner_reps):
                f(k)
            end = time.process_time()
            results.append((k, end-start))
    return results

def gen1(filename):
    inner_reps = 100000
    table = timing_table(collatz, range(1, 1000), inner_reps, 1)
    with open(filename, "w") as f:
        print('run_id, inner_reps, time', file=f)
        for n, t in table:
            # print(f'"fib-nocache", {n}, {inner_reps}, {t}', file=f)
            print(f'{n}, {t}', file=f)

gen1("results.txt")