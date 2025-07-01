import tkinter as tk
from client_setup import create_qdrant_local_client, create_openai_client
from search import multi_stage_search
from chat import chat_with_openai
import os

class MovieBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 MovieBot")
        self.root.geometry("600x500")

        # Chat display (expandable)
        self.chat_area = tk.Text(root, wrap='word', state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Bottom input frame
        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        # Entry field (expandable)
        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        tk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.RIGHT)

        # Setup
        self.qdrant = create_qdrant_local_client()
        self.openai = create_openai_client()
        self.collection = "movie-rag-test"

        self.post("MovieBot", "Hello! Ask me for movie recommendations 🎬")

    def post(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.post("You", user_input)
        self.entry.delete(0, tk.END)

        results = multi_stage_search(self.collection, self.qdrant, user_input, limit=10)
        if not results:
            self.post("MovieBot", "Sorry, I couldn't find anything.")
            return

        reply = chat_with_openai(user_input, results, self.openai)
        self.post("MovieBot", reply)

def main():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    root = tk.Tk()
    MovieBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
