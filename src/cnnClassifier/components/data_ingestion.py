import os
import requests
from cnnClassifier.entity.config_entity import DataIngestionConfig
import zipfile
from cnnClassifier import logger

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
            response = requests.get(self.config.source_URL, stream=True)
            response.raise_for_status()  # Check if the request was successful
            with open(self.config.local_data_file, 'wb') as wf:
                for chunk in response.iter_content(chunk_size=1024):
                    wf.write(chunk)
            logger.info(f"File downloaded successfully and saved to {self.config.local_data_file}")
        else:
            logger.info(f"File already exists at {self.config.local_data_file}")


    def unzip_and_clean(self):
        """Unzips the downloaded file and removes the zip file after extraction."""

        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"File unzipped successfully to {unzip_path}")
        

    def initiate_data_ingestion(self):
        self.download_file()
        self.unzip_and_clean()