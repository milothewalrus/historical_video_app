from utils import download_images_from_wikipedia, get_related_links
from test_moviepy import generate_video
import os

def main():
    # Paths
    image_folder = "/Users/milesj/Code/historical_video_app/assets/images"
    output_video = "/Users/milesj/Code/historical_video_app/output.mp4"
    topic_file = "/Users/milesj/Code/historical_video_app/topic.txt"

    try:
        print("Welcome to the Historical Video Generator!")
        
        # Check for existing topic
        current_topic = None
        if os.path.exists(topic_file):
            with open(topic_file, "r") as file:
                current_topic = file.read().strip()
            print(f"Current historical topic: {current_topic}")

        # Check if assets exist
        assets_exist = os.path.exists(image_folder) and any(
            f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
            for f in os.listdir(image_folder)
        )

        # Step 3: Always prompt for user action first
        if current_topic and assets_exist:
            while True:
                try:
                    choice = input("\nAssets and topic already exist. Do you want to:\n"
                                 "1. Generate the video with existing assets\n"
                                 "2. Change the topic and download new images\n"
                                 "3. Exit\n"
                                 "Enter your choice (1, 2, or 3): ").strip()

                    if choice == "1":
                        confirm = input("Are you sure you want to generate a video with the existing assets? (y/n): ").strip().lower()
                        if confirm == 'y':
                            print(f"Generating video with existing assets for topic: {current_topic}")
                            generate_video(image_folder, output_video)
                            print(f"Video created successfully! Saved as {output_video}.")
                            return
                        else:
                            continue
                    elif choice == "2":
                        print("Switching to a new topic.")
                        current_topic = None
                        break
                    elif choice == "3":
                        print("Exiting program.")
                        return
                    else:
                        print("Invalid choice. Please try again.")
                        continue
                except EOFError:
                    print("\nInput interrupted. Please try again.")
                    continue

        # Step 4: Prompt for a new topic if necessary
        if not current_topic:
            current_topic = input("Enter a new historical topic or fact to search on Wikipedia: ").strip()
            
            # Add image count prompt
            while True:
                try:
                    image_count = int(input("How many images would you like to download? (max 50): ").strip())
                    if 1 <= image_count <= 50:
                        break
                    print("Please enter a number between 1 and 50.")
                except ValueError:
                    print("Please enter a valid number.")
            
            with open(topic_file, "w") as file:
                file.write(current_topic)

        # Step 5: Download images for the current topic
        print(f"Downloading images for topic: {current_topic}")
        download_images_from_wikipedia(current_topic, image_folder, image_count)  # Add image_count parameter


        # Step 6: Confirm downloaded images
        while True:
            print("\nImages downloaded:")
            print("\n".join(os.listdir(image_folder)))
            satisfied = input("Are you satisfied with the images? (y/n): ").strip().lower()
            if satisfied == "y":
                confirm_generate = input("Do you want to generate the video now? (y/n): ").strip().lower()
                if confirm_generate == "y":
                    break
                else:
                    print("Returning to image selection...")
                    continue
            else:
                # Fetch related links
                print(f"Fetching related links for {current_topic}...")
                related_links = get_related_links(current_topic)
                print("Related Wikipedia pages:")
                for i, link in enumerate(related_links, 1):
                    print(f"{i}: {link}")

                # Prompt user to download more images from a specific page
                index = input("Enter the number of the page to download more images from (or press Enter to skip): ").strip()
                if index.isdigit() and 1 <= int(index) <= len(related_links):
                    new_page = related_links[int(index) - 1]
                    print(f"Downloading more images from: {new_page}")
                    download_images_from_wikipedia(new_page, image_folder)

        # Step 7: Generate video only after explicit confirmation
        print(f"Generating video with images in {image_folder}...")
        generate_video(image_folder, output_video)
        print(f"Video created successfully! Saved as {output_video}.")
    except EOFError:
        print("\nError: No input detected. Please ensure you are running the script in an interactive environment.")

if __name__ == "__main__":
    main()