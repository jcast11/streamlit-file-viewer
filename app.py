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

st.title("Lauren's Sonnet")

# Create empty placeholders for each block that will be updated
placeholders = [st.empty() for _ in folders]

# Initialize output areas and display the initial blocks with the first file's content
output_blocks = []
files_per_block = []
st.write(get_files_in_folder(folder))
for i, folder in enumerate(folders):
    files = get_files_in_folder(folder)
    if files:
        file_content = load_file_content(folder, files[0])
        with placeholders[i]:
            #st.write(f"Displaying content from {files[0]} in Block {i + 1}:")
            st.text(file_content)

    output_blocks.append(file_content)
    files_per_block.append(files)
time.sleep(TIME_PERIOD)
# Define the update function
def update_blocks_in_sequence():
    current_file_indices = [0] * len(folders)

    while True:
        for i in {0,1,2}:
            files = files_per_block[i]
            if len(files) > 1:
                # Update file index and load the next file
                current_file_indices[i] = (current_file_indices[i] + 1) % len(files)
                next_file = files[current_file_indices[i]]
                file_content = load_file_content(folders[i], next_file)

                # Update the placeholder for the current block (replace the content)
                with placeholders[i]:
                    #st.write(f"Updating content from {next_file} in Block {i + 1}:")
                    st.text(file_content)

            time.sleep(TIME_PERIOD)  # Wait for the next update

# Automatically start the update process when the app is loaded
update_blocks_in_sequence()

