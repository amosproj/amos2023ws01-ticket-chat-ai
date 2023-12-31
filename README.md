# Ticket-Chat-AI Project (AMOS WS 2023)

## Setup

1. **Clone the Repository**:

   ```bash
   git clone git@github.com:amosproj/amos2023ws01-ticket-chat-ai.git
   ```

## Code Standards and Linting

Superlinter is configured to check the code standards for:

- JavaScript
- Python

### Using Linters Locally

Ensure code standards are met before pushing your changes using either VSCode Extensions or shell commands.

#### Use Extensions in VSCode

Install the following extensions in VSCode and follow the instructions on the installation site, or use the provided instructions:

- Open the file you want to format.
- For Python, use the Black extension (Alt+Shift+F).
- For JavaScript, use the ESLint extension (Alt+Shift+F).

#### Use Shell Commands

Before running the commands, ensure that the required packages are installed by checking and installing from the `requirements.txt` and the `package.json` file.

##### Python - Black Formatter

[Black](https://black.readthedocs.io/en/stable/) is a Python code formatter that automatically formats your code.

- **Usage:**
   Format a single file:

   ```bash
   black your_file.py
   ```

   Format multiple files or a directory:

   ```bash
   black file1.py file2.py directory/
   ```

##### JavaScript - ESLint

[ESLint](https://eslint.org/) is a linting utility for JavaScript.

- **Usage:**
   Lint a JavaScript file:

   ```bash
   npx eslint your_script.js
   ```

   For linting an entire directory:

   ```bash
   npx eslint .
   ```
