from flask_restful import Resource
from flask import request
from tasks.email_tasks import send_email_async, process_async_job


class TriggerEmailTaskResource(Resource):
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'message': 'No input data provided'}, 400
        
        subject = data.get('subject', 'Test Email')
        recipients = data.get('recipients', [])
        body = data.get('body', 'This is a test email')
        
        if not recipients:
            return {'message': 'Recipients list is required'}, 400
        
        task = send_email_async.delay(subject, recipients, body)
        
        return {
            'message': 'Email task triggered',
            'task_id': task.id,
            'status': 'pending'
        }, 202


class TriggerAsyncJobResource(Resource):
    def post(self):
        data = request.get_json()
        
        if not data:
            return {'message': 'No input data provided'}, 400
        
        job_data = data.get('data', 'default data')
        
        task = process_async_job.delay(job_data)
        
        return {
            'message': 'Async job triggered',
            'task_id': task.id,
            'status': 'pending'
        }, 202
