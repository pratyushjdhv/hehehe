from app import create_app, db
from app.models import User, Course, Batch, Enrollment, Payment, Attendance

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Course': Course,
        'Batch': Batch,
        'Enrollment': Enrollment,
        'Payment': Payment,
        'Attendance': Attendance
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
