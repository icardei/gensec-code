import os
import json
import requests
import subprocess
import readline
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def get_installed_packages(venv_path):
    python_exec = os.path.join(venv_path, "bin", "python")
    result = subprocess.run([python_exec, "-m", "pip", "list", "--format=json"], capture_output=True, text=True, check=True)
    packages = json.loads(result.stdout)
    installed_packages = {pkg["name"]:pkg["version"] for pkg in packages}
    return(installed_packages)

def check_vulnerabilities(installed_packages,package):
    post_data = {"package": {"name":package}, "version":installed_packages[package]}
    response = requests.post("https://api.osv.dev/v1/query", json=post_data)
    vuln_results = response.json()
    if vuln_results:
        vuln_report = "\n".join([vuln['details'] for vuln in vuln_results['vulns'] if 'details' in vuln])
        return(vuln_report)

def summarize_vulnerabilities(vuln_output):
    prompt = f"""You are a cybersecurity expert tasked with analyzing security vulnerabilities found in a Python package.  Provide a 100-word summary of each vulnerability found.

        Vulnerabilities:
        {vuln_output}

        """
    summary = llm.invoke(vuln_output)
    print(summary.content)
    return summary.content

if __name__ == "__main__":
    venv_directory = input("Welcome to my Python virtual environment package security analyzer.  Enter the path to a virtual environment for me to analyze: ")
    installed_packages = get_installed_packages(venv_directory)
    while True:
        print(f"The installed packages are: {installed_packages}.")
        print("Enter a package to analyze.  A blank line exits.")
        package = input("llm>> ")
        if package:
            if package in installed_packages:
                print(f"Analyzing {package} v{installed_packages[package]}...")
                report = check_vulnerabilities(installed_packages, package)
                if report:
                    summarize_vulnerabilities(report)
                else:
                    print("No vulnerabilities found")
            else:
                print("Package not found")
        else:
            break
