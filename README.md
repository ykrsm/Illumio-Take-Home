# Illumio Technical Assessment for Yuki Kuroshima

## Task
Description: Write a program that reads a file and finds matches against a predefined set of words. 
There can be up to 10K entries in the list of predefined words. The output of the program should look something like this: 

### Assumptions

Since there was no instruction around invalid file path, I did not handle such case. The script with throw `FileNotFoundError` in this case.

## How to run the program 
Docker ver:
To minimize the issue related to environmental difference, I chose to use docker to run this script.
My local environment has docker version below.
```
docker -v
Docker version 27.0.3, build 7d4bcd8
```

To build, run unit test, and execut the script, please run the command below.
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/input.txt \
--predefined ./resources/predefined_words.txt
```
Below is example output.
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/input.txt \
--predefined ./resources/predefined_words.txt
[+] Building 1.4s (9/9) FINISHED                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 277B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9              0.7s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/4] FROM docker.io/library/python:3.9@sha256:47d6f16aa0de11f2748c73  0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 6.33kB                                        0.0s
 => CACHED [2/4] WORKDIR /app                                              0.0s
 => [3/4] COPY . /app                                                      0.0s
 => [4/4] RUN python -m unittest tests/*                                   0.5s
 => exporting to image                                                     0.0s
 => => exporting layers                                                    0.0s
 => => writing image sha256:271e7df2d46a1d2c23c6241f2e721a728c6af32b2ecb9  0.0s
 => => naming to docker.io/library/python-imagename                        0.0s

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview
Predefined word      Match count
AI                   1
Name                 2
```

To test maximum file size, please run below
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/input_20mb.txt \
--predefined ./resources/predefined_words_10k.txt
```

## What has been tested 

The main functionalities have been tested using unit tests located in tests/test_main.py.

* Notable test cases include handling punctuation edge cases with the test_count_matches function.
* Additionally, manual testing has been conducted with a 20MB input file and 10,000 predefined words.

