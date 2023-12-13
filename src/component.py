import logging
from openai import OpenAI
import requests
import io


from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# configuration variables
KEY_API_TOKEN = '#api_token'
audio_url = 'https://gymbeam.ladesk.com/scripts/file.php?view=Y&file=6edrsokf8axgxe7t28n3zml1fgtgfinn'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_API_TOKEN]


class Component(ComponentBase):
    def __init__(self):
        super().__init__()
        # Nastavení API klíče pro OpenAI
        self.client = OpenAI(api_key=self.configuration.parameters.get(KEY_API_TOKEN))

    def download_audio_from_url(self, audio_url):
        try:
            # Stiahnutie zvukového súboru z URL
            response = requests.get(audio_url)
            response.raise_for_status()  # Zkontroluje, zda byl požadavek úspěšný

            buffer = io.BytesIO(response.content)
            buffer.name = "downloaded_audio.mp3"

            return buffer

        except Exception as e:
            logging.exception(f"Chyba pri stahovaní zvukového súboru z URL: {str(e)}")
            raise UserException("Chyba pri stahovaní zvukového súboru z URL.")

    def send_audio_to_whisper(self, audio_content):
        try:
            # Odeslanie nahrávky na Whisper ASR
            transcript = self.client.audio.transcriptions.create(model="whisper-1", file=audio_content)
            return transcript

        except Exception as e:
            logging.exception(f"Chyba pri zpracovaní Whisper ASR: {str(e)}")
            raise UserException("Chyba pri zpracovaní Whisper ASR.")

    def run(self):
        try:
            # Kontrola povinných parametrov
            self.validate_configuration_parameters(REQUIRED_PARAMETERS)
            audio_content = self.download_audio_from_url(audio_url)

            # Odeslanie nahrávky na Whisper ASR
            transcript = self.send_audio_to_whisper(audio_content)
            
            # Optionally, you can log or use the transcript as needed.
            logging.info(f"Whisper ASR Transcript: {transcript}")
        except UserException as exc:
            logging.exception(exc)
            exit(1)
        except Exception as exc:
            logging.exception(exc)
            exit(2)


if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
