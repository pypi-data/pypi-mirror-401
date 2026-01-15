ARG PROFILE=dev


FROM quay.io/pypa/manylinux_2_28_aarch64:latest AS manylinux-arm64

FROM quay.io/pypa/manylinux_2_28_x86_64:latest AS manylinux-amd64

FROM manylinux-${TARGETARCH} AS base

WORKDIR /app

# we use this variant rather than rustup show since we only want the minimal profile (rustup show installs clippy too)
COPY --from=client rust-toolchain.toml rust-toolchain.toml
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain $(grep "channel" rust-toolchain.toml | grep -oP '(?<=").*(?=")')

ENV PATH="$PATH:/root/.cargo/bin"

RUN cargo install --locked maturin@1.10.2


FROM base AS base-amd64

RUN curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v33.1/protoc-33.1-linux-x86_64.zip \
    && unzip protoc-33.1-linux-x86_64.zip -d /opt/protoc \
    && ln -s /opt/protoc/bin/protoc /usr/local/bin/protoc \
    && rm protoc-33.1-linux-x86_64.zip


FROM base AS base-arm64

RUN curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v33.1/protoc-33.1-linux-aarch_64.zip \
    && unzip protoc-33.1-linux-aarch_64.zip -d /opt/protoc \
    && ln -s /opt/protoc/bin/protoc /usr/local/bin/protoc \
    && rm protoc-33.1-linux-aarch_64.zip


FROM base-${TARGETARCH} AS builder

COPY --from=contracts . /app/contracts
COPY --from=client . /app/client

ARG PROFILE

RUN maturin build --profile $PROFILE --out dist --manifest-path client/Cargo.toml

FROM scratch

COPY --from=builder /app/dist /
