"""
Django management command for managing failed Celery tasks.

Usage:
    python manage.py celery_failed list [--limit N] [--task-name NAME] [--since DATE]
    python manage.py celery_failed show <task_id>
    python manage.py celery_failed retry <task_id>
    python manage.py celery_failed retry --all [--limit N] [--task-name NAME] [--since DATE]
"""
from django.core.management.base import BaseCommand, CommandError
from django_celery_results.models import TaskResult
from celery import current_app
from datetime import datetime
import json


class Command(BaseCommand):
    help = 'Manage failed Celery tasks (list, show, retry)'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand to run')

        # List subcommand
        list_parser = subparsers.add_parser('list', help='List failed tasks')
        list_parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of tasks to display (default: 50)'
        )
        list_parser.add_argument(
            '--task-name',
            type=str,
            help='Filter by task name'
        )
        list_parser.add_argument(
            '--since',
            type=str,
            help='Filter by date (ISO format: YYYY-MM-DD)'
        )

        # Show subcommand
        show_parser = subparsers.add_parser('show', help='Show detailed task info')
        show_parser.add_argument('task_id', type=str, help='Task ID to display')

        # Retry subcommand
        retry_parser = subparsers.add_parser('retry', help='Retry failed task(s)')
        retry_parser.add_argument(
            'task_id',
            nargs='?',
            type=str,
            help='Task ID to retry (omit when using --all)'
        )
        retry_parser.add_argument(
            '--all',
            action='store_true',
            help='Retry all failed tasks matching filters'
        )
        retry_parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of tasks to retry when using --all (default: 50)'
        )
        retry_parser.add_argument(
            '--task-name',
            type=str,
            help='Filter by task name when using --all'
        )
        retry_parser.add_argument(
            '--since',
            type=str,
            help='Filter by date when using --all (ISO format: YYYY-MM-DD)'
        )

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')

        if not subcommand:
            self.stdout.write(self.style.ERROR('Please specify a subcommand: list, show, or retry'))
            return

        if subcommand == 'list':
            self.handle_list(options)
        elif subcommand == 'show':
            self.handle_show(options)
        elif subcommand == 'retry':
            self.handle_retry(options)
        else:
            raise CommandError(f'Unknown subcommand: {subcommand}')

    def handle_list(self, options):
        """List failed tasks with optional filters."""
        queryset = TaskResult.objects.filter(status='FAILURE').order_by('-date_done')

        # Apply filters
        if options.get('task_name'):
            queryset = queryset.filter(task_name=options['task_name'])

        if options.get('since'):
            try:
                since_date = datetime.fromisoformat(options['since'])
                queryset = queryset.filter(date_done__gte=since_date)
            except ValueError:
                raise CommandError(f'Invalid date format: {options["since"]}. Use ISO format (YYYY-MM-DD)')

        # Apply limit
        limit = options.get('limit', 50)
        tasks = queryset[:limit]

        if not tasks:
            self.stdout.write(self.style.WARNING('No failed tasks found.'))
            return

        # Display header
        self.stdout.write(self.style.SUCCESS(f'\nFound {queryset.count()} failed task(s) (showing {len(tasks)}):\n'))
        self.stdout.write('-' * 120)
        self.stdout.write(f'{"TASK ID":<40} {"TASK NAME":<35} {"FAILED AT":<25} {"EXCEPTION"}')
        self.stdout.write('-' * 120)

        # Display tasks
        for task in tasks:
            task_id = task.task_id[:38] + '..' if len(task.task_id) > 40 else task.task_id
            task_name = task.task_name[:33] + '..' if len(task.task_name) > 35 else task.task_name
            date_done = task.date_done.strftime('%Y-%m-%d %H:%M:%S') if task.date_done else 'N/A'

            # Extract short exception summary
            exception_summary = self._get_exception_summary(task)

            self.stdout.write(f'{task_id:<40} {task_name:<35} {date_done:<25} {exception_summary}')

        self.stdout.write('-' * 120)
        self.stdout.write(f'\nUse "celery_failed show <task_id>" to see detailed information.')
        self.stdout.write(f'Use "celery_failed retry <task_id>" to retry a specific task.')
        self.stdout.write(f'Use "celery_failed retry --all" to retry all failed tasks.\n')

    def handle_show(self, options):
        """Show detailed information for a specific task."""
        task_id = options['task_id']

        try:
            task = TaskResult.objects.get(task_id=task_id)
        except TaskResult.DoesNotExist:
            raise CommandError(f'Task with ID {task_id} not found.')

        # Display detailed information
        self.stdout.write(self.style.SUCCESS(f'\n=== Task Details: {task_id} ===\n'))

        self.stdout.write(self.style.HTTP_INFO('Basic Information:'))
        self.stdout.write(f'  Task ID:       {task.task_id}')
        self.stdout.write(f'  Task Name:     {task.task_name}')
        self.stdout.write(f'  Status:        {self.style.ERROR(task.status)}')
        self.stdout.write(f'  Date Created:  {task.date_created if hasattr(task, "date_created") else "N/A"}')
        self.stdout.write(f'  Date Done:     {task.date_done}')

        # Display arguments and keyword arguments
        self.stdout.write(self.style.HTTP_INFO('\nTask Arguments:'))
        if task.task_args:
            try:
                args = json.loads(task.task_args) if isinstance(task.task_args, str) else task.task_args
                self.stdout.write(f'  Args:          {json.dumps(args, indent=2)}')
            except (json.JSONDecodeError, TypeError):
                self.stdout.write(f'  Args:          {task.task_args}')
        else:
            self.stdout.write('  Args:          None')

        if task.task_kwargs:
            try:
                kwargs = json.loads(task.task_kwargs) if isinstance(task.task_kwargs, str) else task.task_kwargs
                self.stdout.write(f'  Kwargs:        {json.dumps(kwargs, indent=2)}')
            except (json.JSONDecodeError, TypeError):
                self.stdout.write(f'  Kwargs:        {task.task_kwargs}')
        else:
            self.stdout.write('  Kwargs:        None')

        # Display exception and traceback
        self.stdout.write(self.style.HTTP_INFO('\nException Details:'))
        if task.result:
            try:
                result = json.loads(task.result) if isinstance(task.result, str) else task.result

                if isinstance(result, dict):
                    if 'exc_type' in result:
                        self.stdout.write(f'  Exception Type: {result["exc_type"]}')
                    if 'exc_message' in result:
                        self.stdout.write(f'  Exception Msg:  {result["exc_message"]}')
                else:
                    self.stdout.write(f'  Result:        {result}')
            except (json.JSONDecodeError, TypeError):
                self.stdout.write(f'  Result:        {task.result}')
        else:
            self.stdout.write('  No exception details available')

        # Display traceback
        if task.traceback:
            self.stdout.write(self.style.HTTP_INFO('\nTraceback:'))
            self.stdout.write(task.traceback)
        else:
            self.stdout.write(self.style.HTTP_INFO('\nTraceback:'))
            self.stdout.write('  No traceback available')

        self.stdout.write('\n')

    def handle_retry(self, options):
        """Retry one or all failed tasks."""
        if options.get('all'):
            self._retry_all(options)
        else:
            if not options.get('task_id'):
                raise CommandError('Please provide a task_id or use --all flag')
            self._retry_single(options['task_id'])

    def _retry_single(self, task_id):
        """Retry a single failed task."""
        try:
            task = TaskResult.objects.get(task_id=task_id)
        except TaskResult.DoesNotExist:
            raise CommandError(f'Task with ID {task_id} not found.')

        if task.status != 'FAILURE':
            self.stdout.write(self.style.WARNING(
                f'Task {task_id} has status {task.status}, not FAILURE. Retrying anyway...'
            ))

        # Get the task function
        try:
            task_func = current_app.tasks.get(task.task_name)
            if not task_func:
                raise CommandError(f'Task {task.task_name} not found in registered tasks.')
        except Exception as e:
            raise CommandError(f'Error loading task {task.task_name}: {e}')

        # Parse args and kwargs
        try:
            args = json.loads(task.task_args) if task.task_args else []
            kwargs = json.loads(task.task_kwargs) if task.task_kwargs else {}

            if not isinstance(args, list):
                args = []
            if not isinstance(kwargs, dict):
                kwargs = {}
        except (json.JSONDecodeError, TypeError) as e:
            raise CommandError(f'Error parsing task arguments: {e}')

        # Retry the task
        try:
            result = task_func.apply_async(args=args, kwargs=kwargs)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Task {task_id} requeued successfully!'
            ))
            self.stdout.write(f'  Original Task:  {task_id}')
            self.stdout.write(f'  New Task ID:    {result.id}')
            self.stdout.write(f'  Task Name:      {task.task_name}')
        except Exception as e:
            raise CommandError(f'Error retrying task: {e}')

    def _retry_all(self, options):
        """Retry all failed tasks matching filters."""
        queryset = TaskResult.objects.filter(status='FAILURE').order_by('-date_done')

        # Apply filters
        if options.get('task_name'):
            queryset = queryset.filter(task_name=options['task_name'])

        if options.get('since'):
            try:
                since_date = datetime.fromisoformat(options['since'])
                queryset = queryset.filter(date_done__gte=since_date)
            except ValueError:
                raise CommandError(f'Invalid date format: {options["since"]}. Use ISO format (YYYY-MM-DD)')

        # Apply limit
        limit = options.get('limit', 50)
        tasks = queryset[:limit]

        if not tasks:
            self.stdout.write(self.style.WARNING('No failed tasks found matching filters.'))
            return

        total_count = queryset.count()
        self.stdout.write(self.style.WARNING(
            f'\nFound {total_count} failed task(s). Will retry {len(tasks)} (limit: {limit}).\n'
        ))

        # Confirm before proceeding
        if total_count > 10:
            confirm = input(f'Continue with retry? (yes/no): ')
            if confirm.lower() not in ['yes', 'y']:
                self.stdout.write(self.style.WARNING('Retry cancelled.'))
                return

        success_count = 0
        error_count = 0

        for task in tasks:
            try:
                task_func = current_app.tasks.get(task.task_name)
                if not task_func:
                    self.stdout.write(self.style.ERROR(
                        f'✗ Task {task.task_id[:12]}... - {task.task_name} not found in registered tasks'
                    ))
                    error_count += 1
                    continue

                args = json.loads(task.task_args) if task.task_args else []
                kwargs = json.loads(task.task_kwargs) if task.task_kwargs else {}

                if not isinstance(args, list):
                    args = []
                if not isinstance(kwargs, dict):
                    kwargs = {}

                result = task_func.apply_async(args=args, kwargs=kwargs)
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Requeued {task.task_id[:12]}... → {result.id[:12]}... ({task.task_name})'
                ))
                success_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'✗ Error retrying {task.task_id[:12]}...: {str(e)[:60]}'
                ))
                error_count += 1

        # Summary
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'Successfully requeued: {success_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors:               {error_count}'))
        self.stdout.write('=' * 80 + '\n')

    def _get_exception_summary(self, task):
        """Extract a short exception summary from task result."""
        if not task.result:
            return 'No exception info'

        try:
            result = json.loads(task.result) if isinstance(task.result, str) else task.result

            if isinstance(result, dict):
                exc_type = result.get('exc_type', '')
                exc_message = result.get('exc_message', '')

                if exc_type:
                    summary = exc_type.split('.')[-1]  # Get class name only
                    if exc_message:
                        # Truncate message to fit
                        max_msg_len = 50
                        msg = exc_message[:max_msg_len]
                        if len(exc_message) > max_msg_len:
                            msg += '...'
                        summary += f': {msg}'
                    return summary
                elif exc_message:
                    return exc_message[:50] + ('...' if len(exc_message) > 50 else '')

            # Fallback to string representation
            result_str = str(result)
            return result_str[:50] + ('...' if len(result_str) > 50 else '')
        except Exception:
            return 'Unable to parse exception'