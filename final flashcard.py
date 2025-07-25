import mysql.connector as a

# Function to create database and tables
def create_db_tables():
    try:
        mydb = a.connect(host='localhost', user='root', password='6915')  # Replace with your MySQL password
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print("Connected to MySQL Server.")
            
            # Create database and tables
            mycursor.execute("CREATE DATABASE IF NOT EXISTS flashcards")
            mycursor.execute("USE flashcards")
            
            mycursor.execute(
                "CREATE TABLE IF NOT EXISTS physics ("
                "question VARCHAR(255), "
                "answer VARCHAR(255), "
                "topic VARCHAR(100), "
                "reviewed BOOLEAN DEFAULT FALSE, "
                "difficulty VARCHAR(50) DEFAULT 'easy')"
            )
            mycursor.execute(
                "CREATE TABLE IF NOT EXISTS chemistry ("
                "question VARCHAR(255), "
                "answer VARCHAR(255), "
                "topic VARCHAR(100), "
                "reviewed BOOLEAN DEFAULT FALSE, "
                "difficulty VARCHAR(50) DEFAULT 'easy')"
            )
            mycursor.execute(
                "CREATE TABLE IF NOT EXISTS biology ("
                "question VARCHAR(255), "
                "answer VARCHAR(255), "
                "topic VARCHAR(100), "
                "reviewed BOOLEAN DEFAULT FALSE, "
                "difficulty VARCHAR(50) DEFAULT 'easy')"
            )
            print("Database and tables created successfully.")
    except Exception as e:
        print("An error occurred: ", str(e))
    finally:
        if mydb.is_connected():
            mydb.close()

# Function to connect to the database
def connect_to_db():
    try:
        connection = a.connect(host='localhost', database='flashcards', user='root', password='6915')
        if connection.is_connected():
            return connection
    except Exception as e:
        print("Error: Please check your database connection. Details: ", str(e))
    return None

# Function to add a new flashcard
def add_flashcard(connection, subject, question, answer, topic):
    cursor = connection.cursor()
    table = subject.lower()
    insert_query = "INSERT INTO " + table + " (question, answer, topic) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (question, answer, topic))
    connection.commit()
    cursor.close()
    print("Flashcard added to " + subject + " table.")

# Function to review flashcards
def review_flashcards_with_answer(connection, subject):
    try:
        cursor = connection.cursor()
        table = subject.lower()
        query = "SELECT question, answer FROM " + table + " WHERE reviewed = FALSE"
        cursor.execute(query)
        flashcards = cursor.fetchall()

        if flashcards:
            for card in flashcards:
                print("Q: " + card[0])
                show_answer = input("Do you want to see the answer? (yes/no): ").lower()
                if show_answer == 'yes':
                    print("A: " + card[1])
                    update_query = "UPDATE " + table + " SET reviewed = TRUE WHERE question = %s"
                    cursor.execute(update_query, (card[0],))
                    connection.commit()
                    print("Flashcard marked as reviewed.\n")
                else:
                    print("Skipping this flashcard.\n")
        else:
            print("No flashcards to review at the moment.")
        cursor.close()
    except Exception as e:
        print("An error occurred: ", str(e))

# Function to delete a flashcard
def delete_flashcards(connection, subject, question):
    cursor = connection.cursor()
    table = subject.lower()
    query = "DELETE FROM " + table + " WHERE question = %s"
    cursor.execute(query, (question,))
    connection.commit()
    cursor.close()
    print("Flashcard deleted.")

# Main function to control the app
def main():
    create_db_tables()
    connection = connect_to_db()
    if connection is None:
        return

    while True:
        print("\nFlashcard App - Choose an option:")
        print("1. Add a new flashcard")
        print("2. Review flashcards")
        print("3. Delete flashcards")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            subject = input("Enter the subject (Physics, Chemistry, Biology): ")
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            topic = input("Enter the topic: ")
            add_flashcard(connection, subject, question, answer, topic)

        elif choice == '2':
            subject = input("Enter the subject to review (Physics, Chemistry, Biology): ")
            review_flashcards_with_answer(connection, subject)

        elif choice == '3':
            subject = input("Enter the subject (Physics, Chemistry, Biology): ")
            question = input("Enter the question of the flashcard to delete: ")
            delete_flashcards(connection, subject, question)

        elif choice == '4':
            print("Exiting the application. Goodbye!")
            if connection.is_connected():
                connection.close()
            break

        else:
            print("Invalid choice. Please try again.")

main()
