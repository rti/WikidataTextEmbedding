set -x

# Build the Docker image
docker build -t wikidata_datadump_textification .

mkdir -p $(pwd)/datadump
mkdir -p $(pwd)/csvfiles
mkdir -p $(pwd)/sqlitedbs

# Run the Docker container with the environment variable and volume mounting
docker run -it \
        -v $(pwd)/datadump:/app/datadump \
        -v $(pwd)/csvfiles:/app/csvfiles \
        -v $(pwd)/sqlitedbs:/app/sqlitedbs \
        -v $HOME/.cache/huggingface/hub:/root/.cache/huggingface/hub \
        -e WIKIMEDIA_TOKEN=$WIKIMEDIA_TOKEN \
        -e N_COMPLETE=100 \
        -e EMBED=True \
        -e EMBED_BATCHSIZE=32768 \
        --security-opt seccomp=unconfined \
        --device /dev/kfd \
        --device /dev/dri \
        wikidata_datadump_textification
