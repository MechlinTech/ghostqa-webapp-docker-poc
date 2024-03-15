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
    text = action.get('text', '')
    option = action.get('option', '')
    assert_type = action.get('assertType', '')
    value = action.get('value', '')
    key = action.get('key', '')
    direction = action.get('direction', '')
    distance = action.get('distance', 0)
    duration = action.get('duration', 0)

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
    elif action_type == 'click':
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
        name = f'Test Step: {action_type}: {selector}'
        
        return f"""
            it('{name}', () => {{
               cy.get("{selector}").check();
            }});
        """
    elif action_type == 'uncheck':
        name = f'Test Step: {action_type}: {selector}'
        
        return f"""
            it('{name}', () => {{
               cy.get("{selector}").uncheck();
            }});
        """
    elif action_type == 'dblclick':
        name = f'Test Step: {action_type}: {selector}'
        
        return f"""
            it('{name}', () => {{
                cy.dblclick("{selector}");
            }});
        """
    elif action_type == 'rightclick':
        return f"""cy.rightclick({selector})"""
    elif action_type == 'assert':
        return generate_assert_code(assert_type, selector, value)
    else:
        return ''

def generate_assert_code(assert_type, selector, value):
    if assert_type == 'exist':
        # name = f'Test Step: assert {assert_type}: {selector} {value}'
        return f"""cy.get("{selector}").should('exist');"""
    elif assert_type == 'equal':
        return f"""cy.get("{selector}").should('have.text', '{value}');"""
    elif assert_type == 'contain':
        return f"""cy.get("{selector}").should('include.text', '{value}');"""
    elif assert_type == 'have.class':
        return f"""cy.get("{selector}").should('have.class', '{value}');"""
    elif assert_type == 'not.exist':
        return f"""cy.get("{selector}").should('not.exist');"""
    elif assert_type == 'have.length':
        return f"""cy.get("{selector}").should('have.length', {value});"""
    else:
        return ''

# Example usage
