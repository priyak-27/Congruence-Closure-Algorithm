## Congruence Closure Algorithm Visualizer

This project implements and visualizes the Congruence Closure (CC) Algorithm in a step-by-step manner. The primary objective is to develop an interactive and educational tool that simplifies understanding of the algorithm’s mechanics. 
This tool is designed for students and learners who are interested in exploring the concept of equivalence classes and conflict detection within the context of congruence closure.

## Features
  1. User Input: Users can input constraints via a web form hosted on a Flask application running on port 80.
  2. Step-by-Step Visualization: The application visualizes the process of congruence closure using NetworkX and PyVis libraries.
  3. Equivalence Class Formation: Watch how equivalence classes are formed dynamically based on the input constraints.
  4. Conflict Detection: The tool identifies and displays conflicts between terms as they arise during the execution of the algorithm.
  5. Interactive Interface: The web interface is designed to be user-friendly, with a Flask backend handling the algorithm’s logic and the frontend displaying real-time graph updates.

## Technologies Used
1. Flask: A micro web framework for Python, used to build and host the web application on port 80.
2. HTML: Used to create the form where users can input constraints.
3. NetworkX: A Python library used for the creation, manipulation, and visualization of complex graphs and networks, which forms the backbone of the visualization.
4. PyVis: A Python library for network visualization, which is used to display the equivalence class graph dynamically in the web interface.

## How to execute the code
1. Clone the repository
2. Install required libraries
3. Run the Flask app: go to the project1 folder, run python3 app.py

This will start the Flask server on port 80. Open your browser and go to http://localhost to interact with the application.

## Usage:
1. Open the web application in a browser.
2. Enter a formula (such as constraints in the form of equalities or inequalities) into the input field.
3. Submit the form to initiate the algorithm.
4. Observe the step-by-step visualization of the Congruence Closure process, including the formation of equivalence classes and conflict detection.

## Future Enhancements:
1. Implementing Backtracking to allow users to go back and explore previous stages of the graph.
2. Adding more detailed explanations and tooltips to each step of the visualization to further assist learning.
3. Extending the application to support more advanced logical constraints and operations beyond the current implementation.
‭
