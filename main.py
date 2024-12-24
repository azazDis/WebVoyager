from webvoyager import WebAgent

# Configuration
TOYODIY_URL = "https://www.toyodiy.com/parts/q.html"
VIN_INPUT_FIELD = "vin"
DEFAULT_VIN = "JT764AEB103102883"
DEFAULT_PART = "alternator assembly"

def main(vin=DEFAULT_VIN, part=DEFAULT_PART):
    # Initialize WebVoyager Agent
    agent = WebAgent(model="gpt-4-vision")  # Use WebVoyager's multimodal model
    agent.open(TOYODIY_URL)

    # Task 1: Input VIN
    agent.type_in_field(field_name=VIN_INPUT_FIELD, text=vin)
    agent.submit_form(field_name=VIN_INPUT_FIELD)

    # Task 2: Search for Part
    query = f"Find the OEM# for the {part}."
    result = agent.extract_data(prompt=query)

    # Display Results
    if result:
        print("Extracted Data:")
        print(result)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
