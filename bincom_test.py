
# bincom_test.py
"""Bincom ICT - Preliminary Python Test
This script performs the required analyses on a local HTML file (bincom_colors.html).
If you don't have the real HTML downloaded, use the included bincom_colors_sample.html to test.
Outputs:
  - Mean color (by frequency closeness)
  - Most worn color (mode)
  - Median color (lexicographic median of the color list)
  - Variance of color frequencies
  - Probability that a randomly chosen color is RED
  - (Optional) Save color frequencies to PostgreSQL
  - Recursive search example
  - Random 4-bit binary -> decimal
  - Sum of first 50 Fibonacci numbers
Usage:
  1. Place the real `bincom_colors.html` in the same folder, or rename the sample provided.
  2. Install dependencies: pip install beautifulsoup4 psycopg2-binary
  3. Run: python bincom_test.py
"""

import random
import statistics
from collections import Counter
import os
import sys

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print("Missing dependency: beautifulsoup4. Install with: pip install beautifulsoup4")
    raise

# --------------- Configuration ---------------
HTML_FILENAME = "bincom_colors.html"   # put the real HTML here
SAMPLE_FILENAME = "bincom_colors_sample.html"  # included for local testing
SAVE_TO_DB = False  # set True if you want to attempt saving to PostgreSQL
# Database config (only used if SAVE_TO_DB = True)
DB_CONFIG = {
    "dbname": "your_dbname",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
}

# --------------- Helpers ---------------
def load_html_colors(filename):
    """Parse the provided HTML and extract color strings from <td> tags or common places."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Strategy: gather text from table cells, list items, and paragraphs
    texts = []
    for tag in soup.find_all(["td","li","p","span","div"]):
        txt = tag.get_text(separator=" ").strip()
        if txt:
            texts.append(txt)

    # Heuristic: common color words appear as standalone tokens separated by spaces or commas
    tokens = []
    for t in texts:
        # split on commas and newlines, then spaces
        for part in t.replace('\n', ' ').split(','):
            for token in part.split():
                token = token.strip()
                if token:
                    tokens.append(token.upper())

    # Filter tokens for likely color names (letters only or containing hyphen)
    colors = [tok for tok in tokens if any(ch.isalpha() for ch in tok)]
    return colors

# --------------- Main Analysis ---------------
def analyze_colors(colors):
    if not colors:
        print('No colors found to analyze.')
        return

    total = len(colors)
    counts = Counter(colors)
    frequencies = list(counts.values())

    # Mean frequency, pick color whose frequency is closest to mean
    mean_freq = statistics.mean(frequencies)
    mean_color = min(counts.keys(), key=lambda c: abs(counts[c] - mean_freq))

    # Mode / most worn
    most_worn = counts.most_common(1)[0][0]

    # Median (lexicographic median of the full color list)
    sorted_colors = sorted(colors)
    median_color = sorted_colors[len(sorted_colors)//2]

    # Variance of frequencies (if at least two samples)
    variance = statistics.variance(frequencies) if len(frequencies) > 1 else 0.0

    # Probability of RED
    prob_red = counts.get("RED", 0) / total

    # Print results
    print("\n--- Analysis Results ---")
    print(f"Total entries parsed: {total}")
    print(f"Unique colors found: {len(counts)}\n")
    print(f"Mean color (by frequency closeness): {mean_color}")
    print(f"Most worn color (mode): {most_worn}")
    print(f"Median color (lexicographic median of list): {median_color}")
    print(f"Variance of frequencies: {variance}")
    print(f"Probability a random pick is RED: {prob_red:.4f}\n")

    # Return structured result
    return {
        "total": total,
        "counts": counts,
        "mean_color": mean_color,
        "most_worn": most_worn,
        "median_color": median_color,
        "variance": variance,
        "prob_red": prob_red,
    }

# --------------- Optional: Save to PostgreSQL ---------------
def save_to_postgres(counts, config):
    try:
        import psycopg2
    except Exception:
        print("psycopg2 is missing. Install with: pip install psycopg2-binary")
        return False

    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS color_frequency (color TEXT PRIMARY KEY, frequency INT);")
        for color, freq in counts.items():
            cur.execute(
                "INSERT INTO color_frequency (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency;",
                (color, freq)
            )
        conn.commit()
        cur.close()
        conn.close()
        print("Saved color frequencies to PostgreSQL.")
        return True
    except Exception as e:
        print(f"Failed to save to PostgreSQL: {e}")
        return False

# --------------- Recursive Search ---------------
def recursive_search(lst, target, index=0):
    if index >= len(lst):
        return False
    if lst[index] == target:
        return True
    return recursive_search(lst, target, index+1)

# --------------- Binary -> Decimal ---------------
def random_binary_to_decimal(bits=4):
    b = ''.join(str(random.randint(0,1)) for _ in range(bits))
    return b, int(b, 2)

# --------------- Fibonacci Sum ---------------
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# --------------- Script entrypoint ---------------
if __name__ == '__main__':
    # Try the real HTML file first, otherwise fall back to sample
    html_file = HTML_FILENAME if os.path.exists(HTML_FILENAME) else (SAMPLE_FILENAME if os.path.exists(SAMPLE_FILENAME) else None)
    if html_file is None:
        print("Could not find bincom_colors.html or the sample file. Please download the HTML file from the Drive link and save it as 'bincom_colors.html' in this folder.")
        sys.exit(1)

    try:
        colors = load_html_colors(html_file)
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        sys.exit(1)

    results = analyze_colors(colors)

    # Attempt DB save if requested
    if SAVE_TO_DB and results:
        save_to_postgres(results['counts'], DB_CONFIG)

    # Demo recursive search
    demo_list = [1, 3, 5, 7, 9]
    target = 7
    print(f"Recursive search: is {target} in {demo_list}? -> {recursive_search(demo_list, target)}")

    # Random binary conversion
    bstr, dec = random_binary_to_decimal(4)
    print(f"Random 4-bit binary: {bstr} -> decimal: {dec}")

    # Sum first 50 Fibonacci numbers
    fib50 = fibonacci_sum(50)
    print(f"Sum of first 50 Fibonacci numbers: {fib50}")
