#What it does: Specifies the starting point for your image. In this case, it uses the official lightweight Python 3.11 image.
#Why it matters: The base image includes tools and libraries you’ll need, saving you from starting from scratch.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#What it does: Sets the working directory inside the container. Any subsequent commands will run in this directory.
#Why it matters: Keeps your application files organized and ensures relative paths work correctly.
WORKDIR / app

#What it does: Copies the requirements.txt file from your local machine to the working directory in the container.
#Why it matters: You need your Python dependencies available to install them inside the container.
#I put it inside my /app because of "."
COPY requirements.txt .

#What it does: Runs a command to install the dependencies listed in requirements.txt using pip.
#Why it matters: Installs everything your app needs to run. The --no-cache-dir option prevents unnecessary caching, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

#What it does: Copies all the files from your project directory into the working directory in the container.
#Why it matters: This includes your app code, templates, and static file
COPY . .

#What it does: Informs Docker that the container will use port 8000.
#Why it matters: This is the port your app will listen on, and you’ll map it to a port on your host machine.
EXPOSE 8000

CMD ["gunicorn", "templatesLecture.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
