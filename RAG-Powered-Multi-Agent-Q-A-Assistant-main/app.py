from flask import Flask, request, render_template, redirect, url_for
from model_For_Rag import classify_query_with_chroma,retrieve_top_k
import re

app = Flask(__name__)

chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    if request.method == "POST":
        user_input = request.form["query"]
        chat_history.append(("user", user_input))
        route =  classify_query_with_chroma(user_input, top_k=3)  
        if route == "calculator":
            bot_reply = "Route for this Query: Calculator"
            chat_history.append(("bot", bot_reply))
        elif route == "dictionary":
            bot_reply = "Route for this Query: Dictionary"
            chat_history.append(("bot", bot_reply))
        else:
            bot_reply = "Route for this Query: RAG"
            chat_history.append(("bot", bot_reply))
            Top_reply = retrieve_top_k(query=user_input, k=3)  
            cleaned_reply = ""
            for i in range(len(Top_reply)):
                Top_reply[i] = Top_reply[i].replace("----", "")
                cleaned_reply += f"{str(i+1) }: {Top_reply[i]}\n\n\n" 
            chat_history.append(("bot", cleaned_reply))
        return redirect(url_for("index"))
    return render_template("chat.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
