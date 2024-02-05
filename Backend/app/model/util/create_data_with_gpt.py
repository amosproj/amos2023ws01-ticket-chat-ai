from openai import OpenAI
import json

client = OpenAI(api_key="<APIKEY>")

for _ in range(1):
    with open("../test_data/test_data_with_gpt/data_9.json", "r") as file:
        tickets = json.load(file)

    for _ in range(100):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": """
                        Please create a data set for support requests and tickets in the specified JSON format:
                        
                        "text": [
                              Here should stay the Problem Description
                        ],
                        "ticket": {
                            "service": "",
                            "category": "",
                            "customerPriority": "",
                            "priority": "",
                            "requestType": ""
                        }
                        
                        The 'text' should contain a detailed problem description with implicit information about the problem .
                        The 'text' should be randomly between 5 to 10 lines
                        Furthermore, under 'ticket', there should be a support ticket matching the email with the following attributes.
                        The 'service' attribute classifies the service of the ticket with the values 'SAP ERP', 'Atlassian', 'Adobe', 'Salesforce', 'Reporting', 'Microsoft Power Platform', 'Microsoft SharePoint', 'Snowflake', 'Microsoft Office'.
                        The 'category' attribute classifies the category of the ticket with values 'Technical Issues', 'Billing & Payment', 'Product Inquiries', 'Account Management', 'Policy Questions'.
                        The 'customerPriority' attribute describes the impact of the problem on the customer and can take the values "Disruption but can work" "Disruption cannot work" "Disruption several cannot work" and "Disruption department cannot work".
                        The 'priority' attribute classifies the relevance of the ticket with the values 'Low', 'Medium', 'High' and 'Very High'
                        The 'requestType' attribute classifies the type of ticket with the values "Incident" or 'Service Request'. Incident describes a ticket if the user has a problem or similar, and Service Request describes a ticket with which the user orders a service.
                        
                        Please create 10 tickets in the specified JSON format. The ticket should be really versatile.
                        Your output should only contain the JSON format.
                    """,
                    },
                ],
            )

            response_str = response.choices[0].message.content
            start_index = response_str.find("[")
            end_index = response_str.rfind("]")
            tickets_str = response_str[start_index : end_index + 1]

            tickets_batch = json.loads(tickets_str)

            tickets.extend(tickets_batch)

        except Exception as e:
            print(f"An error occurred: {e}")

    with open("../test_data/test_data_with_gpt/data_9.json", "w") as file:
        json.dump(tickets, file, indent=4)
