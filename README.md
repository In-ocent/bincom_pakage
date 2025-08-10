
# Bincom ICT - Preliminary Python Test Package

Files:
- bincom_test.py         : Main script that performs the analysis and bonus tasks.
- bincom_colors_sample.html : A sample HTML file you can use to test locally.
- README.md              : This file.

Instructions:
1. Download the real HTML file from the Google Drive link provided by Bincom and save it in this folder as `bincom_colors.html`.
   Drive link (as provided in the test prompt): https://drive.google.com/open?id=1nf9WMDjZWIUnlnKyz7qomEYDdtWfW1Uf
   NOTE: the Drive file may require you to sign in. If you can't download it, replace `bincom_colors.html` with your own file that follows a similar structure (a table of colors).

2. (Optional) If you want to save results to PostgreSQL:
   - Edit `bincom_test.py`, set `SAVE_TO_DB = True` and fill DB_CONFIG with your connection details.
   - Ensure you have `psycopg2-binary` installed and a running PostgreSQL server.

3. Install dependencies:
   ```
   pip install beautifulsoup4
   pip install psycopg2-binary   # only if SAVE_TO_DB=True
   ```

4. Run the script:
   ```
   python bincom_test.py
   ```

5. Upload your `bincom_test.py` to Google Drive or GitHub and submit per Bincom instructions.

Good luck!
