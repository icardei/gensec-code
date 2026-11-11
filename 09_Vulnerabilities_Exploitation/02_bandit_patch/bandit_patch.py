import os
from git import Repo
import subprocess
#from langchain_google_genai import ChatGoogleGenerativeAI
#llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def clone_repository():
    repo_url = input("Enter the repository URL: ")
    target_dir = "./bandit_repository_directory"
    if os.path.isdir(target_dir):
        subprocess.run(["rm", "-rf", target_dir], check=True)
    Repo.clone_from(repo_url, target_dir)
    print(f"Cloned {repo_url} into {target_dir}")
    return target_dir

def bandit_find_high_severity_files(repo_path):
    result = subprocess.run(
                ["bandit", "-r", repo_path, "--confidence-level", "high", "--severity-level", "high"],
                capture_output=True,
                text=True
             )
    bandit_results = result.stdout
    prompt = f"Analyze the results from the Bandit vulnerability scan and return a list of files with high confidence, high severity vulnerabilities in them.  For each, include the line numbers they occur in:\n\n{bandit_results}"
    response = llm.invoke(prompt)
    return response.content

def patch_file(repo_path):
    result = subprocess.run(
                ["bandit", repo_path],
                capture_output=True,
                text=True
             )
    bandit_results = result.stdout
    file_content = open(repo_path,"r", encoding="utf-8").read()
    prompt = f"You are a skilled patch generator that takes a program from a file and a description of its vulnerabilities and then produces a patch for the program in diff format that fixes the problems in the description.\n\n The contents of the program file are: \n {file_content}\n\n The description of the issues in it are: \n {bandit_results}"
    response = llm.invoke(prompt)
    return response.content

# Clone repository
repo_path = clone_repository()

# Analyze code with Bandit
print("Running Bandit to find high severity vulnerabilities...")
bandit_results = bandit_find_high_severity_files(repo_path)
print(f"Files with high severity vulnerabilities:")
print(bandit_results)

while True:
    fix_file = input("Enter a file with a high severity vulnerability for the LLM to fix: ")
    if (os.path.isfile(fix_file)):
        patch_results = patch_file(fix_file)
        print(patch_results)
        break;
    else:
        print("File does not exist.")
