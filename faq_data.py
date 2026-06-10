"""
faq_data.py
-----------
Contains the FAQ dataset for the CodeAlpha FAQ Chatbot.
Topic: Technology & Programming

This module defines a list of dictionaries, each containing:
- 'question': The FAQ question string
- 'answer'  : The corresponding answer string

Add or modify FAQ entries here to expand the chatbot's knowledge base.
"""

FAQ_DATA = [
    # ── Python ──────────────────────────────────────────────────────────────
    {
        "question": "What is Python?",
        "answer": (
            "Python is a high-level, interpreted, general-purpose programming language "
            "known for its simple, readable syntax. It supports multiple programming "
            "paradigms including procedural, object-oriented, and functional programming. "
            "Python is widely used in web development, data science, AI/ML, automation, "
            "and scripting."
        ),
    },
    {
        "question": "How do I install Python?",
        "answer": (
            "Visit the official Python website at https://www.python.org/downloads/ and "
            "download the installer for your operating system (Windows, macOS, or Linux). "
            "Run the installer and make sure to check 'Add Python to PATH' during setup. "
            "Verify the installation by running `python --version` in your terminal."
        ),
    },
    {
        "question": "What is a virtual environment in Python?",
        "answer": (
            "A virtual environment is an isolated Python environment that lets you install "
            "packages for a specific project without affecting the global Python installation. "
            "Create one with `python -m venv env`, activate it with `env\\Scripts\\activate` "
            "(Windows) or `source env/bin/activate` (macOS/Linux), and install packages "
            "with pip inside it."
        ),
    },
    # ── Machine Learning / AI ────────────────────────────────────────────────
    {
        "question": "What is machine learning?",
        "answer": (
            "Machine Learning (ML) is a subset of Artificial Intelligence that enables "
            "systems to learn and improve from experience without being explicitly programmed. "
            "ML algorithms build models from training data to make predictions or decisions. "
            "Key types include supervised learning, unsupervised learning, and reinforcement "
            "learning."
        ),
    },
    {
        "question": "What is the difference between AI and machine learning?",
        "answer": (
            "Artificial Intelligence (AI) is the broad concept of machines performing tasks "
            "that normally require human intelligence. Machine Learning is a *subset* of AI "
            "that focuses on algorithms that learn from data. Deep Learning is a further subset "
            "of ML that uses multi-layered neural networks. Think of it as: AI ⊃ ML ⊃ Deep Learning."
        ),
    },
    {
        "question": "What is natural language processing?",
        "answer": (
            "Natural Language Processing (NLP) is a branch of AI that deals with the interaction "
            "between computers and human language. It enables machines to read, understand, and "
            "generate human text or speech. Common NLP tasks include sentiment analysis, "
            "machine translation, named entity recognition, text summarization, and chatbot development."
        ),
    },
    {
        "question": "What is TF-IDF?",
        "answer": (
            "TF-IDF stands for Term Frequency–Inverse Document Frequency. It is a numerical "
            "statistic used in NLP to reflect how important a word is to a document in a collection. "
            "TF measures how often a term appears in a document; IDF penalises terms that appear "
            "across many documents (common words). The product highlights distinctive, informative words."
        ),
    },
    {
        "question": "What is cosine similarity?",
        "answer": (
            "Cosine similarity measures the cosine of the angle between two non-zero vectors in a "
            "multi-dimensional space. It is widely used in NLP to compare text documents represented "
            "as TF-IDF or word-embedding vectors. A score of 1 means identical direction (very similar), "
            "while 0 means orthogonal (completely dissimilar)."
        ),
    },
    # ── Data Science / Libraries ─────────────────────────────────────────────
    {
        "question": "What is Pandas?",
        "answer": (
            "Pandas is an open-source Python library that provides fast, flexible, and expressive "
            "data structures (Series and DataFrame) designed for working with structured/tabular data. "
            "It offers powerful tools for data cleaning, manipulation, aggregation, merging, and "
            "visualisation preparation, making it a cornerstone of data science workflows."
        ),
    },
    {
        "question": "What is scikit-learn?",
        "answer": (
            "Scikit-learn (sklearn) is a free, open-source machine learning library for Python. "
            "It provides efficient tools for classification, regression, clustering, dimensionality "
            "reduction, model selection, and preprocessing. Built on NumPy, SciPy, and Matplotlib, "
            "it is one of the most widely used ML libraries for practical applications."
        ),
    },
    {
        "question": "What is NLTK?",
        "answer": (
            "NLTK (Natural Language Toolkit) is a leading Python platform for working with human "
            "language data. It provides easy-to-use interfaces to over 50 corpora and lexical "
            "resources (e.g., WordNet), along with libraries for tokenisation, stemming, tagging, "
            "parsing, semantic reasoning, and more. It is excellent for teaching, research, and "
            "NLP prototyping."
        ),
    },
    # ── Web / Frameworks ─────────────────────────────────────────────────────
    {
        "question": "What is Streamlit?",
        "answer": (
            "Streamlit is an open-source Python framework for rapidly building interactive web "
            "applications for data science and machine learning projects — no front-end experience "
            "required. You write pure Python scripts and Streamlit automatically renders them as "
            "beautifully styled, shareable web apps with widgets, charts, and layouts."
        ),
    },
    {
        "question": "What is an API?",
        "answer": (
            "An API (Application Programming Interface) is a set of rules and protocols that "
            "allows different software applications to communicate with each other. APIs define "
            "the methods and data formats that programs use to request and exchange information. "
            "REST APIs (using HTTP) are most common on the web; they use endpoints and JSON "
            "to transfer data between a client and a server."
        ),
    },
    # ── Programming Concepts ─────────────────────────────────────────────────
    {
        "question": "What is object-oriented programming?",
        "answer": (
            "Object-Oriented Programming (OOP) is a programming paradigm that organises code "
            "around 'objects' — instances of classes that bundle data (attributes) and behavior "
            "(methods) together. The four pillars of OOP are Encapsulation, Abstraction, "
            "Inheritance, and Polymorphism. Languages like Python, Java, and C++ support OOP."
        ),
    },
    {
        "question": "What is a neural network?",
        "answer": (
            "A neural network is a computational model inspired by the human brain. It consists "
            "of layers of interconnected 'neurons' (nodes): an input layer, one or more hidden "
            "layers, and an output layer. During training, the network adjusts connection weights "
            "using backpropagation to minimise prediction error. Deep neural networks with many "
            "hidden layers form the basis of deep learning."
        ),
    },
    {
        "question": "What is Git and why is it important?",
        "answer": (
            "Git is a distributed version control system that tracks changes to source code over "
            "time. It allows multiple developers to collaborate, revert to previous states, branch "
            "for new features, and merge work together. GitHub and GitLab are popular cloud platforms "
            "that host Git repositories. Mastering Git is an essential skill for every software developer."
        ),
    },
    {
        "question": "What is the difference between supervised and unsupervised learning?",
        "answer": (
            "In *supervised learning*, the model trains on labelled data (input-output pairs) and "
            "learns to map inputs to correct outputs (e.g., spam classification, house price prediction). "
            "In *unsupervised learning*, the model finds hidden patterns in unlabelled data without "
            "predefined answers (e.g., clustering customers, dimensionality reduction). "
            "Semi-supervised learning combines both approaches."
        ),
    },
    {
        "question": "What is overfitting in machine learning?",
        "answer": (
            "Overfitting occurs when an ML model learns the training data too well — memorising "
            "noise and outliers instead of learning the general pattern. The model performs "
            "excellently on training data but poorly on unseen (test) data. Remedies include: "
            "using more training data, applying regularisation (L1/L2), dropout (for neural networks), "
            "cross-validation, and simplifying the model architecture."
        ),
    },
    {
        "question": "How do I start learning data science?",
        "answer": (
            "Start with Python fundamentals, then learn NumPy and Pandas for data manipulation. "
            "Study statistics and probability basics, then move to Matplotlib/Seaborn for "
            "visualisation. Learn machine learning with scikit-learn, and explore deep learning "
            "with TensorFlow or PyTorch. Practice on Kaggle datasets, build projects, and "
            "document everything on GitHub to build a portfolio."
        ),
    },
    {
        "question": "What is CodeAlpha?",
        "answer": (
            "CodeAlpha is a leading internship and training platform that offers real-world "
            "project-based internships in domains such as Artificial Intelligence, Machine Learning, "
            "Web Development, Cybersecurity, and more. It provides students and fresh graduates "
            "with hands-on experience, mentorship, and certificate recognition to help them "
            "kickstart their professional careers."
        ),
    },
]
