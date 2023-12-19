import logging
from openai import OpenAI
import requests
import io
import pandas as pd
import csv

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# Configuration variables
KEY_API_TOKEN = '#api_token'

# List of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_API_TOKEN]


class Component(ComponentBase):
    def __init__(self):
        super().__init__()
        # Set API key for OpenAI
        self.client = OpenAI(api_key=self.configuration.parameters.get(KEY_API_TOKEN))
        self._output_writer = None

    def download_audio_from_url(self, audio_url):
        try:
            # Download the audio file from URL
            response = requests.get(audio_url)
            response.raise_for_status()  # Check if the request was successful

            buffer = io.BytesIO(response.content)
            buffer.name = "downloaded_audio.mp3"

            return buffer

        except Exception as e:
            logging.exception(f"Error downloading audio file from URL: {str(e)}")
            raise UserException("Error downloading audio file from URL.")

    def send_audio_to_whisper(self, audio_content):
        try:
            # Send the audio recording to Whisper ASR
            transcript = self.client.audio.transcriptions.create(model="whisper-1", file=audio_content)
            return transcript

        except Exception as e:
            logging.exception(f"Error processing Whisper ASR: {str(e)}")
            raise UserException("Error processing Whisper ASR.")
        
    def _parse_table(self):
        """
        Parses the data table.
        """

        # Get tables configuration
        in_tables = self.get_input_tables_definitions()

        if len(in_tables) == 0:
            raise UserException('There is no table specified on the input mapping! You must provide one input table!')
        elif len(in_tables) > 1:
            raise UserException(
                'There is more than one table specified on the input mapping! You must provide one input table!')

        # Get table
        table = in_tables[0]

        # Get table data
        logging.info(f'Processing input table: {table.name}')
        df = pd.read_csv(f'{table.full_path}', dtype=str)

        # Return error if there is no data
        if df.empty:
            logging.info(f'Input table {table.name} is empty!')

        return df
    
    def _create_tables_definitions(self):
        """
        Creates the tables definitions for output tables.
        """
        # Create tables definitions
        self._stats_table = self.create_out_table_definition('stats.csv', incremental=True, primary_key=['timestamp'])
        self.output_table = self.create_out_table_definition(
            'output.csv', incremental=True, primary_key=['id'])

        # Open output file in append mode, set headers and writer
        self._output_file = open(self.output_table.full_path, 'a', encoding='UTF-8', newline='')
        self._output_writer = csv.writer(self._output_file)

    def run(self):
        try:
            # Check mandatory parameters
            self.validate_configuration_parameters(REQUIRED_PARAMETERS)
            
            # Initialize _output_writer
            self._create_tables_definitions()

            df = self._parse_table()

            # For each row in the table
            for index, row in df.iterrows():
                id = row['id']
                message_id = row['message_id']
                audio_url = row['url']
                 # Optionally, you can log or use the transcript as needed.
                logging.info(f"Transcription in progress for audio URL: {audio_url}")
                
                audio_content = self.download_audio_from_url(audio_url)

                # Send the audio recording to Whisper ASR
                transcript = self.send_audio_to_whisper(audio_content)
                # Append the data to the output CSV file
                self._output_writer.writerow([id, message_id, audio_url, transcript.text if hasattr(transcript, 'text') else transcript])

        except UserException as exc:
            logging.exception(exc)
            exit(1)
        except Exception as exc:
            logging.exception(exc)
            exit(2)
        finally:
            # Close the file in the finally block to ensure it's closed even if an error occurs
            if self._output_file:
                self._output_file.close()


if __name__ == "__main__":
    try:
        comp = Component()
        # This triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
