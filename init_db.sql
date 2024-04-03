-- Create the "Graph Generator" database if it doesn't exist
CREATE DATABASE "graph_generator";

-- Connect to the "Graph Generator" database
\c "graph_generator";

-- Create the "question" table
CREATE TABLE IF NOT EXISTS question (
    id SERIAL PRIMARY KEY,
    question_text TEXT
);

-- Create the "opinion" table
CREATE TABLE IF NOT EXISTS opinion (
    id SERIAL PRIMARY KEY,
    user_input TEXT,
    predicted_var TEXT,
    predicted_graph_str TEXT,
    question_id INT REFERENCES question(id)
);
