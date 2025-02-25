import itertools
import time
import json
import os
import concurrent.futures
import cupy as cp
import sympy

def modexp_gpu(a, d, n):
    # Na razie korzystamy z cuPy i funkcji cp.power oraz cp.mod, 
    return cp.mod(cp.power(a, d), n)

def miller_rabin_gpu(n, k=5):
    """Test pierwszości metodą Millera-Rabina z wykorzystaniem GPU."""
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0:
        return False

    # Konwersja na obiekt GPU (dla demonstracji)
    n_gpu = cp.asarray(n, dtype=cp.int64)
    r = 0
    d = n - 1
    # Wyznaczamy r i d (na CPU, bo n to pojedyncza liczba)
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = cp.random.randint(2, n - 2, dtype=cp.int64)
        x = modexp_gpu(a, d, n)
        x = int(x.get())  # Pobranie wyniku z GPU
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def lucas_lehmer_optimized_gpu(p):
    """Test Lucasa-Lehmera dla liczby Mersenne’a M_p = 2^p - 1 z wykorzystaniem GPU."""
    if p == 2:
        return True
    m = (1 << p) - 1  # Mersenne number: 2^p - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0

def check_mersenne_prime_gpu(p):
    """Sprawdza, czy liczba Mersenne’a M_p = 2^p - 1 jest pierwsza przy użyciu GPU."""
    # Najpierw sprawdzamy, czy wykładnik p jest liczbą pierwszą
    if not miller_rabin_gpu(p):
        return None
    # Jeśli p jest pierwsze, wykonujemy test Lucasa-Lehmera
    if lucas_lehmer_optimized_gpu(p):
        return (1 << p) - 1
    return None

def load_last_exponent():
    """Ładuje ostatni sprawdzony wykładnik z pliku (jeśli istnieje)."""
    if os.path.exists("last_exponent.json"):
        with open("last_exponent.json", "r") as f:
            data = json.load(f)
            return data["last_exponent"]
    return 33219280  # Domyślny wykładnik, jeśli plik nie istnieje

def save_last_exponent(exponent):
    """Zapisuje ostatni sprawdzony wykładnik do pliku."""
    with open("last_exponent.json", "w") as f:
        json.dump({"last_exponent": exponent}, f)

def save_prime_to_file(prime):
    """Zapisuje znalezioną liczbę Mersenne’a do pliku."""
    with open("found_primes.txt", "a") as f:
        f.write(f"Znaleziono liczbę pierwszą Mersenne'a: {prime}\n")

def prime_exponent_generator(start):
    """Generator generujący kolejne liczby pierwsze (wykładniki) przy użyciu sympy."""
    p = sympy.nextprime(start)
    while True:
        yield p
        p = sympy.nextprime(p)

def mersenne_prime_generator():
    """Generator przeszukujący kolejne wykładniki i sprawdzający liczby Mersenne’a."""
    start_exponent = load_last_exponent()
    print(f"Rozpoczynam sprawdzanie liczb Mersenne'a od wykładnika: {start_exponent}")

    last_saved_time = time.time()
    throughput_start_time = time.time()
    processed_count = 0

    candidate_exponents = prime_exponent_generator(start_exponent)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_exponent = {}
        # Ustal liczbę zadań równoległych na podstawie liczby rdzeni
        chunk_size = os.cpu_count() or 4

        # Przygotowanie początkowej partii kandydatów
        for _ in range(chunk_size):
            p = next(candidate_exponents)
            future = executor.submit(check_mersenne_prime_gpu, p)
            future_to_exponent[future] = p

        while future_to_exponent:
            done, _ = concurrent.futures.wait(
                future_to_exponent, return_when=concurrent.futures.FIRST_COMPLETED, timeout=1
            )
            current_time = time.time()
            for fut in done:
                p = future_to_exponent.pop(fut)
                try:
                    result = fut.result()
                except Exception as exc:
                    print(f"Błąd dla wykładnika {p}: {exc}")
                    result = None

                processed_count += 1
                elapsed = current_time - throughput_start_time
                rate = (processed_count / elapsed * 60) if elapsed > 0 else 0

                if result:
                    print(f"\nZnaleziono Mersenne prime dla wykładnika {p}: {result}")
                    save_prime_to_file(result)
                    yield result

                # Zlecamy kolejne zadanie
                new_p = next(candidate_exponents)
                new_future = executor.submit(check_mersenne_prime_gpu, new_p)
                future_to_exponent[new_future] = new_p

                # Co 60 sekund zapisujemy postęp
                if current_time - last_saved_time >= 60:
                    save_last_exponent(p)
                    last_saved_time = current_time
                    throughput_start_time = current_time
                    processed_count = 0

                print(f"Sprawdzany wykładnik: {p} | Prędkość: {rate:.2f} kandydatów/min", end="\r")
            if not done:
                current_exponent = next(iter(future_to_exponent.values()))
                elapsed = current_time - throughput_start_time
                rate = (processed_count / elapsed * 60) if elapsed > 0 else 0
                print(f"Sprawdzany wykładnik: {current_exponent} | Prędkość: {rate:.2f} kandydatów/min", end="\r")

if __name__ == "__main__":
    try:
        for prime in mersenne_prime_generator():
            print(f"\nMersenne prime: {prime}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
