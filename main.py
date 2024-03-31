from assets.file_manage import convertDoc2Txt, formatter
from assets.file_manage import filterer, start
from selenium import webdriver


def main(doc_dir, passwd, mail, options, modeSel, model):
    currentDocxString = convertDoc2Txt(doc_dir)
    currentDocxString = formatter(currentDocxString)
    finalizedDictionary = filterer(model, modeSel, currentDocxString)
    if options == "1":
        driver = webdriver.Chrome()
    elif options == "2":
        driver = webdriver.ChromiumEdge()
    elif options == "3":
        driver = webdriver.Firefox()

    start(driver, finalizedDictionary, mail, passwd)


if __name__ == "__main__":
    print("========== Word2Quiz - Credit: MrUnknown6000 ==========")
    OPT = "2"
    # ? 1: Scan Mode - NONE | 2: Linear Mode - STR | 3: Filtered Mode - LIST
    MODE = "2"
    ANSWER_SHEET = "ACDAABBDBDAACABBDCBDBDADACAABAABCDDAAABDCDCAAACCAABDACCCCDABAA"

