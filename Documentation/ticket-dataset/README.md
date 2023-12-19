# Research on a Ticket Dataset

## Customer Support Ticket Dataset

Link: [kaggle.com](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/)

### Example Ticket Structure

```json
{
  "ticketSubject": "Problems with Technic",
  "ticketDescription": "...some text...",
  "ticketType": "technical issue",
  // technical issue, billing inquiry, product inquiry
  "ticketPriority": "low",
  // low, medium, high, critical
  "ticketChannel": "chat",
  // email, phone, chat, social media
  "customerName": "",
  "productPurchased": ""
}
```

The ticket content would be in English, not in German language, and all other fields than them above would be empty.

### How to Use the Dataset?

1. Extract the above-mentioned useful fields
2. Rename them as needed and add missing fields as empty values
3. Mutate the values as needed (e.g., replace "social media" channel with "chat")
4. Use the description twice, once for the ticket description field and also for the text input, that could be changed
   for "email" channel having some additional lines as "Hello Support-Team, ..."
5. Store the preprocessed dataset
6. Train the ticket creation with the new dataset 