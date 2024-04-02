
# Movie Rating System

This project is a movie management system developed using Django and Django Rest Framework. PostgreSQL is used as the database, hosted on Render. The system provides several features to users for managing movies.


## Features

*User Authentication: Users can create accounts and log in securely to access the system.

*Add Movie: Authenticated users can add new movies to the system by providing details such as title, description, release year, etc.

*View Movie List: Users can view a list of all movies available in the system. Each movie is displayed with basic information such as title, release year, and average rating.

*Rate Movie: Users can rate movies on a scale and provide feedback. Ratings contribute to the average rating of the movie, which is displayed to all users.

*Search Movie: Users can search for a specific movie by its title and view its details along with the average rating.


## Technologies Used

1.Django: A high-level Python web framework for rapid development and clean, pragmatic design.

2.Django Rest Framework: A powerful and flexible toolkit for building Web APIs in Django.

3.PostgreSQL: A powerful, open-source object-relational database system.

4.Render: A cloud platform for deploying and scaling web applications.




## Installation

Step 1 : Clone the repository
```bash
  git clone <repository_url>


```
step 2 : Install dependencies.
```bash
  pip install -r requirements.txt

```
Step 3 : Setup PostgreSQL database and configure database settings in settings.py. **note(the .env file is included in the git repository)

Step 4 : Run migrations.
```bash
  python manage.py migrate


```
Step 5 : Start the development server.
```bash
  python manage.py runserver



```
    
## Usage
1.Register a new account or log in with existing credentials.

2.Add movies by providing necessary details.

3.View the list of available movies and their ratings.

4.Rate movies and provide feedback.

5.Search for specific movies by their titles.




## API Testing with Postman 
This collection of Postman requests allows users to test the endpoints of the Movie Management System API. By importing the provided Movie_Rating.postman_collection.json file into Postman, users can quickly and efficiently evaluate the functionality and performance of the API.



Instructions   
1.Download Collection: Download the Movie_Rating.postman_collection.json file from the api_collection folder.

2.Import into Postman: Open Postman and import the downloaded collection by clicking on "Import" in the top left corner, then selecting the JSON file. This will load all the requests and configurations into your Postman workspace.

4.Setup Environment (Optional): If required, set up environment variables such as base URL, authentication tokens, etc., for easier testing across different environments.

5.Run Requests: Run individual requests or entire folders to test various endpoints of the Movie Management System API. Ensure to provide required parameters and payloads according to the API documentation.

6.Analyze Responses: Evaluate the responses received from the API for correctness, completeness, and adherence to specifications. Check for status codes, response bodies, and headers to ensure proper functioning.

7.Monitor Performance: Use Postman's features to monitor API performance, including response times, latency, and error rates. Analyze performance metrics to identify bottlenecks and areas for optimization.




## Acknowledgments
Special thanks to the Django and Django Rest Framework communities for their excellent documentation and support.
