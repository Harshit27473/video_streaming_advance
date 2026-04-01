import os
from pathlib import Path

from  secret_keys import SecretKeys
import boto3
import subprocess


secret_keys = SecretKeys()

class VideoTranscoder:
    def __init__(self):
        self.s3_client =boto3.client(
            "s3", 
            region_name=secret_keys.REGION_NAME,
            aws_access_key_id=secret_keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=secret_keys.AWS_SECRET_ACCESS_KEY,
        )

    def _get_content_type(self, file_path: str):    
        if file_path.endswith(".m3u8"):
            return "application/vnd.apple.mpegurl"
        elif file_path.endswith(".ts"):
            return "video/mp2t"
        
 
    def download_video(self, local_path):
        self.s3_client.download_file(
            secret_keys.S3_BUCKET,
            secret_keys.S3_KEY,
            local_path,
        ) 

    def transcode_video(self, input_path, output_dir):
        # HLS
        cmd = [
            "ffmpeg",
            "-i",
            input_path,
            "-filter_complex",
            "[0:v]split=3[v1][v2][v3];"
            "[v1]scale=640:360:flags=fast_bilinear[360p];"
            "[v2]scale=1280:720:flags=fast_bilinear[720p];"
            "[v3]scale=1920:1080:flags=fast_bilinear[1080p]",
            "-map",
            "[360p]",
            "-map",
            "[720p]",
            "-map",
            "[1080p]",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-profile:v",
            "high",
            "-level:v",
            "4.1",
            "-g",
            "48",
            "-keyint_min",
            "48",
            "-sc_threshold",
            "0",
            "-b:v:0",
            "1000k",
            "-b:v:1",
            "4000k",
            "-b:v:2",
            "8000k",
            "-f",
            "hls",
            "-hls_time",
            "6",
            "-hls_playlist_type",
            "vod",
            "-hls_flags",
            "independent_segments",
            "-hls_segment_type",
            "mpegts",
            "-hls_list_size",
            "0",
            "-master_pl_name",
            "master.m3u8",
            "-var_stream_map",
            "v:0 v:1 v:2",
            "-hls_segment_filename",
            f"{output_dir}/%v/segment_%03d.ts",
            f"{output_dir}/%v/playlist.m3u8",
        ]
        process= subprocess.run(cmd)

        if process.returncode != 0:
            raise Exception("Error in transcoding video")
    
    def upload_files(self, prefix: str, local_dir):
        for root, _, files in os.walk(local_dir):
            for file in files:
                local_path= os.path.join(root, file)
                s3_key = f"{prefix}/{os.path.relpath(local_path, local_dir)}"
                self.s3_client.upload_file(
                    local_path,
                    secret_keys.S3_PROCESSED_VIDEOS_BUCKET, 
                    s3_key,
                    ExtraArgs={
                        'ACL': 'public-read',
                        'ContentType': self._get_content_type(local_path)
                    },
                    )
    
    def process_video(self):
        work_dir = Path("/tmp/workspace")
        work_dir.mkdir(exist_ok=True)
        input_path = work_dir / "input.mp4" 
        output_path = work_dir / "output"
        output_path.mkdir(exist_ok=True)
        try:
            self.download_video(input_path)
            self.transcode_video(str(input_path), str(output_path))
            self.upload_files(secret_keys.S3_KEY, str(output_path) )
        finally:
            if input_path.exists():
                input_path.unlink()
            if output_path.exists():
                import shutil 

                shutil.rmtree(output_path)

VideoTranscoder().process_video()