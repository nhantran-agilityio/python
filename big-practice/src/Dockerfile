# Use the official Python image from the Docker Hub
FROM python:3.12-slim


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install Gunicorn
RUN pip install gunicorn

# Collect static files (adjust according to your needs)
RUN python manage.py collectstatic --noinput

# Expose the port on which the app will run
EXPOSE 8000

# Define the command to run the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "studentManagement.wsgi:application"]
