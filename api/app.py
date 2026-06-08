from fastapi import FastAPI

app = FastAPI()

@app.get("/chat")
def chat(question: str = "hello"):

    with open("data/company_policy.txt", "r") as file:
        policies = file.readlines()

    answer = "Sorry, I could not find information about that."

    for line in policies:
        if question.lower() in line.lower():
            answer = line.strip()
            break

    return {
        "question": question,
        "answer": answer
    }