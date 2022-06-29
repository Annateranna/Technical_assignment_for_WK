Test suit by Anna Ter-Oganesian
Testing application: https://todomvc.com/examples/angular2/

Project Technical_assignment_for_WK contains:
test_todomvc.py - file with all test-cases
pytest.ini - define marks (for positive and negative scenarios)
__init__.py - for packets initializing
requirements.txt - contains requirements with which the tests will definitely  work

To run the test a tester must have: Selenium WebDrv, Pytest,  Chrome driver
Use command in command line (in Selenium virtual environments):
pytest -m "positive and negative" test_todomvc.py

Result in command line must be (for failed test see comments below):
============== short test summary info ============================================
FAILED test_todomvc.py::test_negative_save_empty_item - AssertionError: Blank TODO must be deleted!
============= 1 failed, 8 passed in 93.08s (0:01:33) ==============================


The tested web-application is a simple TODO list. 
Typical business requirements are: 1) add TODO, 2) edit TODO, 3) delete TODO, 4) complete TODO, 5) remove completed TODO

So the main 5 positive test scenarios are:
1. Adding TODO (function test_positive_add_item in test_todomvc.py)
Steps: 
1) Go to "What needs to be done" field
2) Print something
3) Click Enter
Expecting result: new TODO appears with the value from step 2, the count of items to complete is increased by 1

2. Editing TODO (function test_positive_edit_item in test_todomvc.py)
Steps:
(TODO must be added firstly) 
1) Double-click on TODO
2) Edit the existing text
3) Click Enter
Expecting result: the text is changed accordingly

3. Deleting TODO (function test_positive_delete_item in test_todomvc.py)
Steps: 
(TODO must be added firstly) 
1) Hover the mouse cursor above TODO
2) Click on appearing X (delete) button
Expecting result: TODO disappears from the list, item counter disappears too

4. Completing TODO (function test_positive_complete_item in test_todomvc.py)
Steps: 
(TODO must be added firstly) 
1) Click radio-button near the TODO
Expecting result: radio-button is checked, the TODO text is scratched, "Clear complete" link appears, the count of items to complete is decreased by 1

5. Removing completed TODO (function test_positive_clear_complete_item in test_todomvc.py)
Steps: 
(TODO must be added firstly)
1) Complete the TODO
2) Click "Clear complete" link
Expecting result: completed TODO disappears, "Clear complete" link disappears, the count of items to complete disappears


The 4 negative scenarios:
1. Adding a blank TODO (function test_negative_add_blank_item in test_todomvc.py)
Steps: 
1) Go to "What needs to be done" field
2) Without printing something click Enter
Expecting result: no new TODO appears

2. Saving the empty TODO after editing (function test_negative_save_empty_item in test_todomvc.py)
++++THIS TEST HAS FOUND A BUG, it would be mark as FAILED++++
Steps: 
(TODO must be added firstly)
1) Double-click on non-completed TODO
2) Delete all the existing text
3) Click somewhere outside the TODO field (DO NOT press Enter)
Expecting result: the TODO disappears, the count of items to complete is decreased by 1
ACTUAL RESULT: blank TODO remains in the list, the count of items to complete doesn't change

3. Trying to find the "Clear complete" link after completing and incompleting TODO (function test_negative_find_the_complete_link_after_unchecking_item in test_todomvc.py)
Steps:
(TODO must be added firstly) 
1) Add TODO to blank TODO list
2) Check it as complete
3) Uncheck as incomplete
4) Try to click "Clear complete" link
Expecting result: the "Clear complete" link doesn't exist

4. Trying to remove TODO while editing (function test_negative_try_to_remove_item_while_edit in test_todomvc.py)
Steps: 
1) Add TODO to blank TODO list
2) Double-click to edit
3) Try to click X (delete) button
Expecting result: button is invisible and unreachable
