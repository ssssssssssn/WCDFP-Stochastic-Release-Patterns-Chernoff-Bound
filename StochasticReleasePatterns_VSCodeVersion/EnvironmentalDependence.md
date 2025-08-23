# Environmental dependence
This experiment uses Python 3.8. Below is the guide to deploying and installing the required libraries on a Windows system:

## 1. Install Visual Studio Code
- Visit [Visual Studio Code](https://code.visualstudio.com/), and click the **"Download for Windows"** button.
- Run the downloaded installer (.exe file).
- Select **"I accept the agreement"** (A), then click Next.
- Choose the installation folder and click Next twice.
- Uncheck **"Register Code as an editor for supported file types"**, and check the other options, then click Next.
- Confirm the settings and click Install. Once installation is complete, open Visual Studio Code.

## 2. Install the Python Extension
- After opening VS Code, click the Extensions icon in the left activity bar.
- In the Extensions Marketplace, search for Python.
- Select the Python extension provided by Microsoft and click Install.

## 3. Install Python and Configure VS Code
- Visit the [Python official website](https://www.python.org/downloads/release/python-383/).
- Scroll down to the bottom and download the [Windows x86-64 executable installer](https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe).
- Run the installer, ensuring that **"Add Python to PATH"** is checked, then click Install Now.
- After installation, verify that Python is correctly installed by opening CMD and typing:
  ```bash
  python --version
## 4. Select the Python Interpreter in VS Code
- Press `Ctrl+Shift+P` to open the command palette.
- Type **"Python: Select Interpreter"** and select the installed Python version.

## 5. Open the Project and Activate the Virtual Environment
- Open Visual Studio Code.
- Click on **File** in the top-left corner.
- Click **Open Folder** and select the folder where your project is located.
- Choose **"Yes, I trust the authors."**
- Open the terminal in VS Code (**Terminal -> New Terminal**).
- Create a virtual environment in the folder:
  ```bash
  python -m venv .venv
- Activate the virtual environment:
    
    For CMD:
    ```
    .venv\Scripts\activate
    ```
    For PowerShell:
    ```
    .venv\Scripts\Activate.ps1
    ```
## 6. Install Required Libraries

Install the required libraries by running:
```
pip install mpmath scipy numpy matplotlib adjustText
```

### 7. Run the project
- Select and open the Python file you want to run.
- Right-click, find **"Run Python"** in the menu, and click **"Run Python File in Terminal."**