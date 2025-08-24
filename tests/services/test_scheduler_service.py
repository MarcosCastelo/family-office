"""Tests for SchedulerService"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

class TestSchedulerService:
    """Test SchedulerService functionality"""
    
    def setup_method(self):
        """Setup test data for each test method"""
        # Mock the dependencies
        with patch('app.services.scheduler_service.QuoteService'):
            with patch('app.services.scheduler_service.db') as mock_db:
                mock_db.session = Mock()
                from app.services.scheduler_service import SchedulerService
                self.scheduler_service = SchedulerService()
    
    def test_start_scheduler_success(self):
        """Test starting scheduler successfully"""
        # Mock the running property
        mock_scheduler = Mock()
        mock_scheduler.running = False
        self.scheduler_service.scheduler = mock_scheduler
        
        self.scheduler_service.start()
        
        # Verify scheduler was started
        mock_scheduler.start.assert_called_once()
    
    def test_start_scheduler_already_running(self):
        """Test starting scheduler when already running"""
        # Mock the running property
        mock_scheduler = Mock()
        mock_scheduler.running = True
        self.scheduler_service.scheduler = mock_scheduler
        
        self.scheduler_service.start()
        
        # Verify scheduler was not started again
        mock_scheduler.start.assert_not_called()
    
    def test_stop_scheduler_success(self):
        """Test stopping scheduler successfully"""
        # Mock the running property
        mock_scheduler = Mock()
        mock_scheduler.running = True
        self.scheduler_service.scheduler = mock_scheduler
        
        self.scheduler_service.stop()
        
        # Verify scheduler was stopped
        mock_scheduler.shutdown.assert_called_once()
    
    def test_stop_scheduler_not_running(self):
        """Test stopping scheduler when not running"""
        # Mock the running property
        mock_scheduler = Mock()
        mock_scheduler.running = False
        self.scheduler_service.scheduler = mock_scheduler
        
        self.scheduler_service.stop()
        
        # Verify scheduler was not stopped
        mock_scheduler.shutdown.assert_not_called()
    
    def test_get_job_status_success(self):
        """Test getting job status successfully"""
        # Mock jobs
        mock_job1 = Mock()
        mock_job1.id = 'job1'
        mock_job1.name = 'Test Job 1'
        mock_job1.next_run_time = datetime.now()
        mock_job1.trigger = 'cron'
        
        mock_job2 = Mock()
        mock_job2.id = 'job2'
        mock_job2.name = 'Test Job 2'
        mock_job2.next_run_time = None
        mock_job2.trigger = 'interval'
        
        mock_scheduler = Mock()
        mock_scheduler.get_jobs.return_value = [mock_job1, mock_job2]
        mock_scheduler.running = True
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.get_job_status()
        
        assert result['scheduler_running'] is True
        assert result['total_jobs'] == 2
        assert len(result['jobs']) == 2
        assert result['jobs'][0]['id'] == 'job1'
        assert result['jobs'][1]['id'] == 'job2'
    
    def test_get_job_status_error(self):
        """Test getting job status with error"""
        mock_scheduler = Mock()
        mock_scheduler.get_jobs.side_effect = Exception("Test error")
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.get_job_status()
        
        assert 'error' in result
        assert 'Test error' in result['error']
    
    def test_add_custom_job_success(self):
        """Test adding custom job successfully"""
        def test_function():
            pass
        
        mock_scheduler = Mock()
        mock_scheduler.add_job.return_value = Mock()
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.add_custom_job(test_function, 'interval', hours=1)
        
        assert result is not None
        mock_scheduler.add_job.assert_called_once()
    
    def test_add_custom_job_error(self):
        """Test adding custom job with error"""
        def test_function():
            pass
        
        mock_scheduler = Mock()
        mock_scheduler.add_job.side_effect = Exception("Job error")
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.add_custom_job(test_function, 'interval', hours=1)
        
        assert result is None
    
    def test_remove_job_success(self):
        """Test removing job successfully"""
        mock_scheduler = Mock()
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.remove_job('test_job')
        
        assert result is True
        mock_scheduler.remove_job.assert_called_once_with('test_job')
    
    def test_remove_job_error(self):
        """Test removing job with error"""
        mock_scheduler = Mock()
        mock_scheduler.remove_job.side_effect = Exception("Remove error")
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.remove_job('test_job')
        
        assert result is False
    
    def test_pause_job_success(self):
        """Test pausing job successfully"""
        mock_scheduler = Mock()
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.pause_job('test_job')
        
        assert result is True
        mock_scheduler.pause_job.assert_called_once_with('test_job')
    
    def test_resume_job_success(self):
        """Test resuming job successfully"""
        mock_scheduler = Mock()
        self.scheduler_service.scheduler = mock_scheduler
        
        result = self.scheduler_service.resume_job('test_job')
        
        assert result is True
        mock_scheduler.resume_job.assert_called_once_with('test_job')
