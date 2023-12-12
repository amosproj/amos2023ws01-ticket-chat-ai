# Research on Confidence Score for NLPs
The **Confidence Score** indicates how sure an NLP service / machine learning model is that the respective intent was correctly assigned. 
The score can have a value between 0 and 1 or 0 and 100, depending on the machine learning model.

Example of the meaning of a score value:

| Score Value | 	Score Meaning                                                                                           |
|-------------|----------------------------------------------------------------------------------------------------------|
| 90 - 100    | A near exact match of user query and a Knowledge Base question.                                          |
| 70 - 90     | High confidence - typically a good answer that completely answers the user's query                       |
| 50 - 70     | Medium confidence - typically a fairly good answer that should answer the main intent of the user query  |
| 30 - 50     | Low confidence - typically a related answer, that partially answers the user's intent                    |
| < 30        | Very low confidence - typically does not answer the user's query, but has some matching words or phrases |
| 0           | No match, so the answer is not returned.                                                                 |

Is a confidence score the right metric to use to evaluate a text generation model?
Thread with different opinions: https://stats.stackexchange.com/questions/589520/does-the-concept-of-confidence-apply-to-text-generation-tasks

**Research Conclusion until now:** Confidence Score Calculation couldn't be implemented for our type of AI model.

### Alternative Solution / Suggestion:
Implement a rating system, where the user rates the output of our AI model in a scale of 1 - 10.
The rating is saved on the database as another attribute of the generated ticket. 

After a meaningful number of tickets and ratings are created, we can calculate the average rating of all the tickets and evaluate our AI model based on that metric.