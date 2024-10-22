import os
import time
import streamlit as st

# Define the paths to your local or cloud folders
folders = ["./folder1", "./folder2", "./folder3", "./folder4"]
TIME_PERIOD = 15  # Time interval (in seconds)

# Function to load the available files from each folder
def get_files_in_folder(folder):
    return [f for f in os.listdir(folder) if f.endswith('.txt') and os.path.isfile(os.path.join(folder, f))]

# Function to read the content of the selected file
def load_file_content(folder, file):
    file_path = os.path.join(folder, file)
    with open(file_path, "r") as f:
        return f.read().strip()

# Custom CSS for responsiveness and styling
st.markdown("""
    <style>
    /* Make the text responsive and adjust the layout */
    .block-text {
        font-size: calc(12px + 1vw); /* Responsive text size */
        white-space: pre-wrap; /* Ensure text wraps on smaller screens */
        word-wrap: break-word;
    }

    /* Adjust columns for mobile screens */
    @media only screen and (max-width: 600px) {
        .block-column {
            flex-direction: column;
            width: 100%;
        }
    }

    /* Add some padding for readability */
    .streamlit-expanderHeader {
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Lauren's Sonnet")

# Create empty placeholders for each block that will be updated
columns = st.columns(len(folders))  # Create a column for each folder for responsiveness
placeholders = [column.empty() for column in columns]

# Initialize output areas and display the initial blocks with the first file's content
output_blocks = []
files_per_block = []

for i, folder in enumerate(folders):
    files = get_files_in_folder(folder)
    if files:
        file_content = load_file_content(folder, files[0])
        with placeholders[i]:
            st.text(file_content)

    output_blocks.append(file_content)
    files_per_block.append(files)

time.sleep(TIME_PERIOD)

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
                    st.markdown(f"<div class='block-text'>{file_content}</div>", unsafe_allow_html=True)

            time.sleep(TIME_PERIOD)  # Wait for the next update

# Automatically start the update process when the app is loaded
update_blocks_in_sequence()

