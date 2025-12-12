import sqlite3
from datetime import datetime
import os
DB_NAME = os.getenv("TEST_DB","tasks_advanced.db")

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
#-------------------------------------------------------------------------
def create_table():
    """Create categories and tasks table if it does not exist"""
    conn = get_connection()
    cursor = conn.cursor()
    #create table categories
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories(
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL UNIQUE,
                              created_at TEXT
                          )
                          """)
    #create table tasks
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tasks(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       description TEXT,
                       priority TEXT NOT NULL DEFAULT 'Medium',
                       due_date TEXT,
                       status TEXT NOT NULL DEFAULT 'Pending',
                       created_at TEXT NOT NULL,
                       
                       category_id INTEGER NOT NULL,
                       FOREIGN KEY (category_id) REFERENCES categories(id)
                       
                       CHECK(status IN('Pending', 'In Progress', 'Completed'))
                       CHECK(priority IN('Low', 'Medium', 'High'))
                   )
                   
                   """)
    
    
    conn.commit()
    conn.close()
#-------------------------------------------------------------------------
def move_task_to_category(task_id , new_category_name):
    """
        Move a task to a different category.
        If category doesn't exist, create it.
        This is an ATOMIC operation (all or nothing!)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Step 1: Check if new category exists
        cursor.execute("""SELECT id FROM categories WHERE name = ?""",(new_category_name,))
        result = cursor.fetchone()
        
        if result:
            new_category_id = result[0]
            print(f"ℹ️  Category '{new_category_name}' exists (ID: {new_category_id})")        
        else:
            # Step 2: Create new category
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                           INSERT INTO categories (name, created_at)
                           VALUES (?,?)
                           """,(new_category_name , created_at))
            new_category_id = cursor.lastrowid
            print(f"✅ Created category '{new_category_name}' (ID: {new_category_id})")
        # Step 3: Update task's category
        cursor.execute("""
                       UPDATE tasks SET category_id = ? WHERE id = ?
                       """,(new_category_id,task_id))
        
        if cursor.rowcount == 0:
            raise Exception(f"Task {task_id} not found!")
        
        # If we get here, everything succeeded - COMMIT!
        conn.commit()
        print(f"✅ Task {task_id} moved to '{new_category_name}'!")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ Transaction failed: {e}")
        print("↩️  All changes rolled back!")
        return False
    finally:
        conn.close()
#-------------------------------------------------------------------------
def add_task(title, description, priority, due_date, category):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT id FROM categories WHERE name = ? 
                   """,(category,))
    cat_result = cursor.fetchone()
    if cat_result:
        category_id = cat_result[0]
    else:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
                       INSERT INTO categories (name , created_at)
                       VALUES (? ,? )
                       """,(category , created_at))
        category_id = cursor.lastrowid
    status = "Pending"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                   INSERT INTO tasks (title, description, priority, due_date, status, category_id, created_at)
                   VALUES(?,?,?,?,?,?,?)
                   """, (title, description,priority,due_date,status,category_id,created_at))
    conn.commit()
    conn.close()
    print(f"✅ Task '{title}' added successfully!")
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    
    result = cursor.execute("""
                            SELECT * FROM tasks
                            """)
    result = result.fetchall()
    conn.close()
    return result
def get_task_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    
    result = cursor.execute("""
                            SELECT * FROM tasks WHERE id = ?
                            """,(id,))
    result = result.fetchone()
    conn.close()
    return result
def get_category_name(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT name FROM categories WHERE id =? 
                   """,(category_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None

def update_task(task_id , title = None, description = None, priority = None, due_date = None, status = None, category = None, created_at = None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    values = []
    
    if title is not None:
        updates.append("title = ?")
        values.append(title)
    if description is not None:
        updates.append("description = ?")
        values.append(description)
    if priority is not None:
        updates.append("priority = ?")
        values.append(priority)
    if due_date is not None:
        updates.append("due_date = ?")
        values.append(due_date)
    if status is not None:
        updates.append("status = ?")
        values.append(status)
    if created_at is not None:
        updates.append("created_at = ?")
        values.append(created_at)
    if not updates:
        print("No fields to update!")
        conn.close()
        return                            
    
    sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"    
    values.append(task_id)
    cursor.execute(sql , tuple(values))
    conn.commit()
    
    if cursor.rowcount > 0:
        conn.close()
        return True
    else:
        conn.close()
        return False
    
    
    
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM tasks WHERE id = ?
                   """ , (task_id,))
    conn.commit()
    if cursor.rowcount > 0:
        conn.close()
        return f"Task {task_id} Deleted successfully!"
    else:
        conn.close()
        return f"Task {task_id} not found!"
    
    
    
    
    
def filter_task_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute("""
                            SELECT status , COUNT(*) FROM tasks GROUP BY status
                            
                            """)
    result = result.fetchall()
    conn.close()
    return result