# Use an official Python image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY app.py score.py /app/
COPY requirements.txt /app/

COPY best_model.pkl /app/


# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app runs on
EXPOSE 5000

# Run the Flask application when the container starts
CMD ["python", "app.py"]
