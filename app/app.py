import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
from ttkthemes import ThemedTk
import tkinter.font as tkFont
import pandas as pd
import sys
import os
import json
import nltk
from collections import Counter
from itertools import combinations
from nltk.tokenize import word_tokenize
from nltk.draw import dispersion_plot
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
from nltk.text import Text
from tkinter import PhotoImage

# Inizializza la finestra principale
root = ThemedTk(theme="equilux")
root.iconbitmap('favicon_app.ico')
root.title("LinguaGraph")
#root.geometry("1024x768")
root.configure(background="#333333")

# Configura il font personalizzato
custom_font = tkFont.Font(family="Roboto", size=8)

def update_status(label, text):
    label.config(text=text)
    label.update_idletasks()

# Funzione per nascondere la loading screen e mostrare la main window
def finish_loading(loading_screen, main_window):
    loading_screen.destroy()  # Chiudi la loading screen
    main_window.deiconify()  # Mostra la finestra principale
    show_welcome_message()   # Mostra il messaggio di benvenuto dopo il caricamento

# Funzione per mostrare la loading screen
def show_loading_screen(main_window):
    # Nasconde temporaneamente la main window
    main_window.withdraw()

    # Crea una nuova finestra top-level per la schermata di caricamento
    loading_screen = tk.Toplevel()
    loading_screen.title("LinguaGraph Loading...")
    loading_screen.geometry('800x600')  # Imposta le dimensioni della finestra di caricamento
    loading_screen.overrideredirect(True)  # Rimuove la barra del titolo

    # Carica e mostra l'immagine di caricamento
    image_path = 'LinguaGraph.png'  # Sostituisci con il percorso effettivo della tua immagine
    image = PhotoImage(file=image_path)
    background_label = tk.Label(loading_screen, image=image)
    background_label.photo = image
    background_label.pack()

    # Aggiunge un messaggio di stato sopra l'immagine di caricamento
    status_label = tk.Label(loading_screen, text="Loading files, please wait...", bg="#000000", fg="white")
    status_label.place(relx=0.5, rely=0.5, anchor='center')



    # Aggiunge un messaggio di stato
    status_label = tk.Label(loading_screen, text="Loading...")
    status_label.pack()

    # Aggiorna lo stato dopo un certo intervallo (esempio: 1000ms = 1 secondo)
    loading_screen.after(5000, lambda: update_status(status_label, "Almost done..."))

    # Simula il completamento del caricamento dopo un altro intervallo
    loading_screen.after(10000, lambda: finish_loading(loading_screen, main_window))

    # Centra la loading screen sullo schermo
    center_window(loading_screen)

# Funzione per centrare la finestra sullo schermo
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

show_loading_screen(root)

