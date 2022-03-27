<h3>
HOW TO RUN THE SOLUTION:
 </h3>

1- you just need to run "docker-compose up -d" in order to create docker containers.</br>
2- you can execute "docker exec -it perseus-assignment bash" to be able to excute command inside docker container.</br>
3- you should execute command inside docker container like : "python3 src/MyAssignment.py [desired_dbname] ["yes" ,if you want to create tables for provided input files|"no"] ["yes",if you want to insert records into created tables|"no"] [number of query which you want it's result to be displayed ] ex. "python3 src/MyAssignment.py mydb yes yes 1".</br></br></br>
<h3>
queries:
  </h3>
  1- average complete time of a course</br>
  2- average amount of users time spent in a course</br>
  3- average amount of users time spent for each course individually</br>
  4- report of fastest vs. slowest users completing a course</br>
  5- amount of certificates per customer</br></br></br>
<h3>
Extra Details:
  </h3>
1- There is a config folder within the solution which contains a JSON file that represent metadata for each of provided input files in database. It is possible to add more structure to this file and correspondant table will be create automatically.</br>
2- DB file will be created under db folder.</br>
3- If you try to insert a same JSON file into a table twice, PK constraint which defined in table metadata will throw exception and will not allow this operation.</br>
4- A function has been defined which called "show_data_on_chart_bar" that is plotting data using matplotlib library. I defined this but I didn't use since there were some problem with it inside docker container. I know the workaround for this part however I skipped this since it was not mandatory as per your provided description.


