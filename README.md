# Polski

# Szukanie dużych liczb pierwszych Mersenne'a

Projekt **Szukanie dużych liczb pierwszych Mersenne'a** to narzędzie napisane w Pythonie, którego celem jest wyszukiwanie liczb Mersenne'a, czyli liczb postaci \( M_p = 2^p - 1 \), które mogą być liczbami pierwszymi. Projekt wykorzystuje równoległe przetwarzanie oraz akcelerację GPU przy użyciu biblioteki [CuPy](https://cupy.dev/), co pozwala na szybkie wykonywanie obliczeń związanych z testami pierwszości (Miller-Rabin oraz Lucas-Lehmer).

## Główne funkcjonalności

- **Test Millera-Rabina na GPU:**  
  Przyspieszony test pierwszości wykonywany na GPU, dzięki czemu sprawdzanie kandydatów jest bardzo szybkie.

- **Test Lucasa-Lehmera:**  
  Test wykorzystywany do weryfikacji liczb Mersenne'a, zoptymalizowany przy użyciu GPU.

- **Generowanie kandydatów:**  
  Do generowania kolejnych wykładników, dla których liczbą Mersenne'a \( M_p \) ma być potencjalnie pierwsza, wykorzystywana jest biblioteka [Sympy](https://www.sympy.org/), co pozwala na efektywne generowanie liczb pierwszych.

- **Równoległe przetwarzanie:**  
  Projekt korzysta z modułu `concurrent.futures` (ProcessPoolExecutor) do równoległego sprawdzania wielu kandydatów jednocześnie, maksymalnie wykorzystując dostępne rdzenie CPU.

- **Zapisywanie postępów:**  
  - **Plik `last_exponent.json`:** Zapisuje ostatni sprawdzony wykładnik, co umożliwia wznowienie obliczeń po przerwie.
  - **Plik `found_primes.txt`:** Zapisuje znalezione liczby Mersenne'a, które okazały się być liczbami pierwszymi.

## Wymagania

- **Python 3.7+**
- **CuPy:**  
  Instalacja zależnie od wersji CUDA (np. `pip install cupy-cuda11x` dla CUDA 11)
- **Sympy:**  
  `pip install sympy`
- Inne biblioteki: `itertools`, `time`, `json`, `os`, `concurrent.futures` – standardowe dla Pythona.

## Instalacja

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/Kowalec/mersennenumbers.git
   cd liczbypierwsze

2. **Utwórz i aktywuj wirtualne środowisko (opcjonalnie):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Zainstaluj wymagane zależności:**
   Upewnij się, że zastąpisz cupy-cudaXX odpowiednią wersją dla Twojej karty graficznej (np. cupy-cuda11x).

   ```bash
    pip install cupy-cudaXX sympy


5.  **Uruchomienie**
Aby rozpocząć wyszukiwanie liczb Mersenne'a, uruchom główny skrypt:
    ```bash
    python3 mersennenumbers.py


## Struktura projektu

- mersennenumbers.py – główny skrypt wyszukujący liczby Mersenne'a
- last_exponent.json – plik z zapisem ostatniego sprawdzanego wykładnika (tworzony automatycznie)
- found_primes.txt – plik z zapisanymi znalezionymi liczbami pierwszymi


# English

# Searching for Large Mersenne Prime Numbers

The **Searching for Large Mersenne Prime Numbers** project is a Python-based tool designed to search for Mersenne numbers, which are numbers of the form \( M_p = 2^p - 1 \) that may be prime. The project utilizes parallel processing and GPU acceleration using the [CuPy](https://cupy.dev/) library, enabling fast execution of primality tests (Miller-Rabin and Lucas-Lehmer).

## Main Features

- **Miller-Rabin Test on GPU:**  
  A GPU-accelerated primality test that significantly speeds up candidate verification.

- **Lucas-Lehmer Test:**  
  A test specifically used to verify Mersenne numbers, optimized with GPU acceleration.

- **Candidate Generation:**  
  The [Sympy](https://www.sympy.org/) library is used to efficiently generate prime exponents for potential Mersenne primes.

- **Parallel Processing:**  
  The project leverages Python’s `concurrent.futures` (ProcessPoolExecutor) to process multiple candidates simultaneously, maximizing CPU core utilization.

- **Progress Saving:**  
  - **`last_exponent.json` file:** Stores the last checked exponent, allowing computation to resume after a break.  
  - **`found_primes.txt` file:** Records discovered Mersenne primes.

## Requirements

- **Python 3.7+**
- **CuPy:**  
  Installation depends on the CUDA version (e.g., `pip install cupy-cuda11x` for CUDA 11)
- **Sympy:**  
  `pip install sympy`
- Other libraries: `itertools`, `time`, `json`, `os`, `concurrent.futures` – standard for Python.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Kowalec/mersennenumbers.git
   cd liczbypierwsze
   ```

2. **Create and activate a virtual environment (optional):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install required dependencies:**
   Make sure to replace cupy-cudaXX with the appropriate version for your GPU (e.g., cupy-cuda11x).

   ```bash
   pip install cupy-cudaXX sympy
   ```

5. **Run the project**

To start searching for Mersenne primes, run the main script:

    ```bash
    python3 mersennenumbers.py
    ```

## Project Structure

- `mersennenumbers.py` – The main script for searching Mersenne primes
- `last_exponent.json` – File that saves the last checked exponent (created automatically)
- `found_primes.txt` – File storing discovered prime numbers