prefs_file = 'user_preferences.json'
def load_preferences():
    if os.path.exists(prefs_file):
        with open(prefs_file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_preferences(prefs):
    with open(prefs_file, 'w') as f:
        json.dump(prefs, f, indent=4)

user_preference = load_preferences()
def show_welcome_message():
    # Verifica se l'utente ha già scelto di non mostrare il messaggio
    if user_preference.get('dont_show_again', False):
        return

    welcome_window = tk.Toplevel(root)
    welcome_window.title("Welcome to LinguaGraph!")

    welcome_text = """Welcome to LinguaGraph!

This desktop app is designed to assist linguists, literature scholars, and anyone in need of quick linguistic analyses without the need for expensive resources like corpora. With LinguaGraph, key text analyses, whether on short or long texts, are just a few clicks away!

BEFORE YOU BEGIN, SOME INTRODUCTORY NOTES:

- For all documentation, read the README.md file available in the project's Git repository.
- Load Text: the file format compatible with this app is .txt. If you are working with datasets in .csv format, you can use the companion app in the project's Git repository, Dataset Selection, which allows you to choose the column from which to extract the text and save it in .txt.
- Frequency: reports the frequency of a certain word in the corpus, if present.
- Word Frequency by POS: reports the most frequent words divided by part-of-speech in a text (nn, vb, jj).
- Concordance: reports concordances for a certain word in the corpus, if present.
- Sentiment Analysis: performs sentiment analysis of the text, with a chart.
- Co-occurrence Network: displays the co-occurrence network, with a chart.
- Dispersion Plot: shows the dispersion plot for certain words in the corpus, if present, with a chart.
- Lexical Diversity: shows the lexical diversity of the text corpus.
- WordCloud: generates a WordCloud of the text corpus.
- N-grams: shows a number of n-grams chosen by the user, with a chart.
- Readability Score: shows the readability index according to Flesch and Flesch-Kincaid parameters.

More features coming soon!"""

    tk.Label(welcome_window, text=welcome_text, wraplength=400).pack()

    # Checkbox per non mostrare più il messaggio
    dont_show_var = tk.BooleanVar(value=user_preference.get('dont_show_again', False))
    chk_dont_show = tk.Checkbutton(welcome_window, text="Don't show this message again", variable=dont_show_var)
    chk_dont_show.pack()

    def save_preference():
        user_preference['dont_show_again'] = dont_show_var.get()
        save_preferences(user_preference)
        welcome_window.destroy()

    tk.Button(welcome_window, text="OK", command=save_preference).pack()



# Crea e configura il frame per i bottoni
button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
button_frame.grid_columnconfigure(tuple(range(4)), weight=1)  # Distribuisci uniformemente lo spazio

# Crea e configura il frame per l'output
output_frame = ttk.Frame(root)
output_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
root.grid_rowconfigure(1, weight=1)  # Fai in modo che l'output_frame si espanda verticalmente

# Crea l'area di testo scrollabile per l'output
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
output_text.grid(row=0, column=0, sticky="nsew")



# # Crea un frame per i grafici
graph_frame = ttk.Frame(root)
graph_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
root.grid_rowconfigure(1, weight=5)  # Assegna un peso alla riga per espandere il frame
root.grid_columnconfigure(0, weight=5)  # Assegna un peso alla colonna per espandere il frame


# Definisci la larghezza dei bottoni per essere uniformi
button_width = 20

# Aggiungi i percorsi per importare i moduli dalla cartella analysis e src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# ... Importa i moduli necessari e definisci le funzioni ...

from concordance_analysis import find_concordance
from word_freq_pos import word_freq_by_pos
from data_preprocessing import clean_text
from sentiment_analysis import analyze_sentiment
from topic_modeling import perform_lda
from co_occurrence import build_co_occurrence_network
from frequency import count_word_frequency
from dispersion_plot import generate_dispersion_plot
import n_grams
# Importa ulteriori moduli di analisi come necessario



# Definizioni delle funzioni
def load_text_file():
    output_text.delete('1.0', tk.END)
    filepath = filedialog.askopenfilename(initialdir="/", title="Select Text File",
                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])  # Opzionale: aggiungi altri formati se necessario
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text_data = file.read()
                output_text.insert(tk.END, text_data[:1000] + "\n[...]")  # Mostra un'anteprima del testo
                global data
                data = text_data  # Salva il testo per future analisi
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load text file\n{e}")


import spacy
from tkinter import messagebox

# Carica il modello di lingua inglese di Spacy
nlp = spacy.load('en_core_web_sm')

# Aggiungi una checkbox per la pulizia del testo
clean_text_checkbox_value = tk.BooleanVar()
clean_text_checkbox = ttk.Checkbutton(
    output_frame,
    text="Clean Text",
    variable=clean_text_checkbox_value,
    onvalue=True,
    offvalue=False
)

def apply_clean_text():
    output_text.delete("1.0", tk.END)
    if 'data' not in globals():
        messagebox.showwarning("Warning", "Please load a dataset first.")
        return
    if clean_text_checkbox_value.get():  # Solo se la checkbox è selezionata
        try:
            global data
            # Assumi che data sia una stringa contenente il testo
            cleaned_data = clean_text(data)
            output_text.insert(tk.END, "Text cleaned successfully.\n")
            # Salva i dati puliti per analisi successive
            data = cleaned_data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean text\n{e}")


def apply_clean_text():
    global data
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return
    try:
        # Pulizia del testo utilizzando Spacy
        cleaned_text = clean_text(data)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, cleaned_text)
        data = cleaned_text  # Aggiorna la variabile globale `data` con il testo pulito
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_frequency():
    output_text.delete("1.0", tk.END)
    target_word = simpledialog.askstring("Word Frequency", "Enter the word:")
    if target_word:
        try:
            # Assumi che 'data' sia una stringa contenente il testo
            frequency = count_word_frequency(data, target_word)
            if frequency > 0:
                output_text.insert(tk.END, f"The word '{target_word}' appears {frequency} times in the text.\n\n")
            else:
                output_text.insert(tk.END, f"The word '{target_word}' is not present in the corpus!\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating frequency: {e}")

