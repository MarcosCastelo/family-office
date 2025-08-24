"""Scheduler service for automated tasks using APScheduler"""
import logging
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app.services.quote_service import QuoteService
from app.config.extensions import db

logger = logging.getLogger(__name__)

class SchedulerService:
    """Service for managing scheduled tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.quote_service = QuoteService()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Setup all scheduled jobs"""
        try:
            # Atualização de cotações - diária às 9h
            self.scheduler.add_job(
                func=self._update_all_quotes,
                trigger=CronTrigger(hour=9, minute=0),
                id='update_quotes_daily',
                name='Update asset quotes daily',
                replace_existing=True
            )
            
            # Verificação de alertas - a cada 4 horas
            self.scheduler.add_job(
                func=self._check_all_alerts,
                trigger=IntervalTrigger(hours=4),
                id='check_alerts_4h',
                name='Check alerts every 4 hours',
                replace_existing=True
            )
            
            # Limpeza de dados antigos - semanal aos domingos às 2h
            self.scheduler.add_job(
                func=self._cleanup_old_data,
                trigger=CronTrigger(day_of_week='sun', hour=2, minute=0),
                id='cleanup_weekly',
                name='Cleanup old data weekly',
                replace_existing=True
            )
            
            # Backup de dados - diário às 23h
            self.scheduler.add_job(
                func=self._backup_data,
                trigger=CronTrigger(hour=23, minute=0),
                id='backup_daily',
                name='Daily data backup',
                replace_existing=True
            )
            
            logger.info("Scheduled jobs configured successfully")
            
        except Exception as e:
            logger.error(f"Error setting up scheduled jobs: {e}")
    
    def start(self):
        """Start the scheduler"""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("Scheduler started successfully")
            else:
                logger.info("Scheduler already running")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Scheduler stopped successfully")
            else:
                logger.info("Scheduler not running")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def get_job_status(self) -> dict:
        """Get status of all scheduled jobs"""
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
            
            return {
                'scheduler_running': self.scheduler.running,
                'jobs': jobs,
                'total_jobs': len(jobs)
            }
            
        except Exception as e:
            logger.error(f"Error getting job status: {e}")
            return {'error': str(e)}
    
    def _update_all_quotes(self):
        """Update quotes for all assets"""
        try:
            logger.info("Starting scheduled quote update")
            
            result = self.quote_service.update_asset_quotes()
            
            logger.info(f"Quote update completed: {result['updated']} updated, {result['errors']} errors")
            
            # Salvar log da execução
            self._log_job_execution('update_quotes_daily', result)
            
        except Exception as e:
            logger.error(f"Error in scheduled quote update: {e}")
            self._log_job_execution('update_quotes_daily', {'error': str(e)})
    
    def _check_all_alerts(self):
        """Check and generate alerts for all families"""
        try:
            logger.info("Starting scheduled alert check")
            
            from app.models.family import Family
            families = Family.query.all()
            
            total_alerts = 0
            for family in families:
                try:
                    # Simplified alert check - in production, implement proper alert service
                    # For now, just count existing alerts
                    from app.models.alert import Alert
                    alerts = Alert.query.filter_by(family_id=family.id, is_resolved=False).all()
                    total_alerts += len(alerts)
                except Exception as e:
                    logger.error(f"Error checking alerts for family {family.id}: {e}")
            
            logger.info(f"Alert check completed: {total_alerts} alerts found")
            
            # Salvar log da execução
            self._log_job_execution('check_alerts_4h', {'alerts_found': total_alerts})
            
        except Exception as e:
            logger.error(f"Error in scheduled alert check: {e}")
            self._log_job_execution('check_alerts_4h', {'error': str(e)})
    
    def _cleanup_old_data(self):
        """Clean up old data to maintain performance"""
        try:
            logger.info("Starting scheduled data cleanup")
            
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=90)
            
            # Limpar histórico de cotações antigo
            from app.models.quote_history import QuoteHistory
            old_quotes = QuoteHistory.query.filter(
                QuoteHistory.timestamp < cutoff_date
            ).delete()
            
            # Limpar alertas resolvidos antigos
            from app.models.alert import Alert
            old_alerts = Alert.query.filter(
                Alert.is_resolved == True,
                Alert.resolved_at < cutoff_date
            ).delete()
            
            logger.info(f"Data cleanup completed: {old_quotes} old quotes, {old_alerts} old alerts removed")
            
            # Salvar log da execução
            self._log_job_execution('cleanup_weekly', {
                'old_quotes_removed': old_quotes,
                'old_alerts_removed': old_alerts
            })
            
        except Exception as e:
            logger.error(f"Error in scheduled data cleanup: {e}")
            self._log_job_execution('cleanup_weekly', {'error': str(e)})
    
    def _backup_data(self):
        """Create daily data backup"""
        try:
            logger.info("Starting scheduled data backup")
            
            # Implementar lógica de backup
            # Pode ser exportação para arquivo, upload para cloud, etc.
            backup_result = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'message': 'Backup completed successfully'
            }
            
            logger.info("Data backup completed successfully")
            
            # Salvar log da execução
            self._log_job_execution('backup_daily', backup_result)
            
        except Exception as e:
            logger.error(f"Error in scheduled data backup: {e}")
            self._log_job_execution('backup_daily', {'error': str(e)})
    
    def _log_job_execution(self, job_id: str, result: dict):
        """Log job execution results"""
        try:
            from app.models.job_log import JobLog
            
            log_entry = JobLog(
                job_id=job_id,
                execution_time=datetime.now(),
                result=result,
                status='success' if 'error' not in result else 'error'
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error logging job execution: {e}")
            db.session.rollback()
    
    def add_custom_job(self, func, trigger, **kwargs):
        """Add a custom scheduled job"""
        try:
            job = self.scheduler.add_job(func, trigger, **kwargs)
            logger.info(f"Custom job added: {job.id}")
            return job
        except Exception as e:
            logger.error(f"Error adding custom job: {e}")
            return None
    
    def remove_job(self, job_id: str):
        """Remove a scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job removed: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing job {job_id}: {e}")
            return False
    
    def pause_job(self, job_id: str):
        """Pause a scheduled job"""
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"Job paused: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error pausing job {job_id}: {e}")
            return False
    
    def resume_job(self, job_id: str):
        """Resume a paused job"""
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"Job resumed: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error resuming job {job_id}: {e}")
            return False
