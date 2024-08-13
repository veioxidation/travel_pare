from database.memory_db import pool


def reset_memory(thread_id):
    """
    Remove all records from the checkpoints table for the specified thread ID.
    :param thread_id: name of the thread to reset
    :return:
    """
    # Connect to the SQLite database
    with pool.connection() as conn:
        cursor = conn.cursor()

        for table_name in ['checkpoints', 'checkpoint_blobs', 'checkpoint_writes']:
            # SQL query to delete records for the specific thread ID
            delete_query = f"DELETE FROM {table_name} WHERE thread_id = '{thread_id}'"

            # Execute the delete query
            cursor.execute(delete_query)

        # Commit the changes
        conn.commit()

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    reset_memory("Bhutan")