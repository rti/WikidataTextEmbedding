# Use the official Python image from the Docker Hub
FROM rocm/pytorch-nightly:2024-06-04-rocm6.1

# Upgrade the pip version to the most recent version
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
#  torchvision torchaudio


# Copy the rest of the application code into the container
COPY ./wikidata_datadump_textification.py ./wikidata_datadump_textification.py
COPY ./post_process_embed_df.py ./post_process_embed_df.py

# ARG FUNCTION_DIR="/var/task"
# RUN mkdir -p ${FUNCTION_DIR}
# COPY summarize.py ${FUNCTION_DIR}
# COPY --from=model /tmp/model ${FUNCTION_DIR}/model

# Create a volume to store the output CSV files
VOLUME /app/csvfiles

# Set the environment variable inside the Docker container
ENV WIKIMEDIA_TOKEN=$WIKIMEDIA_TOKEN
ENV N_COMPLETE=$N_COMPLETE
ENV EMBED=$EMBED
ENV EMBED_BATCHSIZE=$EMBED_BATCHSIZE

# Run the Python script
CMD ["python", "wikidata_datadump_textification.py"]
# CMD ["python", "post_process_embed_df.py"]