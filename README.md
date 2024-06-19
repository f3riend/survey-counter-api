# Python Flask-API

## Story
Our school requested the development of a survey program: "We want you to develop a survey program for our school so that teachers and administrators can create surveys whenever they want. Only people in the specified category can participate in these surveys. Additionally, we want to view the survey results and download a survey as a PDF whenever we want." To fulfill this request, I developed an API using Python that visualizes the survey data.

## Purpose
The primary purpose of this project is to count and visualize the answers to survey questions. The API processes survey data, creates visualizations, converts them to base64 format, and sends them back to the website for display.

## Working Logic and Flowchart
The website sends a predetermined JSON structure to the API using JavaScript. The API processes the received data, generates visualizations, converts the visualizations to base64 format, and then returns them to the website.

![flowchart](https://github.com/f3riend/flask-counter-api/blob/main/followchart.png)

## JSON Structure
Here is an example of the JSON structure expected by the API:

Request Sample
```json
{
  "questions": [
    {
      "question": "How do you rate our school?",
      "answers": ["Excellent", "Good", "Average", "Poor"],
      "response": ["Good", "Excellent", "Good", "Average", "Poor", "Good"]
    },
    {
      "question": "Would you recommend our school to others?",
      "answers": ["Yes", "No"],
      "response": ["Yes", "Yes", "No", "Yes"]
    }
  ]
}
```
Response Sample

```json
{
  "plots": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  ]
}
```
