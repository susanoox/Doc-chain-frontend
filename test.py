import markdown

# Read the README.md file
with open("README.md", "r", encoding="utf-8") as md_file:
    md_content = md_file.read()

# Convert Markdown content to HTML
html_content = markdown.markdown(md_content)

# Save the HTML content to a new file
with open("README.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

print("README.md has been successfully converted to README.html")
