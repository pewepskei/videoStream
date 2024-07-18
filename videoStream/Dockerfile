# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app/

# Install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /usr/src/app/

# Run migrations and collect static files (if needed)
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Expose the port that the Django app will run on
EXPOSE 8000

# Run the Django application
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]

