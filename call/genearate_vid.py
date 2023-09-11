import subprocess
import os
import asyncio

import asyncio
import os

# Set the name of your virtual environment
virtualenv_name = '/home/golu/venv/vid2vid'

# Set the path to the Python executable inside the virtual environment
python_executable = os.path.join(virtualenv_name, 'bin', 'python') if os.name != 'nt' else os.path.join(virtualenv_name, 'Scripts', 'python.exe')

# Set the path to the file you want to execute
file_to_execute = '/home/golu/Text2Video/text2video_audio.sh'

async def activate_virtualenv():
    # Activate the virtual environment
    activate_script = os.path.join(virtualenv_name, 'bin', 'activate') if os.name != 'nt' else os.path.join(virtualenv_name, 'Scripts', 'activate.bat')
    activate_cmd = f'{activate_script}' if os.name != 'nt' else f'activate {virtualenv_name}'
    await asyncio.create_subprocess_shell('source',activate_cmd)

async def execute_file():
    # Execute the file
    await asyncio.create_subprocess_shell("sh text2video_tts.sh 'She had your dark suit in greasy wash water all year'. fadg0 f")

async def main():
    # Activate the virtual environment
    await activate_virtualenv()

    # Execute the file
    await execute_file()

