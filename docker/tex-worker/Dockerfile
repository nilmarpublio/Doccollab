FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-binaries \
    poppler-utils \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Worker is a minimal environment to run pdflatex; actual job runner can be added later.
CMD ["sleep","infinity"]
