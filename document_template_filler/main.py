from jinja2 import Environment, FileSystemLoader
import os

class DocumentTemplateFiller:
    def __init__(self, template_folder='templates', output_folder='output'):
        self.template_folder = template_folder
        self.output_folder = output_folder
        self.env = Environment(loader=FileSystemLoader(template_folder))

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def fill_template(self, template_name, data, output_name):
        template = self.env.get_template(template_name)
        output_path = os.path.join(self.output_folder, output_name)
        
        with open(output_path, 'w') as output_file:
            output_file.write(template.render(data))

        print(f"Document '{output_name}' generated successfully at '{output_path}'.")

if __name__ == "__main__":
    # Initialize the DocumentTemplateFiller
    template_filler = DocumentTemplateFiller()

    # Example data (you can replace this with user input or data retrieval logic)
    user_data = {
        'name': 'John Doe',
        'company': 'ABC Corp',
        'date': '2024-01-07',
        'content': 'This is the content of the document.'
    }

    # Example template filling
    template_filler.fill_template('example_template.txt', user_data, 'filled_document.txt')