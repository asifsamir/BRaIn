import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Function to create a 'bug' element for each bug in the JSON file
def create_bug_element(bug):
    bug_elem = ET.Element("bug", id=str(bug["bug_id"]))

    # Add 'buginformation' element
    buginfo_elem = ET.SubElement(bug_elem, "buginformation")

    # Add 'summary' element
    summary_elem = ET.SubElement(buginfo_elem, "summary")
    summary_elem.text = bug["bug_title"]

    # Add 'description' element
    description_elem = ET.SubElement(buginfo_elem, "description")
    description_elem.text = bug["bug_description"]

    # Add 'version' element
    version_elem = ET.SubElement(buginfo_elem, "version")
    version_elem.text = bug["version"]

    # Add 'fixed_version' element
    fixed_version_elem = ET.SubElement(buginfo_elem, "fixed_version")
    fixed_version_elem.text = bug["fixed_version"]

    # Add 'project' element
    project_elem = ET.SubElement(buginfo_elem, "project")
    project_elem.text = bug["project"]

    # Add 'sub_project' element
    sub_project_elem = ET.SubElement(buginfo_elem, "sub_project")
    sub_project_elem.text = bug["sub_project"]

    # Add 'fixedFiles' element and 'file' sub-element for each fixed file
    fixed_files_elem = ET.SubElement(bug_elem, "fixedFiles")
    for file in bug["fixed_files"]:
        file_elem = ET.SubElement(fixed_files_elem, "file")
        file_elem.text = file

    return bug_elem


# Function to convert JSON data to XML
def convert_json_to_xml(json_data, output_file):
    # Create root element
    root = ET.Element("bugrepository", name="all")

    # Iterate over each bug report and create an XML element for it
    for bug in json_data:
        bug_elem = create_bug_element(bug)
        root.append(bug_elem)

    # Create a tree from the root
    tree = ET.ElementTree(root)

    # Pretty print the XML
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    # Write the pretty XML to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)


json_bug_file = "D:\Research\Data\Intelligent_Feedback\ML_Relevance_output\Qwen_ZERO_combined.json"
xml_output_file = "D:\Research\Data\Intelligent_Feedback\ML_Relevance_output\Qwen_ZERO_combined.xml"
# Load the JSON file
with open(json_bug_file, 'r') as json_file:
    bug_data = json.load(json_file)

# Convert JSON to XML and save to a file
convert_json_to_xml(bug_data, xml_output_file)

print("Conversion completed!.")
