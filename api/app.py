from fastapi import FastAPI
app = FastAPI()
@app.get("/chat")
def chat(question: str = "hello"):

    q = question.lower()

    if "leave" in q:
        answer = "You can apply leave through the employee portal."

    elif "salary" in q:
        answer = "Salary is credited on the last working day of the month."

    elif "working hours" in q:
        answer = "Working hours are 9 AM to 6 PM."

    elif "dress code" in q:
        answer = "Business casual dress code is followed."

    elif "holiday" in q:
        answer = "Refer to the company holiday calendar."

    else:
        answer = "Sorry, I do not have information about that."

    return {
        "question": question,
        "answer": answer
    }