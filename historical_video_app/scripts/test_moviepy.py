from moviepy.editor import ImageClip, concatenate_videoclips
import os

def generate_video(image_folder, output_path, duration_per_image=3):
    """
    Generate a video from images in the specified folder.
    
    Args:
        image_folder (str): Path to folder containing images
        output_path (str): Path where the output video will be saved
        duration_per_image (int): Duration for each image in seconds
    """
    # Get all image files
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if not image_files:
        raise ValueError("No image files found in the specified folder")

    # Create clips for each image
    clips = []
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        clip = ImageClip(image_path).set_duration(duration_per_image)
        clips.append(clip)

    # Concatenate all clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the result to a file
    final_clip.write_videofile(output_path, fps=24)