def show_concordance():
    output_text.delete("1.0", tk.END)
    word = simpledialog.askstring("Find Concordances", "Enter the word:")
    if word:
        try:
            # Assicurati che 'data' sia una stringa contenente il testo pulito
            if isinstance(data, str):
                concordance_list = find_concordance(data, word.lower())  # Converti in minuscolo per la ricerca
                concordances = '\n'.join([f"{conc.line}\n" for conc in concordance_list])
                output_text.insert(tk.END, f"Concordances for '{word}':\n{concordances}\n\n")
            else:
                messagebox.showwarning("Warning", "Data is not in the correct format. It should be a single text string.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to find concordances\n{e}")


def show_word_freq_by_pos():
    output_text.delete('1.0', tk.END)  # Svuota il box di testo per i risultati precedenti
    pos_input = simpledialog.askstring("Input", "Enter the POS tags separated by commas (e.g., NN, VB):")
    if pos_input:  # Controlla se l'input è stato fornito
        desired_pos = [pos.strip().upper() for pos in pos_input.split(',')]  # Prepara i tag POS dall'input
        try:
            # Chiama la funzione word_freq_by_pos con il testo e i tag POS desiderati
            if isinstance(data, str):
                freq_dist = word_freq_by_pos(data, desired_pos)
                formatted_freq_dist = '\n'.join([f"{word}: {freq}" for word, freq in freq_dist])
                output_text.insert(tk.END, f"Word frequencies for {', '.join(desired_pos)}:\n{formatted_freq_dist}\n\n")
            else:
                messagebox.showwarning("Warning", "Data is not in the correct format. It should be a single text string.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate word frequencies by POS\n{e}")
    else:
        output_text.insert(tk.END, "No POS tags provided.\n\n")

def perform_sentiment_analysis():
    output_text.delete("1.0", tk.END)
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load and clean a text first.")
        return

    try:
        polarity, label = analyze_sentiment(data)  # Assumi che questa funzione restituisca la polarità e l'etichetta

        # Prepara il grafico
        plt.figure()  # Crea una nuova figura
        plt.bar(['Sentiment'], [polarity], color=['blue' if polarity >= 0 else 'red'])
        plt.ylim(-1, 1)
        plt.ylabel('Polarity')
        plt.title('Sentiment Analysis Result')
        plt.xticks([])

        # Mostra il valore della polarità sopra la barra
        if polarity >= 0:
            plt.text(0, polarity, f'{polarity:.2f}', ha='center', va='bottom')
        else:
            plt.text(0, polarity, f'{polarity:.2f}', ha='center', va='top')

        plt.show()  # Mostra il grafico in una nuova finestra

        # Aggiorna il testo con i risultati dell'analisi
        output_text.insert(tk.END, f"Sentiment Analysis Results:\nPolarity: {polarity}\nLabel: {label}\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to perform sentiment analysis\n{e}")


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_co_occurrence_network(text, top_n_words=30, window_size=4):
    """
    Costruisce una rete di co-occorrenza per le prime N parole più frequenti nel testo.
    """
    # Tokenizza il testo e prepara una lista delle parole più comuni
    tokens = word_tokenize(text.lower())
    most_common_words = [word for word, freq in Counter(tokens).most_common(top_n_words)]

    # Crea un grafo vuoto
    G = nx.Graph()

    # Aggiungi i nodi al grafo
    for word in most_common_words:
        G.add_node(word)

    # Scorri il testo per trovare la co-occorrenza entro la finestra specificata
    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i + window_size]
        # Considera solo le parole che sono tra le più comuni
        window = [word for word in window if word in most_common_words]
        # Aggiungi un arco per ogni coppia di parole nella finestra
        for word1, word2 in combinations(window, 2):
            if G.has_edge(word1, word2):
                G[word1][word2]['weight'] += 1
            else:
                G.add_edge(word1, word2, weight=1)

    return G


def show_co_occurrence_network():
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return

    try:
        G = build_co_occurrence_network(data)  # Assumi che questa funzione restituisca il grafo

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, k=0.5)  # Definisce la posizione dei nodi
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500,
                edge_color='gray', linewidths=0.5, font_size=10,
                width=[(G[u][v]['weight'] / 10) for u, v in G.edges()])
        plt.title("Co-Occurrence Network")
        plt.show()  # Mostra il grafico in una nuova finestra
    except Exception as e:
        messagebox.showerror("Error", f"Failed to build co-occurrence network\n{e}")

def generate_dispersion_plot(text, target_words):
    tokens = word_tokenize(text.lower())
    fig, ax = plt.subplots()
    dispersion_plot(tokens, target_words)
    return fig


