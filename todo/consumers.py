import json
import asyncio
import logging
from datetime import timedelta
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

logger = logging.getLogger(__name__)

class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from todo.models import Task
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task = await database_sync_to_async(Task.objects.get)(id=self.task_id)
        self.timer_task = None
        await self.accept()

    async def disconnect(self, close_code):
        await self.stop_loop()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'start':
            await self.start_timer()
        elif action == 'pause':
            await self.pause_timer()
        elif action == 'resume':
            await self.resume_timer()
        elif action == 'reset':
            await self.reset_timer()

    async def start_timer(self):
        self.task.timer_start = timezone.now()
        await self.update_duration()
        self.task.timer_end = None
        self.task.paused_duration = timedelta(seconds=0)
        await self.save_task()

        await self.start_loop()
        await self.send_time_update()
        logger.info(f"[Task {self.task.id}] Timer started at {self.task.timer_start}")

    async def pause_timer(self):
        if self.task.timer_start and not self.task.timer_end:
            self.task.timer_end = timezone.now()
            await self.stop_loop()
            await self.update_duration()
            await self.save_task()
        await self.send_time_update()
        logger.info(f"[Task {self.task.id}] Timer stopped at {self.task.timer_end}")

    async def resume_timer(self):
        if self.task.timer_start and self.task.timer_end:
            paused_time = timezone.now() - self.task.timer_end
            self.task.timer_start += paused_time
            self.task.timer_end = None
            await self.save_task()

            await self.start_loop()
        await self.send_time_update()

    async def reset_timer(self):
        self.task.timer_start = None
        self.task.timer_end = None
        self.task.duration = 0
        await self.stop_loop()
        await self.save_task()
        await self.send_time_update()

    async def timer_loop(self):
        counter = 0
        while True:
            await asyncio.sleep(1)
            counter += 1
            await self.send_time_update()

            if counter % 10 == 0:
                await self.update_duration()
                logger.debug(f"[Task {self.task.id}] Auto-saved duration at {self.task.duration} seconds")

    async def start_loop(self):
        if not self.timer_task or self.timer_task.done():
            self.timer_task = asyncio.create_task(self.timer_loop())

    async def stop_loop(self):
        if self.timer_task:
            self.timer_task.cancel()
            try:
                await self.timer_task
            except asyncio.CancelledError:
                pass

    async def send_time_update(self):
        if self.task.timer_start and not self.task.timer_end:
            duration = timezone.now() - self.task.timer_start
        elif self.task.timer_start and self.task.timer_end:
            duration = self.task.timer_end - self.task.timer_start
        else:
            duration = timedelta(0)

        # Calculate hours, minutes, and seconds
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Send the data back to the client
        await self.send(text_data=json.dumps({
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }))

    async def save_task(self):
        await database_sync_to_async(self.task.save)()

    async def update_duration(self):
        if self.task.timer_start:
            if self.task.timer_end:
                # Paused or stopped
                elapsed = self.task.timer_end - self.task.timer_start
            else:
                # Still running
                elapsed = timezone.now() - self.task.timer_start

            self.task.duration = int(elapsed.total_seconds())
            await self.save_task()
            logger.info(f"[Task {self.task.id}] Duration saved: {self.task.duration} seconds")


