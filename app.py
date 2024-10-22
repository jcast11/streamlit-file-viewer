import os
import time
import streamlit as st

# Define the paths to your local or cloud folders
folders = ["./folder1", "./folder2", "./folder3", "./folder4"]
TIME_PERIOD = 15  # Time interval (in seconds)

# Function to load the available files from each folder
def get_files_in_folder(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

# Function to read the content of the selected file
def load_file_content(folder, file):
    file_path = os.path.join(folder, file)
    with open(file_path, "r") as f:
        return f.read().strip()

st.title('File Content Viewer')

# Create empty placeholders for each block that will be updated
placeholders = [st.empty() for _ in folders]

# Initialize output areas and display the initial blocks with the first file's content
output_blocks = []
files_per_block = []

# Define a function to render the content with custom font size
def display_file_content_with_font_size(block_number, file_name, file_content, font_size=20):
    html_content = f"""
    <div style="font-size: {font_size}px;">
        <strong>Displaying content from {file_name} in Block {block_number}:</strong><br><br>
        <pre>{file_content}</pre>
    </div>
    """
    return html_content

for i, folder in enumerate(folders):
    files = get_files_in_folder(folder)
    if files:
        file_content = load_file_content(folder, files[0])
        with placeholders[i]:
            st.markdown(display_file_content_with_font_size(i + 1, files[0], file_content, font_size=25), unsafe_allow_html=True)

    output_blocks.append(file_content)
    files_per_block.append(files)

# Define the update function
def update_blocks_in_sequence():
    current_file_indices = [0] * len(folders)

    while True:
        for i in range(len(folders)):
            files = files_per_block[i]
            if len(files) > 1:
                # Update file index and load the next file
                current_file_indices[i] = (current_file_indices[i] + 1) % len(files)
                next_file = files[current_file_indices[i]]
                file_content = load_file_content(folders[i], next_file)

                # Update the placeholder for the current block (replace the content)
                with placeholders[i]:
                    st.markdown(display_file_content_with_font_size(i + 1, next_file, file_content, font_size=20), unsafe_allow_html=True)

            time.sleep(TIME_PERIOD)  # Wait for the next update

# Automatically start the update process when the app is loaded
update_blocks_in_sequence()


