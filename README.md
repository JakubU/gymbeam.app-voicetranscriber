VoiceTranscriber
=============

Description

**The VoiceTranscriber component streamlines the integration of LiveAgent recordings and leverages OpenAI's Whisper API for swift and precise voice-to-text translation. Effortlessly convert audio data into readable and editable text for efficient content management and analysis. Experience enhanced communication and streamlined content processing with this powerful voice transcription tool.**

Functionality notes
===================

### 1. Transcription Process

The OpenAI Whisper  Component is designed to transcribe audio files using the Whisper Automatic Speech Recognition (ASR) model. The process involves the following steps:

- **Input Data:** The component takes input data in the form of a CSV file containing ticket IDs and corresponding audio file URLs.

- **Download Audio:** It downloads the audio files from the provided URLs.

- **Whisper ASR:** The audio recordings are sent to the Whisper ASR API for transcription.

- **Output Data:** The transcriptions are then stored in an output CSV file along with the ticket IDs and original audio URLs.

### 2. Configuration

The component requires configuration through a YAML file (`config.yml`). The configuration includes specifying the OpenAI API token.

Example `config.yml`:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
yaml
components:
  openai-whisper-asr:
    parameters:
      api_token: 'your_openai_api_token'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prerequisites
=============

Before using the OpenAI Whisper ASR Component, make sure you have the following prerequisites in place:

### 1. OpenAI API Key

Obtain an API key from OpenAI to authenticate requests to the Whisper ASR API. Follow these steps:

1. Visit the [OpenAI website](https://www.openai.com/).
2. Sign in or create a new account.
3. Navigate to the API section and follow the instructions to generate an API key.


Supported endpoints
===================

## 1. `POST /audio/transcriptions`

- **Description**: Initiates audio transcriptions using the OpenAI Whisper ASR model.
- **Parameters**:
  - `model`: Specifies the ASR model to use (e.g., "whisper-1").
  - `file`: The audio file content to transcribe.
- **Response**: Returns the transcription result.

## 2. `GET /status`

- **Description**: Retrieves the status of the OpenAI Whisper ASR service.
- **Parameters**: None.
- **Response**: Returns the status information.

## 3. `GET /audio/transcriptions/{transcriptionId}`

- **Description**: Retrieves the transcription results for a specific transcription ID.
- **Parameters**:
  - `transcriptionId`: The unique identifier for the transcription job.
- **Response**: Returns the transcription results.

**Note**: Ensure that the OpenAI API key used with the component has the necessary permissions to access and utilize these endpoints. Refer to the OpenAI API documentation for detailed information on each endpoint and their usage. Adjust the details based on the specific characteristics and requirements of the OpenAI Whisper Transcription component.

Configuration
=============


The following configuration parameters are required:

- `#api_token`: OpenAI API key for authentication.

# Input Configuration

The input configuration involves specifying the input table containing audio URLs to be transcribed.

## Input Table Structure

The input table should have the following structure:

| `id` | `url`                                       |
|-------------|---------------------------------------------|
| 1           | https://example.com/audio/sample1.mp3       |
| 2           | https://example.com/audio/sample2.mp3       |
| ...         | ...                                         |

# Output Configuration

The component generates output tables with transcriptions. The output CSV file structure includes:

| `id` | `url`                                       | `text`                            |
|-------------|---------------------------------------------|-----------------------------------|
| 1           | https://example.com/audio/sample1.mp3       | Transcription of audio sample1.mp3|
| 2           | https://example.com/audio/sample2.mp3       | Transcription of audio sample2.mp3|
| ...         | ...                                         | ...                               |

# Example Configuration

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to
your custom path in the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following
command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone https://github.com/JakubU/gymbeam.app-voicetranscriber gymbeam.app-voicetranscriber
cd gymbeam.app-voicetranscriber
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers
documentation](https://developers.keboola.com/extend/component/deployment/)
