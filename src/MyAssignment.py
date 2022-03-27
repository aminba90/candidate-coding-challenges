
import sqlalchemy as db
from sqlalchemy import *
from sqlalchemy.sql import *
import os, json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import sys

class MyAssignment:

    
    def __init__(self,dbname="assignment"):
        self.dbname=dbname
        self.base_path = "/assignment"
        self.files_path = self.base_path+ "/" +"sample_data"
        self.engine = db.create_engine('sqlite:///'+self.base_path+'/db/'+dbname+'.db')
        self.connection=self.engine.connect()
        self.metadata = db.MetaData()
        self.date_format = "%Y-%m-%dT%H:%M:%S.%fZ"


    def loading_JSONS(self):
        
        data_files = [data_json for data_json in os.listdir(self.files_path) if data_json.endswith('.json')]
        for d in data_files:
            final_df=[]
            df=os.path.join(self.files_path,d)
            table_name=d.split('.')[0]
            ret = self.engine.dialect.has_table(self.engine, table_name)
            if ret:
                table = db.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
                columns = table.c
                cols_name=[]
                cols_type=[]
                for c in columns:
                    cols_name.append(c.name)
                    cols_type.append(str(c.type))
                with open(df) as dt_file:
                    json_df=json.load(dt_file)
                    for i, result in enumerate(json_df):
                                        
                        row = {}
                        for N,T in zip(cols_name,cols_type):
                            if T=="DATETIME":
                                row[N]=datetime.strptime(result[N], self.date_format)
                            else:
                                row[N]=result[N]
                        final_df.append(row)
                    try:
                        self.connection.execute(table.insert(), final_df)
                    except Exception as e:
                        print(e)
                           

            else:
                print("Table {} has to be created!".format(table_name))



    def creating_tables(self):
        
        try:
            structfile = os.path.join(self.base_path+"/config","Table_Structures.json")
            with open(structfile) as json_file:
                filedata = json.load(json_file)
                table_names = filedata[0]['tableName'] 
                table_columns = filedata[0]["tableColumn"]
                for table_name, table_column in zip(table_names, table_columns):
                        col_names=[]
                        col_types=[]
                        col_pk=[]
                        
                        for i in table_column:
                            col_types.append(i.get('type'))
                            col_names.append(i['title'])
                            col_pk.append(i['primary'])

                        new_col_type=[]
                        new_col_pk=[]
                        for i in col_types:
                            if i=='String':
                                new_col_type.append(String)
                            elif i=='Integer':
                                new_col_type.append(Integer)
                            elif i=='Date':
                                new_col_type.append(Date)  
                            elif i=='DateTime':
                                new_col_type.append(DateTime)
                        for i in col_pk:
                            if i=='true':
                                new_col_pk.append(True)
                            else:
                                new_col_pk.append(False)

                        test = Table(table_name, self.metadata,
                                    *(Column(column_name, column_type,primary_key=primary_key_flag)
                                    for column_name,
                                    column_type,primary_key_flag in zip(col_names,
                                                            new_col_type,new_col_pk)))
                        self.metadata.create_all(self.engine)
                        
                
        except Exception as e:
            print(e)
            return False
        return true


    #average complete time of a course
    def calc_avg_cmp_course(self):
        with self.connection as con:
            rs = con.execute('SELECT dt.title as course_title,\
                                avg(dt.completion_time_in_day) as avg_time_of_cmplt_course_in_day,\
                                avg(dt.completion_time_in_hour) as avg_time_of_cmplt_course_in_hour\
                                from\
                                (\
                                SELECT \
                                a.title,julianday(b.completedDate)-julianday(b.startDate) as completion_time_in_day,\
                                (julianday(b.completedDate)-julianday(b.startDate))*24 as completion_time_in_hour\
                                from courses a join certificates b on a.id=b.course\
                                ) as dt\
                                group by dt.title')
            result=rs.fetchall()
            df = pd.DataFrame(result)
            df.columns=['course_title','avg_time_of_cmplt_course_in_day','avg_time_of_cmplt_course_in_hour']
            print(df)

    #average amount of users time spent in a course
    def calc_avg_time_user_for_courses(self):
        with self.connection as con:
            rs = con.execute('SELECT dt.firstName||\' \'||dt.lastName as user_fullname,\
                            avg(dt.completion_time_in_day) as average_time_in_day_spent,\
                            avg(dt.completion_time_in_hour) as average_time_in_hour_spent\
                            from\
                            (\
                            SELECT \
                            a.firstName,a.lastName,\
                                julianday(b.completedDate)-julianday(b.startDate) as completion_time_in_day,\
                            (julianday(b.completedDate)-julianday(b.startDate))*24 as completion_time_in_hour\
                            from users a join certificates b on a.id=b.user\
                            ) as dt\
                            group by dt.firstName,dt.lastName')
            result=rs.fetchall()
            df = pd.DataFrame(result)
            df.columns=['user_fullname','average_time_in_day_spent','average_time_in_hour_spent']
            print(df)

    #average amount of users time spent for each course individually
    def calc_avg_time_user_for_courses_indvl(self):
        with self.connection as con:
            rs = con.execute('SELECT dt.firstName||\' \'||dt.lastName as user_fullname,dt.title as course_title,\
                            avg(dt.completion_time_in_day) as average_time_in_day_spent,\
                            avg(dt.completion_time_in_hour) as average_time_in_hour_spent\
                            from\
                            (\
                            SELECT \
                            a.firstName,a.lastName,c.title,\
                                julianday(b.completedDate)-julianday(b.startDate) as completion_time_in_day,\
                            (julianday(b.completedDate)-julianday(b.startDate))*24 as completion_time_in_hour\
                            from users a join certificates b on a.id=b.user\
                                        join courses c on b.course=c.id \
                            ) as dt\
                            group by dt.firstName,dt.lastName,dt.title')
            result=rs.fetchall()
            df = pd.DataFrame(result)
            df.columns=['user_fullname','course_title','average_time_in_day_spent','average_time_in_hour_spent']
            print(df)

    #report of fastest vs. slowest users completing a course
    def calc_avg_fastst_slowst_usr_cmplt_course(self):
        with self.connection as con:
            rs = con.execute('with cte as(\
                            SELECT \
                            a.firstName,a.lastName,c.title,c.id,\
                            (julianday(b.completedDate)-julianday(b.startDate))*24 as completion_time_in_hour\
                            from users a join certificates b on a.id=b.user\
                                        join courses c on b.course=c.id\
                            )\
                            select a.title as course_title,a.user_fullname as fastest_user_cmplt,b.user_fullname as slowest_user_cmplt from\
                            (select firstName||\' \'||lastName as user_fullname,title,\
                            dense_rank() over(partition by title order by completion_time_in_hour asc) as fastest_user\
                            from cte) as a join \
                            (select firstName||\' \'||lastName as user_fullname,title,\
                            dense_rank() over(partition by title order by completion_time_in_hour desc) as slowest_user\
                            from cte) as b on a.title=b.title and a.fastest_user=b.slowest_user\
                            where a.fastest_user=1 and b.slowest_user=1')
            result=rs.fetchall()
            df = pd.DataFrame(result)
            df.columns=['course_title','fastest_user_cmplt','slowest_user_cmplt']
            print(df)

    #mount of certificates per customer
    def calc_amt_certf_per_customer(self):
        with self.connection as con:
            rs = con.execute('SELECT b.firstName||\' \'||b.lastName as user_fullname,\
                            count( a.course) num_certf_per_customer\
                            from certificates a join users b on a.user=b.id\
                            group by b.firstName||\' \'||b.lastName\
                            order by 2')
            result=rs.fetchall()
            df = pd.DataFrame(result)
            df.columns=['user_fullname','num_certf_per_customer']
            print(df)

    def show_data_on_chart_bar(self,df):
        df.plot.bar()
        plt.show()
    
    
        

def main():
    
      
    if len(sys.argv)>1:
        p=MyAssignment(dbname=sys.argv[1])
    else:
        p=MyAssignment()
    if len(sys.argv)>2:
        if sys.argv[2]=='yes':
            p.creating_tables()
        if sys.argv[3]=='yes':
            p.loading_JSONS()
        if sys.argv[4]=='1':
            p.calc_avg_cmp_course()
        if sys.argv[4]=='2':
            p.calc_avg_time_user_for_courses()
        if sys.argv[4]=='3':
            p.calc_avg_time_user_for_courses_indvl()
        if sys.argv[4]=='4':
            p.calc_avg_fastst_slowst_usr_cmplt_course()
        if sys.argv[4]=='5':
            p.calc_amt_certf_per_customer()
    

if __name__ == "__main__":
    main()

