import pytest
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import random

link = "https://todomvc.com/examples/angular2/"


# fixture to define the browser driver
@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()


# for helping to catch an exception if the element is not present on the page
def is_not_element_present(browser, what):
    try:
        browser.find_element_by_css_selector(what)
    except NoSuchElementException:
        return True
    return False


# for helping to catch an exception if the element is not interactable
def is_not_element_available(browser, what):
    try:
        action = ActionChains(browser)
        element = browser.find_element_by_css_selector(what)
        action.move_to_element(element).click().perform()
    except ElementNotInteractableException:
        return True
    return False


@pytest.mark.positive
# test adding new item
def test_positive_add_item(browser):
    browser.get(link)
    time.sleep(2)
    # find the text area
    add_textarea = browser.find_element_by_css_selector(".new-todo")
    add_textarea.click()
    # create random list with numerous values
    item = random.choice(['one', '0a', '@#', '098759485938502840583904580285', 'FGFJJDKK LLL SSSS LLLLL'])
    add_textarea.send_keys(item)
    add_textarea.send_keys(Keys.ENTER)
    # find the adding item
    check = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view label')
    item_counter = browser.find_element_by_css_selector('todo-count, strong')
    time.sleep(2)
    # compare the text in the item and the text that was sent to it
    assert (check.text == item) and (item_counter.text == '1'), 'TODO item has not been added!'


@pytest.mark.positive
# test edit existing item
def test_positive_edit_item(browser):
    # firstly add item
    test_positive_add_item(browser)
    to_edit_text_area = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view label')
    text = to_edit_text_area.text
    action = ActionChains(browser)
    # double click to edit
    action.double_click(to_edit_text_area).perform()
    time.sleep(2)
    search_edit_text_area = browser.find_element_by_css_selector('.editing')
    search_edit_text_area.click()
    # switch to the field
    for_edit_text_area = browser.switch_to.active_element
    browser.implicitly_wait(20)
    # add to the end of the line
    for_edit_text_area.send_keys(Keys.END)
    for_edit_text_area.send_keys('new')
    for_edit_text_area.send_keys(Keys.ENTER)
    time.sleep(2)
    # find the item that has been edited
    check = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view')
    # compare the item after editing and the correct example
    assert check.text == text + 'new', 'TODO item was not edit correctly!'


@pytest.mark.positive
# test delete existing item
def test_positive_delete_item(browser):
    # firstly add item
    test_positive_add_item(browser)
    # necessary actions to move the cursor from inside the window -
    # to get around the Chrome driver bug with move_to_element action
    to_edit_text_area = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view label')
    to_edit_text_area.click()
    action = ActionChains(browser)
    # finding the delete button
    x_button = browser.find_element_by_css_selector('button.destroy')
    # hover above the delete button and click when it became visible
    action.move_to_element(x_button).click().perform()
    time.sleep(2)
    # find if all the elements, counters and links were deleted
    assert is_not_element_present(browser, 'todo-count, strong') and \
           is_not_element_present(browser, '[class=todo-list] > li:nth-child(1)> div.view label'), \
            'TODO item was not deleted!'


@pytest.mark.positive
# test complete an item
def test_positive_complete_item(browser):
    # firstly add item
    test_positive_add_item(browser)
    select_item_to_complete = browser.find_element_by_css_selector('[class=toggle][type=checkbox]:nth-child(1)')
    # check the checkbox
    select_item_to_complete.click()
    time.sleep(2)
    item_counter = browser.find_element_by_css_selector('todo-count, strong')
    text = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1) label')
    # find if the counter was decreased, the button link "Clear completed" appeared, the text was scratched and
    # the item checkbox was checked
    assert (item_counter.text == '0') and browser.find_element_by_css_selector('[class=clear-completed]') and \
           text.value_of_css_property('text-decoration') == 'line-through solid rgb(217, 217, 217)' and \
           text.value_of_css_property('background-image') == 'url("data:image/svg+xml;utf8,%3Csvg%20xmlns%3D%22http%3A//' \
                                                             'www.w3.org/2000/svg%22%20width%3D%2240%22%20height%3D%2240' \
                                                             '%22%20viewBox%3D%22-10%20-18%20100%20135%22%3E%3Ccircle%20' \
                                                             'cx%3D%2250%22%20cy%3D%2250%22%20r%3D%2250%22%20fill%3D%22' \
                                                             'none%22%20stroke%3D%22%23bddad5%22%20stroke-width%3D%223%' \
                                                             '22/%3E%3Cpath%20fill%3D%22%235dc2af%22%20d%3D%22M72%2025L' \
                                                             '42%2071%2027%2056l-4%204%2020%2020%2034-52z%22/%3E%3C/svg%3E")', \
        'TODO item has not be completed!'


