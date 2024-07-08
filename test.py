import openai
import time
import os
import random
from openai import OpenAI

from tqdm import tqdm




def get_response(prompt, temperature=0.5, max_tokens=2048):
    client = OpenAI(
        # This is the default and can be omitted
        api_key='',
    )
    completion =  client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-3.5-turbo",
        temperature=0,
        top_p=0,
        # max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    res = get_response("""
    Week 1: Introduction to Computer Science
Introduction to the field: history and fundamentals.
Understanding computer systems and architecture.
Software vs. hardware: basics and overview.
Week 2-3: Programming Fundamentals
Introduction to programming languages (Python, Java).
Basic constructs: variables, control structures, data types, and functions.
Simple programming exercises and problem-solving.
Week 4-5: Object-Oriented Programming
Concepts of classes, objects, inheritance, encapsulation, and polymorphism.
Practical projects: building small applications.
Introduction to software development tools and environments.
Week 6-7: Data Structures and Algorithms
Introduction to arrays, lists, stacks, queues, and trees.
Basic algorithms: sorting (bubble, merge, quicksort) and searching (binary search).
Algorithm complexity and Big O notation.
Week 8-9: Web Development
Basics of HTML, CSS, and JavaScript.
Introduction to client-server architecture.
Developing a simple dynamic website using a framework (e.g., Flask, Django).
Week 10-11: Databases
Fundamentals of databases: SQL and NoSQL.
Designing and querying databases.
Practical project: Database integration with a web application.
Week 12-13: Software Engineering
Software development life cycle (SDLC).
Agile and Scrum methodologies.
Version control systems: Git.
Week 14-15: Networks and Security
Basics of computer networks: protocols, TCP/IP, routing, and switching.
Cybersecurity fundamentals: threats, vulnerabilities, and safeguards.
Practical exercises on network setup and basic security practices.
Week 16: Capstone Project
Students will propose and develop a capstone project incorporating the skills learned.
Presentations and peer reviews.
Examinations and Evaluations:
Continuous assessment through quizzes, assignments, and projects.
Final examination covering all topics discussed.
 According to the above, please give me a detailed guide.
    
    
    """)
    print(res)