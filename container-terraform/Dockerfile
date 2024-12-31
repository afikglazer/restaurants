# Use an official Python runtime as a parent image
FROM python:3.10-slim

COPY main.py /

# Install any needed packages specified in requirements.txt
# If you have other dependencies, list them in a requirements.txt file
RUN pip install --no-cache-dir boto3 flask

EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "main.py"]
