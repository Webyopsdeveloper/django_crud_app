# Starting the Django CRUD operation project
- Install Django by running the following command in terminal-
	pip install django 

- Install Django restframework by running the following command in 
   terminal-
	pip install djangorestframework 

# For unit test coverage report-
- Run the following command in terminal-
	pip install coverage 

- To execute the unit test cases run the following command in terminal-
	First enter restapi directory by- cd restapi

	then run-
	coverage run manage.py test

- To generate a coverage report run the following command in the terminal
   while in restapi directory - coverage report 

- <p>To generate a HTML coverage report run the following command in the terminal
   while in restapi directory - coverage html <br>
   This will create a htmlcov directory, which you can open in a web <br> 
   browser to explore the coverage details visually. <br>
   To run HTML coverage enter htmlcov directory using - cd htmlcov <br>
   Then for :<br>
  1. windows-> start index.html <br>
  2. Mac-> open index.html <br>
  3. Linux-> xdg-open index.html <br>
   </p>
