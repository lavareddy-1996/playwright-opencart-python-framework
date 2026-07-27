# OpenCart E2E Test Automation Framework

End-to-end UI test automation for the [OpenCart demo store](https://tutorialsninja.com/demo/),
built with **Playwright**, **Pytest**, and **Python**, using the **Page Object Model (POM)**
design pattern.

## Tech Stack
- Python 3.11+
- Playwright (sync API)
- Pytest + pytest-xdist (parallel execution) + pytest-rerunfailures
- Allure & pytest-html for reporting
- Faker for test data generation

## Project Structure
```
.
├── conftest.py            # CLI options, browser/context/page fixtures, Allure attachments
├── config.py               # Test data & credentials (read from env vars)
├── pytest.ini               # Pytest configuration & default CLI flags
├── requirements.txt
├── pages/                  # Page Object Model classes
│   ├── home_page.py
│   ├── login_page.py
│   ├── registration_page.py
│   ├── search_results_page.py
│   ├── product_page.py
│   ├── shopping_cart_page.py
│   ├── checkout_page.py
│   ├── my_account_page.py
│   └── logout_page.py
└── tests/                   # Test cases (add your test_*.py files here)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

Copy `.env.example` to `.env` and fill in test credentials for a real account
on the demo store, or export the variables in your shell:

```bash
cp .env.example .env
```

## Running Tests

```bash
pytest                                    # uses defaults from pytest.ini
pytest -m sanity                          # run a specific marker
pytest --browser=firefox --headed         # override CLI options
pytest tests/test_login.py -k "valid"     # run a specific test
```

Reports are written to `reports/` (HTML report, Allure results, videos, traces).
To view the Allure report:

```bash
allure serve reports/allure-results
```

## Design Notes
- Each page exposes locators in `__init__` and behavior as methods; action
  methods that return the next page (e.g. `login()`, `click_logout()`) enable
  fluent, chainable test code.
- Browser/context/page lifecycle and Allure screenshot/video/trace capture
  live centrally in `conftest.py` rather than in individual page objects.
- Credentials are never hard-coded — they're loaded from environment
  variables via `config.py`.

## Possible Next Steps
- Add `tests/` with sanity/regression suites covering login, registration,
  search, cart, and checkout flows.
- Wire up a GitHub Actions workflow to run the suite and publish the Allure
  report on push.
