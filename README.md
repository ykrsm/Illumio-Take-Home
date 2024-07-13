# Illumio Technical Assessment for Yuki Kuroshima

## Task
Description: Write a program that reads a file and finds matches against a predefined set of words. 

### Assumptions

Since there were no instructions regarding invalid file paths, I did not handle such cases. The script will throw a FileNotFoundError in this case. However, ideally, I should handle invalid file paths to avoid crashing the program.


## How to run the program 
To minimize issues related to environmental differences, I chose to use Docker to run this script.
My local environment has Docker version below.
```
docker -v
Docker version 27.0.3, build 7d4bcd8
```

To build, run unit tests, and execute the script, please run the command below.
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/input.txt \
--predefined ./resources/predefined_words.txt
```
Below is an example output.
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

To change the input and predefined words file, please place the files under the resources directory and update the command argument with the file path.
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/<updated-input-file>.txt \
--predefined ./resources/<updated-predefined-words-file>.txt
```

To test maximum file size, please run the command below:
```
docker build -t python-imagename . && \
docker run python-imagename \
--input ./resources/input_20mb.txt \
--predefined ./resources/predefined_words_10k.txt
```

## What has been tested 

All the functionalities are automated in unit tests tests/test_main.py

It tests:
* Case insensitivity: Ignore case when matching
* Punctuation handling: Remove punctuation before matching
* Whole word match: Match only whole words, not substrings
* File size: Exit if file size exceeds 20MB
* Predefined word count: Exit if predefined word count exceeds 10K
* Predefined word length: Exit if there is a predefined word that exceeds 256 characters
* Predefined word duplicate check: Exit if there is a duplicate predefined word

Additionally, I manually tested the code with a 20MB input file and 10,000 predefined words.
