import os
import sys

def should_skip(file_path, extension=None):
    skip_patterns = ['.git', "__pycache__", "__init__", "test_pages", "repo2text"]
    for pattern in skip_patterns:
        if pattern in file_path:
            return True
    # Only skip non-matching files if an extension is specified
    if extension and not file_path.endswith('.' + extension):
        return True
    return False

def directory_to_text(extension=None):
    # Specify the directory path
    dir_path = '/Users/sachabanks/Desktop/data-dudes-dash'
    output_file = os.path.join(dir_path, 'output.txt')
    
    # Ensure the directory exists
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist.")
        return

    # Write the directory contents to the output file
    with open(output_file, 'w', encoding='utf-8') as file_output:
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if should_skip(file_path, extension):
                    continue
                relative_path = file_path[len(dir_path)+1:]
                file_output.write(f"========== FILE: {relative_path} ==========\n\n")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_input:
                        file_output.write(file_input.read())
                except Exception as e:
                    file_output.write(f"Error reading file: {e}")
                file_output.write("\n\n \n\n")
    
    print(f"Directory contents have been written to {output_file}")

def main():
    # Check if an extension is provided as a command-line argument
    extension = None
    if len(sys.argv) > 1:
        extension = sys.argv[1].strip('.').lower()
    
    # Call the function with the optional file extension
    directory_to_text(extension)

if __name__ == '__main__':
    main()
