import context
from context import llm_model
import litellm


failure = "failure"


def log(m):
    print("[LOG] " + m)


def ask_llm_for_refactoring(spec: str, code: str) -> str:
    try:
        chat_response = litellm.completion(
            model=llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "Given a specification of a system, and a source code,"
                    " propose an improvement of the code that does not change its behavior. First give the proposed code, then explain shortly.",
                },
                {
                    "role": "user",
                    "content": "Specification: "
                    + spec
                    + "(end of the specification) Source code: "
                    + code
                    + "(end of code).",
                },
            ],
            max_tokens=context.max_token,
        )
        res = chat_response.choices[0].message.content
        log("I had an interaction with " + llm_model + " to suggest improvements.")
        log("I gave the following spec: " + spec)
        log("I also gave the following code: " + code)
        log("The LLM gave me the following answer: " + res)
        return res
    except Exception as e:
        print(str(e))
        raise Exception("LLM failure: " + str(type(e))) from e