@pytest.mark.positive
# test remove completed item
def test_positive_clear_complete_item(browser):
    # firstly add and complete item
    test_positive_complete_item(browser)
    # clear existing item
    clear_button = browser.find_element_by_css_selector('[class=clear-completed]')
    clear_button.click()
    time.sleep(2)
    # find if all the elements, counters and links were deleted
    assert is_not_element_present(browser, 'todo-count, strong') and \
           is_not_element_present(browser, '[class=todo-list] > li:nth-child(1)> div.view label') and \
           is_not_element_present(browser, '[class=clear-completed]'), 'Completed TODO has not been cleared!'


@pytest.mark.negative
# test trying to add blank item
def test_negative_add_blank_item(browser):
    browser.get(link)
    time.sleep(2)
    # find the text area
    add_textarea = browser.find_element_by_css_selector(".new-todo")
    add_textarea.click()
    # without entering any value press Enter
    add_textarea.send_keys(Keys.ENTER)
    # find if all the elements, counters and links has not appeared
    assert is_not_element_present(browser, 'todo-count, strong') and \
           is_not_element_present(browser, '[class=todo-list] > li:nth-child(1)> div.view label') and \
           is_not_element_present(browser, '[class=clear-completed]'), 'Blank TODO cannot be added!'


@pytest.mark.negative
# test trying to save empty item
# WILL FAIL!!
def test_negative_save_empty_item(browser):
    # firstly add item
    test_positive_add_item(browser)
    # find the existing item
    to_edit_text_area = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view label')
    action = ActionChains(browser)
    # double click to edit
    action.double_click(to_edit_text_area).perform()
    time.sleep(2)
    # addition click to place cursor inside editing item
    search_edit_text_area = browser.find_element_by_css_selector('.editing')
    search_edit_text_area.click()
    # switch to the field
    for_edit_text_area = browser.switch_to.active_element
    browser.implicitly_wait(20)
    # delete all the data
    for_edit_text_area.clear()
    # DO NOT press Enter
    time.sleep(2)
    # find if the blank item is still there
    assert is_not_element_present(browser, '[class=todo-list] > li:nth-child(1)> div.view'), 'Blank TODO must be deleted!'
    # Actually the test has found a bug: if the user clears the item and then doesn't press Enter and just click
    # somewhere on the screen, the empty item remains


@pytest.mark.negative
# test find Clear complete link after unchecking an item
def test_negative_find_the_complete_link_after_unchecking_item(browser):
    # firstly add item
    test_positive_add_item(browser)
    select_item_to_complete = browser.find_element_by_css_selector('[class=toggle][type=checkbox]:nth-child(1)')
    # check the item
    select_item_to_complete.click()
    time.sleep(2)
    # uncheck the item
    select_item_to_complete.click()
    time.sleep(2)
    assert is_not_element_present(browser, '[class=clear-completed]'), '"Clear completed" link must be invisible!'


@pytest.mark.negative
# test try to remove item while edit
def test_negative_try_to_remove_item_while_edit(browser):
    # firstly add item
    test_positive_add_item(browser)
    to_edit_text_area = browser.find_element_by_css_selector('[class=todo-list] > li:nth-child(1)> div.view label')
    action = ActionChains(browser)
    # double click to edit
    action.double_click(to_edit_text_area).perform()
    time.sleep(2)
    # try to click the delete button
    assert is_not_element_available(browser, '[class=destroy]'), 'TODO cannot be deleted while editing!'
