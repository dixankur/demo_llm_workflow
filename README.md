# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is for creation of demo workflow
* Version: 0.0.1

### Workflow to build

1. The transcript is ingested 
2. The transcript is summarized
3. The user asks the transcript the following questions:
    1. How many people attended the meeting
    2. How would you describe the use case in one sentence
    3. Describe the name of the use case in 3-5 words
    4. What is the target feature
    5. What is the unit of analysis
    6. What is the current process
    7. Where is the data located
    8. What is the desired prediction frequency
    9. Did anyone mention any business constraints
    10. How long should the prediction be retained in the data warehouse
    11. What is the success criteria
    12. What features should be included in the dataset
4. User asks a question
5. The system prepares a document called "Usecase Document" that includes the above data points
6. The system saves the document in the designated folder and emails the user 
7. User has a meeting with the data person at the company to understand where the user can find data related to the use case
8. The user edits the document as needed, includes the information obtained in the step 6 and uploads it in the project folder
9. The system saves the edited document in the designated folder
10. System prepares a "List of Features" document. The document includes:
    1. Features suggested in 3.12
    2. Features included in the document in step 7
    3. Check box next to each feature
    4. Place to include more feature names and table names
    5. Place to define relationship between tables (think of feature discovery feature in DR)
11. The system saves the document in the designated folder and emails the user 
12. User edits the document and uploads it in the project folder
13. System prepares the "Suggested Code to Prepare the Dataset" document based on the information provided in the edited "List of Features" document
14. System saves the documents in the designated folder and emails the user
15. User edits the code as needed, approves it and uploads in the project folder
16. System runs that code and produces a dataset
17. User asks a question
18. System shows the user df.head()
19. User approves the dataset 
20. The dataset is saved into the project folder
21. System divides the dataset into 80% (train) 20% (test)
22. System builds a simple random forest model (no cross validation needed)
23. System suggests visualizations based on documents in the project folder and the features available in the training and test datasets
24. System builds a presentation with 8 slides:
    1. Slide 1: Title (name of the use case)
    2. Slide 2: Title "Current Process"
    3. Slide 3: Title "Data details"
        1. Training and test dataset dates and number of rows
        2. Names of important features
    4. Slide 4: Title "Prediction vs. Actual" (show a bar chart showing the comparison)
    5. Slide 5: Title "Important Features" (show feature importance)
    6. Slide 6: Title "Count of Locations" (showing a table of counts of locations)
    7. Slide:7 Title "Conclusions" (LLM provided output)
    8. Slide 8: Title "Next steps": 
        1. Prediction frequency
        2. Location of the predictions
        3. Date of the next touchpoint
25. System saves the presentation in the designated folder and emails the user
26. User edits the presentation and uploads it in the project folder
27. User asks a question
28. System prepares a model one-pager:
        1. Title
        2. Date
        3. Name of the stakeholder
        4. Name of the data scientist
        5. Executive summary
        6. Prediction vs. Actual chart
        7. Important features
        8. Next steps
29. System saves the document in the designated folder and emails the user
30. User edits the report and uploads it in the project folder
31. Systems emails the report to all the original meeting attendees. 
32. System fills out the draft deployment template
33. System saves the document in the designated folder and emails the user
34. User edits the deployment template and uploads it in the project folder
35. System prepares a prediction pipeline
36. System saves the document in the designated folder and emails the user 
37. User edits the pipeline as needed and uploads file to the project folder
38. System deploys the model
39. System makes prediction
40. System add the predictions to the appropriate folder
41. System analyzes the predictions and creates a presentation
42. System saves the presentation in an appropriate folder and emails the user

### How do I get set up? ###

* Summary of set up
    pip install -r requirements.txt
* Configuration
* Dependencies
* Database configuration
* How to run
    streamlit run .\script_name
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact