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