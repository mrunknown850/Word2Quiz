import time

from colorama import Back, Fore, Style
# print(Fore.YELLOW)
import docx2txt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exc
from selenium.webdriver.common.action_chains import ActionChains


def convertDoc2Txt(doc_direct: str) -> str:
    text = docx2txt.process(doc_direct)
    return text


def formatter(raw_string_inp: str) -> str:
    finalized = raw_string_inp
    while finalized.find("\n\n") != -1:
        finalized = finalized.replace("\n\n", "\n")
    return finalized


def filterer(pre_model, mode, formatted_string: str) -> dict:
    counter = 0  # This count what is the current question in number
    finalized = {}
    formatted_string += " Câu 69420"
    wordsByWord = formatted_string.split()
    SPECIAL_CHAR = "<-"

    optionCycle = 0  # 1 = optA | 2 = optB | 3 = optC | 4 = optD - Title Cycle
    titleList = []
    fullSentenceSegment = ""  # Sentences memory
    optionList = []
    answerList = []
    tmpSubOption = []  # [a, b, c, d]
    # Filtered Everything
    # ? ==================== SCAN MODE ====================
    # ? ================== LINEAR MODE ====================
    if mode == "2":
        for loc, word in enumerate(wordsByWord):
            # ? =============== Check if the sentence is an OPTION ============
            if ("A." in word) or ("B." in word) or ("C." in word) or ("D." in word):
                # ? ================= Check if the sentence is a TITLE ========
                # Title Cycle will + 1 everytime it's an option. 1,2,3 is ignor
                # If Title Cycle = 0 (First Question) -> The sentenceSegment is
                if optionCycle == 0 or ((optionCycle % 4) == 0):
                    titleList.append(fullSentenceSegment)
                    counter += 1
                else:
                    tmpSubOption.append(fullSentenceSegment)

                fullSentenceSegment = ""
                optionCycle += 1
            elif word == "Câu" and wordsByWord[loc + 1][:-1].isdigit():
                # ? ================ If this is NOT the First Question's Title
                if optionCycle != 0:
                    # ? ================ In case the tmpString is currently "D"
                    tmpSubOption.append(fullSentenceSegment)
                    # ! Append the options (1 loop is done)
                    optionList.append(tmpSubOption)
                    # ? ================ Looking for Answer in LINEAR SCAN ====
                    if pre_model[counter - 1] == "A":
                        answerList.append(tmpSubOption[0])
                    elif pre_model[counter - 1] == "B":
                        answerList.append(tmpSubOption[1])
                    elif pre_model[counter - 1] == "C":
                        answerList.append(tmpSubOption[2])
                    elif pre_model[counter - 1] == "D":
                        answerList.append(tmpSubOption[3])
                    tmpSubOption = []
                fullSentenceSegment = ""
                fullSentenceSegment += word
            else:
                fullSentenceSegment += " " + word
    # ? ==================== FILTERED MODE ====================
    # del tmpSubOption, fullSentenceSegment, optionCycle
    titleList = tuple(titleList)
    optionList = tuple(optionList)
    answerList = tuple(answerList)
    try:
        for questionId in range(len(titleList)):
            finalized[questionId] = {}
            finalized[questionId]["title"] = titleList[questionId]
            finalized[questionId]["answer"] = answerList[questionId]
            finalized[questionId]["options"] = optionList[questionId]

        # print(None)
    except IndexError:
        print("Lỗi | Lỗi ký hiệu, kiểm tra lại file")
    # print(titleList)
    # print(optionList)
    return finalized


