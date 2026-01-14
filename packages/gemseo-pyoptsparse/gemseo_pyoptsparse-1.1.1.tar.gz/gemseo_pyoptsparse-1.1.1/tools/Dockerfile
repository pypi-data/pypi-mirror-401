FROM registry.gitlab.com/gemseo/dev/gemseo/multi-python:latest

RUN  dnf -y install libgfortran \
  && dnf clean all \
  && rm -rf /var/cache/dnf
