import os
import subprocess
from django.conf import settings
from celery import shared_task


@shared_task
def process_video(video_id):
    from .models import Video
    try:
        video = Video.objects.get(id=video_id)
        input_path = video.file.path
        filename = os.path.splitext(os.path.basename(input_path))[0]

        # 1080
        high_quality_output = f'videos/converted/{filename}_high.mp4'
        high_quality_path = os.path.join(settings.MEDIA_ROOT, high_quality_output)
        high_quality_command = f'ffmpeg -i {input_path} -c:v libx264 -crf 18 -c:a aac -b:a 192k {high_quality_path}'
        subprocess.run(high_quality_command, shell=True, check=True)

        # 360
        low_quality_output = f'videos/converted/{filename}_low.mp4'
        low_quality_path = os.path.join(settings.MEDIA_ROOT, low_quality_output)
        low_quality_command = f'ffmpeg -i {input_path} -c:v libx264 -crf 28 -c:a aac -b:a 128k {low_quality_path}'
        subprocess.run(low_quality_command, shell=True, check=True)

        # video model update
        video.processed_file = input_path  # Original file path
        video.low_quality = low_quality_output
        video.high_quality = high_quality_output
        video.save()

        return {
            'status': 'success',
            'video_id': video_id,
            'high_quality_path': high_quality_output,
            'low_quality_path': low_quality_output
        }

    except Video.DoesNotExist:
        return {'status': 'error', 'error': 'Video not found'}
    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'error': str(e)}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

