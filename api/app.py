from fastapi import FastAPI

app = FastAPI()

@app.get("/chat")
def chat(question: str = "hello"):

    with open("data/company_policy.txt", "r") as file:
        policies = file.readlines()

    q = question.lower()

    answer = "Sorry, I do not have information about that."

    for line in policies:
        if q in line.lower():
            answer = line.strip()
            break

    return {
        "question": question,
        "answer": answer
    }