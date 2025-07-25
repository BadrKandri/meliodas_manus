from agno.tools.python import PythonTools
from agno.tools.file import FileTools 
from agno.tools import Toolkit, tool
from typing import Dict
import pandas as pd
import zipfile
import os 
import shutil
import subprocess
import re

def execute_code() : 
    return PythonTools() 

def file_operations() : 
    return FileTools()  

def extract_charts_with_spire(excel_file: str, output_directory: str = "charts") -> Dict:
    """
    Extract charts from Excel using Spire.XLS (your working method)
    """
    print(f"📊 Extracting charts with Spire.XLS from: {excel_file}")
    
    try:
        from spire.xls import Workbook
        
        # Create output directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Load workbook
        workbook = Workbook()
        workbook.LoadFromFile(excel_file)
        
        chart_files = []
        total_charts = 0
        
        # Extract charts from each worksheet
        for sheet in workbook.Worksheets:
            for i, chart in enumerate(sheet.Charts):
                chart_filename = f"{sheet.Name}_Chart_{i+1}.png"
                image_path = os.path.join(output_directory, chart_filename)
                
                # Save chart as image
                chart.SaveToImage(image_path)
                
                chart_files.append({
                    "filename": chart_filename,
                    "path": image_path,
                    "sheet": sheet.Name,
                    "chart_index": i + 1
                })
                
                total_charts += 1
                print(f"✅ Saved chart: {chart_filename}")
        
        return {
            "success": True,
            "total_charts": total_charts,
            "charts": chart_files,
            "output_directory": output_directory,
            "method": "spire_xls_extraction"
        }
        
    except ImportError:
        return {
            "success": False,
            "error": "Spire.XLS not installed. Please install with: pip install Spire.XLS",
            "charts": []
        }
    except Exception as e:
        print(f"❌ Spire chart extraction failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "charts": []
        }

def extract_images_from_excel(excel_filepath: str, output_directory: str = "extracted_images") -> Dict:
    """
    Extract embedded images from Excel file
    """
    print(f"🖼️ Extracting images from Excel: {excel_filepath}")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    temp_dir = os.path.join(output_directory, "temp_excel_extract")
    os.makedirs(temp_dir, exist_ok=True)

    extracted_images = []

    try:
        with zipfile.ZipFile(excel_filepath, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        media_path = os.path.join(temp_dir, 'xl', 'media')
        if os.path.exists(media_path):
            for i, filename in enumerate(os.listdir(media_path)):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    source_path = os.path.join(media_path, filename)
                    output_path = os.path.join(output_directory, f"image_{i+1}_{filename}")

                    # Copy image file
                    shutil.copy(source_path, output_path)

                    extracted_images.append({
                        "filename": f"image_{i+1}_{filename}",
                        "path": output_path,
                        "original_name": filename
                    })

                    print(f"✅ Extracted image: {filename}")

        return {
            "success": True,
            "total_images": len(extracted_images),
            "images": extracted_images,
            "output_directory": output_directory
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "images": []
        }

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

class ExcelParserTool(Toolkit) : 
    """
     Use this tool for Excel parsing with working chart extraction
    """
    def __init__(self) : 
        super().__init__(name="excel_parser", tools=[
            self.excel_parser, 
            self.analyze_extracted_image_content,
            self.extract_and_analyze_charts,
            self.extract_and_analyze_images
        ])

    def excel_parser(self, file_path: str) -> Dict:  
        """ 
        Basic Excel parsing for structure and data
        """
        print(f"🔍 Starting Excel analysis for: {file_path}")

        results = {
            "file_path": file_path,
            "sheets": {},
            "success": False,
            "errors": []
        }

        if not os.path.exists(file_path):
            results["errors"].append(f"File not found: {file_path}")
            print(f"❌ File not found: {file_path}")
            return results

        try:
            excel_file = pd.ExcelFile(file_path)

            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)

                results["sheets"][sheet_name] = {
                    "shape": df.shape,
                    "columns": list(df.columns),
                    "dtypes": df.dtypes.to_dict(),
                    "sample_data": df.head(3).to_dict()
                }

                print(f"✅ Loaded sheet: {sheet_name} - {df.shape[0]} rows × {df.shape[1]} cols")

            results["success"] = True
            print("✅ Excel parsing completed successfully!")

        except Exception as e:
            results["errors"].append(str(e))
            print(f"❌ Error: {e}")

        return results
                
    def analyze_extracted_image_content(self, image_path: str) -> Dict:
        """Analyze image content using direct OpenAI API call"""
        print(f"👁️ Analyzing image content: {image_path}")

        try:
            import base64
            import json
            import requests

            if not os.path.exists(image_path):
                return {"error": f"Image file not found: {image_path}"}

            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Get API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return {"error": "OpenAI API key not found"}

            # Direct API call to OpenAI
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image and describe what you see. If this is a chart or graph, focus on: chart type, data values, trends, axes labels, legend, patterns, insights, and key takeaways. If it's a regular image, describe the content, objects, text, and visual elements. Provide a comprehensive analysis. Keep response detailed but under 300 words."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 400
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, 
                                   json=payload,
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content']
                
                print(f"✅ Image analysis completed successfully")
                
                return {
                    "image_path": image_path,
                    "analysis_success": True,
                    "description": description,
                    "file_size": os.path.getsize(image_path),
                    "message": "Image analyzed successfully with vision AI"
                }
            else:
                error_msg = f"API call failed: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('error', {}).get('message', 'Unknown error')}"
                except:
                    error_msg += f" - {response.text}"
                
                print(f"❌ Vision API error: {error_msg}")
                return {
                    "error": error_msg,
                    "analysis_success": False
                }

        except Exception as e:
            print(f"❌ Image analysis error: {str(e)}")
            return {
                "error": f"Failed to analyze image: {str(e)}",
                "analysis_success": False
            }

    def extract_and_analyze_charts(self, file_path: str) -> Dict:
        """Extract charts using Spire.XLS and analyze them with vision AI"""
        print(f"📊🔍 Extracting and analyzing charts from: {file_path}")
        
        # Step 1: Extract charts using your working Spire method
        extraction_result = extract_charts_with_spire(file_path)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "error": extraction_result["error"],
                "message": "Chart extraction failed"
            }
        
        if extraction_result["total_charts"] == 0:
            return {
                "success": True,
                "charts_found": 0,
                "message": "No charts found in the Excel file",
                "extraction_method": "spire_xls"
            }
        
        # Step 2: Analyze each extracted chart with vision AI
        chart_analyses = []
        
        for chart_info in extraction_result["charts"]:
            print(f"🔍 Analyzing chart: {chart_info['filename']}")
            
            analysis = self.analyze_extracted_image_content(chart_info["path"])
            
            if analysis.get("analysis_success"):
                chart_analyses.append({
                    "chart_file": chart_info["filename"],
                    "path": chart_info["path"],
                    "sheet": chart_info["sheet"],
                    "chart_index": chart_info["chart_index"],
                    "analysis": analysis["description"],
                    "file_size": f"{os.path.getsize(chart_info['path'])} bytes",
                    "extraction_method": "spire_xls"
                })
                print(f"✅ Successfully analyzed: {chart_info['filename']}")
            else:
                chart_analyses.append({
                    "chart_file": chart_info["filename"],
                    "path": chart_info["path"],
                    "sheet": chart_info["sheet"],
                    "chart_index": chart_info["chart_index"],
                    "analysis": f"Analysis failed: {analysis.get('error', 'Unknown error')}",
                    "extraction_method": "spire_xls",
                    "analysis_failed": True
                })
                print(f"❌ Analysis failed for: {chart_info['filename']}")
        
        return {
            "success": True,
            "method": "spire_xls_with_vision_analysis",
            "charts_found": len(chart_analyses),
            "total_charts_extracted": extraction_result["total_charts"],
            "chart_analyses": chart_analyses,
            "output_directory": extraction_result["output_directory"],
            "message": f"Successfully extracted {extraction_result['total_charts']} charts and analyzed {len([c for c in chart_analyses if not c.get('analysis_failed')])} with vision AI"
        }

    def extract_and_analyze_images(self, file_path: str) -> Dict:
        """Extract embedded images from Excel and analyze them with vision AI"""
        print(f"🖼️🔍 Extracting and analyzing images from: {file_path}")
        
        # Step 1: Extract images from Excel
        extraction_result = extract_images_from_excel(file_path)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "error": extraction_result["error"],
                "message": "Image extraction failed"
            }
        
        if extraction_result["total_images"] == 0:
            return {
                "success": True,
                "images_found": 0,
                "message": "No embedded images found in the Excel file",
                "extraction_method": "zip_extraction"
            }
        
        # Step 2: Analyze each extracted image with vision AI
        image_analyses = []
        
        for image_info in extraction_result["images"]:
            print(f"🔍 Analyzing image: {image_info['filename']}")
            
            analysis = self.analyze_extracted_image_content(image_info["path"])
            
            if analysis.get("analysis_success"):
                image_analyses.append({
                    "image_file": image_info["filename"],
                    "path": image_info["path"],
                    "original_name": image_info["original_name"],
                    "analysis": analysis["description"],
                    "file_size": f"{os.path.getsize(image_info['path'])} bytes",
                    "extraction_method": "zip_extraction"
                })
                print(f"✅ Successfully analyzed: {image_info['filename']}")
            else:
                image_analyses.append({
                    "image_file": image_info["filename"],
                    "path": image_info["path"],
                    "original_name": image_info["original_name"],
                    "analysis": f"Analysis failed: {analysis.get('error', 'Unknown error')}",
                    "extraction_method": "zip_extraction",
                    "analysis_failed": True
                })
                print(f"❌ Analysis failed for: {image_info['filename']}")
        
        return {
            "success": True,
            "method": "zip_extraction_with_vision_analysis",
            "images_found": len(image_analyses),
            "total_images_extracted": extraction_result["total_images"],
            "image_analyses": image_analyses,
            "output_directory": extraction_result["output_directory"],
            "message": f"Successfully extracted {extraction_result['total_images']} images and analyzed {len([c for c in image_analyses if not c.get('analysis_failed')])} with vision AI"
        }
                         
def excel_parser() : 
    return ExcelParserTool()




@tool("latex_runner")
def compile_latex(tex_file_path: str):
    try:
        subprocess.run(["C:\\tectonic\\tectonic.exe", tex_file_path], check=True)
        print("✅ PDF generated successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Error during LaTeX compilation:", e)
        
@tool

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    mapping = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\^{}', '\\': r'\textbackslash{}', '€': r'\euro{}'
    }
    pattern = re.compile('|'.join(re.escape(k) for k in mapping))
    return pattern.sub(lambda m: mapping[m.group()], text)

tools = [excel_parser(), execute_code(), file_operations(), compile_latex, escape_latex]