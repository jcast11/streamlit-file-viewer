import os
import time
import streamlit as st

# Define the paths to your local folders
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

# Display initial blocks with the first file's content
output_blocks = []
files_per_block = []

for i, folder in enumerate(folders):
    files = get_files_in_folder(folder)
    if files:
        file_content = load_file_content(folder, files[0])
        st.write(f"Displaying content from {files[0]} in Block {i + 1}:")
        st.text(file_content)

    output_blocks.append(file_content)
    files_per_block.append(files)

# Define the update function
def update_blocks_in_sequence():
    current_file_indices = [0] * len(folders)

    while True:
        for i in range(len(folders)):
            files = files_per_block[i]
            if len(files) > 1:
                current_file_indices[i] = (current_file_indices[i] + 1) % len(files)
                next_file = files[current_file_indices[i]]
                file_content = load_file_content(folders[i], next_file)
                st.write(f"Updating content from {next_file} in Block {i + 1}:")
                st.text(file_content)

            time.sleep(TIME_PERIOD)  # Wait for the next update

if st.button("Start"):
    update_blocks_in_sequence()
