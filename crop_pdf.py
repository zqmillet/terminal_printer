import PyPDF2

def crop_pdf(file_path):
    with open(file_path, 'rb') as file:
        input_file = PyPDF2.PdfFileReader(file)

        output = PyPDF2.PdfFileWriter()
        page_number = input_file.getNumPages()

        for index in range(page_number):
            page = input_file.getPage(index)

            # lower_left = page.cropBox.getLowerLeft()
            # upper_right = page.cropBox.getUpperRight()

            # page.trimBox.lowerLeft = lower_left
            # page.trimBox.upperRight = upper_right

            # page.mediaBox.lowerLeft = lower_left
            # page.mediaBox.upperRight = upper_right
            import pdb; pdb.set_trace()

            output.addPage(page)

    with open(file_path, 'wb') as file:
        output.write(file)

def testcases():
    crop_pdf('./main.pdf')

if __name__ == '__main__':
    testcases()
