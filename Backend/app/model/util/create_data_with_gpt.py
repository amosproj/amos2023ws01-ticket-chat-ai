from openai import OpenAI
import json

client = OpenAI(api_key="<APIKEY>")

for _ in range(5):
    with open("../test_data/test_data_with_gpt/data_11.json", "r") as file:
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
                        The 'category' attribute classifies the problem dependent from service. Please extract the values from following. Before ':' states the service and after ':' are the coresponding values.  '"SAP ERP: 4HANA -> Technical Issues, 4HANA -> Billing & Payment, 4HANA -> Product Inquiries, 4HANA -> Account Management, 4HANA -> Policy Questions"
                            "SAP ERP: HANA -> Technical Issues, HANA -> Billing & Payment, HANA -> Product Inquiries, HANA -> Account Management, HANA -> Policy Questions"
                            "SAP ERP: Business One -> Technical Issues, Business One -> Billing & Payment, Business One -> Product Inquiries, Business One -> Account Management, Business One -> Policy Questions"
            
                            "Atlassian: Jira -> Technical Issues, Jira -> Billing & Payment, Jira -> Product Inquiries, Jira -> Account Management, Jira -> Policy Questions"
                            "Atlassian: Sourcetree -> Technical Issues, Sourcetree -> Billing & Payment, Sourcetree -> Product Inquiries, Sourcetree -> Account Management, Sourcetree -> Policy Questions"
            
                            "Adobe: Illustrator -> Technical Issues, Illustrator -> Billing & Payment, Illustrator -> Product Inquiries, Illustrator -> Account Management, Illustrator -> Policy Questions"
                            "Adobe: Photoshop -> Technical Issues, Photoshop -> Billing & Payment, Photoshop -> Product Inquiries, Photoshop -> Account Management, Photoshop -> Policy Questions"
                            
                            "Salesforce: Apex -> Technical Issues, Apex -> Billing & Payment, Apex -> Product Inquiries, Apex -> Account Management, Apex -> Policy Questions"
                            "Salesforce: Trailhead -> Technical Issues, Trailhead -> Billing & Payment, Trailhead -> Product Inquiries, Trailhead -> Account Management, Trailhead -> Policy Questions"
                            
                            "Reporting: Tableau -> Technical Issues, Tableau -> Billing & Payment, Tableau -> Product Inquiries, Tableau -> Account Management, Tableau -> Policy Questions"
                            "Reporting: Microsoft PowerBI -> Technical Issues, Microsoft PowerBI -> Billing & Payment, Microsoft PowerBI -> Product Inquiries, Microsoft PowerBI -> Account Management, Microsoft PowerBI -> Policy Questions"
                            
                            "Microsoft Power Platform: Microsoft Power Apps -> Technical Issues, Microsoft Power App -> Billing & Payment, Microsoft Power App -> Product Inquiries, Microsoft Power App -> Account Management, Microsoft Power App -> Policy Questions"
                            "Microsoft Power Platform: Microsoft Power BI -> Technical Issues, Microsoft Power BI -> Billing & Payment, Microsoft Power BI -> Product Inquiries, Microsoft Power BI -> Account Management, Microsoft Power BI -> Policy Questions"
                           
                            "Microsoft SharePoint: Microsoft SharePoint -> Technical Issues, Microsoft SharePoint -> Billing & Payment, Microsoft SharePoint -> Product Inquiries, Microsoft SharePoint -> Account Management, Microsoft SharePoint -> Policy Questions"
                            "Microsoft SharePoint: SharePoint -> Technical Issues, SharePoint -> Billing & Payment, SharePoint -> Product Inquiries, SharePoint -> Account Management, SharePoint -> Policy Questions"
                            
                            
                            "Snowflake: Snowflake -> Technical Issues, Snowflake -> Billing & Payment, Snowflake -> Product Inquiries, Snowflake -> Account Management, Snowflake -> Policy Questions"
                            "Snowflake: SnowSQL -> Technical Issues, SnowSQL -> Billing & Payment, SnowSQL -> Product Inquiries, SnowSQL -> Account Management, SnowSQL -> Policy Questions"
                            
                            "Microsoft Office: Microsoft Office -> Technical Issues, Microsoft Office -> Billing & Payment, Microsoft Office -> Product Inquiries, Microsoft Office -> Account Management, Microsoft Office -> Policy Questions"
                            "Microsoft Office: Microsoft Word -> Technical Issues, Microsoft Word -> Billing & Payment, Microsoft Word -> Product Inquiries, Microsoft Word -> Account Management, Microsoft Word -> Policy Questions" 
                        one category values is f.e SnowSQL -> Billing & Payment.
                        
                        
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

    with open("../test_data/test_data_with_gpt/data_11.json", "w") as file:
        json.dump(tickets, file, indent=4)
