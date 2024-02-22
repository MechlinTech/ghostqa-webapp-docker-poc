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
            # # Save generated code to a file
            # output_file_path = 'cypress/e2e/3-test/generatedTests.cy.js'
            # with open(output_file_path, 'w') as output_file:
            #     output_file.write('\n'.join(cypress_code))

            # print(f'Cypress tests generated successfully. Check {output_file_path}')
    
            # # Save generated code to a file
            # output_file_path = 'isolated/e2e/cypress/integration/generatedTests.cy.js'
            # with open(output_file_path, 'w') as output_file:
            #     output_file.write('\n'.join(cypress_code))

            # print(f'Cypress tests generated successfully. Check {output_file_path}')

    
    except Exception as e:
        print(f'Error generating Cypress tests: {e}')

def generate_before_each(before_each_actions):
    if not before_each_actions or len(before_each_actions) == 0:
        return ''  # No beforeEach actions specified

    # Generate beforeEach Cypress actions based on the YAML file
    return f"""
        beforeEach(() => {{
            {generate_test_actions(before_each_actions)}
        }});
    """

def generate_test_actions(actions):
    # Generate Cypress actions based on the YAML file
    return '\n'.join([generate_action_code(action) for action in actions])

def generate_action_code(action):
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
        return f"""cy.visit("{selector}");"""
    elif action_type == 'click':
        return f"""cy.get("{selector}").click();"""
    elif action_type == 'type':
        return f"""cy.get("{selector}").type('{text}');"""
    elif action_type == 'press':
        return f"""cy.get('body').type('{key}');"""
    elif action_type == 'wait':
        return f"""cy.wait({duration});"""
    elif action_type == 'scroll':
        return f"""cy.get('body').scroll{'Up' if direction == 'up' else 'Down'}({distance});"""
    elif action_type == 'hover':
        return f"""cy.get("{selector}").trigger('mouseover');"""
    elif action_type == 'select':
        return f"""cy.get("{selector}").select('{option}');"""
    elif action_type == 'check':
        return f"""cy.get("{selector}").check();"""
    elif action_type == 'uncheck':
        return f"""cy.get("{selector}").uncheck();"""
    elif action_type == 'assert':
        return generate_assert_code(assert_type, selector, value)
    else:
        return ''

def generate_assert_code(assert_type, selector, value):
    if assert_type == 'exist':
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
generate_cypress_test('tests.yaml')
