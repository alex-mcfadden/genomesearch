# Project Name

Genome Finder Job Queue - Ginkgo Takehome Project

## Description

This is a web tool that accepts a DNA sequence and enters it into a Celery job queue. The job queue is processed by a worker, which aligns it to a set of common
viral genomes, returning the first close match. The results are stored in a database and displayed on the web page. 

## Technologies

Backend: Python, Django, Celery, Redis, PostgreSQL

Frontend: ReactJS, Axios

## Installation

```
$ git clone
$ docker-compose build
$ docker-compose up
```

## Usage

Navigate to `http://localhost:3000` in your web browser. Submit a DNA sequence
to enter it into the job queue. The same page contains a table of the job queue.


## Contact

If you have any questions or feedback, feel free to reach out to [alexander.mcfadden@gmail.com](alexander.mcfadden@gmail.com).
