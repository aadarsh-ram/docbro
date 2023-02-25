# Docbro

## Introduction
Docbro is your brotha, when it comes to generating an automated documentation website from docstrings. This Python-based website generator can parse any file containing docstrings, written in any language.

This website generator requires a specialized docstring format, close to the reStructuredText docstring format. It generates markdown files first, then converts them to a static website for viewing.

Docbro also has configuration files (`.ignoredirs` and `.ignorefiles`) to ignore certain directories and files. A custom GitHub Action has also been written to automatically deploy the website, and for documentation version control.

## Docstring format
```
"""
docbrostart

:name: <function_name>
:description: <desc>
:param param1: this is a first param
:param param2: this is a second param
:returns: this is a description of what is returned
:raises keyError: raises an exception
:markdown_start:
<Some markdown>
:markdown_end:

docbroend
"""
```

## Check it out!
Visit [this link](https://aadarsh-ram.github.io/delta-hack-23/1.0.0/) to view a sample documentation website created by Docbro. The related project files, for which this site has been generated is present [here](https://github.com/aadarsh-ram/delta-hack-23/tree/main/src).

## Usage
- Create and activate a new virtualenv
```
python -m venv venv
. venv/bin/activate
```
- Install required packages
```
pip install -r requirements.txt
```
- Copy the contents of your project to the `src/` folder
    - Note: The `src/` folder must be present.
- Set the `PROJECT_NAME` environment variable to your project's name.
- Run the following command:
```
python3 docbro.py src/
```
- Your static website will be ready in the `docs/` folder
    - Note: An existing `/docs` folder will be cleared by Docbro
- The `workflows/` folder contains a CI/CD pipeline to automatically deploy the generated website in Github Pages.
    - Note: Remember to configure the `GITHUB_USERNAME` and `GITHUB_REPO` environment variables.
- To generate documentation for a new version of your project, change the `VERSION` environment variable and rerun workflow.