import xml.etree.ElementTree as ET
import pandas as pd
import html

def parse_specific_head(file_path, output_excel_path, target_section="§ 135.1 Applicability."):
    # Load the XML file and parse it
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []

    # Find the DIV8 tag with the correct section
    for div in root.findall(".//DIV8[@N='135.1']"):
        head = div.find('HEAD')
        if head is not None and html.unescape(head.text.strip()) == target_section:
            # Extract the title from the HEAD tag
            head_text = html.unescape(head.text.strip())
            title_parts = head_text.split('§')[-1].split(' ', 1)
            rule_number = title_parts[0].strip()
            rule_title = title_parts[1].strip() if len(title_parts) > 1 else "Unknown Title"

            # Initialize hierarchy tracking
            parent_section = ""
            current_section = ""

            for p in div.findall('P'):
                text = ''.join(p.itertext()).strip()
                if text:
                    # Unescape HTML entities (e.g., `&#xA7;` -> `§`, `&#x2014;` -> `—`)
                    text = html.unescape(text)

                    # Check for hierarchy markers like "(a)", "(1)", etc.
                    if text.startswith("(") and ")" in text[:4]:  # Matches patterns like "(a)" or "(1)"
                        hierarchy_marker = text.split(")", 1)[0].strip()  # Extract the marker
                        
                        # Determine if it's a parent or child section
                        if len(hierarchy_marker) == 1:  # Single letter (e.g., "(a)")
                            parent_section = hierarchy_marker
                            current_section = parent_section  # Reset child marker
                        else:  # Nested child marker (e.g., "(1)", "(a)(1)")
                            current_section = f"{parent_section}{hierarchy_marker}"

                        # Format the text properly
                        text = f"{current_section}) {text.split(')', 1)[1].strip()}"
                    else:
                        # If no new marker, continue with the current section
                        text = f"{current_section}) {text}"

                    # Append the row to the data list
                    data.append([f"{rule_number} {rule_title}", text])

    # Convert to a DataFrame
    df = pd.DataFrame(data, columns=["Rule Title", "Subparts"])

    # Save the DataFrame to an Excel file
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="135.1 Applicability")
    print(f"Table successfully saved to: {output_excel_path}")

# Main function to execute the script
def main():
    # File paths
    xml_file_path = "data/title-14.xml"  # Replace with your XML file path
    output_excel_path = "outputs/output_table.xlsx"    # Replace with your desired output file path

    # Target section to extract
    target_section = "§ 135.1 Applicability."

    # Call the parsing function
    parse_specific_head(xml_file_path, output_excel_path, target_section)

# Run the main function
if __name__ == "__main__":
    main()
