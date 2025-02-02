name: Weekly Wayback Scraper

on:
  schedule:
    - cron: '51 17 * * 0'  # Runs every Sunday at 16:05 UTC

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'  # Specify your desired Python version

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests pandas beautifulsoup4 waybackpy

      - name: Run the script
        run: python wayback.py

      - name: Commit and push results
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add wayback_results/wayback_scraped_data.csv
          git commit -m 'Update Wayback Machine data'
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
