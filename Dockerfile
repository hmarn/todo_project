# Use official Python image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir virtualenv
RUN virtualenv venv
RUN . venv/bin/activate

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
# RUN python manage.py collectstatic --noinput

# Expose the port that Daphne will run on
EXPOSE 8000

# Command to run the application using Daphne for ASGI
CMD ["daphne", "todo_project.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