def show_dispersion_plot():
    output_text.delete("1.0", tk.END)
    words = simpledialog.askstring("Dispersion Plot", "Enter the words separated by commas:")
    if words:
        word_list = [word.strip() for word in words.split(',')]
        if 'data' not in globals() or not isinstance(data, str):
            messagebox.showwarning("Warning", "Please load a text file first.")
            return
        try:
            # Genera il dispersion plot
            tokens = word_tokenize(data.lower())
            #plt.figure()
            nltk.draw.dispersion_plot(tokens, word_list, ignore_case=True)
            plt.show()  # Usa plt.show() per visualizzare il grafico in una nuova finestra

            output_text.insert(tk.END, f"Dispersion plot generated for words: {', '.join(word_list)}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating dispersion plot: {e}")


def show_wordcloud():
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return

    # Genera la word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(data)

    # Visualizza la word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def lexical_diversity(text):
    tokens = word_tokenize(text)
    return len(set(tokens)) / len(tokens) if tokens else 0

def show_lexical_diversity():
    output_text.delete("1.0", tk.END)
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return

    # Calcola la diversità lessicale del testo
    diversity_score = lexical_diversity(data)
    output_text.insert(tk.END, f"Lexical Diversity Score: {diversity_score}\n")

import textstat

def show_readability_scores():
    output_text.delete("1.0", tk.END)
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return

    flesch_reading_ease = textstat.flesch_reading_ease(data)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(data)

    output_text.insert(tk.END, f"Flesch Reading Ease: {flesch_reading_ease}\n")
    output_text.insert(tk.END, f"Flesch-Kincaid Grade Level: {flesch_kincaid_grade}\n")

def show_n_grams():
    output_text.delete("1.0", tk.END)
    if 'data' not in globals() or not isinstance(data, str):
        messagebox.showwarning("Warning", "Please load a text file first.")
        return

    n = simpledialog.askinteger("N-Grams", "Enter the value of n for n-grams:")
    if not n or n < 1:
        messagebox.showwarning("Warning", "Invalid value for n.")
        return

    try:
        n_grams_counter = n_grams.generate_n_grams(data, n)
        most_common_n_grams = n_grams_counter.most_common(10)  # Visualizza i primi 10

        plt.figure()
        # Converte gli n-grammi da tuple a stringhe per il plotting
        n_gram_strings = [' '.join(n_gram) for n_gram, _ in most_common_n_grams]
        counts = [count for _, count in most_common_n_grams]
        plt.barh(n_gram_strings, counts)
        plt.xlabel('Frequencies')
        plt.title(f'Most common {n}-grams')
        plt.show()  # Mostra il grafico in una nuova finestra

        # Visualizza gli n-grammi e le loro frequenze nell'area di testo
        output_text.insert(tk.END, f"Most common {n}-grams:\n\n")
        for n_gram, count in most_common_n_grams:
            n_gram_text = ' '.join(n_gram)
            output_text.insert(tk.END, f"{n_gram_text}: {count}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating n-grams: {e}")

def save_results():
    # Ottieni il testo corrente nel box di output
    results = output_text.get("1.0", tk.END)
    # Chiedi all'utente dove vuole salvare il file
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    if not filepath:
        return  # L'utente ha cancellato il dialogo di salvataggio
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(results)
        messagebox.showinfo("Success", "Results saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save results\n{e}")

# Bottoni per le operazioni
# Crea i bottoni e posizionali su due righe
buttons = [
    ("Load Text", load_text_file),
    ("Frequency", show_frequency),
    ("Word Frequency by POS", show_word_freq_by_pos),
    ("Concordance", show_concordance),
    ("Sentiment Analysis", perform_sentiment_analysis),
    ("Co-Occurrence Network", show_co_occurrence_network),
    ("Dispersion Plot", show_dispersion_plot),
    ("Lexical Diversity", show_lexical_diversity),
    ("WordCloud", show_wordcloud),  # Assumi che questa funzione sia stata definita per gestire gli embeddings
    ("N-Grams", show_n_grams),
    ("Readability Score", show_readability_scores),
    ("Clean Text", apply_clean_text), # Assumi che questa funzione sia stata definita per gestire gli n-grams
    ("Save", save_results),
    ("Exit", root.quit)
]

for i, (text, command) in enumerate(buttons):
    row, col = divmod(i, 4)  # Organizza i bottoni in tre righe, assumendo 4 bottoni per riga
    btn = ttk.Button(button_frame, text=text, command=command, width=button_width)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

root.mainloop()