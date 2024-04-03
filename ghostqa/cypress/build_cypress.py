import yaml
import os
import black

def format_js_code(js_code):
    try:
        print(js_code)
        formatted_code = black.format_str(js_code, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        print(f"Error formatting JavaScript code: {e}")
        return js_code
def generate_test_case_code(test_case,before_each=None):
    # test_case_name = list(test_case.keys())[0]
    # test_case_details = test_case[test_case_name]
    case_name = test_case.get('name', "Unnamed Test Case")
    if before_each == None:
        before_each =  test_case.get('beforeEach', [])
    actions = test_case.get('actions', [])

    # return f"""
    #     describe('{case_name}', () => {{
    #         {generate_before_each(before_each)}
            
    #         it('should execute test steps', () => {{
    #             {generate_test_actions(actions)}
    #         }});
    #     }});
    # """
    return f"""
            describe('{case_name}', () => {{
                {generate_before_each(before_each)}
                
                {generate_test_actions(actions,True)}
            }});
    """
def generate_test_cases(test_cases,before_each):
    # Generate Cypress test code for each test case
    cases = []
    for test_case in test_cases:
        result = generate_test_case_code(test_case,before_each)
        cases.append(result)
    return '\n'.join(cases)


def generate_cypress_testv3(test_suites):
    try:


            # Generate Cypress test code
            cypress_code = []
            for test_suite in test_suites:
                # suite_name = list(test_suite.keys())[0]
                # suite_details = test_suite[suite_name]
                suite_name = test_suite.get('name', "Unnamed Suite")
                test_cases = test_suite.get('testCases', [])
                before_each = test_suite.get('beforeEach', [])
                # Cypress test code template
                cypress_code.append(f"""
                    describe('{suite_name}', () => {{
                        {generate_test_cases(test_cases, before_each)}
                    }});
                """)

            return '\n'.join(cypress_code)    
    except Exception as e:
        print(f'Error generating Cypress tests: {e}')
def generate_cypress_testv2(test_suites):
    try:


            # Generate Cypress test code
            cypress_code = []
            for test_suite in test_suites:
                # suite_name = list(test_suite.keys())[0]
                # suite_details = test_suite[suite_name]
                suite_name = test_suite.get('name', "Unnamed Suite")
                test_cases = test_suite.get('testCases', [])
                before_each = test_suite.get('beforeEach', [])
                # Cypress test code template
                cypress_code.append(f"""
                    describe('{suite_name}', () => {{
                        {generate_test_cases(test_cases, before_each)}
                    }});
                """)

            return '\n'.join(cypress_code)    
    except Exception as e:
        print(f'Error generating Cypress tests: {e}')
def generate_cypress_test(tests):
    try:


            # Generate Cypress test code
            cypress_code = []
            for test in tests:
                test_name = list(test.keys())[0]
                test_details = test[test_name]
                url = test_details.get('url', None)
                actions = test_details.get('actions', [])
                before_each = test_details.get('beforeEach', [])

                # Cypress test code template
                cypress_code.append(f"""
                    describe('{test_name}', () => {{
                        {generate_before_each(before_each)}
                        
                        it('should execute test steps', () => {{
                            {f"cy.visit('{url}');" if url else ""}
                            
                            {generate_test_actions(actions)}
                        }});
                    }});
                """)

            return '\n'.join(cypress_code)    
    except Exception as e:
        print(f'Error generating Cypress tests: {e}')

def generate_before_each(before_each_actions):
    if not before_each_actions or len(before_each_actions) == 0:
        return ''  # No beforeEach actions specified

    # Generate beforeEach Cypress actions based on the YAML file
    return f"""
        beforeEach(() => {{
            {generate_test_actions(before_each_actions,False)}
        }});
    """

def generate_test_actions(actions,wrap_it=True):
    # Generate Cypress actions based on the YAML file
    actions_list = []
    for action in actions:
        actions_list.append(generate_action_code(action,wrap_it) )
    return '\n'.join(actions_list)

def generate_action_code(action,wrap_it=True):
    action_type = action.get('type', '')
    selector = action.get('selector', '')
    not_selector = action.get('not_selector', '')
    text = action.get('text', '')
    option = action.get('option', '')
    assert_type = action.get('assertType', '')
    value = action.get('value', '')
    key = action.get('key', '')
    direction = action.get('direction', '')
    distance = action.get('distance', 0)
    duration = action.get('duration', 0)
    drag_selector = action.get('drag_selector', '')
    drop_selector = action.get('drop_selector', '')
    form_selector = action.get('form_selector', '')
    file_path = action.get('file_path', '')
    x_position = action.get('x_position', 0)
    y_position = action.get('y_position', 0)
    url = action.get('url', '')
    element = action.get('element', '')
    property_name = action.get('property_name', '')
    attribute = action.get('attribute', '')
    expected_value = action.get('expected_value', '')
    expected_title = action.get('expected_title', '')
    expected_url = action.get('expected_url', '')
    expected_length = action.get('expected_length', 0)
    prop_name = action.get('prop_name', '')
    attribute_name = action.get('attribute_name', '')
    expected_text = action.get('expected_text', '')

    if action_type == 'visit':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.visit("{selector}");
                }});
            """
        else:
            return f"""cy.visit("{selector}");""";
    elif action_type == 'click': # TODO confirm from QA Team and Diljot this action is left click
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").click();
                }});
            """
        return f"""cy.get("{selector}").click();"""
    elif action_type == 'type':
        if wrap_it:
        
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").type('{text}');
                }});
            """
        return f"""cy.get("{selector}").type('{text}');"""
    elif action_type == 'press':
        if wrap_it:
        
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.get('body').type('{key}');
                }});
            """
        return f"""cy.get('body').type('{key}');"""
    elif action_type == 'wait':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector} seconds'
            
            return f"""
                it('{name}', () => {{
                cy.wait({duration});
                }});
            """
        return f"""cy.wait({duration});"""
    elif action_type == 'scroll':
        if wrap_it:
    
            name = f'Test Step: {action_type}: {direction} {distance}'
            
            return f"""
                it('{name}', () => {{
                    cy.get('body').scroll{'Up' if direction == 'up' else 'Down'}({distance});
                }});
            """
        return f"""cy.get('body').scroll{'Up' if direction == 'up' else 'Down'}({distance});"""
    elif action_type == 'hover':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").trigger('mouseover');
                }});
            """
        return f"""cy.get("{selector}").trigger('mouseover');"""
    elif action_type == 'select':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector} {option}'
            
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").select('{option}');
                }});
            """
        return f"""cy.get("{selector}").select('{option}');"""
    elif action_type == 'check':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                cy.get("{selector}").check();
                }});
            """
        return f"""cy.get("{selector}").check()"""
    elif action_type == 'uncheck':
        if wrap_it:    
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                cy.get("{selector}").uncheck();
                }});
            """
        return f"""cy.get("{selector}").uncheck()"""
    elif action_type == 'dblclick':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").dblclick();
                }});
            """
        return f"""cy.dblclick("{selector}");"""
    elif action_type == 'rightclick':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").rightclick();  
                }})
            """
        return f"""cy.rightclick({selector})"""
    elif action_type == 'clear_text':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").clear();
                }});
            """
        return f"""cy.get("{selector}").clear();"""
    elif action_type == 'drag_and_drop':
        if wrap_it:
            name = f'Test Step: {action_type}: {drag_selector} to {drop_selector}'
            return f"""
                it('{name}', () => {{
                    const dataTransfer = new DataTransfer();
                    cy.get("{drag_selector}").trigger('dragstart', {{ dataTransfer }});
                    cy.get("{drop_selector}").trigger('drop', {{ dataTransfer }});
                }});
            """
        return f"""
            const dataTransfer = new DataTransfer();
            cy.get("{drag_selector}").trigger('dragstart', {{ dataTransfer }});
            cy.get("{drop_selector}").trigger('drop', {{ dataTransfer }});
        """
    elif action_type == 'checkbox':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").check();
                }});
            """
        return f"""cy.get("{selector}").check();"""
    elif action_type == 'uncheck_checkbox':
        if wrap_it:
            name = f'Test Step: {action_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").uncheck();
                }});
            """
        return f"""cy.get("{selector}").uncheck();"""
    elif action_type == 'submit_form':
        if wrap_it:
            name = f'Test Step: {action_type}: Submit {form_selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{form_selector}").submit();
                }});
            """
        return f"""cy.get("{form_selector}").submit();"""
    elif action_type == 'select_option':
        if wrap_it:
            name = f'Test step: {action_type}: Select {option} from {selector}'
            return f"""
                it('{name}, ()=> {{
                    cy.get("{selector}").select("{option}");
                }});
            """
        return f"""cy.get("{selector}").select("{option}");"""
    elif action_type == 'upload_file':
        if wrap_it:
            name = f'Test Step: {action_type}: Upload file {file_path} to {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").attachFile("{file_path}");
                }});
            """
        return f"""cy.get("{selector}").attachFile("{file_path}");""" 
    elif action_type == 'scroll_into_view':
        if wrap_it:
            name = f'Test Step: {action_type}: Scroll into view {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get("{selector}").scrollIntoView();
                }});
            """
        return f"""cy.get("{selector}").scrollIntoView();"""  
    elif action_type == 'scroll_to_window':
        if wrap_it:
            name = f'Test Step: {action_type}: Scroll window to ({x_position}, {y_position})'
            return f"""
                it('{name}', () => {{
                    cy.scrollTo({x_position}, {y_position});
                }});
            """
        return f"""cy.scrollTo({x_position}, {y_position});"""
    elif action_type == 'go_to_url':
        if wrap_it:
            name = f'Test Step: {action_type}: Go to URL {url}'
            return f"""
                it('{name}', () => {{
                    cy.visit('{url}');
                }});
            """
        return f"""cy.visit('{url}');"""
    elif action_type == 'go_back':
        if wrap_it:
            name = f'Test Step: {action_type}: Go back'
            return f"""
                it('{name}', () => {{
                    cy.go('back');
                }});
            """
        return f"""cy.go('back');"""
    elif action_type == 'go_forward':
        if wrap_it:
            name = f'Test Step: {action_type}: Go forward'
            return f"""
                it('{name}', () => {{
                    cy.go('forward');
                }});
            """
        return f"""cy.go('forward');"""
    elif action_type == 'refresh_page':
        if wrap_it:
            name = f'Test Step: {action_type}: Refresh page'
            return f"""
                it('{name}', () => {{
                    cy.reload();
                }});
            """
        return f"""cy.reload();"""
    elif action_type == 'element_text_contains':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {element} text contains {text}'
            return f"""
                it('{name}', () => {{
                    cy.contains('{element}', '{text}');
                }});
            """
        return f"""cy.contains('{element}', '{text}');"""
    elif action_type == 'element_exist':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} exists'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('exist');
                }});
            """
        return f"""cy.get('{selector}').should('exist');"""
    elif action_type == 'element_not_exist':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} does not exist'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('not.exist');
                }});
            """
        return f"""cy.get('{selector}').should('not.exist');"""
    elif action_type == 'element_is_visible':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is visible'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.visible');
                }});
            """
        return f"""cy.get('{selector}').should('be.visible');"""
    elif action_type == 'element_is_not_visible':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is not visible'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('not.be.visible');
                }});
            """
        return f"""cy.get('{selector}').should('not.be.visible');"""
    elif action_type == 'element_is_enabled':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is enabled'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.enabled');
                }});
            """
        return f"""cy.get('{selector}').should('be.enabled');"""
    elif action_type == 'element_is_visible':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is visible'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.visible');
                }});
            """
        return f"""cy.get('{selector}').should('be.visible');"""
    elif action_type == 'element_is_not_visible': # this is repeated action
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is not visible'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('not.be.visible');
                }});
            """
        return f"""cy.get('{selector}').should('not.be.visible');"""
    elif action_type == 'element_is_enabled': # this is repeated action
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is enabled'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.enabled');
                }});
            """
        return f"""cy.get('{selector}').should('be.enabled');"""
    elif action_type == 'element_is_disabled':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is disabled'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.disabled');
                }});
            """
        return f"""cy.get('{selector}').should('be.disabled');"""
    elif action_type == 'element_has_value':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has value {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.value', '{value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.value', '{value}');"""
    elif action_type == 'element_has_attribute_with_value':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has attribute {attribute} with value {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.attr', '{attribute}', '{value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.attr', '{attribute}', '{value}');"""
    elif action_type == 'element_has_css_property_with_value':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has CSS property {property_name} with value {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.css', '{property_name}', '{value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.css', '{property_name}', '{value}');"""
    elif action_type == 'invoke_value':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').invoke('val').should('eq', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').invoke('val').should('eq', '{expected_value}');"""
    elif action_type == 'validate_page_title':
        if wrap_it:
            name = f'Test Step: {action_type}: Validate Page Title to include {expected_title}'
            return f"""
                it('{name}', () => {{
                    cy.title().should('include', '{expected_title}');
                }});
            """
        return f"""cy.title().should('include', '{expected_title}');"""
    elif action_type == 'validate_current_url':
        if wrap_it:
            name = f'Test Step: {action_type}: Validate Current URL to be {expected_url}'
            return f"""
                it('{name}', () => {{
                    cy.url().should('eq', '{expected_url}');
                }});
            """
        return f"""cy.url().should('eq', '{expected_url}');"""
    elif action_type == 'number_of_element_found':
        if wrap_it:
            name = f'Test Step: {action_type}: Check number of elements found for selector {selector} to be {expected_length}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.length', {expected_length});
                }});
            """
        return f"""cy.get('{selector}').should('have.length', {expected_length});"""    
    elif action_type == 'blur_element':
        if wrap_it:
            name = f'Test Step: {action_type}: Blur element {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').blur();
                }});
            """
        return f"""cy.get('{selector}').blur();"""
    elif action_type == 'fixture':
        if wrap_it:
            name = f'Test Step: {action_type}: Load fixture from file path {file_path}'
            return f"""
                it('{name}', () => {{
                    cy.fixture('{file_path}');
                }});
            """
        return f"""cy.fixture('{file_path}');"""
    elif action_type == 'focus':
        if wrap_it:
            name = f'Test Step: {action_type}: Focus on element {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').focus();
                }});
            """
        return f"""cy.get('{selector}').focus();"""
    elif action_type == 'force_click':
        if wrap_it:
            name = f'Test Step: {action_type}: Force click on element {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').click({{ force: true }});
                }});
            """
        return f"""cy.get('{selector}').click({{ force: true }});"""
    elif action_type == 'select_first_element':
        if wrap_it:
            name = f'Test Step: {action_type}: Select first element matching {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').first();
                }});
            """
        return f"""cy.get('{selector}').first();"""
    elif action_type == 'select_last_element':
        if wrap_it:
            name = f'Test Step: {action_type}: Select last element matching {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').last();
                }});
            """
        return f"""cy.get('{selector}').last();"""
    elif action_type == 'location':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if location property {property_name} is {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.location('{property_name}').should('eq', '{expected_value}');
                }});
            """
        return f"""cy.location('{property_name}').should('eq', '{expected_value}');"""
    elif action_type == 'next_element':
        if wrap_it:
            name = f'Test Step: {action_type}: Select next element from {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').next();
                }});
            """
        return f"""cy.get('{selector}').next();"""
    elif action_type == 'next_all_element':
        if wrap_it:
            name = f'Test Step: {action_type}: Select all next elements from {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').nextAll();
                }});
            """
        return f"""cy.get('{selector}').nextAll();"""
    elif action_type == 'not':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} does not have class {not_selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').not('{not_selector}');
                }});
            """
        return f"""cy.get('{selector}').not('{not_selector}');"""
    elif action_type == 'title':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if page title is {expected_title}'
            return f"""
                it('{name}', () => {{
                    cy.title().should('eq', '{expected_title}');
                }});
            """
        return f"""cy.title().should('eq', '{expected_title}');"""
    elif action_type == 'should_not_equal':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} does not have value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('not.equal', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('not.equal', '{expected_value}');"""
    elif action_type == 'should_include':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} includes value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('include', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('include', '{expected_value}');"""
    elif action_type == 'should_be_null':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is null'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.null');
                }});
            """
        return f"""cy.get('{selector}').should('be.null');"""
    elif action_type == 'should_be_empty':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is empty'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.empty');
                }});
            """
        return f"""cy.get('{selector}').should('be.empty');"""
    elif action_type == 'should_equal':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} equals {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('equal', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('equal', '{expected_value}');"""
    elif action_type == 'should_be_greater_than':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is greater than {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.greaterThan', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('be.greaterThan', '{expected_value}');"""
    elif action_type == 'should_be_less_than':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is less than {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.lessThan', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('be.lessThan', '{expected_value}');"""
    elif action_type == 'have_attribute':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has attribute {attribute_name} with value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.attr', '{attribute_name}', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.attr', '{attribute_name}', '{expected_value}');"""
    elif action_type == 'have_prop':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has prop {prop_name} with value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.prop', '{prop_name}', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.prop', '{prop_name}', '{expected_value}');"""
    elif action_type == 'have_css_value':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} has CSS property {property_name} with value {expected_value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.css', '{property_name}', '{expected_value}');
                }});
            """
        return f"""cy.get('{selector}').should('have.css', '{property_name}', '{expected_value}');"""
    elif action_type == 'contain_text':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} contains text {expected_text}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('contain', '{expected_text}');
                }});
            """
        return f"""cy.get('{selector}').should('contain', '{expected_text}');"""
    elif action_type == 'enter':
        if wrap_it:
            name = f'Test Step: {action_type}: Type Enter in element {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').type('{enter}');
                }});
            """
        return f"""cy.get('{selector}').type('{enter}');"""
    elif action_type == 'should_be_hidden':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is hidden'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.hidden');
                }});
            """
        return f"""cy.get('{selector}').should('be.hidden');"""
    elif action_type == 'should_be_selected':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is selected'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.selected');
                }});
            """
        return f"""cy.get('{selector}').should('be.selected');"""
    elif action_type == 'should_be_checked':
        if wrap_it:
            name = f'Test Step: {action_type}: Check if element {selector} is checked'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('be.checked');
                }});
            """
        return f"""cy.get('{selector}').should('be.checked');"""
    elif action_type == 'assert':
        return generate_assert_code(assert_type, selector, value)
    else:
        return ''
# TODO more actions to be added.

def generate_assert_code(assert_type, selector, value, wrap_it=True):
    if assert_type == 'exist':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('exist');
                }});
            """
        return f"cy.get('{selector}').should('exist');"
    elif assert_type == 'equal':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector} {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.text', '{value}');
                }});
            """
        return f"cy.get('{selector}').should('have.text', '{value}');"
    elif assert_type == 'contain':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector} {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('include.text', '{value}');
                }});
            """
        return f"cy.get('{selector}').should('include.text', '{value}');"
    elif assert_type == 'have.class':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector} {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.class', '{value}');
                }});
            """
        return f"cy.get('{selector}').should('have.class', '{value}');"
    elif assert_type == 'not.exist':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('not.exist');
                }});
            """
        return f"cy.get('{selector}').should('not.exist');"
    elif assert_type == 'have.length':
        if wrap_it:
            name = f'Assert Step: {assert_type}: {selector} {value}'
            return f"""
                it('{name}', () => {{
                    cy.get('{selector}').should('have.length', {value});
                }});
            """
        return f"cy.get('{selector}').should('have.length', {value});"
    else:
        return ''


# Example usage
