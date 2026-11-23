
from sqlalchemy import select

from pm_hook.db.session import SessionLocal
from pm_hook.models.project import Project
from pm_hook.models.task import Task


# Create a database session
db = SessionLocal()

try:
    # 1. Create a Project
    project = Project(
        name="PM Hooks",
        description="Project management assistant",
    )

    # 2. Add Project to the session
    db.add(project)

    # 3. Send INSERT to PostgreSQL
    # This generates project.id without committing
    db.flush()

    project_id = project.id

    print(f"Created project ID: {project_id}")

    # 4. Create a Task belonging to this Project
    task = Task(
        project_id=project_id,
        title="Build first database operation",
        status="pending",
    )

    db.add(task)

    # 5. Commit both records together
    db.commit()

    print("Project and task committed successfully!")

    # 6. Retrieve the Project
    saved_project = db.scalar(
        select(Project).where(Project.id == project_id)
    )

    # Retrieve Tasks belonging to this Project
    saved_tasks = db.scalars(
        select(Task).where(Task.project_id == project_id)
    ).all()

    print("Retrieved project:", saved_project.name)

    for saved_task in saved_tasks:
        print(
            f"Task: {saved_task.title}, "
            f"Project ID: {saved_task.project_id}"
        )

except Exception:
    db.rollback()
    raise

finally:
    db.close()
