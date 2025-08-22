# Playwright Percy Snapshot with Pytest

This repository demonstrates automated browser testing using **Playwright** with **Pytest**, along with **Percy visual snapshots** for visual regression testing.
It includes an HTML report setup with screenshots and URLs automatically embedded on test failures.

---

## Project Structure

- `conftest.py` ─ Pytest configuration and fixtures (Playwright, Percy, Reports)
- `test_playwright.py` ─ Example test cases with Percy snapshots
- `pyproject.toml` ─ Project dependencies and metadata
- `pytest.ini` ─ Pytest settings
- `package.json` ─ Node.js dependencies (for Percy CLI / Playwright install)
- `package-lock.json`
- `requirements.lock`
- `requirements-dev.lock`
- `reports/` ─ Generated pytest-html reports
- `screenshots/` ─ Failure screenshots (auto-created)
- `node_modules/` ─ Node.js modules
- `src/` ─ Python source code
- `README.md`


---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/playwright-percy-snapshot.git
cd playwright-percy-snapshot
```

### 2. Set up Python Environment

It’s recommended to use Rye, venv, or virtualenv.

Using Rye:

```bash
rye sync
```

Or with pip:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

pip install -r requirements.lock
```

### 3. Install Playwright Browsers

```bash
playwright install
```

### 4. Install Percy CLI (Node.js)

```bash
npm install --save-dev @percy/cli
```

## Environment Setup

Create a .env file in the project root:

```ini
PERCY_TOKEN=your_percy_project_token
```

Percy requires this token to run. You can get it from your Percy dashboard.
## Running Tests
### Run Tests with Pytest

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run in Headless Mode

```bash
pytest --browser chromium --headless
```

## Percy Visual Testing

Percy snapshots are captured during test runs and uploaded to your Percy project.

Run with Percy:

```bash
npx percy exec -- pytest --browser chromium
```

After execution, Percy will provide a build link where you can review visual changes.
## Reports & Screenshots

- HTML Report → stored in reports/report.html
- Failure Screenshots → stored in screenshots/
    - Screenshots and page URLs are automatically embedded in the report on failure.

## Example Tests
### Passing Test (test_passed)

- Navigates to Google
- Takes a Percy snapshot
- Asserts "Google" is in the page title

### Failing Test (test_failed)

- Navigates to Google
- Asserts "Bing" is in the page title (expected failure to demonstrate screenshot/report)

## Notes

- Default browser is Chromium.
- Supported browsers: chromium, firefox, webkit.
- HTML report is customized with project metadata and screenshots.

---
