# from moviepy.editor import ImageSequenceClip
# import os


# def get_files_from_directory(directory):
#     files = []
#     for file in os.listdir(directory):
#         full_path = os.path.join(directory, file)
#         if os.path.isfile(full_path):
#             files.append(full_path)
#     return files

# # List of JPG image files
# image_files = get_files_from_directory('./frames')

# # Load each image
# images = sorted([image for image in image_files])
# print(images)
# # # Create a clip from the sequence of images
# clip = ImageSequenceClip(images, fps=30)  # You can adjust the fps as needed

# # # Write the clip to a video file
# clip.write_videofile("./output_video.mp4")