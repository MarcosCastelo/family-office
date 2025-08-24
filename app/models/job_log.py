"""Model for storing job execution logs"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func

class JobLog(db.Model):
    __tablename__ = "job_logs"
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(100), nullable=False)
    execution_time = db.Column(db.DateTime, default=func.now(), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, error, running
    result = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    duration_seconds = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f"<JobLog(job_id={self.job_id}, status={self.status}, execution_time={self.execution_time})>"
    
    @property
    def is_success(self):
        """Check if job execution was successful"""
        return self.status == 'success'
    
    @property
    def is_error(self):
        """Check if job execution had an error"""
        return self.status == 'error'
    
    @property
    def formatted_duration(self):
        """Return formatted duration"""
        if self.duration_seconds:
            if self.duration_seconds < 60:
                return f"{self.duration_seconds:.2f}s"
            elif self.duration_seconds < 3600:
                minutes = self.duration_seconds / 60
                return f"{minutes:.1f}m"
            else:
                hours = self.duration_seconds / 3600
                return f"{hours:.1f}h"
        return "N/A"
    
    @property
    def age_hours(self):
        """Return age of log entry in hours"""
        if self.execution_time:
            delta = datetime.now() - self.execution_time
            return delta.total_seconds() / 3600
        return 0
