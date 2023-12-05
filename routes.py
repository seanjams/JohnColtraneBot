from db import JobRun

def init_routes(app):
    @app.route('/job_runs')
    def list_job_runs():
        with app.app_context():
            return [run.json() for run in JobRun.query.all()]

    @app.route('/job_runs/<int:run_id>')
    def retrieve_job_run(run_id):
        with app.app_context():
            run = JobRun.query.get(run_id)
            return run.json() if run else {}

