# Build the Docker image
docker build -t wikidata_datadump_textification .

# Run the Docker container with the environment variable and volume mounting
docker run -it \
        -v $HOME/Research/Wikidata:/app/datadump \
        -v $(pwd)/csvfiles:/app/csvfiles \
        -v $(pwd)/sqlitedbs:/app/sqlitedbs \
        -v $HOME/.cache/huggingface/hub:/root/.cache/huggingface/hub \
        -e WIKIMEDIA_TOKEN=$WIKIMEDIA_TOKEN \
        -e N_COMPLETE=100 \
        -e EMBED=True \
        -e EMBED_BATCHSIZE=100 \
        wikidata_datadump_textification

# --gpus all \

