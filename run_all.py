import json
import subprocess
import os
import pandas as pd

# Load the JSONL data
jsonl_file_path = '/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/tasks_test.jsonl'
data = []
with open(jsonl_file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Load the CSV file with VIN and part type
csv_file_path = '/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/voyager_test_set.xlsx'
csv_data = pd.read_excel(csv_file_path)

# Ensure the CSV has the required columns
required_columns = ['vin', 'part_type']
if not all(col in csv_data.columns for col in required_columns):
    raise ValueError(f"CSV file must contain the following columns: {required_columns}")

# Create output directory for individual JSONL files
individual_files_dir = '/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/test_tasks'
# os.makedirs(individual_files_dir, exist_ok=True)

# Combine JSONL data with each VIN and part type from the CSV
file_paths = []
for idx, row in csv_data.iterrows():
    vin = row['vin']
    part_type = row['part_type']
    expanded_data = []
    for json_row in data:
        new_row = json_row.copy()
        new_row['ques'] = (
            f"Your task is to find cars on a website. Visit the {json_row['web_name']} website and search "
            f"for the car using the VIN {vin}. After you have entered the VIN, a new webpage will open, which has "
            f"the search results. After this there will be a hyper-linked Model code of the car. Please go to that "
            f"hyper link. A new webpage will open up. In this webpage, search for the part '{part_type}' "
            f"in the search bar. A new webpage will open up. In this webpage, click on the hyperlinked text of part "
            f"type. After clicking, a new webpage will open up. In this webpage look for details of the {part_type}."
        )
        expanded_data.append(new_row)

    # Save each expanded data set to a separate JSONL file
    output_file_path = os.path.join(individual_files_dir, f'task_{idx + 1}.jsonl')
    with open(output_file_path, 'w') as file:
        for item in expanded_data:
            file.write(json.dumps(item) + '\n')
    file_paths.append(output_file_path)

    print(f"Task data saved to {output_file_path}")

tasks = "/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/test_tasks"
# Step 2: Run the agent script (run.py) for each file
for file_path in file_paths:
    try:
        print(f'Processing file: {file_path}')
        subprocess.run([
            "python", "run.py",
            "--test_file", file_path,
            "--max_iter", "10",
            "--output_dir", r"/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/results",
            "--temperature", "1"
        ], check=True)
        print(f"Agent execution completed successfully for {file_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during agent execution for {file_path}: {e}")

# Uncomment this section if you want to process interaction messages
# interaction_file_path = r'/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/interact_messages.json'
# with open(interaction_file_path, 'r') as file:
#     interaction_data = json.load(file)

# answers = []
# for message in interaction_data:
#     if message['role'] == 'assistant' and 'ANSWER;' in message['content']:
#         answer_content = message['content'].split('ANSWER; ')[-1].strip()
#         answers.append(answer_content)

# # Append the results to the CSV
# results_df = csv_data.copy()
# results_df['Answer'] = answers[:len(csv_data)]  # Match the length of the answers with the CSV
# results_csv_path = r'/mnt/d/Dismantly/agent2.0/WebVoyager/test/ToyoDiy/results_with_answers.csv'
# results_df.to_csv(results_csv_path, index=False)

# print(f"Final results with answers saved to: {results_csv_path}")
