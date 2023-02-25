import argparse
import shutil
import os
import markdown

baseURL = os.environ.get('BASE_URL', 'https://aadarsh-ram.github.io/delta-hack-23/')
TEMPLATE = f"""<!DOCTYPE html>
<html>
<head>
    <base href="{baseURL}" target="_blank">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="referrer" content="no-referrer" />
    <meta name="referrer" content="unsafe-url" />
    <meta name="referrer" content="origin" />
    <meta name="referrer" content="no-referrer-when-downgrade" />
    <meta name="referrer" content="origin-when-cross-origin" />
    <title>Page Title</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">\n
    """ + """
    <style>
        body {
            font-family: Helvetica,Arial,sans-serif;
        }
        code, pre {
            font-family: monospace;
        }
    </style>
</head>
<body>
<div class="container">
{{content}}
<a href="index.html">Back to root directory</a>
</div>
</body>
</html>
"""

class Docbro:
    """
    Docbro is your brotha for generating documentation from docstrings in Python
    """
    def parse_file(self, filename):
        """
        Parse a file and return a list of docstrings
        """
        docstrings = []
        with open(filename, 'r') as f:
            curr_docstring = {}
            can_parse = False
            for line in f:
                line = line.strip()

                # Check if we are in a docstring
                if line.startswith('docbrostart'):
                    can_parse = True

                # Check if we are at the end of a docstring
                elif line.startswith('docbroend'):
                    docstrings.append(curr_docstring)
                    curr_docstring = {}
                    can_parse = False
                
                # Parse the docstring
                elif can_parse:
                    if line: # Ignore empty lines
                        splitted = line.split(':')

                        # Parse name, description, returns
                        if splitted[1] in ['name', 'description', 'returns']:
                            curr_docstring[splitted[1]] = splitted[2].strip()
                        
                        # Parse params and raises
                        elif splitted[1].split()[0] == 'param':
                            param_object = {}
                            param_object['name'] = splitted[1].split()[1]
                            param_object['description'] = splitted[2].strip()
                            if curr_docstring.get('params', -1) != -1:
                                curr_docstring['params'].append(param_object)
                            else:
                                curr_docstring['params'] = [param_object]
                        
                        elif splitted[1].split()[0] == 'raises':
                            raise_object = {}
                            raise_object['type'] = splitted[1].split()[1]
                            raise_object['description'] = splitted[2].strip()
                            if curr_docstring.get('raises', -1) != -1:
                                curr_docstring['raises'].append(raise_object)
                            else:
                                curr_docstring['raises'] = [raise_object]
        return docstrings
    
    def generate_markdown(self, docstrings):
        """
        Generate markdown from a list of docstrings
        """
        markdown_output = []
        start_docstring = docstrings[0]
        markdown_output.append('# {}'.format(start_docstring['name']))
        markdown_output.append('## Description')
        markdown_output.append(start_docstring['description'])
        markdown_output.append('## Functions')

        for docstring in docstrings[1:]:
            markdown_output.append('### `{}`'.format(docstring['name']))
            markdown_output.append(docstring.get('description', 'No description provided'))

            # Generate markdown for params
            markdown_output.append('#### Parameters')
            if docstring.get('params', {}) == {}:
                markdown_output.append('No parameters provided')
            else:
                for param in docstring['params']:
                    markdown_output.append('- `{}`: {}'.format(param['name'], param['description']))

            # Generate markdown for returns
            markdown_output.append('#### Returns')
            if docstring.get('returns', {}) == {}:
                markdown_output.append('No return value provided')
            else:
                markdown_output.append(docstring['returns'])

            # Generate markdown for raises
            markdown_output.append('#### Raises')
            if docstring.get('raises', {}) == {}:
                markdown_output.append('No exceptions provided')
            else:
                for raise_object in docstring['raises']:
                    markdown_output.append('- `{}`: {}'.format(raise_object['type'], raise_object['description']))

        return "\n".join(markdown_output)
    
    def parse_project(self, project_path):
        """
        Parse a project and return a list of docstrings
        """
        if os.path.exists('docs'):
            shutil.rmtree('docs')
        os.makedirs('docs')

        project_name = os.path.basename(os.path.normpath(project_path))
        if os.path.exists(f'docs/{project_name}'):
            os.remove(f'docs/{project_name}')
        os.makedirs(f'docs/{project_name}')

        for root, dirs, files in os.walk(project_path, topdown=True):
            # Ignore directories and files
            exclude_dirs = open('.ignoredirs').readlines()
            exclude_files = open('.ignorefiles').readlines()
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            files[:] = [f for f in files if f not in exclude_files]

            # Create directories
            new_root = os.path.join(f'docs/{project_name}', root[len(project_path):])
            if not os.path.exists(new_root):
                os.makedirs(new_root)

            for file in files:
                docstrings = self.parse_file(os.path.join(root, file))
                if docstrings:
                    # Generate markdown
                    markdown_content = self.generate_markdown(docstrings)
                    html = markdown.markdown(markdown_content, extensions=['extra', 'smarty'], output_format='html5')
                    doc = TEMPLATE.replace('{{content}}', html)
                    f = open(os.path.join(new_root, file.split('.')[0] + '.html'), 'w')
                    f.write(doc)
                    f.close()
        
        self.create_index(f'docs/', project_name)
        return 'Docbro has generated documentation for your project!'
    
    def create_index(self, output_path, project_name):
        """
        Create an index.html file for the project
        """
        index = open(os.path.join(output_path, 'index.html'), 'w')
        content = []
        content.append('<html><body>')
        content.append('<h1>Documentation for {}</h1>'.format(project_name))
        for root, dirs, files in os.walk(output_path+project_name, topdown=True):
            content.append('<h2>{}</h2>'.format(root[len(output_path):]))
            content.append('<ul>')
            for file in files:
                if file.endswith('.html'):
                    content.append(f'<li><a href="{os.path.join(root[len(output_path):], file)}">{file}</a></li>')
            content.append('</ul>')
        content.append('</body></html>')
        html = TEMPLATE.replace('{{content}}', '\n'.join(content))
        index.write(html)
        index.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Docbro is a tool for generating documentation from docstrings in Python')
    parser.add_argument('project_path', help='Path to the project')
    args = parser.parse_args()
    docbro = Docbro()
    print (docbro.parse_project(args.project_path))