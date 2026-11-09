from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, init_db

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

# START OF ANJI's section
@app.route("/assignments", methods=["GET", "POST"])
def assignments():
    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if not title or not due_date:
            error = "Please enter an assignment title and due date."
        else:
            connection = get_db_connection()

            connection.execute(
                "INSERT INTO assignments (title, due_date, status) VALUES (?, ?, ?)",
                (title, due_date, "Pending")
            )

            connection.commit()
            connection.close()
            

            return redirect(url_for("assignments"))

    connection = get_db_connection()

    assignment_list = connection.execute(
        "SELECT * FROM assignments ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "assignments.html",
        assignments=assignment_list,
        error=error
    )

#### code to edit
@app.route("/assignments/<int:assignment_id>/edit",
           methods=["GET", "POST"])
def edit_assignment(assignment_id):

    
    ## get_db_connection() function is used to connect to the database and execute operations
    connection = get_db_connection()

    ## operation to get specified row from database
    assignment = connection.execute(
        "SELECT * FROM assignments WHERE id = ?",
        (assignment_id,)
    ).fetchone()

    connection.close()

    if assignment is None:
        return "Assignment not found", 404


    if request.method == "POST":
        title = request.form.get("title", "").strip()
        due_date = request.form.get("due_date", "").strip()
        status = request.form.get("status", "").strip()

        ## checks if values were inputted
        if not title or not due_date:
            return "Title and due date are required.", 400

        if status not in ["Pending", "Submitted"]:
            return "Invalid assignment status.", 400

        connection = get_db_connection()

        ## update the values inside the database table
        connection.execute(
            """
            UPDATE assignments
            SET title = ?, due_date = ?, status = ?
            WHERE id = ?
            """,
            (title, due_date, status, assignment_id)
        )

        connection.commit()
        connection.close()

        ## sends the user back to the assignments page
        return redirect(url_for("assignments"))

    ## it is rendering the html
    return render_template(
        "edit_assignment.html",
        assignment=assignment
    )

## code to delete
@app.route("/assignments/<int:assignment_id>/delete",
           methods=["POST"])
def delete_assignment(assignment_id):

    connection = get_db_connection()

    ## selects specified row
    assignment = connection.execute(
        "SELECT id FROM assignments WHERE id = ?",
        (assignment_id,)
    ).fetchone()

    ## returns not found if assignment is none
    if assignment is None:
        connection.close()
        return "Assignment not found", 404

    ## deletes from database table if found
    connection.execute(
        "DELETE FROM assignments WHERE id = ?",
        (assignment_id,)
    )

    connection.commit()
    connection.close()

    ## redirects users to assingments page after deletion
    return redirect(url_for("assignments"))

# ///// END OF ANJI's section ///////////

if __name__ == "__main__":
    app.run(debug=True)