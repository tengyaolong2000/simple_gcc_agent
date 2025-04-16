from visual_qa import (process_images_and_text, 
                       encode_image, 
                       resize_image,
                       VisualQATool,
                       visualizer)



def test_visual_qa_tool():
    print("Testing VisualQATool...")
    # Initialize the VisualQATool
    tool = VisualQATool()

    # Provide the path to a local image
    image_path = "/Users/tengyaolong/Desktop/GCC_Agent/SCREENSHOTS/screenshot_1_1.png"  # Replace with the path to your test image
    question = "What is happening in this image?"

    # Test the forward method
    try:
        print(f"Question: {question}")
        response = tool.forward(image_path, question)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error during VisualQATool test: {e}")



if __name__ == "__main__":
    # Run the test for VisualQATool
    test_visual_qa_tool()