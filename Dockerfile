# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]