"""
Image Extraction from PDF/DOCX
Extracts images and uses Gemini Vision to describe them
"""

import os
import io
import base64
from PIL import Image
from datetime import datetime
import tempfile

# For PDF image extraction
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("⚠️ PyMuPDF not installed. Install with: pip install PyMuPDF")

# For DOCX image extraction
try:
    from docx import Document as DocxDocument
    from docx.oxml import parse_xml
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# For image description using Gemini Vision
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
import google.generativeai as genai

# Initialize Gemini with vision capabilities
genai.configure(api_key=GEMINI_API_KEY)


def extract_images_from_pdf(pdf_path: str, output_dir: str = None) -> list:
    """
    Extract all images from a PDF file
    Returns list of image info dictionaries
    """
    if not PYMUPDF_AVAILABLE:
        return []
    
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extracted_images = []
    
    try:
        # Open PDF
        pdf_document = fitz.open(pdf_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                # Get image data
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Save image
                image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                # Get image dimensions
                try:
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    width, height = pil_image.size
                except:
                    width, height = "Unknown", "Unknown"
                
                extracted_images.append({
                    "page": page_num + 1,
                    "index": img_index + 1,
                    "filename": image_filename,
                    "path": image_path,
                    "format": image_ext,
                    "width": width,
                    "height": height,
                    "size_kb": len(image_bytes) / 1024
                })
        
        pdf_document.close()
        print(f"✅ Extracted {len(extracted_images)} images from PDF")
        return extracted_images
    
    except Exception as e:
        print(f"⚠️ Error extracting images from PDF: {e}")
        return []


def extract_images_from_docx(docx_path: str, output_dir: str = None) -> list:
    """
    Extract all images from a DOCX file
    Returns list of image info dictionaries
    """
    if not DOCX_AVAILABLE:
        return []
    
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    extracted_images = []
    
    try:
        doc = DocxDocument(docx_path)
        
        # Extract images from document relationships
        image_index = 1
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_data = rel.target_part.blob
                
                # Determine image extension
                content_type = rel.target_part.content_type
                if "png" in content_type:
                    ext = "png"
                elif "jpeg" in content_type or "jpg" in content_type:
                    ext = "jpg"
                elif "gif" in content_type:
                    ext = "gif"
                else:
                    ext = "png"
                
                # Save image
                image_filename = f"img{image_index}.{ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_data)
                
                # Get image dimensions
                try:
                    pil_image = Image.open(io.BytesIO(image_data))
                    width, height = pil_image.size
                except:
                    width, height = "Unknown", "Unknown"
                
                extracted_images.append({
                    "index": image_index,
                    "filename": image_filename,
                    "path": image_path,
                    "format": ext,
                    "width": width,
                    "height": height,
                    "size_kb": len(image_data) / 1024
                })
                
                image_index += 1
        
        print(f"✅ Extracted {len(extracted_images)} images from DOCX")
        return extracted_images
    
    except Exception as e:
        print(f"⚠️ Error extracting images from DOCX: {e}")
        return []


def describe_image_with_gemini(image_path: str) -> str:
    """
    Use Gemini Vision to describe an image
    """
    try:
        # Load image
        img = Image.open(image_path)
        
        # Use Gemini Vision model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = """Analyze this image and provide:
1. A brief description of what the image shows
2. Key elements or objects visible
3. Any text visible in the image
4. The likely purpose or context of this image
5. Any technical details (diagrams, charts, code, etc.)

Be detailed but concise."""
        
        response = model.generate_content([prompt, img])
        return response.text
    
    except Exception as e:
        print(f"⚠️ Error describing image: {e}")
        return f"Error analyzing image: {e}"


def extract_and_describe_images(file_path: str, describe_with_ai: bool = True) -> dict:
    """
    Main function to extract and optionally describe images from documents
    """
    try:
        # Determine file type
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Create output directory
        output_dir = os.path.join(tempfile.gettempdir(), f"extracted_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract images based on file type
        if file_ext == ".pdf":
            if not PYMUPDF_AVAILABLE:
                return {
                    "success": False,
                    "error": "PyMuPDF not installed. Install with: pip install PyMuPDF",
                    "images": []
                }
            images = extract_images_from_pdf(file_path, output_dir)
        elif file_ext == ".docx":
            if not DOCX_AVAILABLE:
                return {
                    "success": False,
                    "error": "python-docx not installed. Install with: pip install python-docx",
                    "images": []
                }
            images = extract_images_from_docx(file_path, output_dir)
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {file_ext}",
                "images": []
            }
        
        # Describe images with AI if requested
        if describe_with_ai and images:
            print("🤖 Analyzing images with Gemini Vision...")
            for img_info in images:
                try:
                    description = describe_image_with_gemini(img_info["path"])
                    img_info["ai_description"] = description
                except Exception as e:
                    img_info["ai_description"] = f"Error: {e}"
        
        return {
            "success": True,
            "total_images": len(images),
            "output_directory": output_dir,
            "images": images
        }
    
    except Exception as e:
        print(f"⚠️ Error in extract_and_describe_images: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "images": []
        }


def format_image_extraction_report(extraction_result: dict) -> str:
    """
    Format image extraction results into readable report
    """
    if not extraction_result["success"]:
        return f"⚠️ Image extraction failed: {extraction_result.get('error', 'Unknown error')}"
    
    images = extraction_result["images"]
    
    if not images:
        return "ℹ️ No images found in the document."
    
    report = f"""✅ **Image Extraction Complete!**

📊 **Summary:**
- Total images extracted: {extraction_result['total_images']}
- Saved to: `{extraction_result['output_directory']}`

---

"""
    
    for img in images:
        report += f"### 🖼️ Image {img.get('index', img.get('page', '?'))}\n\n"
        report += f"- **File:** `{img['filename']}`\n"
        if 'page' in img:
            report += f"- **Page:** {img['page']}\n"
        report += f"- **Format:** {img['format'].upper()}\n"
        report += f"- **Size:** {img['width']} x {img['height']} pixels\n"
        report += f"- **File Size:** {img['size_kb']:.1f} KB\n"
        
        if 'ai_description' in img:
            report += f"\n**AI Analysis:**\n{img['ai_description']}\n"
        
        report += "\n---\n\n"
    
    return report


def detect_image_extraction_request(user_msg: str) -> bool:
    """
    Detect if user wants to extract images
    """
    keywords = [
        "extract image", "get image", "show image", "find image",
        "extract picture", "get picture", "show picture",
        "extract all images", "list images", "image extraction"
    ]
    
    msg_lower = user_msg.lower()
    return any(keyword in msg_lower for keyword in keywords)