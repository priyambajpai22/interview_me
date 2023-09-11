import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pydub import AudioSegment
from pydub.playback import play

import asyncio
from io import BytesIO
import base64
from django.http import HttpResponse
import ssl



class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name
        import pdb;pdb.set_trace()

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        await self.stream_video('/home/golu/Downloads/The.Purge.mp4')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # This function receive messages from WebSocket.
    

    async def receive(self, bytes_data=None,text_data=None):
        import pdb;pdb.set_trace()
        #print(bytes_data)
        import pdb;pdb.set_trace()
        #text_data_json = json.loads(text_data)
        #message = text_data_json["message"]
        #username = text_data_json["username"]

        # Convert the audio data to an AudioSegment
        #bytes_data = base64.b64decode(bytes_data)

        audio = AudioSegment.from_file(BytesIO(bytes_data),format="mp3")
        import pdb;pdb.set_trace()

            # Play the audio
        play(audio)

        await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chatbox_message",
                    "message": "message",
                    "username": "username",
                },
            )
    # Receive message from room group.
    async def stream_video(self, video_path):
        with open(video_path, 'rb') as video_file:
            while True:
                video_data = video_file.read(1024)
                if not video_data:
                    break
                encoded_data = base64.b64encode(video_data).decode('utf-8')
                await self.send(encoded_data)




import argparse
import asyncio
import json
import logging
import os
import platform
import ssl

from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from aiortc.rtcrtpsender import RTCRtpSender
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import argparse

ROOT = os.path.dirname(__file__)


relay = None
webcam = None


def create_local_tracks(play_from, decode):
    global relay, webcam

    if play_from:
        import pdb;pdb.set_trace()
        player = MediaPlayer('/home/golu/Downloads/istockphoto-1212501173-640_adpp_is.mp4',decode=decode)
        return player.audio, player.video
    else:
        options = {"framerate": "30", "video_size": "640x480"}
        if relay is None:
            if platform.system() == "Darwin":
                webcam = MediaPlayer(
                    "default:none", format="avfoundation", options=options
                )
            elif platform.system() == "Windows":
                webcam = MediaPlayer(
                    "video=Integrated Camera", format="dshow", options=options
                )
            else:
                webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(webcam.video)


def force_codec(pc, sender, forced_codec):
    kind = forced_codec.split("/")[0]
    codecs = RTCRtpSender.getCapabilities(kind).codecs
    transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
    transceiver.setCodecPreferences(
        [codec for codec in codecs if codec.mimeType == forced_codec]
    )


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)
from asgiref.sync import async_to_sync

@csrf_exempt
@async_to_sync
async def offer(request):
    parser = argparse.ArgumentParser(description="WebRTC webcam demo")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument("--play-from", help="Read the media from a file and sent it."),
    parser.add_argument(
        "--play-without-decoding",
        help=(
            "Read the media without decoding it (experimental). "
            "For now it only works with an MPEGTS container with only H.264 video."
        ),
        action="store_true",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument(
        "--audio-codec", help="Force a specific audio codec (e.g. audio/opus)"
    )
    parser.add_argument(
        "--video-codec", help="Force a specific video codec (e.g. video/H264)"
    )
    parser.add_argument('runserver',help='run server')

    args = parser.parse_args()
    params=json.loads(request.body)
    #params =  request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    print(args.play_without_decoding)
    audio, video = create_local_tracks(
        True, decode=not args.play_without_decoding
    )

    if audio:
        audio_sender = pc.addTrack(audio)
        if args.audio_codec:
            force_codec(pc, audio_sender, args.audio_codec)
        elif args.play_without_decoding:
            raise Exception("You must specify the audio codec using --audio-codec")

    if video:
        video_sender = pc.addTrack(video)
        if args.video_codec:
            force_codec(pc, video_sender, args.video_codec)
        elif args.play_without_decoding:
            raise Exception("You must specify the video codec using --video-codec")
        
    import pdb;pdb.set_trace()

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    from asgiref.sync import async_to_sync

    return HttpResponse(json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),content_type="application/json")








pcs = set()
