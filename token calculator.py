import tkinter as tk
from tkinter import scrolledtext

# --- Functions ---

def estimate_tokens(text):
    words = len(text.split())
    chars = len(text)
    tokens_by_chars = chars / 4
    tokens_by_words = words / 0.75
    return int(tokens_by_chars), int(tokens_by_words)

def estimate_cost(input_tokens, output_tokens, model="Claude3.5"):
    pricing = {
        "Claude3.5": {"input": 3, "output": 15},  # $ per million tokens
        "GPT4": {"input": 3, "output": 12}
    }
    if model not in pricing:
        raise ValueError("Unknown model")
    cost = (input_tokens * pricing[model]["input"] + output_tokens * pricing[model]["output"]) / 1_000_000
    return round(cost, 4)

def calculate():
    input_text = input_box.get("1.0", tk.END).strip()
    output_text = output_box.get("1.0", tk.END).strip()
    
    input_tokens_chars, input_tokens_words = estimate_tokens(input_text)
    output_tokens_chars, output_tokens_words = estimate_tokens(output_text)
    
    total_tokens_chars = input_tokens_chars + output_tokens_chars
    total_tokens_words = input_tokens_words + output_tokens_words
    
    result = f"""--- Token Estimates ---
Input Tokens: {input_tokens_chars} (chars), {input_tokens_words} (words)
Output Tokens: {output_tokens_chars} (chars), {output_tokens_words} (words)
Total Tokens: {total_tokens_chars} (chars), {total_tokens_words} (words)

--- Cost Estimates ---
Claude3.5: ${estimate_cost(input_tokens_chars, output_tokens_chars, 'Claude3.5')}
GPT4: ${estimate_cost(input_tokens_chars, output_tokens_chars, 'GPT4')}
"""
    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result)
    result_box.config(state='disabled')

# --- GUI Setup ---

root = tk.Tk()
root.title("Token & Cost Estimator")

tk.Label(root, text="Input Text:").grid(row=0, column=0, sticky="w")
input_box = scrolledtext.ScrolledText(root, width=80, height=10)
input_box.grid(row=1, column=0, padx=5, pady=5)

tk.Label(root, text="Expected Output Text:").grid(row=2, column=0, sticky="w")
output_box = scrolledtext.ScrolledText(root, width=80, height=10)
output_box.grid(row=3, column=0, padx=5, pady=5)

calc_button = tk.Button(root, text="Calculate Tokens & Cost", command=calculate)
calc_button.grid(row=4, column=0, pady=10)

result_box = scrolledtext.ScrolledText(root, width=80, height=10, state='disabled')
result_box.grid(row=5, column=0, padx=5, pady=5)

root.mainloop()