def start(driver, questions_dictionary, email, password):
    EMAIL_ENTRY = (
        r'//*[@id="base-0"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/button[2]'
    )
    SUBMIT_BTN = r'/html/body/div[1]/div[1]/div/div[1]/main/footer/button'
    NEW_QUESTION = r'/html/body/div[1]/div[1]/div/div/main/section/div[2]/div/div/div/div/div[2]/div[1]/button'
    ENTRY = r'//*[@id="quiz-editor-content"]/section/div[2]/div/div[2]/div/button'
    NEW_LOOP = (
        r'//*[@id="modal-layer-2"]/div/div/div/body/div/div/div/div[2]/div[1]/button'
    )
    TITLE = (
        r'//*[@id="question-editor-container-mobile"]/main/div/section/div/div[1]/div/div[2]'
    )

    driver.get("https://www.quizizz.com/login")
    actions = ActionChains(driver)
    print("Đang kết nối vào quizizz.com...")
    # Login Screen -> Choose Email Option -> Create Quiz Screen
    driver.find_element(By.XPATH, EMAIL_ENTRY).click()
    emailTxt = driver.find_element(By.NAME, "Enter email address or username")
    passdTxt = driver.find_element(By.NAME, "Password")
    emailTxt.clear()
    passdTxt.clear()
    emailTxt.send_keys(email)
    passdTxt.send_keys(password)
    try:
        """
        REPLACE MODE/SWITCH HERE!!!
        """
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'continue-button'))
        )
        driver.find_element(By.CLASS_NAME, 'continue-button').click()
        print('Đang đăng nhập vào tài khoản Quizzi...')
        # Keyboard Navigate to Quiz Generate Area
        # driver.implicitly_wait(4)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'admin-external-link'))
        )
        driver.find_element(By.CLASS_NAME, 'admin-external-link').click()
        print('Đang vào menu tạo Quiz...')
        # ? ============== LOOP FOR EACH QUESTION ================
        # Initial Loop hole
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, NEW_QUESTION))
        )
        driver.find_element(By.XPATH, NEW_QUESTION).click()

        for questionStack in questions_dictionary.values():

            # ? ======================== WRITE THE QUESTION AND THE ANSWER ====
            print(Fore.YELLOW + '======================================')
            print('Question Title: ' + questionStack['title'])
            print('Options:', end=" ")
            print(questionStack['options'])
            print('Answer:' + questionStack['answer'])
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, TITLE))
            )

            # Interact
            driver.find_element(By.XPATH, TITLE).click()
            actions.send_keys(questionStack['title'])
            actions.perform()
            for i in range(len(questionStack['options'])):
                driver.find_element(By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/main/div/section/div/div[2]/div[1]/div[{i+1}]/div[2]").click()
                actions.send_keys(questionStack['options'][i])
                actions.perform()
                if questionStack['options'][i] == questionStack['answer']:
                    driver.find_element(By.XPATH, f"/html/body/div[1]/div[1]/div/div[2]/main/div/section/div/div[2]/div[1]/div[{i+1}]/div[2]").click()
                    actions.key_down(Keys.CONTROL).send_keys("M").key_up(Keys.CONTROL).perform()
                    # driver.execute_script('arguments[0].click();',
                                        #   driver.find_element(By.XPATH, f'//*[@id="question-editor-container-mobile"]/main/div/section/div/div[2]/div[1]/div[{i+1}]/div[1]/button[3]'))
                    # driver.find_element(By.XPATH,
                    #                     f"/html/body/div[1]/div[1]/div/div[2]/main/div/section/div/div[2]/div[1]/div[{i+1}]/div[1]/button[3]").click()
            time.sleep(1.5)
            driver.find_element(By.XPATH, SUBMIT_BTN).click()
            # ? ======================== ONE QUESTION LOOP DONE ===============

            # ? ======================== GENERATING A NEW CYCLE ===============
            if (questionStack['title'] ==
                    questions_dictionary[len(questions_dictionary) - 1]['title']):
                break
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, ENTRY))
            )
            driver.execute_script('arguments[0].click();',
                                  driver.find_element(By.XPATH, ENTRY))
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, NEW_LOOP))
            )
            driver.execute_script(
                'arguments[0].click();',
                driver.find_element(By.XPATH, NEW_LOOP))
        '''
        REPLACE MODE/SWITCH END
        '''

        #     ? ========================= COMPLETED ALL QUESTION ==============
        print(Fore.WHITE + "======================== Đã Làm Quiz xong! ===================")
        print("Hãy lưu lại Quiz và tắt cửa số trình duyệt")
        input("Ấn Enter để thoát...")
        driver.quit()
        print("Cảm ơn đã sử dụng - Credit: MrUnknown850")

    except exc.TimeoutException:
        print("Lỗi | Mạng chậm quá .-.")
