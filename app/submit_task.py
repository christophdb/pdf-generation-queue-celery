from tasks import generate_multiple_pdfs

html_template = "<h1>Hello World! PDF #{i}</h1>"
output_dir = "/tmp"
count = 100

result = generate_multiple_pdfs.delay(html_template, output_dir, count)
print(f"Task submitted! Task ID: {result.id}")
print(f"Check progress with: python3 check_result.py {result.id}")