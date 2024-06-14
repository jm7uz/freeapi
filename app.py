from flask import Flask, request, jsonify
import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            full_name varchar(100),
            quiz_start varchar(100),
            quiz_end varchar(100),
            quiz_result int(3),
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)
        

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, full_name: str,  quiz_start: str = "", quiz_end: str = "", quiz_result: str = ""):
        sql = """
        INSERT INTO Users(id, full_name, quiz_start, quiz_end, quiz_result) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, full_name, quiz_start, quiz_end, quiz_result), commit=True)
    
    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)
        
        
db = Database(path_to_db="main.db")
try:
    db.create_table_users()
except:
    pass

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/api/user_data', methods=['POST'])
def video_watched():
    watch_data = request.get_json()
    user_id = int(watch_data.get('user_id'))
    full_name = int(watch_data.get('full_name'))
    quiz_start = int(watch_data.get('quiz_start'))
    quiz_end = int(watch_data.get('quiz_end'))
    quiz_result = int(watch_data.get('quiz_result'))
    
    db.add_user(id=int(user_id), full_name=full_name, quiz_start=quiz_start,
                quiz_end=quiz_end, quiz_result=quiz_result)
    

    print(watch_data)
    return jsonify({"message": "Data added."})

@app.route('/api', methods=['GET'])
def video_watcheds():
    all = db.select_all_users()
    return jsonify({"message": f"hello update {all}"})



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
