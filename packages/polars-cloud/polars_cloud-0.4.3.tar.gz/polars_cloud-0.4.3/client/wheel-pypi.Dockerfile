ARG CLIENT_VERSION


FROM python:3.13.10 AS builder

WORKDIR /app/dist

ARG CLIENT_VERSION

RUN pip download --only-binary=:all: \
          --python-version 3.10 \
          --implementation cp \
          --platform manylinux_2_28_x86_64 \
          --no-deps polars-cloud==$CLIENT_VERSION \
 && pip download --only-binary=:all: \
          --python-version 3.11 \
          --implementation cp \
          --platform manylinux_2_28_x86_64 \
          --no-deps polars-cloud==$CLIENT_VERSION \
 && pip download --only-binary=:all: \
          --python-version 3.12 \
          --implementation cp \
          --platform manylinux_2_28_x86_64 \
          --no-deps polars-cloud==$CLIENT_VERSION \
 && pip download --only-binary=:all: \
          --python-version 3.13 \
          --implementation cp \
          --platform manylinux_2_28_x86_64 \
          --no-deps polars-cloud==$CLIENT_VERSION \
 && pip download --only-binary=:all: \
          --python-version 3.14 \
          --implementation cp \
          --platform manylinux_2_28_x86_64 \
          --no-deps polars-cloud==$CLIENT_VERSION

FROM scratch

COPY --from=builder /app/dist /
